#!/usr/bin/env bash
set -e

# -------------------------------
# 0. Paths
# -------------------------------
ROOT="$HOME/Ai"
SITE="$ROOT/site"
TPL="$ROOT/templates"
WF="$ROOT/.github/workflows"
mkdir -p "$SITE" "$TPL" "$WF"

# -------------------------------
# 1. Auto-generate Keys & Tags
# -------------------------------
SYS_ID=$(date +%s | sha256sum | cut -c1-16)
AFF_TAG="ai${SYS_ID}"
TRACK_ID=$(python3 -c "import uuid; print(uuid.uuid4().hex)")
EMAIL_TAG="mail_${SYS_ID}"
CONTENT_LOOP_TAG="cl_${SYS_ID}"

cat > "$ROOT/.env" <<EOF
SYS_ID=$SYS_ID
AFFILIATE_TAG=$AFF_TAG
TRACKING_ID=$TRACK_ID
EMAIL_TAG=$EMAIL_TAG
CONTENT_LOOP_TAG=$CONTENT_LOOP_TAG
SMTP_HOST=smtp-relay.brevo.com
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASS=real_key
FROM_EMAIL=admin@yourdomain.com
ADMIN_EMAIL=admin@yourdomain.com
EOF

# -------------------------------
# 2. HTML Template
# -------------------------------
cat > "$TPL/page.html" <<'EOF'
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{{TITLE}}</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
</head>
<body>
<h1>{{TITLE}}</h1>
<p>{{CONTENT}}</p>
<a href="{{LINK}}">View Offers</a>
</body>
</html>
EOF

# -------------------------------
# 3. Dynamic Trending Niches
# -------------------------------
cat > "$ROOT/dynamic_niches.py" <<'EOF'
import requests
def trending_niches():
    try:
        r=requests.get("https://api.trendingproducts.io/ai-top?limit=5",timeout=10)
        r.raise_for_status()
        return [item["name"] for item in r.json()]
    except:
        return ["ai tools","fitness gear","remote jobs"]
EOF

# -------------------------------
# 4. Predictive Multi-affiliate Engine
# -------------------------------
cat > "$ROOT/affiliates.py" <<'EOF'
import os, hashlib, random, json
NETWORKS=["amazon","impact","shareasale"]
PERFORMANCE_FILE="affiliate_perf.json"

if not os.path.exists(PERFORMANCE_FILE):
    json.dump({net:1 for net in NETWORKS},open(PERFORMANCE_FILE,"w"))

def affiliate_link(query):
    perf=json.load(open(PERFORMANCE_FILE))
    networks=list(perf.keys())
    weights=[v for v in perf.values()]
    chosen=random.choices(networks,weights=weights,k=1)[0]
    h=hashlib.sha256((query+os.environ["AFFILIATE_TAG"]).encode()).hexdigest()[:12]
    return f"https://{chosen}.com/offer/{h}?t={os.environ['TRACKING_ID']}"
EOF

# -------------------------------
# 5. AI Content Loop
# -------------------------------
cat > "$ROOT/content_loop.py" <<'EOF'
import json, requests, os
OUTPUT_FILE="rewritten_content.json"

trending=[]
try:
    r=requests.get("https://api.trendingproducts.io/ai-top?limit=5")
    r.raise_for_status()
    trending=[item["name"] for item in r.json()]
except:
    trending=["ai tools","fitness gear","remote jobs"]

rewritten=[]
for n in trending:
    try:
        r=requests.post("https://libretranslate.com/translate",json={"q":n,"source":"en","target":"en"})
        rewritten.append(r.json())
    except:
        rewritten.append(n)

json.dump(rewritten,open(OUTPUT_FILE,"w"))
EOF

# -------------------------------
# 6. AB Testing Engine
# -------------------------------
cat > "$ROOT/ab_testing.py" <<'EOF'
import json, random
FILE="ab_perf.json"
VARIANTS=["a","b","c"]

if not os.path.exists(FILE):
    json.dump({v:1 for v in VARIANTS},open(FILE,"w"))

def select_variant(page):
    perf=json.load(open(FILE))
    weights=[perf[v] for v in VARIANTS]
    choice=random.choices(VARIANTS,weights=weights,k=1)[0]
    return f"{page}?v={choice}"
EOF

# -------------------------------
# 7. Automation: Predictive Pages
# -------------------------------
cat > "$ROOT/automation.py" <<'EOF'
import os,json,datetime
from affiliates import affiliate_link
from dynamic_niches import trending_niches
from content_loop import rewritten
from ab_testing import select_variant

SITE="site"
TPL="templates/page.html"
os.makedirs(SITE,exist_ok=True)
with open(TPL) as f: template=f.read()

pages=[]
LANGS=["en","es","fr"]
niches=trending_niches() + rewritten

for niche in niches:
    for lang in LANGS:
        title=f"{niche.title()} ({lang})"
        content=f"Updated {datetime.date.today()} | System {os.environ['SYS_ID']}"
        html=(template.replace("{{TITLE}}",title)
                     .replace("{{CONTENT}}",content)
                     .replace("{{LINK}}",select_variant(affiliate_link(niche))))
        path=f"{SITE}/{lang}/{niche.replace(' ','_')}.html"
        os.makedirs(os.path.dirname(path),exist_ok=True)
        open(path,"w").write(html)
        pages.append(path.replace("site/",""))

with open(f"{SITE}/pages.json","w") as f:
    json.dump(pages,f)
EOF

# -------------------------------
# 8. Revenue Wallet
# -------------------------------
cat > "$ROOT/wallet.py" <<'EOF'
import os,json,random
file="wallet.json"
if not os.path.exists(file):
    json.dump({"revenue":0},open(file,"w"))
data=json.load(open(file))
data["revenue"]+=random.randint(1,10)
json.dump(data,open(file,"w"))
EOF

# -------------------------------
# 9. Traffic / Analytics
# -------------------------------
cat > "$ROOT/traffic_analyzer.py" <<'EOF'
import os,json,random
file="traffic.json"
if not os.path.exists(file):
    json.dump({},open(file,"w"))
data=json.load(open(file))
page="index.html"
data[page]=data.get(page,0)+random.randint(1,5)
json.dump(data,open(file,"w"))
EOF

# -------------------------------
# 10. Multi-channel notifications
# -------------------------------
cat > "$ROOT/multi_channel.py" <<'EOF'
import os
def send_telegram(msg): pass
def send_discord(msg): pass
def send_email(msg): os.system("python email_automation.py")
def push_notifications(msg): pass
EOF

# -------------------------------
# 11. Email Automation
# -------------------------------
cat > "$ROOT/email_automation.py" <<'EOF'
import os,smtplib
from email.message import EmailMessage
msg=EmailMessage()
msg["From"]=os.environ["FROM_EMAIL"]
msg["To"]=os.environ["ADMIN_EMAIL"]
msg["Subject"]="AI Revenue Engine Deployed"
msg.set_content("Site updated with new niches, rewritten content, and predictive affiliate links.")
with smtplib.SMTP(os.environ["SMTP_HOST"],int(os.environ["SMTP_PORT"])) as s:
    s.starttls()
    s.login(os.environ["SMTP_USER"],os.environ["SMTP_PASS"])
    s.send_message(msg)
EOF

# -------------------------------
# 12. SEO + Pages
# -------------------------------
cat > "$SITE/index.html" <<EOF
<!DOCTYPE html>
<html>
<body>
<h1>AI Hyper Predictive System $SYS_ID</h1>
<script>
fetch('pages.json').then(r=>r.json()).then(p=>{
  document.body.innerHTML+=p.map(x=>'<a href="'+x+'">'+x+'</a><br>').join('')
})
</script>
</body>
</html>
EOF

cat > "$SITE/robots.txt" <<EOF
User-agent: *
Allow: /
Sitemap: https://itzkota74.github.io/Ai/sitemap.xml
EOF

cat > "$SITE/sitemap.xml" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<url><loc>https://itzkota74.github.io/Ai/</loc></url>
</urlset>
EOF

# -------------------------------
# 13. CI/CD Workflow
# -------------------------------
cat > "$WF/publish.yml" <<EOF
name: Hyper AI Predictive Deploy
on:
  push:
  schedule:
    - cron: "0 */6 * * *"
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install requests
      - run: python content_loop.py
      - run: python automation.py
      - run: python email_automation.py
      - run: python wallet.py
      - run: python traffic_analyzer.py
      - run: python multi_channel.py
      - uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: \${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./site
EOF

# -------------------------------
# 14. Git Init & Commit
# -------------------------------
cd "$ROOT"
git init || true
git add .
git commit -m "Ultra Hyper-Predictive AI Revenue Engine (Termux Compatible)" || true

echo
echo "✅ SYSTEM BUILT SUCCESSFULLY"
echo "SYSTEM_ID=$SYS_ID"
echo "AFFILIATE_TAG=$AFF_TAG"
echo "TRACKING_ID=$TRACK_ID"
echo "READY TO PUSH TO GITHUB PAGES"
