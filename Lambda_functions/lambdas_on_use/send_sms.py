import json
import boto3


def lambda_handler(event, context):
    # TODO implement
    client = boto3.client('sns')
    
    message = event["queryStringParameters"]["message"]
    tel = event["queryStringParameters"]["tel"]
    
    response = client.publish(


    PhoneNumber=tel,
    Message=message,
    
    )
    
    
    
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }