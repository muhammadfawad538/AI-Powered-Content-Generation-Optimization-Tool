from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    # API Configuration
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    llm_provider: str = "openai"  # Options: openai, anthropic

    # Application Configuration
    debug: bool = True
    log_level: str = "info"

    # Rate Limiting
    rate_limit_requests: int = 100
    rate_limit_window: int = 60  # seconds

    # Content Generation
    content_length_limit: int = 5000  # maximum words
    max_tokens: int = 4000
    temperature: float = 0.7

    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 1

    # Research Configuration
    serp_api_key: Optional[str] = None
    research_timeout: int = 10  # seconds

    # Export Configuration
    twitter_api_key: Optional[str] = None
    twitter_api_secret: Optional[str] = None
    facebook_access_token: Optional[str] = None
    wordpress_site_url: Optional[str] = None
    wordpress_username: Optional[str] = None
    wordpress_password: Optional[str] = None

    # Redis Configuration
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: Optional[str] = None
    redis_ttl: int = 3600  # TTL in seconds for cached research results

    # PostgreSQL/Analytics Configuration
    postgres_server: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "seo_analytics"
    postgres_user: str = "analytics_user"
    postgres_password: Optional[str] = None
    database_url: Optional[str] = None  # If provided, overrides other database settings
    analytics_retention_days: int = 365  # Days to retain analytics data

    # Analytics Configuration
    analytics_enabled: bool = True
    analytics_cache_ttl: int = 300  # 5 minutes for analytics cache
    analytics_batch_size: int = 100  # Number of records to process in batches
    privacy_compliance_enabled: bool = True

    class Config:
        env_file = ".env"


settings = Settings()