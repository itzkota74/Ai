import requests
def trending_niches():
    try:
        r=requests.get("https://api.trendingproducts.io/ai-top?limit=5",timeout=10)
        r.raise_for_status()
        return [item["name"] for item in r.json()]
    except:
        return ["ai tools","fitness gear","remote jobs"]
