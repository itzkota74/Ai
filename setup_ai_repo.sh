#!/bin/bash
# ============================================
# Full AI Revenue Engine Setup + GitHub Push
# ============================================

echo "[*] Creating project directory..."
mkdir -p ~/Ai/automation ~/Ai/templates ~/Ai/.github/workflows
cd ~/Ai || exit

# -----------------------
# 1. Environment file
# -----------------------
cat <<EOL > .env
STRIPE_API_KEY=sk_test_mockkey123456
MAILERLITE_API_KEY=mockkey123456
LLM_API_KEY=sk_test_mockkey123456
GITHUB_PAGES_URL=https://itzkota74.github.io/Ai/
EOL

# -----------------------
# 2. automation.py
# -----------------------
cat <<'EOL' > automation.py
import os, sqlite3, datetime

conn = sqlite3.connect('automation/db.sqlite')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    timestamp TEXT
)''')
conn.commit()

def generate_content(prompt):
    return f"<h2>AI Generated Content for {prompt}</h2><p>Discover top products, guides, and tools in {prompt}. Click the affiliate link below!</p>"

def create_landing_page(niche):
    content = generate_content(niche)
    html = f"""
    <html><head><title>{niche} Deals</title></head>
    <body>
        <h1>{niche} Deals & Tips!</h1>
        {content}
        <a href='https://www.example.com/affiliate/{niche.replace(' ','_')}' target='_blank'>Start Now</a>
    </body></html>
    """
    filename = f"automation/{niche.replace(' ','_')}_landing.html"
    with open(filename, 'w') as f:
        f.write(html)
    print(f"[+] Landing page created: {filename}")

def collect_lead(name, email):
    c.execute('INSERT INTO leads (name,email,timestamp) VALUES (?,?,?)', (name,email,str(datetime.datetime.now())))
    conn.commit()
    print(f"[+] Lead collected: {name} | {email}")

niches = ["AI Tools", "Fitness Gadgets", "Crypto Guides", "NFT Tips", "Micro SaaS Tools"]
for niche in niches:
    create_landing_page(niche)
    collect_lead(f"TestUser_{niche}", f"{niche.lower().replace(' ','')}@example.com")

print("[+] Automation run complete.")
EOL

# -----------------------
# 3. email_automation.py
# -----------------------
cat <<'EOL' > email_automation.py
def send_email(to_email, subject, body):
    print(f"[Mock Email] To: {to_email} | Subject: {subject}\n{body}\n")

send_email("user@example.com", "Welcome to your AI Revenue Engine!", "Click here to start: https://example.com")
EOL

# -----------------------
# 4. Landing page template
# -----------------------
cat <<'EOL' > templates/landing_template.html
<html>
<head><title>{{NICHE}} Affiliate Page</title></head>
<body>
<h1>Discover {{NICHE}} Deals Today!</h1>
<p>{{CONTENT}}</p>
<a href="{{AFFILIATE_LINK}}" target="_blank">Get Started</a>
</body>
</html>
EOL

# -----------------------
# 5. GitHub Actions workflow
# -----------------------
cat <<'EOL' > .github/workflows/auto.yml
name: Money Engine Automation
on:
  schedule:
    - cron: '0 */6 * * *'
  push:
    branches:
      - main
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install sqlite3 requests stripe
      - run: python automation.py
      - run: python email_automation.py
EOL

# -----------------------
# 6. Git setup
# -----------------------
echo "[*] Initializing Git..."
git init
git branch -M main

# Prompt for PAT
read -p "Enter your GitHub Personal Access Token: " GITHUB_PAT

git remote remove origin 2>/dev/null
git remote add origin https://itzkota74:${GITHUB_PAT}@github.com/itzkota74/Ai.git

echo "[*] Adding all files..."
git add .env automation.py email_automation.py templates/ .github/

echo "[*] Committing..."
git commit -m "Full end-to-end AI revenue engine setup"

echo "[*] Pushing to GitHub..."
git push -u origin main

echo "[*] Setup complete! Repo is fully operational and pushed."
