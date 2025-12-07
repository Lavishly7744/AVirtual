import requests

payload = {
    "card_number": "371529401789598",
    "amount": 2500,
    "currency": "USD"
}

r = requests.post("http://127.0.0.1:5100/amex_charge", json=payload)
print(r.status_code, r.json())
