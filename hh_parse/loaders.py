from urllib.parse import urljoin

from scrapy import Selector
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose


def clear_salary(salary: str):
    try:
        result = salary.replace("\xa0", '')
    except ValueError:
        result = None
    return result


def glue_description(description):
    result = ''.join(description)
    return result


def create_author_link(author_id: str) -> str:
    author = ""
    if author_id:
        author = urljoin("https://podolsk.hh.ru/employer/", author_id)
    return author


class AutoHhLoaders(ItemLoader):
    default_item_class = dict
    title_out = TakeFirst()
    salary_in = MapCompose(clear_salary)
    salary_out = TakeFirst()
    description_in = MapCompose(glue_description)
    author_url_in = MapCompose(create_author_link)
    site_in = TakeFirst()
    company_name_in = TakeFirst()
    description_employer_in = MapCompose(glue_description, clear_salary)
