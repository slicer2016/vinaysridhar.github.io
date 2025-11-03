FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY webhook.py .

EXPOSE 8080

CMD ["sh", "-c", "gunicorn webhook:app --bind 0.0.0.0:${PORT:-8080} --workers 1 --timeout 120 --log-level info"]