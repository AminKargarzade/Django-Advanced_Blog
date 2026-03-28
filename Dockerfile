FROM docker.arvancloud.ir/python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/

RUN pip3 install -i https://mirror-pypi.runflare.com/simple --upgrade pip
RUN pip3 install -i https://mirror-pypi.runflare.com/simple -r requirements.txt

COPY ./core /app/