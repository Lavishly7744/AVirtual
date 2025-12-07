from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

# Load data from fake systems
def load_data(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return []

@app.route('/')
def dashboard():
    charges = load_data("amex_cards.json")  # Simulated card transactions
    batches = load_data("settlement_batches.json")  # Captured batches
    settlements = load_data("ach_webhook_log.json")  # ACH settlements
    wires = load_data("fake_bank_transfers.json")  # Incoming wires

    return render_template("dashboard.html", charges=charges, batches=batches, settlements=settlements, wires=wires)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5900)
