import os
import boto3
import json
# os environment variables
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
SCRAPING_QUEUE_URL = os.environ.get('SCRAPING_QUEUE_URL', '')

# AWS Lambda that sends SQS messages to launch tasks in ECS
sqs_client = boto3.client('sqs', region_name=AWS_REGION)


def lambda_handler(event, context):
    
    # Load tarjets from targets.json file
    # TODO: Targets should be loaded from S3 bucket
    try:
        with open('targets.json', 'r') as file:
            jobs_f = json.load(file)
    except FileNotFoundError:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'targets.json file not found'
            })
        }   
    print(f"Loaded {len(jobs_f['jobs'])} jobs from targets.json")
    # For each job, send a message to the SQS queue
    msg_count = 0
    for job in jobs_f['jobs']:
    
        # send message to SQS queue
        response = sqs_client.send_message(
           QueueUrl=SCRAPING_QUEUE_URL,
           MessageBody=json.dumps(job)
        )
        
        msg_count += 1
        print(f"Message sent to SQS queue: {response['MessageId']} for job: {job['job_name']}")
        
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': f'{msg_count} Messages sent to SQS queue',
        })
    }