FROM python:slim-bookworm

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app /app/app

EXPOSE 5000

ENV FLASK_APP=app/app.py

CMD ["gunicorn", "--chdir", "/app", "app.app:app", "--workers", "4", "--bind", "0.0.0.0:5000"]
