
FROM python:3.9-alpine
MAINTAINER Moel

ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY ./requirements.txt /requirements.txt
RUN pip install wheel
RUN pip install -r /requirements.txt 

# Setup directory structure
RUN mkdir /app
WORKDIR /app
COPY ./app/ /app

RUN adduser -D user
USER user
