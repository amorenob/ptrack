import scrapy
import logging
from scrapy_playwright.page import PageMethod
from scrapy.http import HtmlResponse
from scraper.items import ProductItem
import os
import json
import re
import boto3
# get loger
logger = logging.getLogger(__name__)



class HtmlSaver(scrapy.Spider):
    """A generic spider to save HTML content from various e-commerce sites into S3."""   
    
    name = "html_saver"
    allowed_domains = ["exito.com", "alkosto.com", "falabella.com", "linio.com.co", "mercadolibre.com.co", "tucarro.com.co", "tudespensa.com.co", "tudepensa.com.mx", "tudepensa.com.pe", "tudepensa.com.ar"]
    #start_urls = ["https://www.exito.com/tecnologia/televisores"]
    
    def __init__(self, config_s3_uri, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bucket_name = os.environ.get("CONFIG_S3_BUCKET", "")
        targets_env = os.environ.get('TARGETS', '[]')
        
        if targets_env:
            try:
                self.targets = json.loads(targets_env)
                print(f"Loaded targets: {self.targets}")
                print(f"Number of targets: {len(self.targets)}")
                print(f"Tarhet 1 : {self.targets['targets']}")
            except json.JSONDecodeError:
                self.targets = []
        else:
            raise ValueError("No targets provided in the TARGETS environment variable.")
        
        self.s3_client = boto3.client("s3")
        
    def save_html_to_s3(self, html_content, filename):
        """Saves the HTML content to an S3 bucket."""
        bucket_name = self.bucket_name
        file_name = f"audit/html/{filename}.html"
        self.s3_client.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=html_content,
            ContentType='text/html'
        )
        logger.info(f"Saved HTML content to s3://{bucket_name}/{file_name}")         
        
    def start_requests(self):
        for target in self.targets["targets"]:
            url = target["url"]
            max_pages = target.get("max_pages", 1)
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
                    #cb_kwargs={"category": tarjet["category"]}
                )

        
    async def parse(self, response):
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
        
        #get site from url www.exito.com --> exito
        site = re.search(r'^(?:https?://)?(?:www\.)?([^/]+)', response.url)
        site = site.group(1) if site else "unknown"
        # Save the HTML content to S3
        filename = re.sub(r'\W+', '_', site.lower()) 
        self.save_html_to_s3(html_content, filename)

        # Create a new response object with the updated HTML
        response = HtmlResponse(url=response.url, body=html_content, encoding='utf-8')

        item = ProductItem()

        yield item

        #await page.close()
