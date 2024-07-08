# Dockerfile
FROM python:3.11-slim

RUN apt-get update -y
RUN apt-get install -y python3-pip python-dev-is-python3 build-essential

WORKDIR /app


# speed up local building process by caching installed requirements
COPY requirements.txt /app

RUN pip install -r requirements.txt


COPY . /app

EXPOSE 4002

# https://docs.gunicorn.org/en/stable/settings.html
CMD gunicorn --bind 0.0.0.0:4002 app:app