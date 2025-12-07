import requests

bin_number = "371529"
r = requests.get(f"http://127.0.0.1:5400/bin_lookup/{bin_number}")
print(r.status_code, r.json())
