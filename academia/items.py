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


class PeopleItem(scrapy.Item):
    first_name = Field(output_processor=TakeFirst())
    last_name = Field(output_processor=TakeFirst())
    display_name = Field(output_processor=TakeFirst())
    url = Field(output_processor=TakeFirst())
    department = Field(output_processor=TakeFirst())
    position = Field(output_processor=TakeFirst())
    interests = Field()
    created_at = Field(output_processor=TakeFirst())
    social = Field()
    email = Field(output_processor=TakeFirst())