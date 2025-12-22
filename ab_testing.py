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
