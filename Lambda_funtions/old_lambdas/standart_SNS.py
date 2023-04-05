import json
import boto3


def lambda_handler(event, context):
    sns = boto3.client('sns', region_name='eu-central-1')
    response = sns.publish(
                            PhoneNumber='your_phone_number',
                            Message="your_message",
                            #"SenderID" = "NTS"
        )


    # Return a success message
    return {
        'statusCode': 200,
        'body': json.dumps("Data Got Succesfully")
    }