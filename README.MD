# Library API

REST API для управления библиотекой: книги, читатели, выдача и возврат книг. Реализовано на FastAPI с PostgreSQL и JWT-аутентификацией.

---

## Инструкция по запуску

1. Клонируйте репозиторий и создайте виртуальное окружение:

```bash
git clone <repo_url>
cd library_api
python -m venv .venv
source .venv/bin/activate  # Linux/MacOS
# или
.venv\Scripts\activate  # Windows
```

2. Установите зависимости:

```bash
pip install -r requirements.txt
```

3. Создадим `.env` в корневом каталоге и перенесём все настройки из `.env.example` в него.

## Список всех возможных настроек `.env`
| Переменная                        | Назначение                                              |
| --------------------------------- | ------------------------------------------------------- |
| `JWT_SECRET_KEY`                  | Секретный ключ для подписи JWT токенов                  |
| `JWT_ALGORITHM`                   | Алгоритм подписи JWT (например, HS256)                  |                   |
| `DB_HOST`                         | Адрес сервера PostgreSQL                                |
| `DB_PORT`                         | Порт подключения к базе данных                          |
| `DB_NAME`                         | Название базы данных                                    |
| `DB_USER`                         | Имя пользователя базы данных                            |
| `DB_PASSWORD`                     | Пароль пользователя базы данных                         |
| `ECHO_SQL`                        | Выводить SQL-запросы в консоль (TRUE/FALSE)             |
| `LOG_FILE`                        | Включить логирование в файл (TRUE/FALSE)                |
| `RATE_LIMITER`                    | Количество допустимых запросов в минуту на пользователя |


4. Настройте подключение к базе данных в `.env`:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/library_db
SECRET_KEY=your_secret_key_for_jwt
```

5. Выполните миграции Alembic для создания таблиц:

```bash
alembic upgrade head
```

6. Запустите приложение:

```bash
uvicorn main:app --reload
# или
python main.py
```

7. **Регистрация первого пользователя (библиотекаря)**:

   * Отправьте POST-запрос на `/auth/register` с JSON:

     ```json
     {
       "email": "admin@example.com",
       "password": "password"
     }
     ```

   * После успешной регистрации получите возможность логина и работы с API.

---

## Структура проекта

* `main.py` — точка входа с созданием FastAPI-приложения.
* `config.py` — настройки приложения.
* `routes/` — папка с роутерами:

  * `auth.py` — регистрация и логин пользователей (библиотекарей).
  * `books.py` — CRUD книги.
  * `readers.py` — CRUD читатели.
  * `borrow.py` — выдача и возврат книг.
* `database/` — папка со структурой данных: ORM-модели SQLAlchemy и Pydantic-схемы.

  * `session.py` - управление сессиями
  * `models.py` — ORM модели SQLAlchemy (пользователи, книги, читатели, выдачи).
  * `schemas.py` — Pydantic-схемы для валидации и сериализации данных.
* `utils/` — вспомогательные функции и утилиты, используемые в проекте.

  * `dependencies.py` — функция для верефикации API запроса защищённого JWT
  * `jwt.py` - функция для генерации и валидации JWT токенов
  * `logger.py` - система логирования
  * `rate_limiter.py` - класс для ограничения количества запросов
* `alembic/` — миграции базы данных.
* `tests/` — тесты Pytest для бизнес-логики и эндпоинтов.
* `logs/` — папка с логами приложения
* `.github/` — папка с тестами для Github Actions

---

## Описание структуры базы данных

* **Пользователи (Users):**

  * id (PK)
  * email (уникальный)
  * password_hash (строка, обязательный)
  * created_at (дата и время)

* **Книги (Books):**

  * id (PK)
  * title (строка, обязательное)
  * author (строка, обязательное)
  * year (число, необязательное)
  * isbn (уникальное, необязательное)
  * copies (число, >=0, по умолчанию 1)
  * description (текст, необязательное, добавлено во второй миграции)

* **Читатели (Readers):**

  * id (PK)
  * name (строка, обязательное)
  * email (уникальный, обязательное)

* **Выдачи книг (BorrowedBooks):**

  * id (PK)
  * book\_id (FK на Books)
  * reader\_id (FK на Readers)
  * borrow\_date (дата и время)
  * return\_date (дата и время, NULL если не возвращена)

### Наглядно структуру можно посмотреть [здесь](https://dbdiagram.io/d/Libre-API-682b270b1227bdcb4ef8590e).

Вот пример описания принятых решений по структуре базы данных, который можно добавить после твоего раздела **Описание структуры базы данных**:

---

## Описание принятых решений по структуре базы данных

1. **Разделение пользователей и читателей:**
   Пользователи (`Users`) отвечают за учетные записи и аутентификацию в системе (библиотекари, администраторы и т.п.), а читатели (`Readers`) — это отдельная сущность, которая отражает фактических посетителей библиотеки, получающих книги. Такое разделение позволяет более гибко управлять ролями и правами доступа.

2. **Модель книги с учетом копий:**
   В модели книги (`Books`) предусмотрено поле `copies`, отражающее количество доступных экземпляров книги. Это упрощает учет и предотвращает выдачу большего количества экземпляров, чем есть в наличии.

3. **Выдачи книг и контроль сроков:**
   Модель `BorrowedBooks` хранит записи о том, какие книги и кому выданы, а также даты выдачи и возврата. Поле `return_date` может быть NULL, если книга еще не возвращена. Это позволяет легко отслеживать текущие и просроченные выдачи.

4. **Возможность расширения:**
   Добавление поля `description` в книгах во второй миграции показывает, что структура может адаптироваться под новые требования без существенных изменений в архитектуре.

5. **Уникальные ограничения:**
   Уникальность email для пользователей и читателей гарантирует отсутствие дублирующих записей и облегчает идентификацию в системе.

6. **Ссылочная целостность:**
   Использование внешних ключей (`FK`) для связывания выдачи с книгами и читателями обеспечивает целостность данных и удобство навигации между связанными сущностями.

---

## Бизнес-логика

### 4.1 Выдача книги

* POST `/borrow/` - выдать книгу
* Тело запроса:
```
{
    "reader_id": 2,
    "book_id": 2
}
```

* Книгу можно выдать только если `copies > 0`.
* При выдаче `copies` уменьшается на 1.
* Создается запись в `BorrowedBooks` с `borrow_date` и `return_date = NULL`.
* Ограничение: читатель не может иметь более 3-х одновременно выданных книг.

**Сложности и решение:**
Проверка ограничений и обновление количества экземпляров сделаны в транзакции (запросы о выдаче остаются в бд), чтобы избежать гонок при параллельных запросах.

---

### 4.2 Возврат книги

* При возврате `copies` увеличивается на 1.
* В записи о выдаче выставляется `return_date`.
* Проверяется, что книга действительно была выдана этому читателю и не была уже возвращена.

**Сложности:**
Обработка ошибок, если книга не была выдана или уже возвращена, реализована через HTTP исключения с понятными сообщениями.

---

### 4.3 Управление читателями и книгами

* CRUD операции защищены JWT.
* Читатели не имеют своих паролей, ими управляют библиотеки.
* ISBN уникален, количество экземпляров не может быть отрицательным.

---

## Реализация аутентификации

* Используется библиотека **python-jose** для генерации и проверки JWT-токенов.
* Пароли хранятся в хешированном виде с помощью **passlib\[bcrypt]**.
* При регистрации пользователя пароль хешируется.
* При логине проверяется пароль и, в случае успеха, возвращается JWT access token.
* Все эндпоинты управления книгами, читателями, выдачей и возвратом защищены JWT.
* Эндпоинты `/auth/register` и `/auth/login` — открытые.
* Для получения текущего пользователя используется FastAPI-зависимость `get_current_user`, которая валидирует токен из заголовка Authorization.


### Полный список ендпоинтов и их описание можно глянуть [здесь](https://www.postman.com/aviation-astronomer-88961798/libre-api/collection/uiprwju/libre-api)

---

## Предложение дополнительной функции

### Просроченные книг

**Идея:**
Добавить фоновый таск, который раз в сутки проверяет записи в `BorrowedBooks` без `return_date` и с датой выдачи старше допустимого срока (например, 30 дней). Находит читателей с просроченными книгами и отправляет им email-уведомления.

**Реализация:**

* Использовать FastAPI background tasks или Celery.
* В базе добавить поле `due_date` или вычислять срок из `borrow_date`.
* Настроить SMTP-сервер и шаблоны писем.
* Создать отдельный эндпоинт или расписание, вызывающее задачу отправки писем.

---