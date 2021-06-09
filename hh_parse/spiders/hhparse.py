import scrapy

from .xpath_selectors import DATA_VACANCY, DATA_EMPLOYER
from ..loaders import AutoHhLoaders, AutoHhLoaderCompany


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
            # переход к парсингу страницы автора объявления
            if key == 'author_url':
                yield from self._get_follow(response, value["xpath"], self.employer_parse)
        yield loader.load_item()

    def employer_parse(self, response):
        # переход к парсингу всех объявлений этого автора
        self._get_follow(response, '//a[@data-qa="employer-page__employer-vacancies-link"]/@href',
                                    self.parse)
        loader = AutoHhLoaderCompany(response=response)
        for key, value in DATA_EMPLOYER.items():
            loader.add_xpath(field_name=key, **value)
        yield loader.load_item()
