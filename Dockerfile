# Use this as a base image
FROM ubuntu:14.04

# Maintainer Info
MAINTAINER Ricardo Lobo <ricardolobo@audienciazero.org>

# set default environment
ENV APP_IN_PRODUCTION=false

# update repos and install
# pip3, supervisor, nginx
# python postgres adapter
RUN apt-get update && \
apt-get -y install \
python3-pip \
supervisor \
nginx \
python3-psycopg2 \
python3-lxml

# install Pillow dependencies
RUN apt-get -y install \
libtiff5-dev \
libjpeg8-dev \
zlib1g-dev \
libfreetype6-dev \
liblcms2-dev \
libwebp-dev \
tcl8.6-dev \
tk8.6-dev \
python-tk

# development dependencies
RUN apt-get -y install nano

# copy code to image
COPY . /var/www/

# set the working directory
WORKDIR /var/www/

# install django and django dependencies using pip3
RUN pip3 install -r /var/www/dist/requirements.txt

# make init script executable
RUN chmod ug+x /var/www/dist/initialize.sh

# set locale
RUN locale-gen pt_PT.UTF-8

# remove nginx default site
RUN rm /etc/nginx/sites-enabled/default

# copy supervisor configuration
COPY ./dist/lcdmarket.conf /etc/supervisor/conf.d/lcdmarket.conf

# default command
CMD ["/usr/bin/supervisord"]