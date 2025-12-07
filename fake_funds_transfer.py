from flask import Flask, request, jsonify
import random
import time
import json
import os

app = Flask(__name__)

TRANSFER_LOG = "fake_bank_transfers.json"

if os.path.exists(TRANSFER_LOG):
    with open(TRANSFER_LOG, "r") as f:
        transfers = json.load(f)
else:
    transfers = []

@app.route('/bank/fund_transfer', methods=['POST'])
def fund_transfer():
    payload = request.json
    print(f"💸 Incoming Fake Fund Transfer: {payload}")

    transfer = {
        "wire_transfer_id": f"WT{time.strftime('%Y%m%d')}{random.randint(1000,9999)}",
        "origin_bank": payload.get("origin_bank", "Bank of America N.A."),
        "amount": payload.get("amount", 0),
        "currency": payload.get("currency", "USD"),
        "settlement_date": time.strftime("%Y-%m-%d"),
        "batch_id": payload.get("batch_id"),
        "settlement_id": payload.get("settlement_id"),
        "swift_code": payload.get("swift_code", "BOFAUS3N"),
        "reference_number": f"2025FEDWIRE{random.randint(10000000,99999999)}",
        "status": "Completed"
    }

    transfers.append(transfer)

    # Save updated
    with open(TRANSFER_LOG, "w") as f:
        json.dump(transfers, f, indent=2)

    return jsonify({
        "transfer_logged": True,
        "wire_transfer_id": transfer["wire_transfer_id"],
        "reference_number": transfer["reference_number"],
        "message": "Fake bank wire/ACH transfer recorded successfully."
    }), 200

@app.route('/bank/fund_transfers', methods=['GET'])
def get_fund_transfers():
    return jsonify({
        "transfers": transfers,
        "report_date": time.strftime("%Y-%m-%d"),
        "message": "Fund transfer history retrieved."
    }), 200

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return jsonify({"message": "Fake Fund Transfer Server Active"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5800)
