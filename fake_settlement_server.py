from flask import Flask, request, jsonify
import random
import datetime

app = Flask(__name__)

def generate_batch_id():
    return str(random.randint(100000, 999999))

def generate_settlement_report(transactions):
    now = datetime.datetime.utcnow()
    batch_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    total_amount = sum([txn.get("amount", 0) for txn in transactions])
    batch_id = generate_batch_id()

    report = {
        "batch_id": batch_id,
        "batch_time": batch_time,
        "transactions_settled": len(transactions),
        "total_amount_settled": round(total_amount, 2),
        "currency": "USD",
        "settlement_status": "Success",
        "funding_account": "AMEX FUNDING ACCOUNT",
        "funds_expected_date": (now + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    }

    return report

@app.route("/batch-capture", methods=["POST"])
def batch_capture():
    data = request.get_json()

    transactions = data.get("transactions", [])

    if not transactions:
        return jsonify({"error": "No transactions provided"}), 400

    settlement_report = generate_settlement_report(transactions)

    return jsonify(settlement_report), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5900)
