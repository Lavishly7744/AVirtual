from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Simulated BIN registry
FAKE_BIN_DB = {
    "340000": {
        "scheme": "amex",
        "type": "credit",
        "brand": "Amex Platinum",
        "prepaid": False,
        "country": {
            "name": "United States",
            "alpha2": "US"
        },
        "bank": {
            "name": "AMEX Bank of New York",
            "url": "https://americanexpress.com",
            "phone": "+1-800-528-4800"
        }
    },
    "371234": {
        "scheme": "amex",
        "type": "credit",
        "brand": "Amex Gold",
        "prepaid": False,
        "country": {
            "name": "United States",
            "alpha2": "US"
        },
        "bank": {
            "name": "Amex National Trust",
            "url": "https://amex.com",
            "phone": "+1-888-999-8888"
        }
    }
}

@app.route("/bin/<bin_number>", methods=["GET"])
def lookup_bin(bin_number):
    prefix = bin_number[:6]
    result = FAKE_BIN_DB.get(prefix)
    if result:
        return jsonify({
            "bin": prefix,
            "valid": True,
            **result
        })
    else:
        return jsonify({
            "bin": prefix,
            "valid": False,
            "error": "BIN not found in simulated registry"
        }), 404

@app.route("/bin", methods=["POST"])
def lookup_post():
    data = request.get_json()
    bin_number = data.get("bin", "")
    return lookup_bin(bin_number)

if __name__ == "__main__":
    app.run(port=5500)
