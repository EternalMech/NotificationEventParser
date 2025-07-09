import os

class Settings:
    DB_HOST = os.environ.get("POSTGRES_HOST", "localhost")
    DB_PORT = int(os.environ.get("POSTGRES_PORT", 5432))
    DB_NAME = os.environ.get("POSTGRES_DB", "notification_db")
    DB_USER = os.environ.get("POSTGRES_USER", "user")
    DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "password")

    @property
    def database_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
