import scrapy
import logging

# get loger
logger = logging.getLogger(__name__)

class ExitoSpider(scrapy.Spider):
    name = "exito"
    allowed_domains = ["exito.com"]
    start_urls = ["https://www.exito.com/tecnologia/televisores"]

    def parse(self, response):
        # generic dummy response 
        # TODO exito crawl logic
        print("Exito site is reachable.")
        logger.info("Exito site is reachable.")
        yield {
            "name": "test product",
            "url": response.url,
            "description": "This is a test product description.",
            "category": "test category",
            "current_price": 100,
            "original_price": '100.000',
            "discount": 0,
        }
