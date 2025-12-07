from flask import Flask, request, jsonify
import datetime
import requests
import os

app = Flask(__name__)

@app.route('/clear_batch', methods=['POST'])
def clear_batch():
    data = request.get_json()
    merchant_endpoint = data.get("merchant_endpoint", None)

    batch_info = {
        "batch_id": f"BATCH{random.randint(10000000,99999999)}",
        "total_transactions": len(data.get("transactions", [])),
        "total_amount": sum(txn["amount"] for txn in data.get("transactions", [])),
        "cleared_at": datetime.datetime.now().isoformat()
    }

    if merchant_endpoint:
        try:
            requests.post(merchant_endpoint, json=batch_info, timeout=10)
        except Exception as e:
            print(f"Merchant webhook error: {e}")

    return jsonify(batch_info)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5200)
