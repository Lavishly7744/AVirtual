from flask import Flask, request, send_file, jsonify
from fpdf import FPDF
import random
import os
import time
import json

app = Flask(__name__)

BANK_REPORT_DIR = "bank_reports"
WEBHOOK_LOG = "ach_webhook_log.json"

if not os.path.exists(BANK_REPORT_DIR):
    os.makedirs(BANK_REPORT_DIR)

# Load ACH webhook events (from fake_ach_webhook.py) for matching
if os.path.exists(WEBHOOK_LOG):
    with open(WEBHOOK_LOG, "r") as f:
        webhook_events = json.load(f)
else:
    webhook_events = []

# Helper: generate fake bank settlement PDF
def generate_bank_pdf(settlement):
    pdf = FPDF()
    pdf.add_page()

    # Bank logo simulation
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Bank of America Settlement Report", ln=True, align='C')

    pdf.set_font("Arial", "", 12)
    pdf.ln(10)

    pdf.cell(0, 10, f"Settlement ID: {settlement['settlement_id']}", ln=True)
    pdf.cell(0, 10, f"Batch ID: {settlement['batch_id']}", ln=True)
    pdf.cell(0, 10, f"Amount Settled: ${settlement['amount']:.2f}", ln=True)
    pdf.cell(0, 10, f"Settlement Date: {settlement['pushback_timestamp']}", ln=True)
    pdf.cell(0, 10, f"Bank Reference: {settlement['bank_reference']}", ln=True)
    pdf.cell(0, 10, f"Transaction Type: ACH Credit", ln=True)

    pdf.ln(10)
    pdf.cell(0, 10, "This document serves as a confirmation of the successful settlement.", ln=True)
    pdf.cell(0, 10, "Bank of America, N.A.", ln=True)

    # Save to file
    filename = f"{BANK_REPORT_DIR}/settlement_{settlement['settlement_id']}.pdf"
    pdf.output(filename)
    return filename

# API: Generate or retrieve settlement PDF
@app.route('/bank/settlement_report/<settlement_id>', methods=['GET'])
def settlement_report(settlement_id):
    print(f"📄 Generating fake settlement report for: {settlement_id}")

    settlement = next((s for s in webhook_events if s['settlement_id'] == settlement_id), None)

    if not settlement:
        return jsonify({"error": "Settlement ID not found."}), 404

    pdf_path = generate_bank_pdf(settlement)
    return send_file(pdf_path, as_attachment=True)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return jsonify({"message": "Fake Bank Reports Server Active"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
