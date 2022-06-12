FROM python:slim
WORKDIR /realmusic
ADD requirements.txt .
RUN apt-get update && \
    apt-get -y install libpq-dev gcc && \
    apt-get -y install postgresql-client && \
    apt-get -y install cron && \
    pip install -r requirements.txt
ADD . .