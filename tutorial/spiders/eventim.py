import scrapy


class QuotesSpider(scrapy.Spider):
    name = "eventim"
    start_urls = [
        'http://www.eventim.hu/en/search/?#city=Budapest&category=&maincategory=1&from=&until=&search_string='
    ]

    def parse(self, response):
        for quote in response.xpath('//div[@class="List EventContentList clearfix"]/div[@class="List-item"]'):
            yield {
                'name': quote.xpath('./a/div[@class="List-section List-content"]/h3[@itemprop="name"]/text()').extract_first(),
                'price': quote.xpath('./h2[@itemprop="name"]/span[@class="price"]/text()').extract_first(),
                'place': quote.xpath('./a//strong[@itemprop="name"]/text()').extract_first(),
                'time': quote.xpath('.//div[@class="List-date"]/span/text()').extract_first()
            }

        # next_page_url = response.xpath('//li[@class="next"]/a/@href')	.extract_first()
        # if next_page_url is not None:
        #     yield scrapy.Request(response.urljoin(next_page_url))
