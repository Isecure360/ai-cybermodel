# ui/utils.py
import requests

def get_prediction(url, base_url):
    resp = requests.post(f"{base_url}/predict", json={"url": url})
    resp.raise_for_status()
    return resp.json()

def get_model_info(base_url):
    resp = requests.get(f"{base_url}/metadata")
    resp.raise_for_status()
    return resp.json()