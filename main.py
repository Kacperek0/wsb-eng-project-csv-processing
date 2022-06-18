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
        try:
            line = line.decode('windows-1250')
            line = line.split(';')
            result.append({
                'date': line[0],
                'description': line[1].strip('"\\ '),
                'category': line[3].strip('"\\ '),
                'amount': line[4]
            })
        except IndexError:
            continue

    return result


def lambda_handler(event, context):
    """Receive file from S3 bucket, process it and return a JSON file to S3 bucket."""
    print(event)

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='windows-1250')

    try:
        response = s3.get_object(
            Bucket=bucket,
            Key=key)

        lines = response['Body'].read().split(b'\n')

        result = parse_csv_mbank(lines)

    except Exception as e:
        print(e)
        print(f'Error getting object {key} from bucket {bucket}.')
        raise e

    transactions = {
        'transactions': result,
    }

    transactions = json.dumps(transactions)

    s3.put_object(bucket='wsb-eng-transactions-bucket', Key='transactions.json', Body=transactions)

    
    print(json.dumps(result))


    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(result)
    }
