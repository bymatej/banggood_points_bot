FROM python:3.8.3-slim-buster
MAINTAINER Matej Jelić "programming@bymatej.com"

ENV BANGGOOD_USERNAME =
ENV BANGGOOD_PASSWORD =
ENV BROWSER_SLEEP = 2
ENV BANGGOOD_SHIPTO = US
ENV BANGGOOD_CURRENCY = USD

COPY ./requirements.txt /requirements.txt
WORKDIR /
RUN pip install -r requirements.txt

RUN webdrivermanager chrome --linkpath /usr/local/bin
COPY src/ app/
ENTRYPOINT [ "python" ]
CMD [ "/app/bot.py" ]