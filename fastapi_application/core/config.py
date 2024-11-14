import os
from pathlib import Path

from pydantic import BaseModel
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 30


class ApiV1Prefix(BaseModel):
    prefix: str = "/api/v1"
    users: str = "/api/v1/users"


class DatabaseConfig(BaseModel):
    url: str = os.getenv("DB_URL")
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10


class RabbitMQConfig(BaseModel):
    url_amqp: str = os.getenv("RABBITMQ_URL")
    vhost: str = os.getenv("VHOST")
    quitue: str = os.getenv("QUITUE")


class Settings(BaseSettings):
    api_prefix: ApiV1Prefix = ApiV1Prefix()
    db: DatabaseConfig = DatabaseConfig()
    run: RunConfig = RunConfig()
    auth_jwt: AuthJWT = AuthJWT()
    rabbitmq: RabbitMQConfig = RabbitMQConfig()


settings = Settings()
