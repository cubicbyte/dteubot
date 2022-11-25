# syntax=docker/dockerfile:1

FROM python:3.12

WORKDIR /data

VOLUME cache cache
VOLUME chat-configs chat-configs
VOLUME logs logs

COPY . /app
RUN pip3 install -r /app/requirements.txt

CMD [ "python3", "."]
