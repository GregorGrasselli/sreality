import os

from sqlalchemy import URL

POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_HOST = os.environ["POSTGRES_HOST"]
POSTGRES_DB = os.environ["POSTGRES_DB"]


SQLALCHEMY_DATABASE_URI = URL.create(
    "postgresql+psycopg",
    username=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    database=POSTGRES_DB,
)
