import json
import random
import datetime
import os

CARD_FILE = "amex_cards.json"

# ✅ Your fixed PANs
FIXED_PANS = [
    "371529401789598",
    "371529376817317",
    "371529188371313",
    "371529555742872",
    "371529610276403"
]

# ✅ Your original names
CARDHOLDERS = [
    "Amias Woods", "Mccoy Fowler", "Lennon Swanson", "Jefferson Willis", "Pierce Ortega",
    "Kelvin Huang", "Idris Paul", "August Bridges", "Alijah Vazquez", "Ocean Figueroa"
]

# ✅ Your original billing addresses
ADDRESSES = [
    {
        "line1": "1045 Emily Renzelli Boulevard",
        "city": "Salinas", "state": "CA", "zip": "93907", "phone": "831-663-2923"
    },
    {
        "line1": "3008 Rogers Street",
        "city": "Beallsville", "state": "PA", "zip": "15313", "phone": "513-602-6157"
    },
    {
        "line1": "4338 Ruckman Road",
        "city": "Shawnee", "state": "OK", "zip": "74801", "phone": "405-878-5524"
    },
    {
        "line1": "1964 Walton Street",
        "city": "Salt Lake City", "state": "UT", "zip": "84104", "phone": "801-381-0735"
    },
    {
        "line1": "1685 Horner Street",
        "city": "Cuyahoga Falls", "state": "OH", "zip": "44221", "phone": "330-922-6872"
    },
    {
        "line1": "3276 Maxwell Farm Road",
        "city": "Fredericksburg", "state": "VA", "zip": "22401", "phone": "540-227-2987"
    }
]

def generate_expiry():
    future = datetime.datetime.now() + datetime.timedelta(days=random.randint(365, 1825))
    return future.strftime("%m/%y")

def load_cards():
    if os.path.exists(CARD_FILE):
        with open(CARD_FILE, "r") as f:
            return json.load(f)
    return []

def save_cards(cards):
    with open(CARD_FILE, "w") as f:
        json.dump(cards, f, indent=2)

def create_card(index, unlimited=False):
    name = CARDHOLDERS[index % len(CARDHOLDERS)]
    address = ADDRESSES[index % len(ADDRESSES)]

    card = {
        "pan": FIXED_PANS[index % len(FIXED_PANS)],
        "cvv": f"{random.randint(1000, 9999)}",
        "expiry": generate_expiry(),
        "cardholder": name,
        "status": "ACTIVE",
        "balance": float('inf') if unlimited else 5000.00,
        "address": {
            "line1": address["line1"],
            "city": address["city"],
            "state": address["state"],
            "zip": address["zip"],
            "country": "US",
            "phone": address["phone"]
        }
    }
    return card

# === CLI generator ===
if __name__ == "__main__":
    print("💳 Amex Card Generator (using fixed PANs)")
    unlimited = input("Unlimited balance? (y/n): ").strip().lower() == "y"

    cards = load_cards()

    for i in range(len(FIXED_PANS)):
        card = create_card(i, unlimited=unlimited)
        cards.append(card)

        print("\n=== Amex Card Created ===")
        print(f"PAN     : {card['pan']}")
        print(f"CVV     : {card['cvv']}")
        print(f"Expiry  : {card['expiry']}")
        print(f"Name    : {card['cardholder']}")
        print(f"Address : {card['address']['line1']}, {card['address']['city']}, {card['address']['state']} {card['address']['zip']}")
        print(f"Phone   : {card['address']['phone']}")
        balance_display = "Unlimited" if unlimited else f"${card['balance']:.2f}"
        print(f"Balance : {balance_display}")

    save_cards(cards)
