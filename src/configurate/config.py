import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from typing import Optional

from pydantic import BaseSettings, validator, SecretStr, RedisDsn, PostgresDsn, Field

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN", "")
# TELEGRAM_BOTANIM_CHANNEL_ID = int(os.getenv("TELEGRAM_BOTANIM_CHANNEL_ID", "0"))


BASE_DIR = Path(__file__).absolute().parent.parent
# SQLITE_DB_FILE = BASE_DIR / "db.sqlite3"
TEMPLATES_DIR = BASE_DIR / "templates"
CONFIGURATE_DIR = BASE_DIR / "configurate/log_config.json"


# DATE_FORMAT = "%d.%m.%Y"
# VOTE_ELEMENTS_COUNT = 3

# VOTE_RESULTS_TOP = 10

# ALL_BOOKS_CALLBACK_PATTERN = "all_books_"
# VOTE_BOOKS_CALLBACK_PATTERN = "vote_"


class Settings(BaseSettings):
    bot_token: SecretStr
    bot_name: str
    admins: list[int]

    container_name: str = Field(..., env="BOT_CONTAINER_NAME")
    image: str = Field(..., env="BOT_IMAGE_NAME")

    fsm_mode: str

    redis_user: str = Field(..., env="REDIS_DATABASE_USER")
    redis_pass: str = Field(..., env="REDIS_DATABASE_PASSWORD")
    redis_host: str = Field(..., env="REDIS_DATABASE_HOST")
    redis_port: str = Field(..., env="REDIS_DATABASE_PORT")
    redis_lvl: int = Field(..., env="REDIS_DATABASE_LEVEL")
    redis_dsn: RedisDsn

    database_mode: str
    postgres_user: str = Field(..., env="POSTGRES_DATABASE_USER")
    postgres_pass: str = Field(..., env="POSTGRES_DATABASE_PASSWORD")
    postgres_db: str = Field(..., env="POSTGRES_DATABASE_NAME")
    postgres_host: str = Field(..., env="POSTGRES_DATABASE_HOST")
    postgres_port: str = Field(..., env="POSTGRES_DATABASE_PORT")
    postgres_dsn: Optional[PostgresDsn]

    debug: bool

    @validator("fsm_mode")
    def check_fsm_mode(cls, value):
        if value not in ("memory", "redis"):
            raise ValueError("Incorrect fsm_mode. Must be one of: memory, redis")

    @validator("redis_dsn")
    def skip_validating_redis(cls, value, values):
        if values.get("fsm_mode") == "redis" and value is None:
            raise ValueError("Redis config is missing, though fsm_type is 'redis'")
        return value

    @validator("database_mode")
    def check_database_mode(cls, value):
        if value not in ("sqlite3", "postgresql"):
            raise ValueError("Incorrect database_mode. Must be one of: sqlite3, postgresql")
        return value

    @validator("postgres_dsn")
    def skip_validating_postgres(cls, value, values):
        if values.get("database_mode") == "postgresql" and value is None:
            raise ValueError("PostgreSql config is missing, though database_type is 'postgresql'")
        return value

    @validator("admins")
    def check_correct_admins_ids(cls, value):
        for i in value:
            if i < 0:
                raise ValueError("Incorrect admins ids. Must be only positive numbers.")

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


@lru_cache
def get_settings() -> Settings:
    return Settings()


config = get_settings()

import functools

def debug(func):
    """Print the function signature and return value"""
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]                      # 1
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
        signature = ", ".join(args_repr + kwargs_repr)           # 3

        value = func(*args, **kwargs)
        return value
    return wrapper_debug


