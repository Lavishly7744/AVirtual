import requests
from flask import Flask, request, jsonify
import random

proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

app = Flask(__name__)

@app.route("/charge", methods=["POST"])
def charge():
    data = request.get_json()
    decision = random.choice(["approved", "declined"])
    auth_code = ''.join([str(random.randint(0, 9)) for _ in range(6)]) if decision == "approved" else None
    return jsonify({
        "decision": decision,
        "auth_code": auth_code,
        "gateway": "Fake StripeNet"
    })

@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Fake StripeNet Gateway Active"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
