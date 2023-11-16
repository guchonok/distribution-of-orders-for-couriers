import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), "../.env"))

HOST = os.getenv("HOST", "0.0.0.0")
PORT: int = int(os.getenv("PORT", 8000))

ON_PRODUCTION: bool = False
SECRET_KEY = "secret"

POSTGRES_DB_NAME: str = os.getenv("POSTGRES_DB", "courier")
POSTGRES_USERNAME: str = os.getenv("POSTGRES_USER", "user")
POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "password")
POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "postgresql")
POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
