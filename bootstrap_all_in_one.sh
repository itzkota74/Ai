#!/usr/bin/env bash
set -e

# ---------- STRUCTURE ----------
mkdir -p site automation templates .github/workflows analytics

# ---------- ENV ----------
cat <<EOT > .env
# Affiliate (replace YOURTAG later)
AMAZON_TAG=YOURTAG

# Email (Brevo free tier – fill later)
SMTP_HOST=smtp-relay.brevo.com
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASS=BREVO_API_KEY
FROM_EMAIL=you@example.com

# Analytics (optional)
PLAUSIBLE_DOMAIN=itzkota74.github.io
EOT

# ---------- INDEX (FIXES 404) ----------
cat <<'EOT' > site/index.html
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>AI Revenue Engine</title>
</head>
<body>
<h1>AI Revenue Engine</h1>
<p>Live monetized pages:</p>
<ul id="list"></ul>
<script>
fetch('pages.json').then(r=>r.json()).then(p=>{
  const ul=document.getElementById('list');
  p.forEach(x=>{
    const li=document.createElement('li');
    li.innerHTML=`<a href="${x}">${x}</a>`;
    ul.appendChild(li);
  });
});
</script>
</body>
</html>
EOT

# ---------- TEMPLATE ----------
cat <<'EOT' > templates/page.html
<!doctype html>
<html>
<head><meta charset="utf-8"><title>{{TITLE}}</title></head>
<body>
<h1>{{TITLE}}</h1>
<p>{{CONTENT}}</p>
<a href="{{AFFILIATE}}" target="_blank">View Offers</a>
</body>
</html>
EOT

# ---------- AUTOMATION ----------
cat <<'EOT' > automation.py
import os, json, shutil, datetime

NICHES = ["AI Tools","Fitness Gadgets","Crypto Guides","Micro SaaS"]
SITE="site"
os.makedirs(SITE, exist_ok=True)

def render(title, content, aff):
    with open("templates/page.html") as f:
        html=f.read()
    return html.replace("{{TITLE}}",title)\
               .replace("{{CONTENT}}",content)\
               .replace("{{AFFILIATE}}",aff)

pages=[]
for n in NICHES:
    fn=f"{n.replace(' ','_')}.html"
    aff=f"https://www.amazon.com/s?k={n.replace(' ','+')}&tag={os.getenv('AMAZON_TAG','YOURTAG')}"
    html=render(n,f"Best {n} curated {datetime.date.today()}",aff)
    with open(f"{SITE}/{fn}","w") as f: f.write(html)
    pages.append(fn)

with open(f"{SITE}/pages.json","w") as f:
    json.dump(pages,f)

print("Published:", pages)
EOT

# ---------- EMAIL (FREE TIER READY) ----------
cat <<'EOT' > email_automation.py
import smtplib, os
from email.message import EmailMessage

def send(to,sub,body):
    msg=EmailMessage()
    msg["From"]=os.getenv("FROM_EMAIL")
    msg["To"]=to
    msg["Subject"]=sub
    msg.set_content(body)
    with smtplib.SMTP(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT")) ) as s:
        s.starttls()
        s.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))
        s.send_message(msg)

# Example (commented until creds set)
# send("user@example.com","Welcome","Your AI site is live")
EOT

# ---------- ANALYTICS (OPTIONAL) ----------
cat <<'EOT' > analytics/README.md
Add to site/index.html head:
<script defer data-domain="YOURDOMAIN" src="https://plausible.io/js/script.js"></script>
EOT

# ---------- GITHUB ACTIONS ----------
cat <<'EOT' > .github/workflows/publish.yml
name: Publish Site
on:
  push:
    branches: [ main ]
  schedule:
    - cron: "0 */6 * * *"
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with: { python-version: "3.11" }
      - run: python automation.py
      - run: |
          git config user.name github-actions
          git config user.email github-actions@github.com
          git add site/
          git commit -m "Auto-publish site" || echo "No changes"
          git push
EOT

# ---------- HARDEN ----------
cat <<'EOT' > .gitignore
.env
__pycache__/
*.pyc
venv/
node_modules/
EOT

# ---------- COMMIT ----------
git add .
git commit -m "All-in-one compiled system" || true
git push

echo "DONE"
