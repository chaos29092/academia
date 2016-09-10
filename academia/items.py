# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field
from scrapy.loader.processors import TakeFirst,Join,MapCompose

def strip_doi(value):
    if value:
        value = value[1:].strip()
    return value

class FirstItem(scrapy.Item):
    first_name = Field(output_processor=TakeFirst())
    last_name = Field(output_processor=TakeFirst())
    display_name = Field(output_processor=TakeFirst())
    url = Field(output_processor=TakeFirst())
    department = Field(output_processor=TakeFirst())
    position = Field(output_processor=TakeFirst())
    interests = Field()
    created_at = Field(output_processor=TakeFirst())
    crawl_date = Field(output_processor=TakeFirst())
    papers = Field(output_processor=TakeFirst())

class SecondBookItem(scrapy.Item):
    title = Field(output_processor=TakeFirst())
    first_online = Field(output_processor=TakeFirst())
    doi = Field(input_processor=MapCompose(strip_doi),output_processor=TakeFirst())
    cite_this = Field(output_processor=TakeFirst())

    journal_title = Field(output_processor=TakeFirst())
    citation_year = Field(output_processor=TakeFirst())
    citation_volume = Field(output_processor=TakeFirst())
    citation_issue = Field(output_processor=TakeFirst())
    citation_pages = Field(output_processor=TakeFirst())

    authors = Field()
    views = Field(output_processor=TakeFirst())
    abstract = Field(output_processor=Join())
    url = Field(output_processor=TakeFirst())

class UrlItem(scrapy.Item):
    name = Field(output_processor=TakeFirst())
    url = Field(output_processor=TakeFirst())