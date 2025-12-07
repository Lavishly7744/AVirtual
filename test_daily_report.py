import requests

r = requests.get("http://127.0.0.1:5500/daily_report")
print(r.status_code, r.json())
