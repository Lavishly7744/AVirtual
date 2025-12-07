from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # 🔥 Just a dummy for session management

# Load data from JSON files
def load_data(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return []

# Route: Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # 🔥 Fake authentication: accept anything
        session['logged_in'] = True
        return redirect(url_for('dashboard'))
    return render_template('login.html')

# Route: Dashboard (requires login)
@app.route('/')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    charges = load_data("amex_cards.json")
    batches = load_data("settlement_batches.json")
    settlements = load_data("ach_webhook_log.json")
    wires = load_data("fake_bank_transfers.json")

    # Search functionality
    query = request.args.get('query', '')

    if query:
        charges = [c for c in charges if query in c.get('pan', '') or query.lower() in c.get('cardholder', '').lower()]
        batches = [b for b in batches if query in b.get('batch_id', '')]
        settlements = [s for s in settlements if query in s.get('settlement_id', '')]
        wires = [w for w in wires if query in w.get('wire_transfer_id', '')]

    return render_template("dashboard.html", charges=charges, batches=batches, settlements=settlements, wires=wires, query=query)

# Route: Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5900)

