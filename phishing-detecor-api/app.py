# app.py

from routes.health import handle_health
from routes.predict import handle_predict, handle_batch_predict


def lambda_handler(event, context):
    path = event.get("path", "")
    method = event.get("httpMethod", "")

    if path == "/health" and method == "GET":
        return handle_health(event, context)

    elif path == "/predict" and method == "POST":
        return handle_predict(event, context)

    elif path == "/predict/batch" and method == "POST":
        return handle_batch_predict(event, context)

    return {
        "statusCode": 404,
        "body": "Route not found"
    }