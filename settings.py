from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings for the API.
    Update: countries_settings variable added
    to facilite env var configuration on google cloud."""

    app_name: str = "TTPS"
    secret_key: str = "LA_POSTA_VA_AL_DOT_ENV"
    algorithm: str = "HS256"
    access_token_expiration_minutes: int = 600
    fake_cron_key: str = "LA_POSTA_VA_AL_DOT_ENV"
    mail_email: str = "cuack@mail.com"
    mail_pass: str = "cuack"
    mail_server: str = "smtp.mail.com"
    mail_port: int = 587
    front_url: str = "http://localhost:3000"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
