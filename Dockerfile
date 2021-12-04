FROM python:3.8
RUN apt update
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /var/www/watcher
WORKDIR /var/www/watcher
COPY requirements.txt /var/www/watcher
RUN python -m pip install --upgrade pip && pip install -r requirements.txt
COPY . /var/www/watcher
