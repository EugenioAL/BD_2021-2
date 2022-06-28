FROM postgres:latest

ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_USER=postgres
ENV POSTGRES_DB=postgres

RUN apt-get update 
RUN apt-get install -y python3
RUN apt-get update 
RUN apt-get -y install python3-pip
RUN apt-get update 
RUN python3 -m pip install --upgrade pip
RUN apt-get update
RUN pip install psycopg2-binary
RUN apt-get update

ADD . /usr/app/
