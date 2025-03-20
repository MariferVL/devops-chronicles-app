FROM python:slim-bookworm

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app /app/app
COPY migrations /app/migrations    
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 5000

ENV FLASK_APP=app/app.py

ENTRYPOINT ["/app/entrypoint.sh"]
