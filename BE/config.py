from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "HelpServiceBE"
    mongodb_url: str
    aws_access_key_id: str
    aws_secret_access_key: str
    bucket: str

    AUTH_JWT_ALGORITHM: str
    AUTH_JWT_PRIVATE_KEY: str
    AUTH_JWT_EXPIRATION_SECONDS: str
    AUTH_PASSWORD_HASH_SALT: str
    AUTH_PASSWORD_HASH_CYCLES: int

    class Config:
        env_file = ".env"


settings = Settings()
