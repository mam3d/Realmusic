FROM python:slim
WORKDIR /realmusic
ADD requirements.txt .
RUN pip3 install -r requirements.txt
ADD . .