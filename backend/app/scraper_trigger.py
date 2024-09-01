import boto3

def handler(event, context):
    client = boto3.client('ecs')
    response = client.run_task(
        cluster='scraper-cluster',
        taskDefinition='scraper-task',
        launchType='FARGATE',
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': ['subnet-12345678'],  # Replace with your subnet
                'assignPublicIp': 'ENABLED'
            }
        }
    )
    return {
        'statusCode': 200,
        'body': 'Scraper task started'
    }