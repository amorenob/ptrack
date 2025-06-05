import os
import boto3
import json
# os environment variables
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
SCRAPING_QUEUE_URL = os.environ.get('SCRAPING_QUEUE_URL', '')

# AWS Lambda that sends SQS messages to launch tasks in ECS
sqs_client = boto3.client('sqs', region_name=AWS_REGION)


def lambda_handler(event, context):
    
    message = {
        'spider_name': 'generic',
        'site': 'alkosto',
        'config_s3_uri': f's3://{os.environ.get("CONFIG_S3_BUCKET", "")}/config/alkosto.yaml',
        'targets': [
            {
                'url': 'https://www.alkosto.com/tv/smart-tv/c/BI_120_ALKOS',
                'category': 'tecnologia',
                'tags': ['televisores', 'tecnologia'],
                'max_pages': 1
            },
            {
                'url': 'https://www.alkosto.com/celulares/smartphones/c/BI_101_ALKOS',
                'category': 'tecnologia',
                'tags': ['celulares', 'tecnologia'],
                'max_pages': 1,
            },
            {
                'url': 'https://www.alkosto.com/electrodomesticos/grandes-electrodomesticos/refrigeracion/c/BI_0610_ALKOS',
                'category': 'electrodomesticos',
                'tags': ['regrigeracion', 'hogar'],
                'max_pages': 1
            }
        ]
    }
    # send message to SQS queue
    response = sqs_client.send_message(
        QueueUrl=SCRAPING_QUEUE_URL,
        MessageBody=json.dumps(message)
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Message sent to SQS queue',
            'messageId': response['MessageId']
        })
    }