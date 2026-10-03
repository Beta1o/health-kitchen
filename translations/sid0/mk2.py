import json
J=json.load(open('/mnt/c/WSL/davita/translations/jobs_sid0.json'))
L={"For the dough":"Untuk adonan","For brushing and topping":"Untuk olesan dan taburan","For the filling":"Untuk isian","For the meat":"Untuk daging","For the rice":"Untuk nasi","For the chicken":"Untuk ayam","For the vegetables":"Untuk sayuran","For the topping":"Untuk taburan","For the kebab":"Untuk kebab","For the tahini salad":"Untuk salad tahini","For the top":"Untuk bagian atas","For the dill yoghurt salad":"Untuk salad yogurt dill","For the bread":"Untuk roti","For the marag and idam":"Untuk marag dan idam","To serve":"Untuk penyajian","For the stew":"Untuk semur","For the qursan bread":"Untuk roti qursan","For the onion topping":"Untuk taburan bawang","For the batter":"Untuk adonan cair","For cooking and serving":"Untuk memasak dan penyajian","For the jareesh":"Untuk jareesh","For the kushna":"Untuk kushna","For the hunaini":"Untuk hunaini","For the stock":"Untuk kaldu","For the yogurt finish":"Untuk sentuhan akhir yogurt","To garnish and serve":"Untuk hiasan dan penyajian","Dough":"Adonan","Bulool (spiced syrup)":"Bulool (sirop berempah)","For the jamriyya":"Untuk jamriyya","For the broth":"Untuk kaldu","For the bottom of the pot":"Untuk dasar panci","For brushing":"Untuk olesan","For the fish and broth":"Untuk ikan dan kaldu","For the filling and top":"Untuk isian dan taburan","For the potatoes":"Untuk kentang","For the humar (tamarind) sauce":"Untuk saus humar (asam jawa)","For the garlic yoghurt sauce":"Untuk saus yogurt bawang putih","For the kashna":"Untuk kashna","For the beans":"Untuk kacang","For the dakous":"Untuk dakous","For the dagoos (salsa)":"Untuk dagoos (salsa)","For the fish":"Untuk ikan"}
def build(start,recs,out):
    res=[]
    for n,(t,d,p,s,ing,st,h) in enumerate(recs):
        j=J[start+n]
        def pr(k,L2):
            src=j[k]
            assert len(src)==len(L2),(j['id'],k,len(src),len(L2))
            return [[(L[g] if g else None),x] for (g,_),x in zip(src,L2)]
        res.append({"id":j['id'],"translations":{"id":{"title":t,"description":d,"portions":p,"serving_size":s,"ingredients":pr('ingredients',ing),"steps":pr('steps',st),"hints":pr('hints',h),"food_choices":[]}}})
    json.dump(res,open(out,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
