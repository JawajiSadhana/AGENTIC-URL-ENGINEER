from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    rate_limit_shorten: str = "10/minute"
    rate_limit_redirect: str = "100/minute"
    admin_user: str = "admin"
    admin_pass: str = "admin123"
    class Config: env_file = ".env"

settings = Settings()