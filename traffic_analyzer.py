import os,json,random
file="traffic.json"
if not os.path.exists(file):
    json.dump({},open(file,"w"))
data=json.load(open(file))
page="index.html"
data[page]=data.get(page,0)+random.randint(1,5)
json.dump(data,open(file,"w"))
