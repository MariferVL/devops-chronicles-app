FROM python:slim-bookworm

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app /app/app

RUN chmod +x /app/app/entrypoint.sh

EXPOSE 5000

ENV FLASK_APP=app/app.py

ENTRYPOINT ["/app/app/entrypoint.sh"]
