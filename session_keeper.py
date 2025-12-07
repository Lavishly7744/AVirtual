import time
import requests

def keep_sessions_alive():
    endpoints = [
        "http://localhost:6001/ledger",
        "http://localhost:7000/fedach/settlement",
        "http://localhost:7000/fedwire/transfer"
    ]

    while True:
        for url in endpoints:
            try:
                requests.get(url, timeout=5)
                print(f"✅ Keepalive: {url}")
            except:
                print(f"⚠️ Failed keepalive: {url}")
        time.sleep(30)

if __name__ == "__main__":
    keep_sessions_alive()
