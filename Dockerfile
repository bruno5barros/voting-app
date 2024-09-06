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

RUN chmod -R +x /scripts
RUN chmod -R +x /app
RUN pip install -r requirements.txt
RUN python manage.py collectstatic --noinput

#EXPOSE 80
EXPOSE 8000

RUN chown -R nobody:nogroup /app
USER nobody

#ENTRYPOINT ["/scripts/run.sh"]
