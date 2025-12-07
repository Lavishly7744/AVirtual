from flask import Flask, render_template_string, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)
CARD_FILE = "amex_cards.json"
LOG_FILE = "charge_log.json"

def load_cards():
    if os.path.exists(CARD_FILE):
        with open(CARD_FILE, "r") as f:
            return json.load(f)
    return []

def save_cards(cards):
    with open(CARD_FILE, "w") as f:
        json.dump(cards, f, indent=2)

def load_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    return []

# === Admin Dashboard Home ===
@app.route("/")
def dashboard():
    cards = load_cards()
    logs = load_logs()
    return render_template_string("""
    <h2>💳 Amex Admin Dashboard</h2>

    <h3>Cards</h3>
    <table border="1" cellpadding="6">
        <tr><th>Cardholder</th><th>PAN</th><th>CVV</th><th>Expiry</th><th>Status</th><th>Balance</th><th>Actions</th></tr>
        {% for card in cards %}
        <tr>
            <td>{{ card.cardholder }}</td>
            <td>{{ card.pan }}</td>
            <td>{{ card.cvv }}</td>
            <td>{{ card.expiry }}</td>
            <td>{{ card.status }}</td>
            <td>{{ card.balance }}</td>
            <td>
                <form method="POST" action="/freeze" style="display:inline">
                    <input type="hidden" name="pan" value="{{ card.pan }}">
                    <button type="submit">{{ 'Unfreeze' if card.status == 'FROZEN' else 'Freeze' }}</button>
                </form>
                <form method="POST" action="/edit" style="display:inline">
                    <input type="hidden" name="pan" value="{{ card.pan }}">
                    <input type="number" name="balance" step="0.01" placeholder="New Balance">
                    <button type="submit">Update</button>
                </form>
                <form method="POST" action="/delete" style="display:inline">
                    <input type="hidden" name="pan" value="{{ card.pan }}">
                    <button type="submit">Delete</button>
                </form>
            </td>
        </tr>
        {% endfor %}
    </table>

    <h3>Charges</h3>
    <table border="1" cellpadding="6">
        <tr><th>Time</th><th>Cardholder</th><th>Last4</th><th>Amount</th><th>Status</th><th>Auth</th></tr>
        {% for log in logs|reverse %}
        <tr>
            <td>{{ log.timestamp }}</td>
            <td>{{ log.cardholder or '-' }}</td>
            <td>{{ log.pan_last4 }}</td>
            <td>${{ log.amount_charged }}</td>
            <td>{{ log.response_text }}</td>
            <td>{{ log.auth_code or '-' }}</td>
        </tr>
        {% endfor %}
    </table>
    """, cards=cards, logs=logs)

# === Admin Actions ===

@app.route("/freeze", methods=["POST"])
def freeze_card():
    pan = request.form.get("pan")
    cards = load_cards()
    for c in cards:
        if c["pan"] == pan:
            c["status"] = "FROZEN" if c["status"] == "ACTIVE" else "ACTIVE"
    save_cards(cards)
    return redirect(url_for("dashboard"))

@app.route("/edit", methods=["POST"])
def edit_balance():
    pan = request.form.get("pan")
    new_balance = float(request.form.get("balance", 0.0))
    cards = load_cards()
    for c in cards:
        if c["pan"] == pan:
            c["balance"] = new_balance
    save_cards(cards)
    return redirect(url_for("dashboard"))

@app.route("/delete", methods=["POST"])
def delete_card():
    pan = request.form.get("pan")
    cards = load_cards()
    cards = [c for c in cards if c["pan"] != pan]
    save_cards(cards)
    return redirect(url_for("dashboard"))

# === API for automation if needed ===

@app.route("/api/cards")
def api_cards():
    return jsonify(load_cards())

@app.route("/api/charges")
def api_charges():
    return jsonify(load_logs())

if __name__ == "__main__":
    app.run(port=5900)
