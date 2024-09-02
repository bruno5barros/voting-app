FROM python:alpine3.20

ENV PYTHONUNBUFFERED=1

USER root

RUN apk update
RUN python -m pip install --upgrade pip
RUN apk add --no-cache curl

COPY ./requirements.txt /app/requirements.txt
COPY ./app /app

WORKDIR /app

RUN chmod -R 777 ./wait-for-it.sh
RUN pip install -r requirements.txt

USER nobody