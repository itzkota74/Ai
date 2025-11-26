#!/usr/bin/env python3
import requests
import urllib3
import subprocess

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print("🔓 ROUTER BYPASS TOOL")
print("=" * 35)

target = "192.168.1.1"

print(f"🎯 Targeting: {target}")

# Try without SSL verification
print("\n🔓 Testing with SSL verification disabled...")
try:
    response = requests.get(f"https://{target}", verify=False, timeout=5)
    print(f"✅ HTTPS (no verify): Status {response.status_code}")
    if response.status_code == 200:
        print("✅ Router admin page accessible!")
        # Check for router brand
        if 'tp-link' in response.text.lower():
            print("📡 Router: TP-Link")
        elif 'netgear' in response.text.lower():
            print("📡 Router: Netgear")
        elif 'asus' in response.text.lower():
            print("📡 Router: Asus")
        elif 'linksys' in response.text.lower():
            print("📡 Router: Linksys")
        elif 'd-link' in response.text.lower():
            print("📡 Router: D-Link")
except Exception as e:
    print(f"❌ HTTPS failed: {e}")

# Try HTTP instead
print("\n🌐 Testing HTTP (port 80)...")
try:
    response = requests.get(f"http://{target}", timeout=5)
    print(f"✅ HTTP: Status {response.status_code}")
    if response.status_code == 200:
        print("✅ Router admin accessible via HTTP!")
        print("💡 Visit: http://192.168.1.1")
except Exception as e:
    print(f"❌ HTTP failed: {e}")

# Try common router admin paths
print("\n🔍 Testing common admin paths...")
paths = ['/admin', '/login', '/', '/cgi-bin/login', '/webpages/login.html']
for path in paths:
    try:
        response = requests.get(f"http://{target}{path}", timeout=2)
        if response.status_code == 200:
            print(f"✅ Found admin page: {path}")
    except:
        pass

# Try to brute force common credentials
print("\n🔑 Testing default credentials...")
credentials = [
    ('admin', 'admin'),
    ('admin', 'password'),
    ('admin', '1234'),
    ('admin', ''),
    ('root', 'admin'),
    ('admin', 'admin123'),
]

for username, password in credentials:
    try:
        response = requests.get(f"http://{target}", auth=(username, password), timeout=2)
        if response.status_code == 200:
            print(f"🎉 CREDENTIALS WORK: {username}:{password}")
            break
    except:
        pass

print("\n🚀 Alternative access methods:")
print("1. Use a web browser on your device: http://192.168.1.1")
print("2. Try different browsers if one fails")
print("3. Look for router model on the device itself")
print("4. Check for mobile app for router management")
