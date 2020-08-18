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
#RUN webdrivermanager firefox --linkpath /usr/local/bin

#RUN apt update && \
#    apt install -y wget bzip2
#RUN wget https://github.com/mozilla/geckodriver/releases/download/$GECKO_DRIVER_VERSION/geckodriver-$GECKO_DRIVER_VERSION-linux64.tar.gz && \
#    tar -xvzf geckodriver-$GECKO_DRIVER_VERSION-linux64.tar.gz && \
#    rm geckodriver-$GECKO_DRIVER_VERSION-linux64.tar.gz && \
#    chmod +x geckodriver && \
#    cp geckodriver /usr/local/bin/
##RUN webdrivermanager firefox --linkpath /usr/local/bin
#
#RUN FIREFOX_SETUP=firefox.tar.bz2 && \
#    apt purge -y firefox && \
#    wget -O $FIREFOX_SETUP "https://download.mozilla.org/?product=firefox-latest&os=linux64" && \
#    tar xjf $FIREFOX_SETUP -C /opt/ && \
#    ln -s /opt/firefox/firefox /usr/bin/firefox && \
#    rm $FIREFOX_SETUP

COPY src/ app/
WORKDIR /app/
ENTRYPOINT [ "python3" ]
CMD [ "/app/bot.py" ]