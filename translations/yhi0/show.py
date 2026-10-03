import json,sys
d=json.load(open('../jobs_yhi0.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for i,j in enumerate(d[a:b],a):
    o={"i":i,"id":j["id"]}
    for k in ("title","description","portions","serving_size"):o[k]=j[k]
    for k in("ingredients","steps","hints"):
        o[k]=[(t if g is None else [g,t]) for g,t in j[k]]
    o["fc"]=j["food_choices"]
    print(json.dumps(o,ensure_ascii=False))
