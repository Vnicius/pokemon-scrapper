# -*- coding: utf-8 -*-

import scrapy
from PokemonScrapper.items import PokemonItem
import re


class ProkemonScrapper(scrapy.Spider):
    name = 'PokemonScrapper'
    start_urls = [
        'https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number']

    def parse(self, response):
        for item in response.xpath('//table/tr'):
            new_item, page = self.get_pk(item)

            if new_item:
                def handler(current):
                    return lambda res: self.getBiology(current, res)

                yield scrapy.Request('https://bulbapedia.bulbagarden.net' + page, callback=handler(new_item))

    def get_pk(self, tr):
        pk = PokemonItem()

        if tr.xpath('td[2]//text()'):
            pk['ndex'] = tr.xpath('td[2]//text()').extract_first().strip()
            pk['name'] = tr.xpath(
                'td[3]//a/@title').extract_first()
            pk['icon'] = 'https:' + tr.xpath(
                'td[3]//a/img/@src').extract_first()

            types = []

            for i in range(5, 7):
                if tr.xpath('td[%d]' % i):
                    types.append(
                        tr.xpath('td[%d]/a/span/text()' % i).extract_first())

            pk['types'] = types

            page = tr.xpath(
                'td[3]//a/@href').extract_first()

            return pk, page

        return None, None

    def getBiology(self, current, response):

        div = str(response.xpath(
            '//div[@id="mw-content-text"]').extract()).encode('utf-8').replace('\n', '')

        match = re.search(
            r'<h2><span class="mw-headline" id="Biology">Biology</span></h2>(.+)<h2><span class="mw-headline" id="In_the_anime">In the anime</span></h2>', div)

        if match:
            txt = re.sub(r'<div[^<]+>.+</div>', '', str(match.group(1)))
            txt = re.sub(r'<[^<]+>', '', txt)
            txt = re.sub(r'\\n', '', txt)
            txt = re.sub(r'\[\d+\]', '', txt)

            current['biology'] = txt.encode().decode('unicode_escape')

        return current
