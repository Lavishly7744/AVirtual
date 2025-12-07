import pandas as pd
import matplotlib.pyplot as plt
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

def analyze_attempts(df):
    summary = {}

    merchants = df["merchant"].unique()

    for merchant in merchants:
        subset = df[df["merchant"] == merchant]
        total = len(subset)
        successes = len(subset[subset["result"] == "SUCCESS"])
        pendings = len(subset[subset["result"] == "PENDING"])
        declines = len(subset[subset["result"] == "DECLINED"])

        success_rate = (successes / total) * 100 if total > 0 else 0
        pending_rate = (pendings / total) * 100 if total > 0 else 0
        decline_rate = (declines / total) * 100 if total > 0 else 0

        summary[merchant] = {
            "total_attempts": total,
            "successes": successes,
            "pendings": pendings,
            "declines": declines,
            "success_rate": round(success_rate, 2),
            "pending_rate": round(pending_rate, 2),
            "decline_rate": round(decline_rate, 2)
        }

    return summary

def plot_summary(summary):
    merchants = list(summary.keys())
    success_rates = [summary[m]["success_rate"] for m in merchants]
    decline_rates = [summary[m]["decline_rate"] for m in merchants]
    pending_rates = [summary[m]["pending_rate"] for m in merchants]

    x = range(len(merchants))
    
    plt.figure(figsize=(12,6))
    plt.bar(x, success_rates, width=0.3, label="Success %", align="center", color="green")
    plt.bar(x, decline_rates, width=0.3, bottom=success_rates, label="Decline %", align="center", color="red")
    plt.bar(x, pending_rates, width=0.3, bottom=[s+d for s,d in zip(success_rates, decline_rates)], label="Pending %", align="center", color="blue")

    plt.xticks(x, merchants, rotation=45)
    plt.ylabel("Rate (%)")
    plt.title("Checkout Attempt Outcomes per Merchant")
    plt.legend()
    plt.tight_layout()
    plt.savefig("checkout_summary.png")
    plt.show()

def main():
    df = load_log_file()
    summary = analyze_attempts(df)

    print("\n=== Checkout Analytics Summary ===\n")
    for merchant, stats in summary.items():
        print(f"Merchant: {merchant}")
        for k, v in stats.items():
            print(f"  {k}: {v}")
        print()

    plot_summary(summary)

    # Save report
    today = time.strftime("%Y-%m-%d", time.localtime())
    df.to_csv(f"checkout_attempts_{today}.csv", index=False)
    print(f"\n✅ Full raw data saved as checkout_attempts_{today}.csv")

if __name__ == "__main__":
    main()
