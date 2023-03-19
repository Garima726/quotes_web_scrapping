import scrapy
from scrapy_splash import SplashRequest

class ScrapedQuotesSpider(scrapy.Spider):
    name = "scraped_quotes"
    allowed_domains = ["quotes.toscrape.com"]
    

    script = '''
        function main(splash, args)
            assert(splash:go(args.url))
            assert(splash:wait(0.5))
            return splash:html()
        end
    '''

    def start_requests(self):
        yield SplashRequest(url='http://quotes.toscrape.com/js/', callback=self.parse, endpoint='execute', args={
            'lua_source': self.script
        })

    def parse(self, response):
        for quotes in response.xpath("//div[@class='quote']"):
            yield{
                'quote': quotes.xpath(".//span[@class='text']/text()").get(),
                'author': quotes.xpath(".//span/small/text()").get(),
                'tags': quotes.xpath(".//div/a/text()").getall()
            }
        next_page = response.xpath("//li[@class='next']/a/@href").get()
        if next_page:
            absolute_url = f"http://quotes.toscrape.com{next_page}"
            yield SplashRequest(url=absolute_url, callback=self.parse, endpoint='execute', args={
                'lua_source': self.script
            })