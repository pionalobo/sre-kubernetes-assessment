FROM python:3.14-slim

RUN useradd --create-home --uid 10001 appuser

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser collector.py .

USER appuser

CMD ["python", "collector.py"]