# routes/predict.py

import json
from utils.dummy_model import predict_url


def handle_predict(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        url = body.get("url")

        if not url:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "URL is required"})
            }

        prediction, confidence = predict_url(url)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "url": url,
                "prediction": prediction,
                "confidence": confidence,
                "model_version": "v1_dummy"
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

# routes/predict.py (add this)

def handle_batch_predict(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        urls = body.get("urls", [])

        results = []

        for url in urls:
            prediction, confidence = predict_url(url)
            results.append({
                "url": url,
                "prediction": prediction,
                "confidence": confidence
            })

        return {
            "statusCode": 200,
            "body": json.dumps({"results": results})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }