from datetime import datetime, time
import scrapy
from scrapy import Selector

from tutorial.items import TutorialItem


class currencySpider(scrapy.Spider):
    name = 'curr'
    start_urls = [
        'http://welovebudapest.com/Ajax/Events?limit=99&filter={"EventTypes":[],"S":null,"E":null,"OnlyFree":false,"PriceRange":[0,0],"ShownOn":[0,2]}'
    ]

    def parse(self, response):
        for site in Selector(response).xpath('//div[@itemscope="itemscope"]'):
            item = TutorialItem()
            item['name'] = site.xpath('./h2[@itemprop="name"]/a/text()').extract_first()
            item['price'] = site.xpath('./h2[@itemprop="name"]/span[@class="price"]/text()').extract_first()
            item['place'] = site.xpath(
                './div[@class="details"]/div[@itemprop="location"]/span/a/text()').extract_first()
            new_date = site.xpath('./div[@class="details"]/div[@class="datetime"]/time/text()').extract_first()
            fmt = "%m/%d/%Y"
            try:
                new_date = datetime.strptime(new_date, fmt)
            except ValueError, v:
                if len(v.args) > 0 and v.args[0].startswith('unconverted data remains: '):
                    new_date = new_date[:-(len(v.args[0]) - 26)]
                    new_date = datetime.strptime(new_date, fmt)
                else:
                    raise v
            # item['time'] = datetime.strptime(
            #     site.xpath('./div[@class="details"]/div[@class="datetime"]/time/text()').extract_first(), "%m/%d/%Y")
            item['date'] = new_date
            new_time = new_date
            fmt = "%I:%M %p"
            yield item
