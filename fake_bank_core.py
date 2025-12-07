from flask import Flask, request, jsonify
import datetime
import os
import json

app = Flask(__name__)

ledger_file = "settlement_files/bank_ledger.json"
os.makedirs("settlement_files", exist_ok=True)

def save_ledger(entry):
    if not os.path.exists(ledger_file):
        with open(ledger_file, "w") as f:
            json.dump([], f)

    with open(ledger_file, "r") as f:
        ledger = json.load(f)

    ledger.append(entry)

    with open(ledger_file, "w") as f:
        json.dump(ledger, f, indent=2)

@app.route('/deposit', methods=['POST'])
def deposit_funds():
    data = request.get_json()
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "merchant_account": data["merchant_account"],
        "amount": data["amount"],
        "reference": data["reference"],
        "status": "DEPOSITED"
    }
    save_ledger(entry)
    return jsonify({"status": "success", "entry": entry})

@app.route('/ledger', methods=['GET'])
def get_ledger():
    with open(ledger_file, "r") as f:
        ledger = json.load(f)
    return jsonify(ledger)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6001)
