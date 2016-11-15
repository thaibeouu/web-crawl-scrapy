import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://welovebudapest.com/Ajax/Events?limit=99&filter={"EventTypes":[],"S":null,"E":null,"OnlyFree":false,"PriceRange":[0,0],"ShownOn":[0,2]}'
    ]

    def parse(self, response):
        for quote in response.xpath('//div[@itemscope="itemscope"]'):
            yield {
                'name': quote.xpath('./h2[@itemprop="name"]/a/text()').extract_first(),
                'price': quote.xpath('./h2[@itemprop="name"]/span[@class="price"]/text()').extract_first(),
                'place': quote.xpath('./div[@class="details"]/div[@itemprop="location"]/span/a/text()').extract_first(),
                'time': quote.xpath('./div[@class="details"]/div[@class="datetime"]/time/text()').extract_first()
            }

            # next_page_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
            # if next_page_url is not None:
            #     yield scrapy.Request(response.urljoin(next_page_url))
