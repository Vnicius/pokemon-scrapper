# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PokemonItem(scrapy.Item):
    ndex = scrapy.Field()
    name = scrapy.Field()
    icon = scrapy.Field()
    types = scrapy.Field()
    biology = scrapy.Field()
