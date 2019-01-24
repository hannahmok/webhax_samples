FROM ubuntu:bionic

RUN apt update
RUN apt install -y apache2 curl python3 vim

RUN a2enmod cgi
RUN rm /var/www/html/index.html

ADD index.py /var/www/html/index.py
ADD books /var/www/html/books
ADD site.conf /etc/apache2/sites-available/000-default.conf

CMD /usr/sbin/apache2ctl -D FOREGROUND
