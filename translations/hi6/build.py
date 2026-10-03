import json,sys
# usage: build.py partN  (reads hi6/pN.py defining DATA list of tuples)
def conv(l):
    if l is None: return []
    return [[None,x] if isinstance(x,str) else [x[0],x[1]] for x in l]
def build(data):
    out=[]
    for (id,t,d,p,s,ing,st,h,fc) in data:
        out.append({"id":id,"translations":{"hi":{"title":t,"description":d,"portions":p,"serving_size":s,"ingredients":conv(ing),"steps":conv(st),"hints":conv(h),"food_choices":fc}}})
    return out
