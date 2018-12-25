#!/usr/bin/env python
import logging, time, datetime, sys, ConfigParser, json, os
from configs.config_factory import ConfigFactory
from const import *
from log import gen_logger#, gen_tracer
from autologging import logged#, traced
from adapters.kafka_adapter import Kafka_Consumer, Kafka_Producer
from controllers.blush_moderation_controller import BlushModerationController
from helpers.cloudwatch_metric_writer import CloudWatchMetricWriter
from helpers.kerberos_helper import KerberosUtil
from helpers.s3_util import S3Utils
from httpserver.server import SimpleHTTPServer
# from helpers.json_helper import JSONHelper
import threading
import subprocess

# KAFKACONFIG = ConfigParser.ConfigParser()
# KAFKACONFIG.read("/etc/consumer/consumer.ini")
KAFKACONFIG = ConfigFactory(CONFIG_FILE).get_config()
CONSUMERCONFIG = ConfigFactory(CONFIG_FILE).get_config()


# @traced(logging.getLogger("blush.consumer.trace"))
@logged(logging.getLogger("blush.consumer.general"))
def main():
    global threads
    global stop_threads
    stop_threads = False
    main._log.info("Main Function Starting")
    threads = [threading.Thread(target=run_consumer),
               threading.Thread(target=run_kinit),
               SimpleHTTPServer(CONSUMERCONFIG)]
    main._log.info("Starting 3 threads: Kafka Consumer, HTTP server for healthcheck, and Kerberos ticket refreshing.")
    for thread in threads:
        thread.start()
    time.sleep(2)
    for thread in threads:
        thread.join()
    main._log.info("All threads have been stopped. Consumer EXITs now.")

    
@logged(logging.getLogger("blush.consumer.general"))
def run_kinit():
    # Periodically refreshing the Kerberos ticket is the most stable method (although there is re-downloading method in consumer) to solve unexpected ticket/KeyTab problems.
    next_call = time.time()
    connection_timeout = int(KAFKACONFIG.get('Settings', 'connection_timeout')) / 10 # This interval is tunable.
    principal = KAFKACONFIG.get('Settings', 'principal')
    bucket = KAFKACONFIG.get('Settings', 'bucket')
    keytab_key = KAFKACONFIG.get('Settings', 'keytab_key')
    keytabs_path = KAFKACONFIG.get('Settings', 'keytab_path')
    run_kinit._log.debug(" For Kerberos ticket refreshing, principal={}, S3 bucket={}, S3 key={}, KeyTab path={}.".format(principal, bucket, keytab_key, keytabs_path))
    login_retry = int(KAFKACONFIG.get('Settings', 'login_retry'))
    login_retry_poll = int(KAFKACONFIG.get('Settings', 'login_retry_poll'))
    while True:
        run_kinit._log.info(" Refreshing the Kerberos Ticket...")
        if stop_threads:
            break
        if KerberosUtil.refresh_ticket(principal):
            run_kinit._log.debug(" Periodically refreshing the Kerberos ticket using KINIT-R at {} has succeeded.".format(datetime.datetime.now()))
        else:
            run_kinit._log.error(" Periodically refreshing the Kerberos ticket using KINIT-R at {} has failed! Trying other KINIT methods...".format(datetime.datetime.now()))
            if not KerberosUtil.validate_ticket():
                run_kinit._log.debug("Since KINIT-R does not work, initializing the ticket cache using KINIT-KT.")
                if KerberosUtil.kinit(login_retry, login_retry_poll, principal, keytabs_path, keytab_key, bucket):
                    run_kinit._log.debug(" Periodically refreshing the Kerberos ticket using KINIT-KT in addition to -R has succeeded.")
                else:
                    run_kinit._log.error(" Periodically refreshing the Kerberos ticket using KINIT-KT in addition to -R has failed! Trying again after {} seconds.".format(connection_timeout))
        next_call = next_call + connection_timeout
        time.sleep(next_call - time.time())
    run_kinit._log.info("Periodically refreshing has been terminated.")
    
    
@logged(logging.getLogger("blush.consumer.general"))
def run_consumer():
    # Pull the all needed ssl certs from s3 at launch
    files = json.loads(KAFKACONFIG.get('certs', 'files')) # Kafka_certs
    bucket = KAFKACONFIG.get('Settings', 'bucket') # Kafka_settings
    run_consumer._log.info("Pulling SSL certs from s3")
    for cert in files:
        if not S3Utils.copy_to_local(bucket, cert['src'], cert['dst']):
            run_consumer._log.warning("Could not download " + cert['dst'] + " from s3.")

    (models_data, get_models_data_failed) = get_models_data()
    get_models_data_time = time.time()
    get_models_data_timeout = float(CONSUMERCONFIG.get('Settings', 'get_models_data_timeout'))

    cloudwatch_region = CONSUMERCONFIG.get(LOGSECTION, 'cloudwatch_region')
    cloudwatch_namespace = CONSUMERCONFIG.get(LOGSECTION, "cloudwatch_namespace_kafka_consumer")

    json_dir = 'json-inputs/'
    json_files = os.listdir(json_dir)

    count = 1
    for each_json in json_files[0:0]:
        msg_value_fake = json.load(open(json_dir + each_json, 'r'))
        start_time = time.time()
        run_consumer._log.info("******************** Processing JSON {} ********************".format(count))
        run_consumer._log.info("Blush Controller Classes")
        run_consumer._log.info("Message was {0}".format(msg_value_fake))
        controller = BlushModerationController(msg_value_fake)
        response_message = controller.execute(models_data)
        run_consumer._log.info("-------------------- Response Message --------------------")
        run_consumer._log.info("Response Payload was {0}".format(response_message))
        seconds_to_complete = time.time() - start_time
        run_consumer._log.info("******************** End Processing JSON {} ********************".format(count))
        count += 1
        # gen_logger.info("Main Function Exiting. Took {0} minutes to complete".format(round(minutes_to_complete / 60, 2)))

    run_consumer._log.info("######################## Mock Test Complete ########################")

    keytab_retry_limit = int(KAFKACONFIG.get('Settings', 'keytab_retry_limit'))
    keytab_retry_interval = int(KAFKACONFIG.get('Settings', 'keytab_retry_interval'))
    keytab_retry_count = 0
    while keytab_retry_count < keytab_retry_limit:
        try:
            consumer = Kafka_Consumer(KAFKACONFIG)
            producer = Kafka_Producer(KAFKACONFIG)
            producer.connect()
            # Keytab and principal re-download is done by helpers/kerberos_helper.py in adapters/kafka_adapter.py.
            keytab_retry_count = 0
            run_consumer._log.debug("Kafka consumer-producer connection has been established.")
            for msg in consumer.connect():
                #run_consumer._log.debug(" ******* Reading Messages from kafka ... *******")
                run_consumer._log.debug("Now the messages looping starts.")
                start_time = time.time()
                run_consumer._log.info(msg)
                if get_models_data_failed and ((time.time() - get_models_data_time) > get_models_data_timeout):
                    (models_data, get_models_data_failed) = get_models_data()
                    get_models_data_time = time.time()
                msg_value = json.loads(msg.value.replace("'", "\""))
                run_consumer._log.info("Message was {0}".format(msg_value))
                controller = BlushModerationController(msg_value)
                response_message = controller.execute(models_data)
                
                # Adding Timestamp and RequestID
                local_dt = str(datetime.datetime.now())
                response_message['OutboundTimeStamp'] = local_dt
                response_message['InboundTimeStamp'] = str(msg_value['InboundTimeStamp'])
                response_message['RequestID'] = str(msg_value['RequestID'])
                # End changes
                
                run_consumer._log.info("Response Payload was {0}".format(response_message))
                response = producer.send(json.dumps(response_message))
                run_consumer._log.info("The result of the send was {0}".format(response))
                seconds_to_complete = time.time() - start_time
                CloudWatchMetricWriter(cloudwatch_region).put_metric(cloudwatch_namespace, "Time", seconds_to_complete, "Consumers_Step", "Message_Processing", "Seconds")
				# gen_logger.info("Main Function Exiting. Took {0} minutes to complete".format(round(minutes_to_complete / 60, 2)))
        except Exception as e:
            run_consumer._log.debug("Connection problem detected. Consumer messages looping breaks here.")
            run_consumer._log.error(" Exception in connection: {}.".format(e))
            keytab_retry_count += 1
            run_consumer._log.debug("Retrying to launch the consumer for the {}th time.".format(keytab_retry_count))
            time.sleep(keytab_retry_interval)
            if keytab_retry_count >= keytab_retry_limit:
                run_consumer._log.error("Connection problem still exists after {} times. Exit.".format(keytab_retry_count))
                break
        else:
            run_consumer._log.error("Connection problem detected and remained unsolved. Exit.")
            break
    run_consumer._log.info("Consumer has been terminated.")
    global stop_threads
    stop_threads = True
    threads[2].stop()
    run_consumer._log.info("HTTP Server has been terminated.")

    
@logged(logging.getLogger("blush.consumer.general"))
def get_models_data():
    failed = False
    models_data = {}
    models_data['nudity'] = {}

    gesture_data = {}
    tensorflow_use_ssl = CONSUMERCONFIG.get(TFSERVING, "tensorflow_use_ssl").lower()
    if tensorflow_use_ssl != 'false':
        # try to download the certificate since we are using ssl
        tensorflow_cert_bucket = CONSUMERCONFIG.get(TFSERVING, 'tensorflow_cert_bucket')
        tensorflow_ssl_cert_src = CONSUMERCONFIG.get(TFSERVING, 'tensorflow_ssl_cert_src')
        tensorflow_ssl_cert_dst = CONSUMERCONFIG.get(TFSERVING, 'tensorflow_ssl_cert_dst')
        if not S3Utils.copy_to_local(tensorflow_cert_bucket, tensorflow_ssl_cert_src, tensorflow_ssl_cert_dst):
            get_models_data._log.warning("Could not download " + tensorflow_ssl_cert_dst + " from s3.")

        try:
            gesture_data['tensorflow_ssl_cert'] = open(tensorflow_ssl_cert_dst+'hi').read()
        except:
            get_models_data._log.error("Missing tensorflow certificate {}".format(tensorflow_ssl_cert_dst))
            failed = True
    models_data['gesture'] = gesture_data
    
    return (models_data, failed)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (KeyboardInterrupt, EOFError):
        print("\nAborted due to keyboard interruption.")
        sys.exit(1)
