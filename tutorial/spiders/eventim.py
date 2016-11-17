from datetime import datetime

import scrapy

from tutorial.items import TutorialItem


class QuotesSpider(scrapy.Spider):
    name = "eventim"
    start_urls = [
        'http://www.eventim.hu/en/search/?city=Budapest&elu=1&ecp=%d' % n for n in range(1, 6)
        ]
    base_url = 'http://www.eventim.hu'

    def parse(self, response):
        links = response.xpath(
            '//div[@class="List EventContentList clearfix"]/div[@class="List-item"]/a/@href').extract()
        for link in links:
            absolute_url = self.base_url + link
            yield scrapy.Request(absolute_url, callback=self.parse_2nd_level)

    def parse_2nd_level(self, response):
        links = response.xpath('//a[@class="eventlist-link clearfix"]/@href').extract()
        for link in links:
            absolute_url = self.base_url + link
            yield scrapy.Request(absolute_url, callback=self.parse_3rd_level)

    @staticmethod
    def parse_3rd_level(response):
        item = TutorialItem()
        item['title'] = response.xpath(
            '//h2[@class="page-name--event block--auto"]/a/text()').extract_first()
        item['price'] = response.xpath('./h2[@itemprop="name"]/span[@class="price"]/text()').extract_first()
        item['location'] = response.xpath('//span[@class="event-data--venue block--auto"]/text()').extract_first()
        time_string = response.xpath('//meta[@itemprop="startDate"]/@content').extract_first()
        time_format = "%Y-%m-%dT%H:%M" #isoformat
        item['start_time'] = datetime.strptime(time_string, time_format)
        return item
