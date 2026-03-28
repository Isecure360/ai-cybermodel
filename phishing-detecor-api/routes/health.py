# routes/health.py

import json

def handle_health(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "status": "ok",
            "service": "phishing-api",
            "version": "1.0.0"
        })
    }