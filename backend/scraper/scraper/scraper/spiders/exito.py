import scrapy
import logging
from scrapy_playwright.page import PageMethod
from scrapy.http import HtmlResponse
from scraper.items import ProductItem
import re
# get loger
logger = logging.getLogger(__name__)

def abort_request(request):
    return (
        request.resource_type in ["image", "media", "stylesheet"]  # Block resource-heavy types
        or any(ext in request.url for ext in [".jpg", ".png", ".gif", ".css", ".mp4", ".webm"])  # Block specific file extensions
    )

class ExitoSpider(scrapy.Spider):
    name = "exito"
    allowed_domains = ["exito.com"]
    start_urls = ["https://www.exito.com/tecnologia/televisores"]
    
    custom_settings = {
        "PLAYWRIGHT_ABORT_REQUEST": abort_request,  # Aborting unnecessary requests
    }
    
    tarjets = [{
        "tags": ["televisores", "tecnologia"],
        "url": "https://www.exito.com/tecnologia/televisores",
        "category": "tecnologia",
        "max_pages": 2,
    }]
    
    def start_requests(self):
        for tarjet in self.tarjets:
            url = tarjet["url"]
            max_pages = tarjet.get("max_pages", 1)
            for page in range(1, max_pages + 1):
                page_url = f"{url}?page={page}"
                yield scrapy.Request(
                    url=page_url,
                    callback=self.parse,
                    meta={
                        "playwright": True,
                        "playwright_include_page": True,
                        "playwright_page_methods": [
                            PageMethod("wait_for_selector", "//div[contains(@class,'product-grid_fs-product-grid___qKN2')]", timeout=10000),
                            PageMethod("wait_for_timeout", 2000),
                        ],
                        "playwright_page_close": True,
                    },
                    cb_kwargs={"category": tarjet["category"]}
                )

        
    async def parse(self, response, category):
        # generic dummy response 
        
        page = response.meta["playwright_page"]
                
        # Scroll to the bottom of the page
        await page.evaluate("""
            new Promise((resolve) => {
                var totalHeight = 0;
                var distance = 100;
                var timer = setInterval(() => {
                    window.scrollBy(0, distance);
                    totalHeight += distance;

                    if (totalHeight >= document.body.scrollHeight){
                        clearInterval(timer);
                        resolve();
                    }
                }, 100);
            })
        """)
        await page.wait_for_timeout(2000)
        
        # Get the updated HTML content
        html_content = await page.content()

        # Create a new response object with the updated HTML
        response = HtmlResponse(url=response.url, body=html_content, encoding='utf-8')

        # Get all products
        products = response.xpath("//div[contains(@class,'productCard_productInfo')]")

        for product in products:
            item = ProductItem()
            item["name"] = product.xpath(".//h3[contains(@class,'styles_name')]/text()").get()
            item["url"] = "https://www.exito.com" + product.xpath(".//@href").get()
            item["current_price"] = product.xpath(".//div[contains(@class,'ProductPrice_container')]/p/text()").get()
            item["original_price"] = product.xpath(".//p[contains(@class,'promotion_price-dashed')]/text()").get()
            item["discount"] = product.xpath(".//div[contains(@class,'promotion_discount')]/span/text()").get()
            item["category"] = category
            #item['brand'] = product.xpath(".//span[contains(@class,'productBrandName')]/text()").get()
            #item["tags"] = tags + [item["brand"]]
            item["description"] = ""
            yield item

        #await page.close()
