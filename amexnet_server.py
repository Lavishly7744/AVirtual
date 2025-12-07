import requests
from flask import Flask, request, jsonify
import random
import datetime

# ✅ Define SOCKS5 proxy settings for Tor
proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

app = Flask(__name__)

# === Dummy Acquirer Processor ===
@app.route("/process", methods=["POST"])
def process_transaction():
    data = request.get_json()

    pan = data.get("pan")
    amount = data.get("amount")
    merchant_id = data.get("merchant_id")

    # Basic dummy approval logic
    if not pan or not amount or not merchant_id:
        return jsonify({"status": "error", "reason": "missing_fields"}), 400

    # Randomly approve or decline (for realism)
    decision = random.choices(["approved", "declined"], weights=[90, 10])[0]

    auth_code = ''.join([str(random.randint(0,9)) for _ in range(6)]) if decision == "approved" else None

    response = {
        "decision": decision,
        "auth_code": auth_code,
        "network_time": datetime.datetime.utcnow().isoformat() + "Z"
    }

    return jsonify(response)

# === Forward to Fake Merchant for Settlement (optional) ===
@app.route("/settlement", methods=["POST"])
def settlement():
    data = request.get_json()

    merchant_endpoint = data.get("merchant_endpoint")
    batch_data = data.get("batch_data")

    if not merchant_endpoint or not batch_data:
        return jsonify({"status": "error", "reason": "missing_fields"}), 400

    try:
        # Route through Tor proxy
        response = requests.post(
            merchant_endpoint,
            json=batch_data,
            proxies=proxies,   # ✅ Forced Tor routing
            timeout=15
        )
        merchant_result = response.json()
    except Exception as e:
        return jsonify({"status": "failed", "error": str(e)}), 502

    return jsonify({
        "status": "sent_to_merchant",
        "merchant_response": merchant_result
    })

# === Health Check ===
@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "AmexNet Processor Active"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
