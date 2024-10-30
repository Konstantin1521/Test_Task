FROM python:3.11

WORKDIR /app

COPY requirements.txt ./
COPY .env ./

RUN pip install --no-cache-dir -r requirements.txt

COPY fastapi-application ./fastapi-application

ENV PYTHONPATH=/app/fastapi-application

CMD ["uvicorn", "fastapi-application.main:app", "--host", "0.0.0.0", "--port", "8000"]
