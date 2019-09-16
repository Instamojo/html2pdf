FROM ubuntu:16.04

ENV DEBIAN_FRONTEND=noninteractive

# Pre-requisites for wkhtmltpdf and our application
RUN apt-get update -y && apt-get install -y \
    software-properties-common \
    build-essential \
    xorg \
    libssl-dev \
    libxrender-dev \
    libjpeg-turbo8-dev \
    fontconfig \
    xfonts-75dpi \
    wget

# Download wkhtmltopdf binary
RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.xenial_amd64.deb && \
    dpkg -i wkhtmltox_0.12.5-1.xenial_amd64.deb && \
    apt -f install

# Install font packages to install commonly used fonts. Accept Eula for Microsoft Fonts automatically.
RUN echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true | debconf-set-selections && \
    apt-get install -y ttf-mscorefonts-installer fonts-roboto fonts-noto

# Install python3.6
RUN add-apt-repository ppa:jonathonf/python-3.6 && apt-get update
RUN apt-get install python3.6 -y

# Set default version for `python3` as python3.6 (instead of 3.5)
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.5 1
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 2

# Application dependencies
COPY requirements.txt ./
RUN apt-get install -y python3-pip
RUN pip3 install -r requirements.txt

# PYTHONUNBUFFERED: Force stdin, stdout and stderr to be totally unbuffered. (equivalent to `python -u`)
# PYTHONHASHSEED: Enable hash randomization (equivalent to `python -R`)
ENV PYTHONUNBUFFERED=1 PYTHONHASHSEED=random

ADD app.py gunicorn.conf.py ./

# Copy testcases and tests
# This is used only by CircleCI while running tests
COPY tests.py ./
COPY testcases ./testcases

EXPOSE 8080

USER nobody

ENTRYPOINT ["usr/local/bin/gunicorn"]

# Show the extended help
CMD ["--conf", "gunicorn.conf.py", "app:application"]
