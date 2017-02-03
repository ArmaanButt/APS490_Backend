FROM ubuntu:14.04

RUN echo "deb http://archive.ubuntu.com/ubuntu precise main universe" > /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -y \
    gcc \
    python3.4 \
    python-pip \
    mysql-client-core-5.5

WORKDIR /usr/src/app
ADD . /usr/src/app
ADD requirements.txt /usr/src/app/requirements.txt


RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD script.sh /usr/src/app/script.sh
RUN chmod +x script.sh

EXPOSE 5000

ENTRYPOINT ["./script.sh"]
