# Используем официальный образ Python
FROM python:3.12-slim

# Об авторах (опционально)
LABEL authors="ExtroEd"

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем проект
COPY . .

# Устанавливаем Poetry
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"

# Устанавливаем зависимости
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

# Открываем порт
EXPOSE 8000

RUN poetry run python manage.py collectstatic --noinput

# Команда запуска (если не используется docker-compose)
CMD ["poetry", "run", "gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
