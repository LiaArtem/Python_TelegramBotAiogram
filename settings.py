from environs import Env
from dataclasses import dataclass


@dataclass
class Bots:
    TELEGRAM_TOKEN: str
    TELEGRAM_ADMIN_CHAT_ID: int
    OPENWEATHERMAP_TOKEN: str
    IS_WORK_REDIS_DB: bool
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_CURS_DB_NO: int
    REDIS_SECURITIES_DB_NO: int
    REDIS_STORAGE_DB_NO: int
    REDIS_STORAGE_JOB_DB_NO: int
    REDIS_PASSWORD: str


@dataclass
class Settings:
    bots: Bots


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bots=Bots(
            TELEGRAM_TOKEN=env.str('TELEGRAM_TOKEN'),
            TELEGRAM_ADMIN_CHAT_ID=env.int('TELEGRAM_ADMIN_CHAT_ID'),
            OPENWEATHERMAP_TOKEN=env.str('OPENWEATHERMAP_TOKEN'),
            IS_WORK_REDIS_DB=env.bool('IS_WORK_REDIS_DB'),
            REDIS_HOST=env.str('REDIS_HOST'),
            REDIS_PORT=env.int('REDIS_PORT'),
            REDIS_CURS_DB_NO=env.int('REDIS_CURS_DB_NO'),
            REDIS_SECURITIES_DB_NO=env.int('REDIS_SECURITIES_DB_NO'),
            REDIS_STORAGE_DB_NO=env.int('REDIS_STORAGE_DB_NO'),
            REDIS_STORAGE_JOB_DB_NO=env.int('REDIS_STORAGE_JOB_DB_NO'),
            REDIS_PASSWORD=env.str('REDIS_PASSWORD')
        )
    )


settings = get_settings('settings')
