# Dockerfile
FROM python:3.14-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port API runs on
EXPOSE 8000

# Run the application
CMD ["uvicorn", "src.mini_search.api:app", "--host", "0.0.0.0", "--port", "8000"]