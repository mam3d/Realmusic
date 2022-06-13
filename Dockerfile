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
    apt-get -y install postgresql-client && \
    apt-get -y install cron
ADD . .