#!/data/data/com.termux/files/usr/bin/python3
# mega_ultra_ai_full.py
# Unified entrypoint for Ultra AI Engine (Termux-ready)
# Auto-deploy, logging, Git push, Telegram/Discord notifications

import os
import sys
import time
import random
import json
import subprocess
import logging

# Ensure modules path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# ----------------------------
# 1️⃣ Import all modules
# ----------------------------
try:
    import mega_ultra_ai_engine
    import mega_ultra_ai_dynamic
    import automation
    import email_automation
    import traffic_analyzer
    import wallet
    import affiliates
    import multi_channel
    import dynamic_niches
except ModuleNotFoundError as e:
    print(f"[ERROR] Missing module: {e.name}. Make sure all files exist in {BASE_DIR}")
    sys.exit(1)

# ----------------------------
# 2️⃣ Environment Variables
# ----------------------------
os.environ.setdefault("SYS_ID", f"{random.getrandbits(64):x}")
os.environ.setdefault("AFFILIATE_TAG", f"ai{os.environ['SYS_ID']}")
os.environ.setdefault("TRACKING_ID", "")

# ----------------------------
# 3️⃣ Logging
# ----------------------------
logs_dir = os.path.join(BASE_DIR, "logs")
os.makedirs(logs_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(logs_dir, "mega_ultra_ai_full.log"),
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logging.info("Ultra AI Engine initialized")

# ----------------------------
# 4️⃣ Core Engine Runner
# ----------------------------
def run_full_engine():
    logging.info("Launching full Ultra AI Engine...")

    # Core engine
    logging.info("Starting mega_ultra_ai_engine...")
    mega_ultra_ai_engine.run_engine()

    # Dynamic engine
    logging.info("Starting mega_ultra_ai_dynamic...")
    mega_ultra_ai_dynamic.run_dynamic()

    # Automation
    logging.info("Running automation tasks...")
    automation.run_tasks()
    email_automation.run_email()
    
    # Traffic & analytics
    traffic_analyzer.run_traffic_analysis()
    
    # Wallet & affiliates
    wallet.run_wallet()
    affiliates.run_affiliate_tracking()
    
    # Multi-channel & niches
    multi_channel.run_channels()
    dynamic_niches.run_niches()

    logging.info("All modules executed successfully.")

# ----------------------------
# 5️⃣ Auto Git push (every 30 mins)
# ----------------------------
def git_push_loop():
    while True:
        try:
            subprocess.run(["git", "add", "."], cwd=BASE_DIR)
            subprocess.run(["git", "commit", "-m", f"Auto-update {time.strftime('%Y-%m-%d %H:%M:%S')}"], cwd=BASE_DIR)
            subprocess.run(["git", "push", "origin", "main"], cwd=BASE_DIR)
            logging.info("Git push completed successfully.")
        except Exception as e:
            logging.error(f"Git push failed: {e}")
        time.sleep(1800)  # 30 mins

# ----------------------------
# 6️⃣ Telegram/Discord Notifications
# ----------------------------
def send_notifications(msg):
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")
    webhook = os.environ.get("DISCORD_WEBHOOK_URL", "")

    if token and chat_id:
        try:
            import requests
            requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                          data={"chat_id": chat_id, "text": msg})
            logging.info("Telegram notification sent")
        except Exception as e:
            logging.error(f"Telegram notification failed: {e}")

    if webhook:
        try:
            import requests
            requests.post(webhook, json={"content": msg})
            logging.info("Discord notification sent")
        except Exception as e:
            logging.error(f"Discord notification failed: {e}")

# ----------------------------
# 7️⃣ Main Execution
# ----------------------------
if __name__ == "__main__":
    send_notifications(f"✅ SYSTEM {os.environ['SYS_ID']} STARTED")
    run_full_engine()
    # Run Git push loop in background
    import threading
    threading.Thread(target=git_push_loop, daemon=True).start()
    logging.info("Ultra AI Engine is running in background.")
    print(f"✅ Deployment complete. System ID: {os.environ['SYS_ID']}")
