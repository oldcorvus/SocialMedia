
FROM python:3.8.12
MAINTAINER Moel

ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY ./requirements.txt /requirements.txt

RUN pip3 install -r /requirements.txt



# Setup directory structure
RUN mkdir /app
WORKDIR /app
COPY ./app /app/

RUN useradd -ms /bin/bash user

USER user
