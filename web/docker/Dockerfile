FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN mkdir /AutoBot

WORKDIR /AutoBot

COPY web/requirements.txt /AutoBot/

RUN pip install --upgrade pip && pip install -r requirements.txt

RUN apt-get update && apt-get install -y cron

ADD . /AutoBot/
