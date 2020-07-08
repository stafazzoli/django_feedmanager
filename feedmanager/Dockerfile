FROM python:3.8

ENV PYTHONUNBUFFERED 1
ENV DOCKER_CONTAINER 1

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt
RUN rm requirements.txt

COPY . /app/

EXPOSE 8000