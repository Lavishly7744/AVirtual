from flask import Flask, request, jsonify
import random
import string
import time

app = Flask(__name__)

def generate_auth_code():
    return ''.join(random.choices(string.digits, k=6))

def generate_rrn():
    return ''.join(random.choices(string.digits, k=12))

@app.route("/charge", methods=["POST"])
def charge():
    data = request.get_json()

    pan = data.get("pan")
    expiry = data.get("expiry")
    cvv = data.get("cvv")
    address = data.get("address", {})
    amount = data.get("amount", 0.0)

    # Basic validation
    if not (pan and expiry and cvv and address):
        return jsonify({"error": "Invalid card details."}), 400

    # Simulate AVS match
    avs_result = "Y"  # Full address + zip match

    response = {
        "approved": True,
        "auth_code": generate_auth_code(),
        "acquirer_id": "40000001",
        "issuer_id": "30000001",
        "merchant_category_code": "5311",  # Retail stores
        "retrieval_reference_number": generate_rrn(),
        "response_code": "00",  # Approved
        "avs_result": avs_result,
        "cvv_result": "M",  # CVV Match
        "amount_authorized": amount,
        "currency": "USD",
        "card_type": "AMEX",
        "eci": "05",  # Frictionless 3DS
        "timestamp": int(time.time()),
        "message": "Approved"
    }

    return jsonify(response), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100)


