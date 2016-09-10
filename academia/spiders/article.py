# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from academia.items import FirstItem
import json
import time


class ArticleSpider(CrawlSpider):
    name = "article"
    allowed_domains = ["academia.edu"]
    start_urls = (
        'https://www.academia.edu/People/Innovation_statistics',
    )
    custom_settings = {
        'ITEM_PIPELINES':{
            # 'academia.pipelines.MongoChemistryArticlePipeline': 300,
            },
    }

    rules = (
        Rule(LinkExtractor(allow=('/People/.*\?page=[0-9]+'), restrict_xpaths=("//a[@rel='next']")),follow=True,callback='parse_item'),
    )

    def parse_start_url(self, response):
        return self.parse_item(response)

    def parse_item(self, response):
        for sel in response.xpath('//div[@class="media_v2 slick-user-strip row"]'):
            json_body = json.loads(sel.xpath('.//script[@data-card-contents-for-user]/text()').extract_first())
            loader = ItemLoader(FirstItem(),response)

            loader.add_value('url',json_body['url'])
            loader.add_value('first_name',json_body.get('first_name'))
            loader.add_value('last_name',json_body.get('last_name'))
            loader.add_value('display_name',json_body.get('display_name'))
            loader.add_value('department',json_body.get('department'))
            loader.add_value('position',json_body.get('position'))
            loader.add_value('interests',json_body.get('interests'))
            loader.add_value('created_at',json_body.get('created_at'))
            loader.add_value('crawl_date', time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())))

            papers = sel.xpath('.//span[@class="u-fw700"]/text()').extract_first()
            loader.add_value('papers',papers)

            yield loader.load_item()
