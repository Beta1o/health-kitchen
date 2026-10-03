import json
def N(x):
    return [i if isinstance(i,list) else [None,i] for i in (x or [])]
def R(id,title,desc,portions,serving,ings,steps,hints,fc):
    return {"id":id,"translations":{"ur":{"title":title,"description":desc,"portions":portions,"serving_size":serving,"ingredients":N(ings),"steps":N(steps),"hints":N(hints),"food_choices":fc or []}}}
import re
def fix(t):
    if isinstance(t,str):
        t=t.replace("گارباںزو","گاربانزو").replace("جوا لہسن","پھانک لہسن").replace("جوے لہسن","پھانکیں لہسن")
        t=re.sub(r'(?<=[\u0600-\u06ff])\.(?=\s|$)','۔',t)
        return t
    if isinstance(t,list): return [fix(x) for x in t]
    if isinstance(t,dict): return {k:fix(v) for k,v in t.items()}
    return t
def save(n,items):
    items=fix(items)
    json.dump(items,open(f"/mnt/c/WSL/davita/translations/out_xur6_part{n}.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
