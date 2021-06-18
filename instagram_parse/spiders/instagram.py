import datetime as dt
import scrapy
import json

class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['www.instagram.com', 'instagram.com']
    start_urls = ['https://www.instagram.com/accounts/login/']
    login_path = '/accounts/login/ajax/'
    tags_path = '/explore/tags/{tag}/'

    def __init__(self, login, password, tags, *args, **kwargs):
        super(InstagramSpider, self).__init__(*args, *kwargs)
        self.login = login
        self.password = password
        self.tags = tags

    def parse(self, response):
        try:
            js_data = self.js_data_extract(response)
            yield scrapy.FormRequest(response.urljoin(self.login_path),
                                     method='POST',
                                     callback=self.parse,
                                     formdata={
                                         'username': self.login,
                                         'enc_password': self.password,
                                     },
                                     headers={
                                         "X-CSRFToken": js_data['config']['csrf_token'],
                                     }
                                     )
        except AttributeError:
            r_data = response.json()
            if r_data.get('authenticated'):
                for tag in self.tags:
                    url = self.tags_path.format(tag=tag)
                    yield response.follow(url, callback=self.tag_page_parse)

    def tag_page_parse(self, response):
        js_data = self.js_data_extract(response)
        insta_tag = InstTag(js_data['entry_data']['TagPage'][0]['data'])
        yield insta_tag.get_tag_item()
        print(1)

    def js_data_extract(self, response):
        js = response.xpath('//script[contains(text(), "window._sharedData = ")]/text()').extract_first()
        start_index = js.index('{')
        data = json.loads(js[start_index:-1])
        return data


class InstTag:
    query_hash = "9b498c08113f1e09617a1703c22b2f32"

    def __init__(self, hashtag: dict):
        self.variables = {
            "tag_name": hashtag["name"],
            "first": 100,
        }
        self.hashtag = hashtag

    def get_tag_item(self):
        item = dict()
        item["item_type"] = "tag"
        item["date_parse"] = dt.datetime.utcnow()
        data = {}
        for key, value in self.hashtag.items():
            if not (isinstance(value, dict) or isinstance(value, list)):
                data[key] = value
        item["data"] = data
        return item

    def paginate_params(self):
        url_query = {"query_hash": self.query_hash, "variables": json.dumps(self.variables)}
        return url_query

    def get_post_items(self):
        for edge in self.hashtag["edge_hashtag_to_media"]["edges"]:
            yield dict(date_parse=dt.datetime.utcnow(), data=edge["node"], item_type="post")
