from flask import Flask, request, jsonify
from webhook_verifier import verify_webhook

app = Flask(__name__)

@app.route("/merchant_listener", methods=["POST"])
def merchant_listener():
    timestamp = request.headers.get("X-Timestamp")
    signature = request.headers.get("X-Signature")
    raw_payload = request.data.decode("utf-8")

    if not verify_webhook(raw_payload, timestamp, signature):
        return jsonify({"error": "Invalid signature"}), 403

    return jsonify({"status": "Webhook accepted"}), 200

if __name__ == "__main__":
    app.run(port=6000)
