palmetto_store/
│── .git/                      # Git-репозиторий
│── .gitignore                 # Игнорируемые файлы
│── LICENSE                    # Лицензия
│── README.md                  # Описание проекта
│── docker-compose.yml         # Конфиг для Docker
│── Dockerfile                 # Образ Docker
│── pyproject.toml             # Poetry-зависимости
│── poetry.lock                # Lock-файл Poetry
│── .env                       # Переменные окружения (не в Git!)
│── config/                    # Главные настройки проекта
│   │── __init__.py
│   │── settings.py            # Конфиг Django (разбить на base, dev, prod)
│   │── urls.py                # Основные URL
│   │── wsgi.py                 # WSGI для сервера Gunicorn
│   │── asgi.py                 # ASGI для WebSocket'ов
│   │── celery.py               # Конфигурация Celery
│   └── gunicorn.conf.py        # Настройки Gunicorn
│── manage.py                   # Django-скрипт
│── apps/                       # Все приложения Django
│   │── __init__.py
│   │── authentication/         # Авторизация и JWT
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── services.py        # Бизнес-логика
│   │   ├── tasks.py           # Фоновые задачи Celery
│   │   └── tests.py
│   │── orders/                # Работа с заказами
│   │── products/              # Товары и каталог
│── db/                         # Конфигурация базы данных
│   ├── init.sql
│── static/                     # Статические файлы
│── media/                      # Загрузка изображений
│── scripts/                    # Скрипты для запуска проекта
│── tests/                      # Тесты (unit + integration)
│── logs/                       # Логи сервера и ошибок
│── docs/                       # Документация проекта
│   ├── business_logic.md       # Бизнес-логика
│   ├── api_documentation.md    # API-документация
└── ci-cd/                      # Настройки CI/CD
    ├── gitlab-ci.yml
