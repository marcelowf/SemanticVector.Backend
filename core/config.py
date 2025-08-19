from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    embedding_model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"
    log_level: str = "INFO"

settings = Settings()