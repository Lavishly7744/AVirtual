from flask import Flask, request, jsonify
import datetime
import random
import json

app = Flask(__name__)

# Response codes mapped to messages
RESPONSE_MAP = {
    "00": "Approved",
    "05": "Do Not Honor",
    "14": "Invalid Card Number",
    "51": "Insufficient Funds",
    "54": "Expired Card",
    "91": "Issuer Unavailable"
}

def iso_response(code, trace_id, cardholder=None):
    return {
        "MTI": "0210",
        "DE39": code,
        "message": RESPONSE_MAP.get(code, "Unknown"),
        "auth_code": ''.join(random.choices("ABCDEFGHJKLMNPQRSTUVWXYZ23456789", k=6)) if code == "00" else None,
        "trace_id": trace_id,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "cardholder": cardholder
    }

@app.route("/iso_authorize", methods=["POST"])
def iso_authorize():
    try:
        data = request.get_json()
        pan = data.get("DE02")  # PAN field
        expiry = data.get("DE14")  # YYMM
        amount = float(data.get("DE04", 0.00))
        cvv = data.get("DE52")
        trace_id = data.get("DE11", str(random.randint(100000, 999999)))

        if not pan or len(pan) < 15:
            return jsonify(iso_response("14", trace_id)), 400

        if expiry and expiry < datetime.datetime.now().strftime("%y%m"):
            return jsonify(iso_response("54", trace_id)), 400

        if amount > 10000:
            return jsonify(iso_response("51", trace_id)), 403

        return jsonify(iso_response("00", trace_id, cardholder="Simulated User"))
    except Exception:
        return jsonify(iso_response("91", "000000")), 500

if __name__ == "__main__":
    app.run(port=5901)
