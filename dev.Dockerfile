FROM python:slim
WORKDIR /realmusic
RUN apt-get update && \
    apt-get -y install libpq-dev gcc
ADD requirements.txt .
RUN pip install -r requirements.txt
ADD . .