import scrapy

class ExitoSpider(scrapy.Spider):
    name = 'exito'
    start_urls = ['https://www.exito.com']

    def parse(self, response):
        # Add your parsing logic here
        pass