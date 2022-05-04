import json

import requests
import boto3
import urllib.parse

s3 = boto3.client('s3')
def lambda_handler(event, context):
    """"""
    print(event)
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

    try:
        response = s3.get_object(
            Bucket=bucket,
            Key=key)
        print("CONTENT TYPE: " + response['ContentType'])
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e


    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": response['ContentType']
    }

print(lambda_handler(None, None))
