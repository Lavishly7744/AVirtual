# /Amex/payment_rail_spoofer.py

from flask import Flask, request, jsonify
import random

app = Flask(__name__)

@app.route("/authorize", methods=["POST"])
def authorize_payment():
    data = request.json
    response = {
        "authorized": True,
        "auth_code": str(random.randint(100000,999999)),
        "reference_id": f"REF-{random.randint(1000000,9999999)}",
        "amount": data.get("amount"),
        "currency": data.get("currency", "USD"),
        "merchant_id": data.get("merchant_id"),
        "status": "approved"
    }
    return jsonify(response)

@app.route("/settle", methods=["POST"])
def settle_payment():
    return jsonify({"settlement_status": "success", "batch_id": random.randint(10000,99999)})

if __name__ == "__main__":
    app.run(port=5055)
