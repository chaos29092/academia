# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from academia.items import UrlItem
from pymongo import MongoClient

# 抓某数据库里的url的meta，但是貌似没软件抓的多，估计是自动转向或者网络原因，或者是url格式问题
client = MongoClient()
db = client.academia_copy
l=[]
for data in db.url.find():
    l.append(data['url'])

class UrlSpider(CrawlSpider):
    name = "url"
    # allowed_domains = ["academia.edu"]
    start_urls = (l)
    custom_settings = {
        'ITEM_PIPELINES':{
            'academia.pipelines.MongoUrlPipeline': 300,
            },
    }

    rules = (
        # Rule(LinkExtractor(allow=('/People/.*\?page=[0-9]+'), restrict_xpaths=("//a[@rel='next']")),follow=True,callback='parse_item'),
    )

    def parse_start_url(self, response):
        return self.parse_item(response)

    def parse_item(self, response):
        loader = ItemLoader(UrlItem(),response)

        loader.add_xpath('name','//title/text()')
        loader.add_value('url',response.url)

        yield loader.load_item()
