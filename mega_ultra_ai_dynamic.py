#!/usr/bin/env python3
import os, time, random, requests, json, subprocess, logging
from datetime import datetime

# Logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/engine.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# --------------------------
# Auto-generate dynamic IDs & keys
# --------------------------
SYS_ID = f"SYS{random.randint(100000,999999)}"
AFF_TAG = f"AI{random.randint(100000,999999)}"
TRACK_ID = f"T{random.randint(1000,9999)}"
TELEGRAM_BOT_TOKEN = f"TOKEN{random.randint(1000000,9999999)}"
TELEGRAM_CHAT_ID = f"CHAT{random.randint(1000,9999)}"
DISCORD_WEBHOOK = f"https://discord.com/api/webhooks/{random.randint(1000000,9999999)}/AUTO"

# Modules
MODULES = ["automation","email_automation","traffic_analyzer","wallet","multi_channel","ab_testing","content_loop","affiliates"]

# --------------------------
# Module Runner
# --------------------------
def run_modules():
    results = {}
    for module in MODULES:
        try:
            results[module] = random.randint(1,100)
        except Exception as e:
            logging.error(f"Module {module} failed: {e}")
            results[module] = None
    return results

# --------------------------
# Build HTML Dashboard
# --------------------------
def build_dashboard(data):
    os.makedirs("site", exist_ok=True)
    html = "<html><head><title>Ultra AI Dashboard</title></head><body>"
    html += "<h1>Metrics</h1><table border=1><tr><th>Module</th><th>Value</th></tr>"
    for k,v in data.items():
        html += f"<tr><td>{k}</td><td>{v}</td></tr>"
    html += "</table></body></html>"
    with open("site/dashboard.html","w") as f:
        f.write(html)

# --------------------------
# Auto Git Push
# --------------------------
def git_push():
    try:
        subprocess.run(["git","add","."], check=True)
        subprocess.run(["git","commit","-m",f"Auto-update {datetime.utcnow().isoformat()}"], check=False)
        subprocess.run(["git","push","origin","main"], check=False)
        logging.info("Git push successful")
    except Exception as e:
        logging.error(f"Git push failed: {e}")

# --------------------------
# Notifications
# --------------------------
def notify_telegram(msg):
    try:
        requests.get(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            params={"chat_id": TELEGRAM_CHAT_ID, "text": msg}, timeout=5
        )
    except Exception as e:
        logging.error(f"Telegram notification failed: {e}")

def notify_discord(msg):
    try:
        requests.post(DISCORD_WEBHOOK, json={"content": msg}, timeout=5)
    except Exception as e:
        logging.error(f"Discord notification failed: {e}")

# --------------------------
# Main Loop
# --------------------------
while True:
    metrics = run_modules()
    build_dashboard(metrics)
    msg = f"✅ SYSTEM {SYS_ID} UPDATE\nAffiliate Tag: {AFF_TAG}\nTracking ID: {TRACK_ID}\nMetrics: {metrics}"
    notify_telegram(msg)
    notify_discord(msg)
    git_push()
    logging.info(f"Update complete: {metrics}")
    time.sleep(1800)  # 30-minute interval
