FROM python:3.10
RUN apt update
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /var/www/watcher
WORKDIR /var/www/watcher
COPY requirements.txt /var/www/watcher
RUN python -m pip install --upgrade pip && pip install -r requirements.txt
COPY . /var/www/watcher
RUN django-admin startproject watcher .
RUN django-admin startapp watcherapp
RUN chmod +x /var/www/watcher/entrypoint.sh
ENTRYPOINT [ "/var/www/watcher/entrypoint.sh" ]
CMD ["python", "/var/www/watcher/watcher/manage.py", "runserver", "0.0.0.0:8090"]