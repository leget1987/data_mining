import json
import time
from pathlib import Path

import requests


class Parse5ka:
    headers = {
        "User-Agent": "Dmitriy Lobanov"
    }

    def __init__(self, start_url, save_path: Path):
        self.start_url = start_url
        self.save_path = save_path

    def _get_response(self, url):
        while True:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response
            time.sleep(0.5)

    def run(self):
        for product in self._parse(self.start_url):
            file_path = self.save_path.joinpath(f"{product['id']}.json")
            self._save(product, file_path)

    def _parse(self, url):
        while url:
            response = self._get_response(url)
            data: dict = response.json()
            url = data["next"]
            for product in data['results']:
                yield product

    def _save(self, data: dict, file_path: Path):
        file_path.write_text(json.dumps(data, ensure_ascii=False))


def get_save_path(dir_name: str) -> Path:
    save_path = Path(__file__).parent.joinpath(dir_name)
    if not save_path.exists():
        save_path.mkdir()
    return save_path


class ParseCategories5ka(Parse5ka):

    def run(self):
        response = super()._get_response(self.start_url)
        data = response.json()
        self._parse_category(data)

    def _parse_category(self, data):
        for category in data:
            next_url = f"https://5ka.ru/api/v2/special_offers/?store=363H&records_per_page=12&page=1&categories=" \
                       f"{category['parent_group_code']}&ordering=&price_promo__gte=&price_promo__lte=&search="
            category['products'] = []
            for product in super()._parse(next_url):
                category['products'].append(product)
            file_path = self.save_path.joinpath(f"{category['parent_group_code']} {category['parent_group_name']}.json")
            super()._save(category, file_path)


if __name__ == '__main__':
    url = "https://5ka.ru/api/v2/categories/"
    product_path = get_save_path('products')
    parser = ParseCategories5ka(url, product_path)
    parser.run()
