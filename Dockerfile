FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python", "-m", "weather"]
