import requests

transfer = {
    "merchant_id": "merchant123",
    "amount": 3000,
    "currency": "USD",
    "destination_bank": "Fake Bank of USA",
    "destination_account": "123456789"
}

r = requests.post("http://127.0.0.1:5300/ach_transfer", json=transfer)
print(r.status_code, r.json())
