FROM ubuntu:16.04

RUN apt-get update && apt-get install -y build-essential python3 python3-dev python3-pip

# Thanks to DouBan! #
RUN mkdir ~/.pip && \
    cd ~/.pip/  && \
    echo "[global] \ntrusted-host = pypi.douban.com \nindex-url = http://pypi.douban.com/simple" >  pip.conf

RUN pip3 install autologging
RUN mkdir -p /etc/
COPY *.* /etc
WORKDIR /etc/
EXPOSE 8080
CMD ["python3", "Test_Image.py"]
