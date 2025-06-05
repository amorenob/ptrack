import os
import boto3
import json
# os environment variables
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
CLUSTER_NAME = os.environ.get('ECS_CLUSTER_NAME', '')
TASK_DEFINITION = os.environ.get('ECS_TASK_DEFINITION', '')
SUBNET_1 =  os.environ.get('SUBNET_1') 
SUBNET_2 =  os.environ.get('SUBNET_2')
SECURITY_GROUP = os.environ.get('SECURITY_GROUP') 

# AWS Lambda that lauch tasks in ECS
ecs_client = boto3.client('ecs')


def lambda_handler(event, context):
    
    for record in event.get('Records', []):
        # Process SQS message
        if 'body' in record:
            body = json.loads(record['body'])
            spider_name = body.get('spider_name', 'default_spider')
            site = body.get('site', 'default_site')
            config_s3_uri = f's3://{os.environ.get("CONFIG_S3_BUCKET", "")}/config/{site}.yaml'
            
            targets = body.get('targets', [])

            if not spider_name or not site or not config_s3_uri:
                return {
                    'statusCode': 400,
                    'body': json.dumps({
                        'message': 'Missing required parameters: spider_name, site, or config_s3_uri'
                    })
                }

        response = ecs_client.run_task(
            cluster=CLUSTER_NAME,
            taskDefinition=TASK_DEFINITION,
            launchType='FARGATE',
            networkConfiguration={
                'awsvpcConfiguration': {
                    'subnets': [SUBNET_1, SUBNET_2],
                    'securityGroups': [SECURITY_GROUP],
                    'assignPublicIp': 'ENABLED'
                }
            },
            overrides={
                'containerOverrides': [
                    { 'name': 'scraper',
                     'environment': [
                        {'name': 'SPIDER_NAME', 'value': spider_name},
                        {'name': 'SITE', 'value': site},
                        {'name': 'CONFIG_S3_URI', 'value': config_s3_uri},
                        {'name': 'TARGETS', 'value': json.dumps(targets)}
                    ],
                    'command': ['scrapy', 'crawl', spider_name, '-a', f'config_s3_uri={config_s3_uri}'],
                    }]
                })

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'ECS task launched successfully'})
    }
    