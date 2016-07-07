FROM python:2.7
MAINTAINER alejandro.barrera@duke.edu

# basic flask environment
RUN pip install --upgrade pip \
	&& pip install flask

RUN apt-get update && apt-get install -y \
    git \
    openjdk-7-jdk

ENV GETHIC_GIT https://github.com/alexbarrera/get-hic.git

# TODO: Possibly remove when creating additional project to install get-hic server
ADD bin/juicebox_tools.jar /Users/abarrera/bin/

RUN git clone $GETHIC_GIT

# flask app in env
ENV FLASK_APP get-hic/__init__.py

# expose web server port
# only http, for ssl use reverse proxy
EXPOSE 8000

# fireup flask app
CMD ["flask", "run", "-p", "8000", "-h", "0.0.0.0"]