from flask import Flask, jsonify, request

app = Flask(__name__)

# Static BIN metadata for your fake Amex cards
FAKE_BIN_DATABASE = {
    "371529": {
        "bin": "371529",
        "scheme": "AMEX",
        "type": "Credit",
        "brand": "American Express",
        "prepaid": "No",
        "bank": {
            "name": "American Express Bank FSB",
            "url": "https://www.americanexpress.com",
            "phone": "+1-800-528-4800",
            "city": "Salt Lake City",
            "state": "UT",
            "country": "US"
        },
        "country": {
            "name": "United States",
            "alpha2": "US",
            "currency": "USD"
        },
        "category": "PLATINUM",
        "level": "Platinum",
        "issuer_website": "https://www.americanexpress.com"
    }
}

@app.route("/lookup/<bin_number>", methods=["GET"])
def lookup_bin(bin_number):
    bin_prefix = bin_number[:6]
    data = FAKE_BIN_DATABASE.get(bin_prefix)
    
    if data:
        return jsonify(data), 200
    else:
        return jsonify({"error": "BIN not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5400)
