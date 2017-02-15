from datetime import datetime
import common
import scrapy

from tutorial.items import TutorialItem
# python /usr/local/lib/python2.7/dist-packages/scrapy/cmdline.py crawl budapest


class Budapest(scrapy.Spider):
    name = "budapest"
    start_urls = [
        'http://www.budapest.com/things_to_do/budapest_events.en.html',
        'http://www.budapest.com/things_to_do/budapest_events.en.html?first=10'
        ]
    base_url = 'http://www.budapest.com'

    def parse(self, response):
        links = response.xpath(
            '//div[@class="event_list_item"]/div[@class="event_text_cont"]/div[@class="event_morelink"]/a/@href').extract()
        for link in links:
            absolute_url = self.base_url + link
            yield scrapy.Request(absolute_url, callback=self.parse_2nd_level)

    @staticmethod
    def parse_2nd_level(response):
        item = TutorialItem()
        item['title'] = response.xpath(
            '//h3[@itemprop="summary"]/text()').extract_first()
        # item['price'] = "From " + response.xpath('//section[@itemprop="offers" and position()=last()]/div/p/em/span/text()').extract_first()
        item['location'] = response.xpath('//span[@itemprop="location"]/text()').extract_first().strip().rstrip()
        raw_description_list = response.xpath('//div[@itemprop="description"]/p/text()').extract()
        item['description'] = "".join(str(x) for x in filter(None, common.cleanup(raw_description_list))) \
            .replace("\'", "").replace(",", "").replace("[", "").replace("]", " ").replace("  ", " ")
        time_string = response.xpath('(//label[@class="morefields_label"])[1]/following::span/text()')[5].extract()
        time_string_list = "".join(time_string.split()).split('-')
        time_format = "%B%d,%Y"
        item['start_time'] = datetime.strptime(time_string_list[0], time_format)
        if len(time_string_list) > 1:
            item['end_time'] = datetime.strptime(time_string_list[1], time_format)
        # item['category'] = time_string
        # item['start_time'] = datetime.strptime(time_string, time_format)
        return item
