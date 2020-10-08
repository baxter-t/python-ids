FROM ubuntu:18.04

MAINTAINER Thomas Baxter "Baxter.t98@gmail.com"

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && \
    apt-get install -y python3-pip wireshark python3-dev tshark

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

RUN python3 --version

CMD ["python3", "main.py", "10.128.0.8" , "test"]
