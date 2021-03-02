FROM python:3.6
EXPOSE 80
MAINTAINER telminov <telminov@soft-way.biz>
WORKDIR /opt/ca
VOLUME /data/
VOLUME /conf/
VOLUME /static/

RUN apt-get clean && apt-get update
RUN apt-get install -y \
                    vim \
                    supervisor \
                    curl \
                    locales \
                    python3-pip npm

RUN pip install --upgrade pip

RUN ln -s /usr/bin/nodejs /usr/bin/node

RUN locale-gen ru_RU.UTF-8
ENV LANG ru_RU.UTF-8
ENV LANGUAGE ru_RU:ru
ENV LC_ALL ru_RU.UTF-8

RUN mkdir /var/log/ca

ENV PYTHONUNBUFFERED 1


RUN cp project/local_settings.sample.py project/local_settings.py


CMD test "$(ls /conf/local_settings.py)" || cp project/local_settings.sample.py /conf/local_settings.py; \
    rm project/local_settings.py;  ln -s /conf/local_settings.py project/local_settings.py; \
    rm -rf static; ln -s /static static; \
    rm -rf media; ln -s /media media; \
    npm install; rm -rf static/node_modules; mv node_modules static/; \
    python ./manage.py migrate; \
    python ./manage.py collectstatic --noinput; \
    /usr/bin/supervisord -c /etc/supervisor/supervisord.conf --nodaemon

COPY supervisor/supervisord.conf /etc/supervisor/supervisord.conf
COPY supervisor/prod.conf /etc/supervisor/conf.d/ca.conf
COPY requirements.txt /ca/

RUN pip install -r requirements.txt
COPY . /opt/ca