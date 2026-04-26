FROM python:3.14-slim

WORKDIR /app

COPY pyproject.toml .
COPY src/ ./src/

RUN pip install --no-cache-dir .

COPY . .

EXPOSE 8000

CMD ["uvicorn", "mini_search.api:app", "--host", "0.0.0.0", "--port", "8000"]