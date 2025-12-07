from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

@app.route('/fedach/settlement', methods=['POST'])
def fedach_settlement():
    data = request.get_json()
    return jsonify({
        "fedach_reference": f"FEDACH{random.randint(100000,999999)}",
        "status": "settled",
        "settled_at": datetime.datetime.now().isoformat()
    })

@app.route('/fedwire/transfer', methods=['POST'])
def fedwire_transfer():
    data = request.get_json()
    return jsonify({
        "fedwire_reference": f"FEDWIRE{random.randint(100000,999999)}",
        "status": "transferred",
        "transferred_at": datetime.datetime.now().isoformat()
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000)
