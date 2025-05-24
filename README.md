ibrary API (FastAPI)

RESTful API для управления библиотечным каталогом. Позволяет управлять книгами, читателями и их взаимодействием. JWT-аутентификация и роль библиотекаря.

 Установка и запуск



Создайте и активируйте virtualenv:

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

Установите зависимости:

pip install -r requirements.txt

Запустите API:

uvicorn app.main:app --reload

Swagger UI:

http://127.0.0.1:8000/docs

 Структура проекта

app/
├── main.py          # Точка входа FastAPI
├── models.py        # ORM-модели для SQLAlchemy
├── schemas.py       # Схемы Pydantic (валидация API)
├── database.py      # Подключение к базе
├── utils.py         # Хеширование и JWT
└── routes/
    ├── auth.py      # Регистрация/логин
    ├── books.py     # CRUD-книги
    ├── readers.py   # CRUD-читатели
    └── borrow.py    # Выдача/возврат книг

 JWT аутентификация

/auth/register — создает библиотекаря

/auth/login — выдает JWT access_token

Защищённые endpointы: /books, /readers, /borrow

JWT-токен в Swagger: Authorize > Bearer {token}

 Реализация бизнес-логики

 /borrow/take

Есть ли доступные экземпляры?

У читателя меньше 3 книг?

Создаётся BorrowedBook, quantity -= 1

↺ /borrow/return

Есть активная запись (return_date = NULL)?

Устанавливается return_date

quantity += 1

 Alembic миграции

alembic init alembic
alembic revision --autogenerate -m "initial"
alembic upgrade head

# Добавить description:
alembic revision --autogenerate -m "add description field"
alembic upgrade head

 Тесты (pytest)

Нельзя взять 4-ю книгу

Нет доступных копий

Без токена — 401

С токеном — 200

 Творческая фича

Рейтинг книг

После возврата читатель может оценить книгу (1–5)

Новая таблица: Rating(reader_id, book_id, score)

В GET /books — средняя оценка

 Git + PEP8

PEP8-стиль, black/lint

Содержательные коммиты

Код чётко разбит по модулям

