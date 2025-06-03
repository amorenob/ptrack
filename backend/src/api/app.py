import json

# API Implementation
# Dummy fr now
def lambda_handler(event, context):
    message = json.dumps({"Dummy now"})
    return {
        'statusCode': 200,
        'body': message
    }