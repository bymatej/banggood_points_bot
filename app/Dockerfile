#FROM python:3.8.5-slim-buster
FROM ubuntu:focal
MAINTAINER Matej Jelić "programming@bymatej.com"

ARG DEBIAN_FRONTEND=noninteractive
ARG GECKO_DRIVER_VERSION='v0.27.0'
ENV BANGGOOD_USERNAME =
ENV BANGGOOD_PASSWORD =
ENV BROWSER_SLEEP = 2
ENV BANGGOOD_SHIPTO = US
ENV BANGGOOD_CURRENCY = USD

RUN apt update && \
    apt install -y python3 python3-pip firefox-geckodriver

COPY ./requirements.txt /requirements.txt
WORKDIR /
RUN pip3 install -r requirements.txt

COPY src/ app/
WORKDIR /app/
ENTRYPOINT [ "python3" ]
CMD [ "/app/bot.py" ]