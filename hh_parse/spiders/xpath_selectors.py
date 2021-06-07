DATA_VACANCY = {
    "title": {"xpath": '//h1/text()'},
    "salary": {"xpath": '//p[@class="vacancy-salary"]//span[@class="bloko-header-2 bloko-header-2_lite"]/text()'},
    "description": {"xpath": '//div[@class="g-user-content"]//text()'},
    "key_skills": {"xpath": '//div[@class="bloko-tag bloko-tag_inline"]//text()'},
    "author_url": {"xpath": '//a[@class="vacancy-company-name"]/@href'},
}