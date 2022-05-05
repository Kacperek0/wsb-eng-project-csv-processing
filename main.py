import csv
import json
import datetime

import requests
import boto3
import urllib.parse


s3 = boto3.client('s3')


def parse_csv_mbank(lines):
    """Parse CSV file from mBank."""

    result = []

    for line in lines:
         result.append({
            'date': line[0],
            'description': line[1],
            'category': line[3],
            'amount': line[4]
        })

    return result

def lambda_handler(event, context):
    """Receive file from S3 bucket, process it and return a JSON file to S3 bucket."""
    print(event)

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

    try:
        response = s3.get_object(
            Bucket=bucket,
            Key=key).splitlines()

        lines = csv.reader(response)
        next(lines)

        result = parse_csv_mbank(lines)

    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e


    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(result)
    }
