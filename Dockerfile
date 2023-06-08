FROM python:3.11-alpine

# Install build dependencies
RUN apk update && apk add --no-cache \
    g++ \
    gcc \
    gfortran \
    musl-dev \
    lapack-dev \
    && rm -rf /var/cache/apk/*

WORKDIR /app

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt

COPY ./ ./
