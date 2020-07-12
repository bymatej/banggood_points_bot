FROM python:3.8.3-slim-buster
MAINTAINER Matej Jelić "programming@bymatej.com"

COPY ./requirements.txt /requirements.txt
WORKDIR /
RUN pip install -r requirements.txt
RUN webdrivermanager firefox --linkpath /usr/local/bin

COPY . /
ENTRYPOINT [ "python" ]
CMD [ "app/app.py" ]

# Todo: add banggood username and password as environment variables and remove it from config file