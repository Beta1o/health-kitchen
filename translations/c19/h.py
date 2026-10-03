import json,re
FR={"1/2":"½","1/3":"⅓","2/3":"⅔","1/4":"¼","3/4":"¾","1/8":"⅛"}
def fx(s):
    if not isinstance(s,str): return s
    s=s.replace("∕","/")
    def m(x):
        w,f=x.group(1),x.group(2)
        if f in FR: return (w or "")+FR[f]
        return x.group(0)
    return re.sub(r'(?<![\d/])(?:(\d+) )?(\d{1,2}/\d{1,2})(?![\d/])',m,s)
def pairs(l,conv):
    r=[list(x) if isinstance(x,(tuple,list)) else [None,x] for x in l]
    if conv: r=[[a,fx(b)] for a,b in r]
    return r
def L(title,desc,portions,serving,ing,steps,hints=(),fc=(),ar=False):
    return {"title":title,"description":desc,"portions":portions,"serving_size":fx(serving) if ar else serving,
            "ingredients":pairs(ing,ar),"steps":pairs(steps,ar),"hints":pairs(hints,ar),"food_choices":list(fc)}
def A(*a,**k): return L(*a,ar=True,**k)
def save(name,recs):
    json.dump([{"id":i,"translations":t} for i,t in recs],open(f"/mnt/c/WSL/davita/translations/{name}","w"),ensure_ascii=False,indent=1)
