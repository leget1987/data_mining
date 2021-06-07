import scrapy

from .xpath_selectors import DATA_VACANCY
from ..loaders import AutoHhLoaders

# 1. название вакансии
# 2. оклад (строкой от до или просто сумма)
# 3. Описание вакансии
# 4. ключевые навыки - в виде списка названий
# 5. ссылка на автора вакансии


class HhSpider(scrapy.Spider):
    name = 'hh_parse'
    allowed_domains = ['hh.ru/', 'podolsk.hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?schedule=remote&L_profession_id=0&area=113']

    def _get_follow(self, response, selector, callback) -> object:
        for link in response.xpath(selector):
            yield response.follow(link, callback=callback)

    def parse(self, response):
        yield from self._get_follow(response, "//div[@class='bloko-gap bloko-gap_top']//a[@class='bloko-button']/@href",
                                    self.parse)
        yield from self._get_follow(response, '//span[@class="resume-search-item__name"]//a[@class="bloko-link"]/@href',
                                    self.vacancy_parse)

    def vacancy_parse(self, response):
        loader = AutoHhLoaders(response=response)
        loader.add_value("url", response.url)
        for key, value in DATA_VACANCY.items():
            loader.add_xpath(field_name=key, **value)
        yield loader.load_item()
