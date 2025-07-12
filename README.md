# Notification Event Parser

Система для парсинга событий с KudaGo и отправки уведомлений о предстоящих мероприятиях.

## Описание

Проект состоит из нескольких компонентов:
- **KudaGo Worker** - парсер событий с KudaGo API
- **Notification Worker** - система уведомлений о предстоящих событиях
- **FastAPI** - REST API для управления событиями и уведомлениями
- **PostgreSQL** - база данных для хранения событий и уведомлений
- **Alembic** - система миграций базы данных

## Архитектура

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   KudaGo API    │    │  Notification    │    │   FastAPI       │
│                 │    │     Worker       │    │                 │
└─────────┬───────┘    └────────┬─────────┘    └─────────┬───────┘
          │                     │                        │
          └─────────────────────┼────────────────────────┘
                                │
                    ┌───────────▼───────────┐
                    │     PostgreSQL        │
                    │   (Events, Notifications) │
                    └───────────────────────┘
```

## Быстрый старт

### Для Windows (PowerShell):
```powershell
# Полная сборка и запуск (рекомендуется для первого запуска)
.\setup.ps1 full-setup

# Просмотр логов
.\setup.ps1 logs

# Остановка проекта
.\setup.ps1 down
```

### Для Linux/Mac (Make):
```bash
# Полная сборка и запуск
make full-setup

# Просмотр логов
make logs

# Остановка проекта
make down
```

### Ручной запуск:
```bash
# Сборка и запуск всех сервисов
docker-compose up -d

# Применение миграций
docker-compose up alembic -d
```

## API Endpoints

После запуска API доступен по адресу: http://localhost:8000

### Документация API
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Основные endpoints:

#### События (`/api/v1/events`)
- `GET /events` - список событий с пагинацией и поиском
- `GET /events/{event_id}` - получить конкретное событие
- `POST /events` - создать новое событие
- `GET /events/upcoming/notifications` - события для уведомлений

#### Уведомления (`/api/v1/notifications`)
- `GET /notifications` - список отправленных уведомлений
- `GET /notifications/stats` - статистика по уведомлениям
- `DELETE /notifications/{notification_id}` - удалить уведомление

## Команды управления

### Windows (PowerShell)
```powershell
.\setup.ps1 help                    # Показать справку
.\setup.ps1 full-setup              # Полная сборка и запуск
.\setup.ps1 build                   # Собрать контейнеры
.\setup.ps1 up                      # Запустить проект
.\setup.ps1 down                    # Остановить проект
.\setup.ps1 restart                 # Перезапустить проект
.\setup.ps1 logs                    # Показать логи
.\setup.ps1 clean                   # Очистить все
.\setup.ps1 migrate                 # Применить миграции
.\setup.ps1 api                     # Запустить только API
.\setup.ps1 workers                 # Запустить только workers
```

### Linux/Mac (Make)
```bash
make help                           # Показать справку
make full-setup                     # Полная сборка и запуск
make build                          # Собрать контейнеры
make up                             # Запустить проект
make down                           # Остановить проект
make restart                        # Перезапустить проект
make logs                           # Показать логи
make clean                          # Очистить все
make migrate                        # Применить миграции
make api                            # Запустить только API
make workers                        # Запустить только workers
```

## Структура проекта

```
NotificationEventParser/
├── backend/
│   ├── src/
│   │   ├── api/                    # FastAPI приложение
│   │   │   ├── main.py            # Основное приложение
│   │   │   └── routes/            # API роуты
│   │   ├── models/                # Модели данных
│   │   │   ├── db/                # SQLAlchemy модели
│   │   │   └── schemas/           # Pydantic схемы
│   │   ├── repository/            # Работа с БД
│   │   │   ├── crud/              # CRUD операции
│   │   │   └── migrations/        # Миграции Alembic
│   │   ├── workers/               # Фоновые процессы
│   │   │   ├── kudago_worker.py   # Парсер KudaGo
│   │   │   └── notification_worker.py # Система уведомлений
│   │   └── config/                # Конфигурация
│   ├── requirements.txt           # Python зависимости
│   └── Dockerfile                 # Docker образ
├── docker-compose.yaml            # Docker Compose конфигурация
├── Makefile                       # Команды для Linux/Mac
├── setup.ps1                      # Команды для Windows
└── README.md                      # Документация
```

## Система уведомлений

### Логика работы:
1. Notification Worker запускается каждые 5 минут
2. Проверяет события, которые начинаются в течение следующих 24 часов и 7 дней
3. Отправляет уведомления за день и за неделю до события
4. Отслеживает отправленные уведомления в таблице `notification_sent`

### Типы уведомлений:
- day_before — за 24 часа до события
- week_before — за 7 дней до события

## База данных

### Основные таблицы:
- **events** - события с KudaGo
- **kudago_events** - отслеживание обработанных событий
- **notification_sent** - отправленные уведомления

### Миграции:
```bash
make migrate
# или
# docker-compose run --rm alembic alembic revision --autogenerate -m "описание"
```

## Конфигурация

### Переменные окружения:
Создайте файл `.env` в корне проекта:
```env
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=notification_db
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
DATABASE_URL=postgresql+asyncpg://user:password@postgres:5432/notification_db
```

## Логирование

### Просмотр логов:
```bash
make logs
# или
# docker-compose logs -f api
# docker-compose logs -f kudago_worker
# docker-compose logs -f notification_worker
```

## Отладка

### Проверка статуса сервисов:
```bash
docker-compose ps
```

### Подключение к базе данных:
```bash
docker-compose exec postgres psql -U user -d notification_db
```

### Перезапуск конкретного сервиса:
```bash
docker-compose restart api
# или
# docker-compose restart kudago_worker
# docker-compose restart notification_worker
```

## Мониторинг

### API Health Check:
```bash
curl http://localhost:8000/health
```

### Статистика уведомлений:
```bash
curl http://localhost:8000/api/v1/notifications/stats
```


### Создание миграций:
```bash
docker-compose run --rm alembic alembic revision --autogenerate -m "описание изменений"
make migrate
```

## Лицензия

MIT License — см. файл [LICENSE.md](LICENSE.md)
