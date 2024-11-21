from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # MongoDB Settings
    MONGODB_URL: str
    MONGODB_DB: str
    MONGODB_COLLECTION: str
    
    # API Settings
    API_HOST: str
    API_PORT: int
    DEBUG: bool
    
    # Model Settings
    GROQ_API_KEY: str
    EMBEDDING_MODEL: str
    LLM_MODEL: str
    
    # Vector DB Settings
    CHROMA_DB_PATH: str
    
    # Data Settings
    CSV_DATA_PATH: str
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()