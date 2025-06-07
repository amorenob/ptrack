import json
import os
import boto3
import hashlib
# API Implementation
# Dummy fr now

PRICE_HISTORY_TABLE = os.environ.get('PRICE_HISTORY_TABLE', 'price_history-dev')
PRODUCTS_TABLE = os.environ.get('PRODUCTS_TABLE', 'products-dev')

# DynamoDB client
db_client = boto3.client('dynamodb')

def lambda_handler(event, context):
    print("Received event:", event)
    request_body = event.get('body', {})
    
    try:
        request_body = json.loads(request_body)
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid JSON in request body'})
        }
    
    # /product/history
    if event['path'] == '/product/history':
        product_url = request_body.get('productUrl')
        if not product_url:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'productId query parameter is required'})
            }
        
        product_id = hashlib.sha256(product_url.encode()).hexdigest().lower()
        
        # Fetch historical price data from DynamoDB
        try:
            response = db_client.query(
                TableName=PRICE_HISTORY_TABLE,
                KeyConditionExpression='product_id = :productId',
                ExpressionAttributeValues={
                    ':productId': {'S': product_id}
                }
            )
            historical_data = response.get('Items', [])
            message = json.dumps(historical_data)
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }
    
    return {
        'statusCode': 200,
        'body': message
    }