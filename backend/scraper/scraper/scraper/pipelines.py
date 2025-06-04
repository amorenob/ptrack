# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import boto3
import hashlib
import re
import time
import os

def get_site(url):
    """
    Extracts the site from the given URL.
    Example: https://www.exito.com/product/12345 --> site = exito.com
    """
    site = re.search(r'^(?:https?://)?(?:www\.)?([^/]+)', url)
    if site:
        return site.group(1)
    else:
        return None


# Pipeline to add urlshash and site to each item
class PlusPipeline:
    def process_item(self, item, spider):
        # Add urlshash and site to the item
        url = item.get('url', '')
        if url:
            item['product_id'] = hashlib.sha256(url.encode()).hexdigest().lower()
            item['site'] = get_site(url)
        # timestamp in seconds
        item['timestamp'] = int(time.time())
        # last updated timestamp in ISO format
        item['last_updated'] = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(item['timestamp']))
        return item



class CleanItemPipeline(object):
    """Pipeline for cleaning item fields"""
    def process_item(self, item, spider):

        # handle NoneType fields
        for key in item.keys():
            if item[key] is None:
                item[key] = ''

        # strip whitespace from string fields
        for key in item.keys():
            if isinstance(item[key], str):
                item[key] = item[key].strip()
        
        for field in ['current_price', 'original_price', 'discount']:
            if field in item and isinstance(item[field], str):
                # Remove non-numeric characters except digits
                item[field] = re.sub(r'[^\d]', '', item[field])
                # Convert price fields to int if they are not empty
                item[field] = int(item[field]) if item[field] else 0

            
        return item

# Dynamodb pipeline to store items in AWS DynamoDB
class DynamoDBPipeline:
    def __init__(self):
        # TODO: move this to settings.py
        # get env
        PRODUCTS_TABLE = os.getenv('PRODUCTS_TABLE', 'products')
        PRICES_TABLE = os.getenv('PRICE_HISTORY_TABLE', 'prices')
        # set aws region
        AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
        self.dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
        self.products_table = self.dynamodb.Table(PRODUCTS_TABLE)
        self.prices_table = self.dynamodb.Table(PRICES_TABLE)

    def process_item(self, item, spider):
        # Convert item to a dictionary
        item_dict = ItemAdapter(item).asdict()
        # Store product information in the products table
        self.products_table.put_item(
            Item={
                'product_id': item_dict['product_id'],
                'name': item_dict.get('name', ''),
                'site': item_dict.get('site', ''),
                'url': item_dict.get('url', ''),
                'description': item_dict.get('description', ''),
                'category': item_dict.get('category', ''),
                'features': item_dict.get('features', []),
                'current_price': item_dict.get('current_price', 0),
                'last_updated': item_dict.get('last_updated', ''),
            }
        )
        
        # Store price information in the prices table
        self.prices_table.put_item(
            Item={
                'product_id': item_dict['product_id'],
                'timestamp': item_dict.get('timestamp', ''),
                'current_price': item_dict.get('current_price', 0),
                'original_price': item_dict.get('original_price', 0),
                'discount': item_dict.get('discount', 0),
                'last_updated': item_dict.get('last_updated', '')
            }
        )
        
        return item