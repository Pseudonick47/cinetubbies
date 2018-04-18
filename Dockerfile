FROM python:3
ENV PYTHONUNBUFFERED 1
RUN apt-get -qq update
RUN apt-get -qq -y install netcat
RUN mkdir /code
WORKDIR /code
ADD backend/requirements.txt /code/
RUN pip install -r requirements.txt
ADD backend /code/
