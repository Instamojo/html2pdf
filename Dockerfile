FROM ubuntu:14.04

RUN sed 's/main$/main universe/' -i /etc/apt/sources.list
RUN apt-get update
RUN apt-get upgrade -y

# Download and install wkhtmltopdf
RUN apt-get install -y build-essential xorg libssl-dev libxrender-dev wget gdebi && apt-get install -y python-pip
RUN echo "deb http://httpredir.debian.org/debian jessie contrib" > /etc/apt/sources.list.d/contrib.list ;\
    echo "deb http://httpredir.debian.org/debian jessie-updates contrib" >> /etc/apt/sources.list.d/contrib.list ;\
    echo "deb http://security.debian.org jessie/updates contrib" >> /etc/apt/sources.list.d/contrib.list
RUN apt-get update -y && apt-get install --force-yes -y ttf-mscorefonts-installer fonts-roboto
RUN fc-cache -fv
RUN wget http://download.gna.org/wkhtmltopdf/0.12/0.12.3/wkhtmltox-0.12.3_linux-generic-amd64.tar.xz
RUN tar -xJf wkhtmltox-0.12.3_linux-generic-amd64.tar.xz
RUN cp wkhtmltox/bin/wkhtmltopdf /usr/local/bin/wkhtmltopdf
RUN cp wkhtmltox/bin/wkhtmltoimage /usr/local/bin/wkhtmltoimage
RUN pip install werkzeug executor gunicorn

ADD app.py /app.py
ADD guincorn.conf.py /guincorn.conf.py
EXPOSE 80

ENTRYPOINT ["usr/local/bin/gunicorn"]

# Show the extended help
CMD ["--conf", "guincorn.conf.py", "app:application"]
