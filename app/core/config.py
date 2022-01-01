from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    debug: bool = False
    authjwt_secret_key: str
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_csrf_protect: bool = True
    authjwt_cookie_samesite: str = "lax"
    # authjwt_refresh_token_expires: int
    # authjwt_access_token_expires: int

    class Config:
        env_file = ".env"


settings = Settings()
