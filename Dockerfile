FROM debian:jessie
MAINTAINER Smartribe <contact@smartri.be>


RUN apt-get -y update && apt-get -y upgrade
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y install 	python3 \
			python3-pip \ 
			locales

## Setting locales (encoding) ##
RUN dpkg-reconfigure locales && \
    locale-gen C.UTF-8 && \
    /usr/sbin/update-locale LANG=C.UTF-8
ENV LC_ALL C.UTF-8

RUN pip3 install https://www.djangoproject.com/download/1.7c1/tarball/

RUN mkdir -p /srv
ADD . /srv/smartribe

RUN pip3 install -r /srv/smartribe/requirements.prod.txt


RUN useradd -d /srv/smartribe gunicorn
RUN chown -R gunicorn: /srv

USER gunicorn
WORKDIR /srv/smartribe

RUN rm db.sqlite3

RUN python3 /srv/smartribe/manage.py migrate

EXPOSE 7777

CMD ["-w", "2", "-b", "0.0.0.0:7777", "smartribe.wsgi:application"]
ENTRYPOINT ["/usr/local/bin/gunicorn"]
