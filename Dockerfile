LABEL authors="ExtroEd"

ENTRYPOINT ["top", "-b"]

# Используем официальный образ Python
FROM python:3.10

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . .

# Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"

# Устанавливаем зависимости через Poetry
RUN poetry install --no-root

# Запускаем сервер
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
