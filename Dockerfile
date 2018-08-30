FROM ubuntu:16.04

ENV DEBIAN_FRONTEND=noninteractive

# Pre-requisites for wkhtmltpdf and our application
RUN apt-get update -y && apt-get install -y \
    build-essential \
    xorg \
    libssl-dev \
    libxrender-dev \
    fontconfig

# Download wkhtmltopdf binary
RUN apt-get install -y wget && \
    wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz && \
    tar -xJf wkhtmltox-0.12.4_linux-generic-amd64.tar.xz && \
    cp wkhtmltox/bin/wkhtmltopdf /usr/local/bin/wkhtmltopdf && \
    rm -rf wkhtmltox wkhtmltox-0.12.4_linux-generic-amd64.tar.xz

# Install font packages to install commonly used fonts. Accept Eula for Microsoft Fonts automatically.
RUN echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true | debconf-set-selections && \
    apt-get install -y ttf-mscorefonts-installer fonts-roboto fonts-noto

# Application dependencies
RUN apt-get install -y python-pip && pip install werkzeug executor gunicorn requests

# PYTHONUNBUFFERED: Force stdin, stdout and stderr to be totally unbuffered. (equivalent to `python -u`)
# PYTHONHASHSEED: Enable hash randomization (equivalent to `python -R`)
ENV PYTHONUNBUFFERED=1 PYTHONHASHSEED=random

ADD app.py gunicorn.conf.py tests.py testcases/  ./

EXPOSE 8080

USER nobody

ENTRYPOINT ["usr/local/bin/gunicorn"]

# Show the extended help
CMD ["--conf", "gunicorn.conf.py", "app:application"]

RUN python tests.py
