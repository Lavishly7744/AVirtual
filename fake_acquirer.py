from flask import Flask, request, jsonify
import random
import time
import json

app = Flask(__name__)

# File to store fake transaction logs
TRANSACTION_LOG_FILE = "fake_transactions.json"

# Function to save settlements
def save_transaction(data):
    try:
        with open(TRANSACTION_LOG_FILE, "r") as f:
            transactions = json.load(f)
    except:
        transactions = []

    transactions.append(data)
    with open(TRANSACTION_LOG_FILE, "w") as f:
        json.dump(transactions, f, indent=4)

# Simulate ISO8583-style Authorization Response
def generate_auth_response(amount, currency="USD"):
    return {
        "authorized": True,
        "auth_code": f"A{random.randint(10000, 99999)}",
        "avs_result": "Y",  # Address match
        "cvv_result": "M",  # CVV match
        "amount": amount,
        "currency": currency,
        "transaction_id": f"txn_{random.randint(1000000000, 9999999999)}",
        "issuer_network": "American Express",
        "response_message": "Approved",
        "response_code": "00"
    }

# Handle Authorization Requests
@app.route('/authorize', methods=['POST'])
def authorize():
    data = request.json
    print(f"💳 Incoming authorization request: {data}")
    amount = data.get('amount', 1000)
    currency = data.get('currency', "USD")

    time.sleep(random.uniform(0.5, 1.5))  # Simulate realistic network delay

    response = generate_auth_response(amount, currency)
    print(f"✅ Authorization Approved: {response}")
    return jsonify(response), 200

# Handle Settlement Requests
@app.route('/settle', methods=['POST'])
def settle():
    data = request.json
    print(f"💸 Incoming settlement request: {data}")

    settlement_response = {
        "settled": True,
        "settlement_id": f"set_{random.randint(1000000000, 9999999999)}",
        "settlement_amount": data.get('amount', 1000),
        "currency": data.get('currency', "USD"),
        "settlement_date": time.strftime("%Y-%m-%d"),
        "response_message": "Settlement successful",
        "response_code": "00"
    }

    save_transaction(settlement_response)

    print(f"✅ Settlement Logged: {settlement_response}")
    return jsonify(settlement_response), 200

# Catch-all route for unknown paths
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    print(f"⚡ Received request on unknown path: {path}")
    return jsonify({"message": "Fake Acquirer Server active."}), 200

# Run the server
if __name__ == "__main__":
    from os import environ
    port = int(environ.get('PORT', 5000))
    print(f"✅ Fake Acquirer Server running on port {port}")
    app.run(host="0.0.0.0", port=port)
