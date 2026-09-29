# Wallet API

Асинхронный REST API для управления балансом кошелька. Позволяет пополнять и снимать средства с обработкой конкурентных запросов.

## Возможности

- Получение баланса кошелька
- Пополнение кошелька (DEPOSIT)
- Снятие средств (WITHDRAW)
- Защита от отрицательного баланса
- Атомарные операции на уровне БД
- Обработка конкурентных запросов (race condition)
- Асинхронный стек (FastAPI + SQLAlchemy)

## Технологии

- **Python** 3.11
- **FastAPI** — веб-фреймворк
- **SQLAlchemy** (async) — ORM
- **Alembic** — миграции
- **PostgreSQL** — база данных
- **Pytest** + **httpx** — тестирование
- **Docker** + **Docker Compose** — контейнеризация

## Структура проекта

```

├── app/
│ ├── api/
│ │ └── v1/
│ │ └── wallets.py # эндпоинты кошелька
│ ├── models/
│ │ ├── database.py # подключение к БД
│ │ └── wallet.py # ORM модель
│ ├── schemas/
│ │ └── wallet.py # Pydantic схемы
│ ├── settings.py # конфигурация
│ └── main.py # входная точка
├── alembic/ # Alembic миграции
├── tests/ # тесты
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .env

```

## Быстрый старт

### 1. Клонирование репозитория

git clone https://github.com/Tvoysuperior/wallet-api.git
cd wallet-api
### 2. Настройка окружения
Создайте файл .env в корне проекта:

env

DB_USER=postgres

DB_PASSWORD=postgres

DB_HOST=localhost

DB_PORT=5432

DB_NAME=wallet_db
### 3. Запуск через Docker 
docker-compose up -d

API будет доступно по адресу: http://localhost:8000

Документация Swagger: http://localhost:8000/docs

### 4. Локальный запуск (без Docker)
Установите зависимости:

pip install -r requirements.txt
Настройте PostgreSQL и примените миграции:

alembic upgrade head

Запустите сервер:

uvicorn app.main:app --reload

API Эндпоинты

Получить баланс кошелька

GET /api/v1/wallets/{wallet_uuid}

Ответ:

json
{
  "wallet_uuid": "123e4567-e89b-12d3-a456-426614174000",
  "balance": 1500
}
Выполнить операцию (пополнение/снятие)

POST /api/v1/wallets/{wallet_uuid}/operation

Тело запроса:

json
{
  "operation_type": "DEPOSIT",  // или "WITHDRAW"
  "amount": 500
}

Успешный ответ (200):

json
{
  "wallet_uuid": "123e4567-e89b-12d3-a456-426614174000",
  "balance": 2000
}

Ошибки:

404 Not Found — кошелёк не найден

409 Conflict — недостаточно средств

### 5.Тестирование

Запуск тестов

pytest tests/ -v

Запуск тестов в Docker

docker-compose run --rm app pytest tests/ -v

### Что тестируется

Получение баланса существующего/несуществующего кошелька

Пополнение и снятие средств

Ошибка при недостатке средств

Атомарность конкурентных списаний — два параллельных запроса на снятие не позволяют уйти в минус

