FROM tiangolo/uwsgi-nginx-flask:python3.5

ENV DEBIAN_FRONTEND noninteractive
ENV STATIC_PATH /app/web/static

RUN apt-get update
RUN apt-get install -y xorg libxrender-dev xvfb wget tar

RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.3/wkhtmltox-0.12.3_linux-generic-amd64.tar.xz
RUN tar vxf wkhtmltox-0.12.3_linux-generic-amd64.tar.xz 
RUN cp wkhtmltox/bin/wk* /usr/bin/

COPY ./requirements.txt /app/requirements.txt
COPY ./web/requirements.txt /app/web/requirements.txt
RUN pip install -r /app/web/requirements.txt
RUN pip install -r /app/requirements.txt
COPY . /app
RUN pip install /app/

EXPOSE 80
