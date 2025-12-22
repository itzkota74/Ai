import os, hashlib, random
NETWORKS=["amazon","impact","shareasale"]
def affiliate_link(query):
    h=hashlib.sha256((query+os.environ["AFFILIATE_TAG"]).encode()).hexdigest()[:12]
    net=random.choice(NETWORKS)
    return f"https://{net}.com/offer/{h}?t={os.environ['TRACKING_ID']}"
