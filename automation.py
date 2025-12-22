import os,json,datetime
from affiliates import affiliate_link
from dynamic_niches import trending_niches

SITE="site"
TPL="templates/page.html"
os.makedirs(SITE,exist_ok=True)
with open(TPL) as f:
    template=f.read()

pages=[]
LANGS=["en","es","fr"]
niches=trending_niches()

for niche in niches:
    for lang in LANGS:
        title=f"{niche.title()} ({lang})"
        content=f"Updated {datetime.date.today()} | System {os.environ['SYS_ID']}"
        html=(template.replace("{{TITLE}}",title)
                     .replace("{{CONTENT}}",content)
                     .replace("{{LINK}}",affiliate_link(niche)))
        path=f"{SITE}/{lang}/{niche.replace(' ','_')}.html"
        os.makedirs(os.path.dirname(path),exist_ok=True)
        open(path,"w").write(html)
        pages.append(path.replace("site/",""))

with open(f"{SITE}/pages.json","w") as f:
    json.dump(pages,f)
