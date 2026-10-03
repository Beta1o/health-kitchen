import json,re
J=json.load(open('/mnt/c/WSL/davita/translations/jobs_yfr2.json'))
LAB={'Fruit/veg portions':'Portions de fruits et légumes','For the dressing':'Pour la vinaigrette','For the meatballs':'Pour les boulettes','For the batter':'Pour la pâte à frire','For the toppings':'Pour la garniture','For the satay sauce':'Pour la sauce satay','For the salsa':'Pour la salsa','For the filling':'Pour la farce','To make the eyeballs':'Pour faire les yeux','For the relish':'Pour le condiment','For the cheesy garlic popcorn topping':'Pour l’assaisonnement du pop-corn au fromage et à l’ail','For the chilli lemon popcorn topping':'Pour l’assaisonnement du pop-corn au piment et au citron','For the vegetables':'Pour les légumes','For the side salad':'Pour la salade d’accompagnement','For the sauce':'Pour la sauce','For the pastry':'Pour la pâte','For the topping':'Pour la garniture','For the dip':'Pour la trempette','For the greens':'Pour les légumes verts','For the parsnip crisps':'Pour les chips de panais','For the sesame yoghurt':'Pour le yaourt au sésame'}
def lst(src,txt):
    txt=list(txt)
    out=[]
    for i,(g,t) in enumerate(src):
        if g and re.match(r'Fruit/veg portions per serving: (\d+)$',t) and len(txt)==len(src)-1 and i==len(src)-1:
            n=re.match(r'.*: (\d+)$',t).group(1); out.append([LAB[g],'Portions de fruits et légumes par portion : '+n]); continue
        out.append([LAB[g] if g else None, txt[i]])
    return out
def R(i,title,desc,portions,serving,ings,steps,hints=()):
    s=J[i]
    assert len(ings)==len(s['ingredients']),(i,'ing',len(ings),len(s['ingredients']))
    assert len(steps)==len(s['steps']),(i,'steps')
    h=lst(s['hints'],hints)
    assert len(h)==len(s['hints']),(i,'hints',len(h),len(s['hints']))
    return {"id":s['id'],"translations":{"fr":{"title":title,"description":desc,"portions":portions,"serving_size":serving,
      "ingredients":lst(s['ingredients'],ings),"steps":lst(s['steps'],steps),"hints":h,"food_choices":[]}}}
def save(n,recs):
    json.dump(recs,open(f'/mnt/c/WSL/davita/translations/out_yfr2_part{n}.json','w'),ensure_ascii=False,indent=0)
