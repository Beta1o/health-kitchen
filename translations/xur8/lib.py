import json
def R(id,t,d,p,s,ing,st,h=(),f=(),ig=None,sg=None,hg=None):
    """ing/st/h: lists of text, or (group,text) tuples."""
    def pr(l): return [list(x) if isinstance(x,tuple) else [None,x] for x in l]
    return {"id":id,"translations":{"ur":{"title":t,"description":d,"portions":p,"serving_size":s,"ingredients":pr(ing),"steps":pr(st),"hints":pr(h),"food_choices":list(f)}}}
def save(n,recs):
    json.dump(recs,open(f'/mnt/c/WSL/davita/translations/out_xur8_part{n}.json','w'),ensure_ascii=False,indent=1)
