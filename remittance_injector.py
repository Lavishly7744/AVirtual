import json
import random
import datetime

def generate_remittance_entry(card_number, amount, merchant_id):
    now = datetime.datetime.utcnow()
    remittance = {
        "remittance_id": f"REM-{random.randint(100000,999999)}",
        "merchant_id": merchant_id,
        "card_number": card_number,
        "amount": amount,
        "currency": "USD",
        "settlement_date": now.strftime("%Y-%m-%d"),
        "status": "settled"
    }
    return remittance

def generate_remittance_batch(entries=10):
    batch = []
    for _ in range(entries):
        entry = generate_remittance_entry(
            card_number="3" + str(random.randint(40000000000000, 49999999999999)),
            amount=random.randint(100, 10000) / 100,
            merchant_id=f"MID{random.randint(1000,9999)}"
        )
        batch.append(entry)
    return batch

if __name__ == "__main__":
    batch = generate_remittance_batch(5)
    with open("fake_remittance_batch.json", "w") as f:
        json.dump(batch, f, indent=2)
    print("Generated remittance batch with 5 entries.")
