FROM python:alpine3.20

ENV PYTHONUNBUFFERED=1

USER root

RUN apk update
RUN python -m pip install --upgrade pip
RUN apk add --no-cache curl

COPY ./requirements.txt /app/requirements.txt
COPY ./app /app
COPY ./scripts /scripts

WORKDIR /app

RUN chmod -R +x ./wait-for-it.sh
RUN chmod -R +x /scripts
RUN chmod -R +x /app
RUN chmod -R 755 /app/static
RUN pip install -r requirements.txt
RUN python manage.py collectstatic --noinput

EXPOSE 80

#USER nobody

ENTRYPOINT ["/scripts/run.sh"]
