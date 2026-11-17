# Calculator backend in a small Python image.
#
# Build:  docker build -t finn-calculator .
# Run:    docker run --rm -p 5000:5000 finn-calculator

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

RUN useradd --create-home --uid 1000 appuser
USER appuser

EXPOSE 5000

# Bind to 0.0.0.0 so the port is reachable from outside the container.
# The `python app.py` entry point uses 127.0.0.1:5000, which only works outside Docker.
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
