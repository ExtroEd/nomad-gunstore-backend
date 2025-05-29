FROM python:3.12-slim

LABEL authors="ExtroEd"

WORKDIR /app

RUN apt-get update && apt-get install -y curl \
    && curl -sSL https://install.python-poetry.org | python - \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.local/bin:$PATH"
ENV PYTHONUNBUFFERED=1

RUN poetry config virtualenvs.create false

# Копируем только зависимости сначала (для кэширования)
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

RUN mkdir -p /app/logs

# Копируем весь остальной проект
COPY . .

# Копируем и настраиваем entrypoint
COPY entrypoint.web.sh /app/entrypoint.sh
COPY entrypoint.celery.sh /app/entrypoint.celery.sh
RUN chmod +x /app/entrypoint.web.sh /app/entrypoint.celery.sh
