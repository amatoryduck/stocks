FROM ubuntu:18.04

RUN apt -y update && apt -y upgrade
RUN apt install -y python3
RUN apt install -y python3-pip
RUN /usr/bin/pip3 install yfinance && /usr/bin/pip3 install lxml && /usr/bin/pip3 install bs4
RUN /usr/bin/pip3 install PyPI && /usr/bin/pip3 install psycopg2-binary

COPY . .