# Быстрый старт

## Для Windows (PowerShell)

```powershell
# 1. Полная сборка и запуск (рекомендуется для первого запуска)
.\setup.ps1 full-setup

# 2. Логи и завершить проект
.\setup.ps1 logs
.\setup.ps1 down
```

## Для Linux/Mac

```bash
# 1. Полная сборка и запуск
make full-setup

# 2. Логи и завершить проект
make logs
make down
```

## Что запустится

- API: http://localhost:8000
- Документация: http://localhost:8000/docs
- База данных: PostgreSQL на порту 5432
- Workers: KudaGo парсер и система уведомлений

## Основные команды

### Windows
```powershell
.\setup.ps1 help
.\setup.ps1 up
.\setup.ps1 down
.\setup.ps1 logs
.\setup.ps1 clean
```

### Linux/Mac
```bash
make help
make up
make down
make logs
make clean
```

## Переменные окружения

Создайте `.env` файл в корне проекта:
```env
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=notification_db
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
DATABASE_URL=postgresql+asyncpg://user:password@postgres:5432/notification_db
```

## Дальнейшие шаги

1. Откройте http://localhost:8000/docs
2. Протестируйте API endpoints
3. Добавьте свои события через POST /api/v1/events
4. Проверьте логи workers: `.\setup.ps1 logs`

## Возможные проблемы

- Порт занят: Измените порт в docker-compose.yaml
- База не подключается: Проверьте переменные окружения
- Workers не работают: Проверьте логи `.\setup.ps1 logs` 
- Нет уведомлений в базе данных: они формируются раз в 5 минут
