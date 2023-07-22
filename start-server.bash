#!/usr/bin/env bash

source /app/venv/bin/activate
# sleep infinity
cd /app/sreality/server
flask db upgrade
cd /app/sreality/scrape_sreality
scrapy runspider scrape_sreality/spiders/sreality.py
cd /app/sreality/server
flask run --host=0.0.0.0  # if this was not a toy, this should be replaced by uvicorn or similar
