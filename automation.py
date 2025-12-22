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
