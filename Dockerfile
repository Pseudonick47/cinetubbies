FROM python:3
ENV PYTHONUNBUFFERED 1

RUN apt-get -qq update
RUN apt-get -qq -y install netcat
RUN mkdir /code
WORKDIR /code
RUN pip install pipenv

ADD backend/ /code
WORKDIR /code/backend
