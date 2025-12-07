import pandas as pd
import json
import time

def load_log_file(log_path="multi_checkout_log.txt"):
    columns = ["timestamp", "merchant", "card_pan", "result"]
    records = []

    with open(log_path, "r") as f:
        lines = f.readlines()

    for line in lines:
        parts = line.strip().split("|")
        if len(parts) == 4:
            timestamp, merchant, card_pan, result = [p.strip() for p in parts]
            records.append([timestamp, merchant, card_pan, result])

    df = pd.DataFrame(records, columns=columns)
    return df

def classify_cards(df):
    successes = df[df["result"] == "SUCCESS"]["card_pan"].unique()
    pendings = df[df["result"] == "PENDING"]["card_pan"].unique()
    declines = df[df["result"] == "DECLINED"]["card_pan"].unique()
    errors = df[df["result"].str.contains("ERROR")]["card_pan"].unique()

    groups = {
        "Group_A_Strong": list(successes),
        "Group_B_PendingOnly": [c for c in pendings if c not in successes],
        "Group_C_New": []  # We fill this later by checking amex_cards.json
    }

    all_tested_cards = set(successes) | set(pendings) | set(declines) | set(errors)

    with open("amex_cards.json", "r") as f:
        all_cards = json.load(f)
    
    all_pans = [card["pan"] for card in all_cards]

    # Find cards never used yet
    for pan in all_pans:
        if pan not in all_tested_cards:
            groups["Group_C_New"].append(pan)

    return groups

def save_campaigns(groups):
    with open("card_campaigns.json", "w") as f:
        json.dump(groups, f, indent=2)

def main():
    df = load_log_file()
    groups = classify_cards(df)
    save_campaigns(groups)

    print("\n=== Smart Campaign Groups Created ===\n")
    for group_name, cards in groups.items():
        print(f"{group_name}: {len(cards)} cards")

    today = time.strftime("%Y-%m-%d", time.localtime())
    df.to_csv(f"campaign_raw_attempts_{today}.csv", index=False)
    print(f"\n✅ Full raw attempt data saved as campaign_raw_attempts_{today}.csv")

if __name__ == "__main__":
    main()
