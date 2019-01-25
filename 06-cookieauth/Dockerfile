FROM ubuntu:bionic

RUN apt update
RUN apt install -y apache2 curl python3 vim python3-scrypt

RUN a2enmod cgi
RUN rm /var/www/html/index.html

ADD index.py /var/www/html/index.py
ADD site.conf /etc/apache2/sites-available/000-default.conf

CMD /usr/sbin/apache2ctl -D FOREGROUND
