import json

import requests

def lambda_handler(event, context):
    res = requests.get('https://google.com')

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "Requests_status_code": res.status_code,
            "Requests body": res.text
        })
    }

print(lambda_handler(None, None))
