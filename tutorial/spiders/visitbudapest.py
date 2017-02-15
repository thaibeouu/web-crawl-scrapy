from datetime import datetime
import scrapy
import common

from tutorial.items import TutorialItem

# python /usr/local/lib/python2.7/dist-packages/scrapy/cmdline.py crawl visitbudapest


class VisitBudapest(scrapy.Spider):
    name = 'visitbudapest'
    start_urls = [
        'http://visitbudapest.travel/budapest-events/'
    ]
    base_url = 'http://visitbudapest.travel'

    def parse(self, response):
        links = response.xpath(
            '//li[@class="bizresult"]/div[@class="bizdetails"]/div[@class="bizintro a-blu"]/a/@href').extract()
        for link in links:
            absolute_url = self.base_url + link
            yield scrapy.Request(absolute_url, callback=self.parse_2nd_level)

    @staticmethod
    def parse_2nd_level(response):
        item = TutorialItem()
        item['title'] = response.xpath('//h1/a/text()').extract_first()
        item['category'] = common.convert_cat(response.xpath('//*[@id="profile-data"]/p[1]/text()').extract_first().split(",")[0])
        raw_description_list = response.xpath('//*[@id="content-area"]/div[2]/p/text()').extract()
        item['description'] = "".join(str(x) for x in filter(None, common.cleanup(raw_description_list))) \
            .replace("\'", "").replace(",", "").replace("[", "").replace("]", " ").replace("  ", " ")
        item['location'] = response.xpath('//*[@id="profile-data"]/p[3]/text()').extract_first()
        price_check = response.xpath('//*[@id="content-area"]/div/p[strong[starts-with(., "Entrance")]]/text()')\
            .extract()
        if len(price_check) > 1:
            price_string = response.xpath('//*[@id="content-area"]/div/p[strong[starts-with(., "Entrance")]]/text()')\
                .extract()
            item['price'] = "".join(x.rstrip().replace('\n', '') for x in price_string).rstrip()
        time_string = response.xpath('//*[@id="profile-data"]/ul[2]/li/text()').extract_first().strip()
        time_string = "".join(time_string.split())
        time_string_list = "".join(time_string.split()).split('-')
        time_format = "%b%d,%Y"
        item['start_time'] = datetime.strptime(time_string_list[0], time_format)
        if len(time_string_list) > 1:
            item['end_time'] = datetime.strptime(time_string_list[1], time_format)
        return item
