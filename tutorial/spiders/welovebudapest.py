from datetime import datetime
from common import Category

import scrapy
from scrapy import Selector

from tutorial.items import TutorialItem
# python /usr/local/lib/python2.7/dist-packages/scrapy/cmdline.py crawl welovebudapest

event_types = []


class WeLoveBudapest(scrapy.Spider):
    name = 'welovebudapest'
    start_urls = [
        'http://welovebudapest.com/Ajax/Events?limit=99&filter={"EventTypes":[],"S":null,"E":null,"OnlyFree":false,"PriceRange":[0,0],"ShownOn":[0,2]}'
    ]

    def parse(self, response):
        for site in Selector(response).xpath('//div[@itemscope="itemscope"]'):
            item = TutorialItem()
            item['category'] = Category.Concert
            item['title'] = site.xpath('./h2[@itemprop="name"]/a/text()').extract_first()
            item['price'] = site.xpath('./h2[@itemprop="name"]/span[@class="price"]/text()').extract_first()
            location = site.xpath(
                './div[@class="details"]/div[@itemprop="location"]/span/a/text()').extract_first()
            if location:
                item['location'] = location[2:]
            else:
                location = site.xpath('./div[@class="details"]/div[@itemprop="location"]/span/text()').extract_first()
                item['location'] = location
            time_array = site.xpath('./div[@class="details"]/div[@class="datetime"]/time/text()')
            start_time = time_array[0].extract()
            end_time = None
            # check if ending time exists
            if len(time_array) > 1:
                end_time = site.xpath('./div[@class="details"]/div[@class="datetime"]/time/text()')[1].extract()
            fmt = "%m/%d/%Y"
            try:
                start_time = datetime.strptime(start_time, fmt)
                item['start_time'] = start_time
            except ValueError, v:
                if len(v.args) > 0 and v.args[0].startswith('unconverted data remains: '):
                    fmt = "%m/%d/%Y %I:%M %p"
                    start_time = datetime.strptime(start_time, fmt)
                    item['start_time'] = start_time
                else:
                    raise v
            if end_time:
                fmt = "%m/%d/%Y"
                try:
                    end_time = datetime.strptime(end_time, fmt)
                    item['end_time'] = end_time
                except ValueError, v:
                    if len(v.args) > 0 and v.args[0].startswith('unconverted data remains: '):
                        fmt = "%m/%d/%Y %I:%M %p"
                        end_time = datetime.strptime(end_time, fmt)
                        item['end_time'] = end_time
                    else:
                        raise v
            yield item
