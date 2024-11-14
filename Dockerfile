FROM python:3.11

WORKDIR /app

COPY requirements.txt ./
COPY .env ./
COPY start.sh ./

RUN pip install --no-cache-dir -r requirements.txt

COPY fastapi_application ./fastapi_application

ENV PYTHONPATH=/app/fastapi_application

CMD ["./start.sh"]
