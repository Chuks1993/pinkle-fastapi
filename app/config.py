from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    auth0_scope: str
    domain: str
    api_audience: str
    domain: str
    issuer: str
    debug: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
