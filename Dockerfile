FROM python:slim
WORKDIR /realmusic
ADD requirements.txt .
RUN apt-get update && \
    apt-get -y install libpq-dev gcc && \
    apt -y install postgresql-client && \
    pip install -r requirements.txt
ADD . .