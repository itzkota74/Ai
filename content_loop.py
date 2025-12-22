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
