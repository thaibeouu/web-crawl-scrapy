# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class TutorialItem(Item):
    title = Field()
    price = Field()
    location = Field()
    start_time = Field()
    end_time = Field()
    category = Field()
    description = Field()
