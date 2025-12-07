from flask import Flask, request, jsonify
import random
import datetime

app = Flask(__name__)

def generate_stan():
    return str(random.randint(100000, 999999))

def generate_rrn():
    return str(random.randint(100000000000, 999999999999))

def generate_iso8583_response(card_number, amount):
    now = datetime.datetime.utcnow()
    transmission_dt = now.strftime("%m%d%H%M%S")  # MMDDhhmmss

    response = {
        "mti": "0110",  # 0110 = Authorization Response
        "fields": {
            "2": card_number,  # Primary Account Number (PAN)
            "3": "000000",     # Processing Code
            "4": f"{int(amount * 100):012}",  # Transaction Amount (12 digits, cents)
            "7": transmission_dt,  # Transmission Date and Time
            "11": generate_stan(),  # STAN (System Trace Audit Number)
            "37": generate_rrn(),   # Retrieval Reference Number
            "39": "00",             # Response Code (00 = Approved)
            "49": "840",            # Transaction Currency Code (840 = USD)
        }
    }

    return response

@app.route("/iso8583-authorize", methods=["POST"])
def iso8583_authorize():
    data = request.get_json()

    card_number = data.get("pan")
    amount = data.get("amount", 0.0)

    if not card_number:
        return jsonify({"error": "Missing card number"}), 400

    iso8583_message = generate_iso8583_response(card_number, amount)

    return jsonify(iso8583_message), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5800)
