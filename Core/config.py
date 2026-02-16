from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent  

class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env")  

settings = Settings()