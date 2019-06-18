FROM python:3.6.8
  
RUN apt-get update
RUN apt-get install -y --no-install-recommends \
        libatlas-base-dev gfortran nginx
RUN pip install uwsgi
RUN pip install supervisor
COPY ./requirement-new.txt /project/requirements.txt

RUN pip3 install -r /project/requirements.txt

RUN useradd --no-create-home nginx

RUN rm /etc/nginx/sites-enabled/*
RUN rm -r /root/.cache

COPY nginx/nginx.conf /etc/nginx/
COPY nginx/clinic.conf /etc/nginx/conf.d/
COPY uwsgi.ini /etc/uwsgi/
COPY supervisord.conf /etc/

RUN pip install mysql-connector-python-rf
COPY ./ /project

WORKDIR /project

CMD ["/usr/local/bin/supervisord", "-c", "/etc/supervisord.conf"]

