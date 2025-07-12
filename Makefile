.PHONY: build up down restart logs clean migrate api workers help

# Основные команды
build: ## Собрать все контейнеры
	docker-compose build

up: ## Запустить весь проект
	docker-compose up -d

down: ## Остановить весь проект
	docker-compose down

restart: ## Перезапустить весь проект
	docker-compose restart

logs: ## Показать логи всех сервисов
	docker-compose logs -f

clean: ## Очистить все контейнеры и volumes
	docker-compose down -v --remove-orphans
	docker system prune -f

# Миграции
migrate: ## Применить миграции базы данных
	docker-compose up alembic -d
	sleep 5
	docker-compose logs alembic

# Отдельные сервисы
api: ## Запустить только API сервер
	docker-compose up api -d

workers: ## Запустить только workers
	docker-compose up kudago_worker notification_worker -d

# Полная сборка и запуск
full-setup: ## Полная сборка и запуск проекта (рекомендуется для первого запуска)
	docker-compose down -v --remove-orphans
	docker-compose build
	docker-compose up postgres -d
	sleep 10
	docker-compose up alembic -d
	sleep 5
	docker-compose up -d
	@echo "🚀 Проект запущен!"
	@echo "📊 API доступен по адресу: http://localhost:8000"
	@echo "📚 Документация API: http://localhost:8000/docs"
	@echo "📝 Логи: make logs"

# Помощь
help: ## Показать эту справку
	@echo "Доступные команды:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' 