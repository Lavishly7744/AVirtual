import os
import datetime
import random
from aba_forge import generate_fake_routing

def generate_nacha_file(settlement_id, merchant_name, merchant_account, amount_cents):
    today = datetime.datetime.now()
    effective_date = (today + datetime.timedelta(days=1)).strftime("%y%m%d")

    fake_routing = generate_fake_routing()

    file_header = f"101 {fake_routing} 987654321 {today.strftime('%y%m%d')} A094101FakeBankName           {today.strftime('%y%m%d')}"
    batch_header = f"5225Merchant Payroll    {fake_routing} PPDPAYROLL  {today.strftime('%y%m%d')}"
    entry_detail = f"627{fake_routing}{merchant_account:>15}{amount_cents:010d}       {merchant_name[:22]:<22}0000000000"
    batch_control = f"822500000100000{amount_cents:010d}                          {fake_routing}987654321"
    file_control = "9000001000001000000000010000000000100000000000000"

    nacha_data = "\n".join([
        file_header,
        batch_header,
        entry_detail,
        batch_control,
        file_control
    ])

    filename = f"settlement_files/{settlement_id}.ach"
    os.makedirs("settlement_files", exist_ok=True)
    with open(filename, "w") as f:
        f.write(nacha_data)

    return filename
