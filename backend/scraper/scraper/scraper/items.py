# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ProductItem(scrapy.Item):
    product_id = scrapy.Field()  # Unique identifier for the product
    name = scrapy.Field()
    site = scrapy.Field()  # Name of the site where the product is listed
    url = scrapy.Field()
    description = scrapy.Field()
    category = scrapy.Field()
    last_updated = scrapy.Field()  # Timestamp of the last update
    features = scrapy.Field()  # List of features or specifications
    current_price = scrapy.Field()  # Current price of the product
    original_price = scrapy.Field()  # Original price before any discounts
    discount = scrapy.Field()  # Discount percentage or amount