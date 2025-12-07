def generate_full_swift_message(transaction_id, sender_bic="FAKEUS33", receiver_bic="REALUS00"):
    today = datetime.datetime.now()

    mt103_data = f"""
{1:F01{sender_bic}XXXX0000000000}
{2:I103{receiver_bic}XXXXN}
{4:
:20:{transaction_id}
:23B:CRED
:32A:{today.strftime('%y%m%d')}USD1000,00
:50K:/000123456789
John Doe
123 Forgery Ave
Fake City, NY
:59:/123987654
Merchant Co
Real Street
Legit City, CA
:71A:OUR
-}
"""

    filename = f"settlement_files/{transaction_id}.swift"
    with open(filename, "w") as f:
        f.write(mt103_data)

    return filename

