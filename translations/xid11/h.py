import json,sys
J={r['id']:r for r in json.load(open('/mnt/c/WSL/davita/translations/jobs_xid11.json'))}
def conv(orig,new):
    orig=orig or []
    assert len(orig)==len(new),(len(orig),len(new),new[:1])
    return [[o[0],n] if isinstance(n,str) else list(n) for o,n in zip(orig,new)]
def T(i,title,desc,por,serv,ing,steps,hints,fc):
    j=J[i]
    assert len(fc)==len(j['food_choices']),i
    return {"id":i,"translations":{"id":{"title":title,"description":desc if j['description'] is not None else None,
     "portions":por if j['portions'] is not None else None,"serving_size":serv if j['serving_size'] is not None else None,
     "ingredients":conv(j['ingredients'],ing),"steps":conv(j['steps'],steps),"hints":conv(j['hints'],hints),"food_choices":fc}}}
def save(n,L):
    json.dump(L,open(f'/mnt/c/WSL/davita/translations/out_xid11_part{n}.json','w'),ensure_ascii=False,indent=1)
LBL={"chef":"Catatan Koki","carb":"Karbohidrat","kp":"Kalium/fosfat","pk":"Fosfat/kalium","prot":"Protein","gf":"Bebas gluten","veg":"Vegetarian","vegan":"Vegan","health":"Pilihan lebih sehat","cheap":"Pilihan lebih hemat","store":"Penyimpanan","tips":"Tips","energy":"Energi","safety":"Keamanan pangan","serve":"Saran penyajian"}
def g(k,t): return (LBL[k],t)
