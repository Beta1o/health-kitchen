import json,sys,importlib.util
d={r['id']:r for r in json.load(open('/mnt/c/WSL/davita/translations/jobs_yfr3.json'))}
jobs=json.load(open('/mnt/c/WSL/davita/translations/jobs_yfr3.json'))
GM={"Fruit/veg portions":"Portions de fruits/légumes","For the filling":"Pour la garniture","For the chana chaat":"Pour le chana chaat","For the marinade":"Pour la marinade","For the salad":"Pour la salade","For the sponge":"Pour le biscuit","For the dressing":"Pour la vinaigrette","For the mint chutney":"Pour le chutney à la menthe","For the tomato salad":"Pour la salade de tomates","For the dough":"Pour la pâte","For the custard":"Pour la crème anglaise","For the topping":"Pour la garniture du dessus","For the salsa":"Pour la salsa","To garnish":"Pour décorer","For the jelly":"Pour la gelée","Toppings":"Garnitures","To serve":"Pour servir"}
def build(part,start):
    spec=importlib.util.spec_from_file_location('p',f'/mnt/c/WSL/davita/translations/yfr3/{part}.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    GM.update(getattr(m,'GM',{}))
    out=[]
    for k,t in enumerate(m.R):
        j=jobs[start+k]
        title,desc,ing,st,hi,fc=t[:6]
        port=t[6] if len(t)>6 else j['portions']; ss=t[7] if len(t)>7 else j['serving_size']
        def pair(src,tr):
            assert len(src)==len(tr),(j['id'],len(src),len(tr))
            return [[GM[g] if g else None,x] for (g,_),x in zip(src,tr)]
        assert len(j['food_choices'])==len(fc),j['id']
        out.append({"id":j['id'],"translations":{"fr":{"title":title,"description":desc if j['description'] is not None else None,"portions":port,"serving_size":ss,
          "ingredients":pair(j['ingredients'],ing),"steps":pair(j['steps'],st),"hints":pair(j['hints'],hi),"food_choices":fc}}})
    json.dump(out,open(f'/mnt/c/WSL/davita/translations/out_yfr3_{part}.json','w'),ensure_ascii=False)
build(sys.argv[1],int(sys.argv[2]))
