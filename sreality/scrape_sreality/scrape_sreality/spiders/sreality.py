import datetime
import json

import scrapy
from scrapy.exceptions import CloseSpider


class SrealitySpider(scrapy.Spider):
    name = "sreality"
    allowed_domains = ["www.sreality.cz"]

    def __init__(self):
        super().__init__()
        self._timestamp_milliseconds = int(datetime.datetime.now().timestamp() * 1000)
        self._page = 1

    @property
    def _url(self):
        params = {
            "category_main_cb": 1,
            "category_type_cb": 1,
            "per_page": 100,
            "noredirect": 1,  # necessary to avoid duplicate requests
            "tms": self._timestamp_milliseconds,
            "page": self._page,
        }
        params_str = "&".join(f"{key}={value}" for key, value in params.items())
        return f"https://www.sreality.cz/api/en/v2/estates?{params_str}"

    def start_requests(self):
        url = self._url
        yield scrapy.Request(url)

    def parse(self, response):
        data = json.loads(response.text)
        estates = _get_safe(data, ["_embedded", "estates"])
        if estates is None:
            raise CloseSpider(f"No estates found on page {self._page}")
        for estate in estates:
            yield {
                "title": estate.get("name"),
                "image": _get_safe(estate, ["_links", "images", 0, "href"]),
                "id": self._get_id(estate),
            }
        self._page += 1
        yield response.follow(self._url, self.parse)

    @staticmethod
    def _get_id(estate):
        self_address = _get_safe(estate, ["_links", "self", "href"])
        id_string = self_address.split("/")[-1]
        return int(id_string)


def _get_safe(data, path):
    """Get value nested in `data` at `path`.
    If `path` does not point to anyting in `data`, return None.
    Path exists examples:
    >>> _get_safe({'key': 'value'}, ['key'])
    'value'
    >>> _get_safe({'key1': {'key2': ['value']}}, ['key1', 'key2', 0])
    'value'

    Path does not exist:
    >>> _get_safe({'key1': 'value'}, ['key2']) is None
    True
    >>> _get_safe({'key1': [{'key2': 'value'}]}, ['key1', 1, 'key2']) is None
    True
    >>> _get_safe({}, ['key']) is None
    True
    """
    current = data
    for key in path:
        try:
            current = current[key]
        except (KeyError, IndexError):
            return None
    return current
