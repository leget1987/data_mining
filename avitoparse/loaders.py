from urllib.parse import urljoin

from itemloaders.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader


def clear_price(price: str):
    try:
        result = price.replace("\xa0", ' ')
    except ValueError:
        result = None
    return result


def clear_data(address: str):
    try:
        result = address.replace("\n", '')
    except ValueError:
        result = None
    return result


def concatenate_items(items):
    result = "".join(items)
    return result


def create_author_link(author: str) -> str:
    return urljoin("https://avito.ru", author)


class AutoAvitoLoader(ItemLoader):
    default_item_class = dict
    title_in = MapCompose(clear_price)
    price_in = MapCompose(clear_price)
    price_out = TakeFirst()
    flat_address_in = MapCompose(clear_data)
    flat_description_in = MapCompose(clear_data, concatenate_items)
    author_link_in = MapCompose(create_author_link)
    author_link_out = TakeFirst()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_value('item_type', 'flat')
