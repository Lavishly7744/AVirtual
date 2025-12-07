from flask import Flask, request, jsonify
import datetime
import json
import os
from nacha_forge import generate_nacha_file
from swift_forge import generate_mt103_file

app = Flask(__name__)

@app.route('/settle', methods=['POST'])
def settle_transaction():
    data = request.get_json()
    settlement_id = f"ACH{random.randint(10000000,99999999)}"
    merchant_name = data.get("merchant_name", "Merchant LLC")
    merchant_account = data.get("merchant_account", "123456789")
    amount_cents = int(float(data.get("amount", 0)) * 100)

    # Forge files
    generate_nacha_file(settlement_id, merchant_name, merchant_account, amount_cents)
    generate_mt103_file(settlement_id, merchant_name, merchant_account, amount_cents/100)

    transfer_data = {
        "settlement_id": settlement_id,
        "merchant_name": merchant_name,
        "merchant_account": merchant_account,
        "amount": data.get("amount"),
        "settled_at": datetime.datetime.now().isoformat()
    }

    os.makedirs("settlement_files", exist_ok=True)
    with open("settlement_files/ach_transfers.json", "a") as f:
        json.dump(transfer_data, f)
        f.write("\n")

    return jsonify({"status": "success", "settlement_id": settlement_id})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5300)
