# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os

import sqlalchemy
from sqlalchemy import sql


class ScrapeSrealityPipeline:
    def __init__(self):
        postgres_password = os.environ["POSTGRES_PASSWORD"]
        postgres_user = os.environ["POSTGRES_USER"]
        postgres_host = os.environ["POSTGRES_HOST"]
        postgres_db = os.environ["POSTGRES_DB"]

        sqlalchemy_database_uri = sqlalchemy.URL.create(
            "postgresql+psycopg",
            username=postgres_user,
            password=postgres_password,
            host=postgres_host,
            database=postgres_db,
        )

        self._engine = sqlalchemy.create_engine(sqlalchemy_database_uri)
        self._connection = self._engine.connect()

    def process_item(self, item, spider):
        # the on conflict part is used to ensure no duplications if
        # scrapy is run multiple times
        query = sql.text(
            """
            INSERT INTO flats (original_id, title, image_url)
            VALUES (:id, :title, :image)
            ON CONFLICT (original_id) DO NOTHING
            """
        )
        self._connection.execute(query, parameters=item)
        self._connection.commit()
        return item

    def close_spider(self, spider):
        self._connection.close()
        self._engine.dispose()
