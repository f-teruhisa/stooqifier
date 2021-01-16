# Use slim-buter image instead of alpine, because alpine can make builds slower
FROM python:3.9.1-slim-buster
USER root

LABEL maintainer = "f-teruhisa <teru_fukumoto@outlook.jp>"

RUN apt-get update && \
    apt-get install -y --no-install-recommends

RUN mkdir /work
WORKDIR /work
ADD . /work

# Use pipenv for management dependencies woth virtualenv
RUN pip install --upgrade pip && \
    pip install --upgrade setuptools && \
    pip install -r requirements.txt
