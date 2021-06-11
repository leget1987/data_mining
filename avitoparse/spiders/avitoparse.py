import scrapy

from .xpath_selectors import DATA_FLAT
from ..loaders import AutoAvitoLoader


class AvitoSpider(scrapy.Spider):
    name = 'avito_parse'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/podolsk/kvartiry/prodam']

    def _get_follow(self, response, selector, callback) -> object:
        for link in response.xpath(selector):
            yield response.follow(link, callback=callback)

    def parse(self, response):
        yield from self.pagination(response)
        yield from self._get_follow(response, "//a[@class='link-link-39EVK link-design-default-2sPEv title-root-395AQ "
                                              "iva-item-title-1Rmmj title-listRedesign-3RaU2 "
                                              "title-root_maxHeight-3obWc']/@href", self.flat_parse)

    def flat_parse(self, response):
        loader = AutoAvitoLoader(response=response)
        loader.add_value("url", response.url)
        for key, value in DATA_FLAT.items():
            loader.add_xpath(field_name=key, **value)
        yield loader.load_item()

    def pagination(self, response):
        # получаем количество страниц пагинации
        try:
            index_span = len(response.xpath('//div[@class="pagination-root-2oCjZ"]//span/text()'))
            res = int(response.xpath(f'//div[@class="pagination-root-2oCjZ"]/span[{index_span - 1}]/text()')
                      .extract_first())
            for i in range(2, res + 1):
                url = f'{response.url}?p={i}'
                yield response.follow(url)
        except TypeError:
            pass
