# NotificationEventParser

**NotificationEventParser** — это Python-проект для парсинга событий с KudaGo и отправки уведомлений, использующий PostgreSQL, Alembic для миграций и полностью контейнеризованный с помощью Docker Compose.

---

## 📦 Структура проекта

```
NotificationEventParser/
├── backend/
│   ├── src/
│   │   ├── workers/
│   │   │   ├── kudago_worker.py
│   │   │   └── notification_worker.py
│   │   ├── models/
│   │   └── repository/
│   │       └── migrations/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── scripts/
│       ├── entrypoint_project.sh
│       ├── entrypoint_alembic.sh
│       └── entrypoint_alembic_revision.sh
├── docker-compose.yaml
└── Makefile
```

---

## 🚀 Быстрый старт

### 1. Клонируйте репозиторий и настройте переменные окружения

Создайте `.env` в корне или используйте переменные окружения (пример):

```
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=notification_db
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
DATABASE_URL=postgresql+asyncpg://user:password@postgres:5432/notification_db
```

### 2. Соберите образы

```sh
docker-compose build
```

### 3. Примените миграции Alembic

```sh
docker-compose up alembic
```
или
```sh
docker-compose run --rm alembic /scripts/entrypoint_alembic.sh
```

### 4. Запустите воркеры и базу

```sh
docker-compose up kudago_worker notification_worker postgres
```

---

## 🛠️ Основные команды

- **Применить миграции:**  
  `docker-compose up alembic`
- **Создать новую миграцию:**  
  `docker-compose run --rm alembic /scripts/entrypoint_alembic_revision.sh "migration message"`
- **Запустить парсер и нотификатор:**  
  `docker-compose up kudago_worker notification_worker postgres`
- **Остановить все сервисы:**  
  `docker-compose down`

---

## 📝 Описание воркеров

- **kudago_worker.py** — асинхронно парсит события с KudaGo, сохраняет новые в базу, избегает дубликатов.
- **notification_worker.py** — отвечает за отправку уведомлений (нереализовано)

---

## 🗄️ Миграции и база данных

- Используется Alembic для управления схемой.
- Все миграции хранятся в `backend/src/repository/migrations/versions/`.
- Для чистого старта можно удалить volume базы:  
  `docker-compose down -v`

---

## 🐳 Docker Compose

- Все сервисы полностью изолированы.
- Для разработки и продакшена можно использовать разные переменные окружения.


---

## 📄 Лицензия

Проект распространяется под лицензией MIT.
