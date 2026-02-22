from pydantic_settings import BaseSettings
from pydantic import ConfigDict, Field, validator
from typing import Optional
from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "AI_CTO_AGENT"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = Field(default="dev-key-change-in-production")
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database
    DATABASE_URL: str = "sqlite:///./app.db"
    REDIS_URL: Optional[str] = None
    
    # OpenAI
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL_HIGH: str = "gpt-4-1106-preview"
    OPENAI_MODEL_MEDIUM: str = "gpt-3.5-turbo-16k"
    OPENAI_MODEL_FAST: str = "gpt-3.5-turbo"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-ada-002"
    
    # OpenRouter
    OPENROUTER_API_KEY: Optional[str] = None
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENROUTER_DEFAULT_MODEL: str = "mistralai/mistral-7b-instruct"
    
    # Cohere
    COHERE_API_KEY: Optional[str] = None
    COHERE_EMBED_MODEL: str = "embed-english-v2.0"
    
    # Vector DB
    VECTOR_DB_TYPE: str = "chroma"
    VECTOR_DB_PATH: str = "./vector_store"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    LOG_RETENTION: int = 10
    LOG_ROTATION: str = "500 MB"
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 60
    RATE_LIMIT_PERIOD: int = 60
    
    @validator("OPENAI_API_KEY", pre=True, always=True)
    def validate_openai_key(cls, v):
        if not v and os.getenv("ENVIRONMENT") == "production":
            raise ValueError("OPENAI_API_KEY is required in production")
        return v
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()