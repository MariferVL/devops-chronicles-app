FROM python:slim-bookworm

WORKDIR /app

COPY requirements.txt .

RUN apt update && apt install -y netcat-openbsd && \
    pip install --no-cache-dir -r requirements.txt

COPY app /app/app

COPY docker/scripts/ /app/scripts/

RUN chmod +x /app/scripts/*.sh

EXPOSE 5000

ENV FLASK_APP=app/app.py

ENTRYPOINT ["/app/scripts/entrypoint.sh"]