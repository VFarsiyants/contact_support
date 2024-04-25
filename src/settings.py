from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent


class DBSettings(BaseSettings):
    """Database settings"""
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_ECHO: bool = False


class BotSettings(BaseSettings):
    """Bot settings"""
    BOT_TOKEN: str


db_settings = DBSettings()
bot_settings = BotSettings()
