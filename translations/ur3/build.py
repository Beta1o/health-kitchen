import json,sys
def build(recs, jobs_slice, outpath):
    out=[]
    for r,j in zip(recs,jobs_slice):
        def pairs(key,vals):
            src=j[key]
            res=[]
            for (g,_),v in zip(src,vals):
                if isinstance(v,(list,tuple)): res.append([v[0],v[1]])
                else: res.append([g,v])
            return res
        out.append({"id":j["id"],"translations":{"ur":{"title":r["t"],"description":r["d"],"portions":r["p"],"serving_size":r["s"],"ingredients":pairs("ingredients",r["i"]),"steps":pairs("steps",r["st"]),"hints":pairs("hints",r["h"]),"food_choices":r["f"]}}})
    json.dump(out,open(outpath,"w",encoding="utf-8"),ensure_ascii=False,indent=1)
    print(len(out))
