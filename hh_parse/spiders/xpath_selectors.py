DATA_VACANCY = {
    "title": {"xpath": '//h1/text()'},
    "salary": {"xpath": '//p[@class="vacancy-salary"]//span[@class="bloko-header-2 bloko-header-2_lite"]/text()'},
    "description": {"xpath": '//div[@class="g-user-content"]//text()'},
    "key_skills": {"xpath": '//div[@class="bloko-tag bloko-tag_inline"]//text()'},
    "author_url": {"xpath": '//a[@class="vacancy-company-name"]/@href'},
}

DATA_EMPLOYER = {
    'company_name': {'xpath': '//h1[@data-qa="bloko-header-1"]//span[@data-qa="company-header-title-name"]//text()'},
    'site': {'xpath': '//a[@data-qa="sidebar-company-site"]/@href'},
    'field_of_activity': {'xpath': '//div[@class="employer-sidebar-block"]/p/text()'},
    "description_employer": {"xpath": '//div[@class="g-user-content"]//text()'},
}
