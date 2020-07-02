FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /Stockify

COPY Pipfile Pipfile.lock /Stockify/
RUN pip install pipenv && pipenv install --system

COPY . /Stockify/
