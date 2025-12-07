from flask import Flask, request, jsonify
import random
import time
import json
import os

app = Flask(__name__)

# Store sent webhooks for debugging/logging
WEBHOOK_LOG = "ach_webhook_log.json"

# Load existing webhook events if any
if os.path.exists(WEBHOOK_LOG):
    with open(WEBHOOK_LOG, "r") as f:
        webhook_events = json.load(f)
else:
    webhook_events = []

@app.route('/webhook/ach_pushback', methods=['POST'])
def ach_pushback():
    payload = request.json
    print(f"🏦 Received fake ACH pushback webhook: {payload}")

    settlement_id = payload.get("settlement_id", f"settle_{random.randint(10000,99999)}")
    batch_id = payload.get("batch_id", f"batch_{random.randint(1000,9999)}")
    amount = payload.get("amount", 0)

    event = {
        "settlement_id": settlement_id,
        "batch_id": batch_id,
        "amount": amount,
        "pushback_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "status": "ACH Settled",
        "bank_reference": f"ACHREF{random.randint(10000000,99999999)}"
    }

    webhook_events.append(event)

    # Save updated webhook events
    with open(WEBHOOK_LOG, "w") as f:
        json.dump(webhook_events, f, indent=2)

    return jsonify({
        "webhook_received": True,
        "bank_reference": event["bank_reference"],
        "message": "Fake ACH settlement webhook processed."
    }), 200

@app.route('/webhook/logs', methods=['GET'])
def webhook_logs():
    return jsonify({
        "webhook_events": webhook_events,
        "log_date": time.strftime("%Y-%m-%d"),
        "message": "Webhook log retrieval successful."
    }), 200

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return jsonify({"message": "Fake ACH Pushback Webhook Server Active"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5600)
