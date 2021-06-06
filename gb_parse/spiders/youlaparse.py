import re

import pymongo
import scrapy


class YoulaparseSpider(scrapy.Spider):
    name = 'youlaparse'
    allowed_domains = ['auto.youla.ru']
    start_urls = ['https://auto.youla.ru/']
    client_db = pymongo.MongoClient("mongodb://localhost:27017")
    db = client_db["lobanov_parse_db"]

    def _get_follow(self, response, selector, callback) -> object:
        for link in response.css(selector):
            url = link.attrib.get('href')
            yield response.follow(url, callback=callback)

    def parse(self, response):
        yield from self._get_follow(response, '.TransportMainFilters_brandsList__2tIkv a.blackLink', self.brand_parse)

    def brand_parse(self, response):
        yield from self._get_follow(response, '.Paginator_block__2XAPy a.Paginator_button__u1e7D', self.brand_parse)
        yield from self._get_follow(response, 'a.SerpSnippet_name__3F7Yu.blackLink', self.car_parse)

    def car_parse(self, response):
        data = dict(title=response.css('.AdvertCard_advertTitle__1S1Ak::text').extract_first(),
                    list_photo=[x.attrib.get('src') for x in response.css('.PhotoGallery_photoImage__2mHGn')],
                    specifications=[{itm.css(".AdvertSpecs_label__2JHnS::text").extract_first(): itm.css(
                        ".AdvertSpecs_data__xK2Qx::text").extract_first() or itm.css(
                        ".AdvertSpecs_data__xK2Qx a::text").extract_first()} for itm in
                                    response.css("div.AdvertCard_specs__2FEHc .AdvertSpecs_row__ljPcX")],
                    description=response.css('.AdvertCard_descriptionInner__KnuRi::text').extract_first(),
                    link_author=get_author_id(response))
        self.save(data)

    def save(self, data):
        collection = self.db['lobanov_youla']
        collection.insert_one(data)


def get_author_id(response):
    marker = "window.transitState = decodeURIComponent"
    for script in response.css("script"):
        try:
            if marker in script.css("::text").extract_first():
                re_pattern = re.compile(r"youlaId%22%2C%22([a-zA-Z|\d]+)%22%2C%22avatar")
                result = re.findall(re_pattern, script.css("::text").extract_first())
                return (
                    response.urljoin(f"/user/{result[0]}").replace("auto.", "", 1)
                    if result
                    else None
                )
        except TypeError:
            pass
