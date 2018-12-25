import json

class JSONHelper:
    """This class handles any JSON related tasks"""

    def load_from_file(self, file_path):
        try:
            with open(file_path) as json_data_file:
                data = json.load(json_data_file)
        except ValueError:
            print('Error loading the request')
            raise

        return data


import yaml

class yaml_helper:
    """This class handles all the YAML related tasks"""

    def load(self, filename):
        if filename is None:
            raise ValueError('Config file name is missing')
        try:
            with open(filename, 'r') as ymlfile:
                file = yaml.load(ymlfile)
        except:
            print('An error occucred while reading the file ', filename)
            raise
        return file


import boto3, logging, time
from autologging import logged
from datetime import datetime


@logged(logging.getLogger("blush.consumer.general"))
class CloudWatchMetricWriter:

    """Updates the CloudWatch init script"""
    def __init__(self, region):
        self.region = region
        self.cloudwatch = boto3.client('cloudwatch', region_name=region)

    def put_metric(self, namespace, metric_name, metric_val, dimension_key, dimension_val, unit):
        """Puts the metric"""
        # sending only one dimension for the time being. TODO: change it for multiple dimensions if required
        # Put custom metrics
        self.__log.info("Updating the CloudWatch Metric...")
        self.__log.info("Time: {3}, Metric: {0}, Name: {1}, Value: {2}".format(namespace, metric_name, metric_val, time.time()))
        response = self.cloudwatch.put_metric_data(
                    Namespace=namespace,
                    MetricData=[
                        {
                            'MetricName': metric_name,
                            'Dimensions': [
                                {
                                    'Name': dimension_key,
                                    'Value': dimension_val
                                },
                            ],
                            'Value': metric_val,
                            'Unit': unit,
                            'StorageResolution': 1
                        },
                    ])
        self.__log.info("Response: {0}".format(response))
