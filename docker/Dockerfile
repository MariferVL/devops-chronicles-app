FROM python:slim-bookworm

WORKDIR /app

RUN echo "=== Build Context: Listing all Python files ===" && \
    find . -type f -name "*.py" | sort

RUN echo "=== Build Context: Listing migration version files ===" && \
    find . -type f -path "app/migrations/versions/*" | sort

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app /app/app

RUN echo "=== Image: Listing /app/app/migrations/versions/ ===" && \
    ls -laR /app/app/migrations/versions

RUN chmod +x /app/app/entrypoint.sh

EXPOSE 5000

ENV FLASK_APP=app/app.py

ENTRYPOINT ["/app/app/entrypoint.sh"]
