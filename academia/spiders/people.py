# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from academia.items import PeopleItem
import json
import time
import re


class PeopleSpider(CrawlSpider):
    name = "people"
    allowed_domains = ["academia.edu"]
    start_urls = (
        'https://www.academia.edu/Directory/People/0..1155',
    )
    custom_settings = {
        'ITEM_PIPELINES':{
            'academia.pipelines.MongoPeoplePipeline': 300,
            },
    }

    rules = (
        Rule(LinkExtractor(allow=('/Directory/People'), restrict_xpaths=("//li[@class='col-xs-12 col-sm-6 col-md-4 text-truncate']/a")),follow=True),
        Rule(LinkExtractor(deny=('/Directory/'), restrict_xpaths=("//li[@class='col-xs-12 col-sm-6 col-md-4 text-truncate']/a")),callback='parse_item'),

    )

    def parse_item(self, response):
        # extract user id,create url
        js = response.xpath('//div[@id="content"]/script/text()').extract_first()
        m=re.split(r'\)\;',js)
        user = m[0][35:]
        social = m[2][22:]
        json_body = json.loads(user)
        user_id = json_body.get('id')
        user_domain = json_body.get('domain_name')
        url = 'http://'+user_domain+'.academia.edu/v0/users/'+str(user_id)+'/details?subdomain_param=api'

        yield scrapy.Request(url=url,callback=self.parse_email,meta={'user':user,'social':social})

    def parse_email(self,response):
        user = response.meta['user']
        social = response.meta['social']

        email = json.loads(str(response.body_as_unicode()))
        email = email.get('details').get('public_email')

        user = json.loads(user)
        loader = ItemLoader(PeopleItem())
        loader.add_value('url',user.get('url'))
        loader.add_value('first_name',user.get('first_name'))
        loader.add_value('last_name',user.get('last_name'))
        loader.add_value('display_name',user.get('display_name'))
        loader.add_value('department',user.get('department'))
        loader.add_value('position',user.get('position'))
        loader.add_value('interests',user.get('interests'))
        loader.add_value('created_at',user.get('created_at'))
        loader.add_value('email',email)

        try:
            social=json.loads(social)
            loader.add_value('social',social)
        finally:
            return loader.load_item()

