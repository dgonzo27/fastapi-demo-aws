FROM python:3.9-slim-buster

WORKDIR /usr/src

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && apt-get -y install \
    netcat gcc postgresql \
    && apt-get clean

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/
RUN pip install -r requirements.txt

COPY . /usr/src/