import requests

batch = {
    "merchant_id": "merchant123",
    "transactions": [
        {"card_number": "371529401789598", "amount": 2500},
        {"card_number": "378282246310005", "amount": 1000}
    ],
    "total_amount": 3500,
    "currency": "USD"
}

r = requests.post("http://127.0.0.1:5200/settlement_batch", json=batch)
print(r.status_code, r.json())
