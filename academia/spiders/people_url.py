# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from academia.items import PeopleUrlItem
import re


class PeopleUrlSpider(CrawlSpider):
    name = "people_url"
    allowed_domains = ["academia.edu"]
    start_urls = (
	'https://www.academia.edu/Directory/People',
    )
    custom_settings = {
        'ITEM_PIPELINES':{
            'academia.pipelines.MongoPeopleUrlPipeline': 300,
            },
    }

    rules = (
        Rule(LinkExtractor(allow=('/Directory/People'), restrict_xpaths=("//li[@class='col-xs-12 col-sm-6 col-md-4 text-truncate']/a")),follow=True,callback='parse_url'),

    )

    def parse_url(self, response):
        for sel in response.xpath("//li[@class='col-xs-12 col-sm-6 col-md-4 text-truncate']/a/@href").extract():
            if not re.search("\/Directory\/People\/",sel):
                loader = ItemLoader(PeopleUrlItem())
                loader.add_value('people_url',sel)
                yield loader.load_item()




