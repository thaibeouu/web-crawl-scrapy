from datetime import datetime

import scrapy
from scrapy import Selector

from tutorial.items import TutorialItem


class WeLoveBudapest(scrapy.Spider):
    name = 'welovebudapest'
    start_urls = [
        'http://welovebudapest.com/Ajax/Events?limit=99&filter={"EventTypes":[],"S":null,"E":null,"OnlyFree":false,"PriceRange":[0,0],"ShownOn":[0,2]}'
    ]

    def parse(self, response):
        for site in Selector(response).xpath('//div[@itemscope="itemscope"]'):
            item = TutorialItem()
            item['title'] = site.xpath('./h2[@itemprop="name"]/a/text()').extract_first()
            item['price'] = site.xpath('./h2[@itemprop="name"]/span[@class="price"]/text()').extract_first()
            location = site.xpath(
                './div[@class="details"]/div[@itemprop="location"]/span/a/text()').extract_first()
            if location:
                item['location'] = location[2:]
            new_date = site.xpath('./div[@class="details"]/div[@class="datetime"]/time/text()').extract_first()
            fmt = "%m/%d/%Y"
            try:
                new_date = datetime.strptime(new_date, fmt)
                item['start_date'] = new_date
            except ValueError, v:
                if len(v.args) > 0 and v.args[0].startswith('unconverted data remains: '):
                    fmt = "%m/%d/%Y %I:%M %p"
                    new_date = datetime.strptime(new_date, fmt)
                    item['start_time'] = new_date
                else:
                    raise v
            yield item
