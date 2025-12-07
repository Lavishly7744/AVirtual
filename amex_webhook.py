from flask import Flask, request, jsonify
import random
import json
import requests

app = Flask(__name__)
MERCHANT_WEBHOOK = "http://localhost:6000/merchant_event"  # Replace with actual

@app.route("/send_webhook", methods=["POST"])
def send_webhook():
    payload = {
        "event": "charge.succeeded",
        "data": {
            "pan": "341234567890123",
            "amount": 100.00,
            "auth_code": ''.join(random.choices("ABCDEFGHJKLMNPQRSTUVWXYZ23456789", k=6)),
            "trace_id": str(random.randint(100000000000, 999999999999))
        }
    }
    headers = {"Content-Type": "application/json"}
    res = requests.post(MERCHANT_WEBHOOK, json=payload, headers=headers)
    return jsonify({"status": "sent", "merchant_response": res.status_code})

if __name__ == "__main__":
    app.run(port=5800)
