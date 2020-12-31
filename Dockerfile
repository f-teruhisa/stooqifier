# Use slim-buter image instead of alpine, because alpine can make builds slower
FROM python:3.9.1-slim-buster

LABEL maintainer = "f-teruhisa <teru_fukumoto@outlook.jp>"

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    git \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir /work
WORKDIR /work
ADD . /work

RUN mkdir -p /src

COPY Pipfile Pipfile.lock /

# Use pipenv for management dependencies woth virtualenv
RUN pip install pipenv --no-cache-dir && \
    pipenv install --system --deploy && \
    pip uninstall -y pipenv virtualenv-clone virtualenv
