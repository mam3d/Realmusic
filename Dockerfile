FROM python:slim AS builder
ADD requirements.txt .
RUN python -m venv venv
ENV PATH="/venv/bin:$PATH"
RUN apt-get update && \
    apt-get -y install libpq-dev gcc && \
    pip install -r requirements.txt


FROM python:slim
WORKDIR /realmusic
COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"
RUN apt-get update && \
    apt-get -y install sudo && \
    apt-get -y install postgresql-client && \
    apt-get -y install cron && \
    apt-get -y install nginx && \
    apt-get -y install sudo

ADD . .
# edit default file with custom nginx config
RUN rm /etc/nginx/sites-enabled/default
COPY nginx/realmusic.conf  /etc/nginx/sites-enabled/
ADD start.sh /
RUN chmod +x /start.sh
EXPOSE 80 8000
CMD ["/start.sh"]