import requests
from flask import Flask, request, jsonify

proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

app = Flask(__name__)

@app.route("/push_report", methods=["POST"])
def push_report():
    data = request.get_json()
    report_url = data.get("report_url")
    report_payload = data.get("report_payload")
    try:
        response = requests.post(report_url, json=report_payload, proxies=proxies, timeout=15)
        return jsonify({"status": "report_pushed", "gateway_response": response.json()})
    except Exception as e:
        return jsonify({"error": str(e)}), 502

@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Fake Merchant Reporting API Active"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5500)
