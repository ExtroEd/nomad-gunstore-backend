📦 Первый запуск или после изменения зависимостей:
docker-compose down
docker-compose down -v
docker-compose up --build

🌀 Запуск без пересборки:
docker-compose up

🧩 Выполнение команды Django (например, миграции):
docker-compose exec web poetry run python manage.py makemigrations
docker-compose exec web poetry run python manage.py migrate
docker-compose exec web poetry run python manage.py createsuperuser

Если у тебя уже всё собрано, просто:
docker-compose up -d

npm run dev