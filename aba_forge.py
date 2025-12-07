import random

def generate_fake_routing():
    routing_prefix = random.choice(["021", "026", "031", "061"])
    institution = random.randint(10000, 99999)
    suffix = random.randint(0,9)
    return f"{routing_prefix}{institution}{suffix}"

def generate_aba_entry(bank_name="Fake Bank LLC"):
    routing_number = generate_fake_routing()
    return {
        "routing_number": routing_number,
        "bank_name": bank_name,
        "address": "123 Forgery St, Faketown, USA"
    }

if __name__ == "__main__":
    print(generate_aba_entry())
