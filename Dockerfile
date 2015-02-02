FROM debian:jessie
MAINTAINER Smartribe <contact@smartribe.fr>

RUN apt-get -y update 
RUN apt-get -y upgrade

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y install 	python3 \
			python3-pip \ 
			locales \
			supervisor

## Setting locales (encoding) ##
RUN dpkg-reconfigure locales && \
    locale-gen C.UTF-8 && \
    /usr/sbin/update-locale LANG=C.UTF-8
ENV LC_ALL C.UTF-8

RUN mkdir -p /srv
ADD . /srv/smartribe
RUN mkdir -p /srv/smartribe/media

RUN pip3 install -r /srv/smartribe/requirements.prod.txt

RUN useradd -d /srv/smartribe gunicorn
RUN chown -R gunicorn: /srv

USER gunicorn
WORKDIR /srv/smartribe

EXPOSE 7777
VOLUME /srv/smartribe/media
CMD ["/bin/bash","/srv/smartribe/start.sh"]
