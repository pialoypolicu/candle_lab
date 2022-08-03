import os
from pathlib import Path
from dotenv import load_dotenv

dotenv_path = Path(".env")
load_dotenv(dotenv_path=dotenv_path)

DB_ENGINE = os.environ.get("DB_ENGINE")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
