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
