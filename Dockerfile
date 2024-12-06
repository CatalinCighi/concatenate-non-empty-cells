FROM python:3.11-slim
WORKDIR /app

# Install any required system packages if needed
# RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create non-root user
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV PORT=5000
ENV MODE=api

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD curl -f http://localhost:5000/concatenate || exit 1

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
