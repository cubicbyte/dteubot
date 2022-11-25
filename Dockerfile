# syntax=docker/dockerfile:1

FROM python:3.11

WORKDIR /data

COPY . /app

RUN pip install -r /app/requirements.txt

CMD ["python", "/app"]
