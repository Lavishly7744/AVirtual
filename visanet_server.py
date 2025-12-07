from flask import Flask, request, jsonify
import random
import time

app = Flask(__name__)

@app.route('/authorize', methods=['POST'])
def authorize():
    payload = request.json
    print(f"💳 VISA AUTH REQUEST: {payload}")

    card_number = payload.get("card_number", "")
    if not card_number.startswith("4"):
        return jsonify({
            "authorized": False,
            "network_response_code": "14",
            "message": "Invalid Visa card number."
        }), 400

    return jsonify({
        "authorized": True,
        "network_response_code": "00",
        "auth_code": f"V{random.randint(10000,99999)}",
        "transaction_id": f"txn_{random.randint(10000000,99999999)}",
        "avs_result": "Y",
        "cvv_result": "M",
        "message": "Approved"
    }), 200

@app.route('/capture_batch', methods=['POST'])
def capture_batch():
    payload = request.json
    print(f"💸 VISA CAPTURE BATCH: {payload}")

    return jsonify({
        "batch_id": f"batch_{random.randint(1000,9999)}",
        "capture_success": True,
        "message": "Batch captured successfully."
    }), 200

@app.route('/refund', methods=['POST'])
def refund():
    payload = request.json
    print(f"💸 VISA REFUND REQUEST: {payload}")

    return jsonify({
        "refunded": True,
        "refund_id": f"refund_{random.randint(1000000,9999999)}",
        "message": "Refund processed successfully."
    }), 200

@app.route('/3ds-challenge', methods=['POST'])
def three_ds_challenge():
    payload = request.json
    print(f"🔒 3DS CHALLENGE REQUEST (VISA): {payload}")

    return jsonify({
        "3ds_authenticated": True,
        "authentication_result": "Y",
        "message": "3DS authentication successful."
    }), 200

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return jsonify({"message": "Fake VisaNet Server Active"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000)
