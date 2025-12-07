# Fake Amex/Stripe Banking Network

This project simulates a full fake financial clearing network including:
- Card authorization
- Settlement
- ACH fake transfers
- BIN lookups
- Merchant daily reports

## 🛠 Services Overview

| Service | Port | Purpose |
|:---|:---|:---|
| amex_gateway.py | 5100 | Fake Authorization + Balance Enforcement |
| amexnet_server.py | 5000 | Fake Amex API |
| stripenet_server.py | 5001 | Fake Stripe API |
| fake_clearinghouse.py | 5200 | Fake Merchant Settlement Acceptance |
| fake_ach_settlement.py | 5300 | Fake ACH Wire Transfers |
| bin_responder.py | 5400 | Fake BIN Metadata Service |
| merchant_reporting_api.py | 5500 | Fake Daily Reporting for Merchants |

## 🚀 Quick Start

1. Install Docker and Docker Compose.
2. Clone this repo or place all project files together.
3. From the project directory, run:

```bash
docker-compose up --build
