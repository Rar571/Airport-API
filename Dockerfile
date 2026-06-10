FROM python:3.12-slim

LABEL maintainer="airport"

ENV PYTHONBUFFERED 1

WORKDIR app/

COPY requirements.txt .

RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt

RUN adduser \
        --disabled-password \
        --no-create-home \
        my_user

RUN chown -R my_user:my_user /media
RUN chmod -R 755 /media

COPY . .
RUN mkdir -p /vol/web/media

USER my_user