import scrapy
import yaml
import json
import boto3
from scrapy_playwright.page import PageMethod
from scrapy.http import HtmlResponse
from scraper.items import ProductItem
import os

def abort_request(request):
    return (
        request.resource_type in ["image", "media", "stylesheet"]  # Block resource-heavy types
        or any(ext in request.url for ext in [".jpg", ".png", ".gif", ".css", ".mp4", ".webm"])  # Block specific file extensions
    )

class GenericSpider(scrapy.Spider):
    name = "generic"
    allowed_domains = ["generic.com"] 
    
    #custom_settings = {
    #    "PLAYWRIGHT_ABORT_REQUEST": abort_request,  # Aborting unnecessary requests
    #}

    def __init__(self, config_s3_uri, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_s3_uri = config_s3_uri
        self.config = self.load_config_from_s3(config_s3_uri)
        self.selectors = self.config["selectors"]
        self.base_url = self.config.get("base_url", "https://www.generic.com")
        self.allowed_domains = self.config.get("base_url", "https://www.generic.com").replace("https://", "").replace("http://", "").split("/")[0].split(",")

        targets_env = os.environ.get('TARGETS', '[]')
        if targets_env:
            try:
                self.targets = json.loads(targets_env)
            except json.JSONDecodeError:
                self.targets = []
        else:
            print("No TARGETS environment variable found, using empty list.")
        
    def load_config_from_s3(self, s3_uri):
        s3 = boto3.client("s3")
        bucket, key = s3_uri.replace("s3://", "").split("/", 1)
        obj = s3.get_object(Bucket=bucket, Key=key)
        return yaml.safe_load(obj["Body"].read())

    def start_requests(self):
        for target in self.targets:
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
                            PageMethod("wait_for_selector", self.selectors["wait_for"], timeout=10000),
                            PageMethod("wait_for_timeout", 2000),
                        ],
                        "playwright_page_close": True,
                    },
                    cb_kwargs={"category": target["category"]}
                )

    async def parse(self, response, category):
        page = response.meta["playwright_page"]
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
        html_content = await page.content()
        response = HtmlResponse(url=response.url, body=html_content, encoding='utf-8')
        products = response.xpath(self.selectors["product"])
        for product in products:
            item = ProductItem()
            item["name"] = product.xpath(self.selectors["name"]).get()
            item["url"] = product.xpath(self.selectors["url"]).get()
            # If url is sref path adde base url
            if item["url"] and not item["url"].startswith("http"):
                item["url"] = self.base_url + item["url"]
            item["current_price"] = product.xpath(self.selectors["current_price"]).get()
            item["original_price"] = product.xpath(self.selectors["original_price"]).get()
            item["discount"] = product.xpath(self.selectors["discount"]).get()
            item["category"] = category
            item["description"] = ""
            yield item