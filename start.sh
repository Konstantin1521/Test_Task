#!/bin/sh

# Переходим в директорию fastapi_application
cd fastapi_application

# Получаем текущую версию миграций
CURRENT_VERSION=$(alembic current)

# Получаем последнюю версию миграций
LATEST_VERSION=$(alembic heads)

# Сравниваем версии
if [ "$CURRENT_VERSION" != "$LATEST_VERSION" ]; then
    echo "Выполняем миграции..."
    alembic upgrade head
else
    echo "Миграции уже актуальны."
fi

# Запускаем приложение
exec uvicorn main:app --host 0.0.0.0 --port 8000
