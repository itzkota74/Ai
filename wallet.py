import os,json,random
file="wallet.json"
if not os.path.exists(file):
    json.dump({"revenue":0},open(file,"w"))
data=json.load(open(file))
data["revenue"]+=random.randint(1,10)
json.dump(data,open(file,"w"))
