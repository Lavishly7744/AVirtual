from flask import Flask, request, jsonify
import requests
import json
import time
import hmac
import hashlib

app = Flask(__name__)
WEBHOOK_SECRET = "my_am3x_shared_secret"
MERCHANT_ENDPOINT = "http://localhost:6000/merchant_listener"

def sign_payload(payload):
    timestamp = str(int(time.time()))
    base = f"{timestamp}.{payload}"
    signature = hmac.new(WEBHOOK_SECRET.encode(), base.encode(), hashlib.sha256).hexdigest()
    return timestamp, signature

@app.route("/send_webhook", methods=["POST"])
def send_webhook():
    data = {
        "event": "charge.succeeded",
        "trace_id": str(int(time.time() * 1000)),
        "amount": 100.00,
        "auth_code": "9ZX14F"
    }

    payload = json.dumps(data)
    ts, sig = sign_payload(payload)

    headers = {
        "Content-Type": "application/json",
        "X-Timestamp": ts,
        "X-Signature": sig
    }

    res = requests.post(MERCHANT_ENDPOINT, data=payload, headers=headers)
    return jsonify({"sent": True, "status": res.status_code})

if __name__ == "__main__":
    app.run(port=5800)
