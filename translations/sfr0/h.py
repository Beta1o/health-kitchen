import json,sys,importlib.util
from pathlib import Path
H=Path(__file__).resolve().parent
JOBS={j['id']:j for j in json.load(open(H.parent/'jobs_sfr0.json',encoding='utf-8'))}
G={'For the stew':'Pour le ragoût','For the dough':'Pour la pâte','For the rice':'Pour le riz','For the filling':'Pour la farce','For the meat':'Pour la viande','For the chicken':'Pour le poulet','For the batter':'Pour la pâte liquide','For the vegetables':'Pour les légumes','For the topping':'Pour la garniture','For the kebab':'Pour le kebab','For the marag and idam':'Pour le marag et l’idam','Dough':'Pâte','For the broth':'Pour le bouillon','For the jareesh':'Pour le jareesh','For the fish and broth':'Pour le poisson et le bouillon','For the bread':'Pour le pain','To garnish and serve':'Pour garnir et servir','For the kashna':'Pour la kashna','For the beans':'Pour les haricots','Bulool (spiced syrup)':'Bulool (sirop épicé)','For the tahini salad':'Pour la salade de tahini','For the humar (tamarind) sauce':'Pour la sauce humar (tamarin)','For the dakous':'Pour le dakous','For the hunaini':'Pour le hunaini','For the jamriyya':'Pour la jamriyya','For the bottom of the pot':'Pour le fond de la marmite','For the fish':'Pour le poisson','For brushing and topping':'Pour badigeonner et garnir','For the dill yoghurt salad':'Pour la salade de yaourt à l’aneth','To serve':'Pour servir','For the kushna':'Pour la kushna','For the yogurt finish':'Pour la finition au yaourt','For the filling and top':'Pour la farce et le dessus','For the potatoes':'Pour les pommes de terre','For the garlic yoghurt sauce':'Pour la sauce au yaourt et à l’ail','For the top':'Pour le dessus','For cooking and serving':'Pour la cuisson et le service','For the stock':'Pour le bouillon','For the qursan bread':'Pour le pain qursan','For the onion topping':'Pour la garniture d’oignons','For brushing':'Pour badigeonner','For the dagoos (salsa)':'Pour le dagoos (salsa)'}
def build(R):
    out=[]
    for r in R:
        j=JOBS[r['id']]
        def lst(k,key):
            v=r[key]; assert len(v)==len(j[k]),(r['id'],k,len(v),len(j[k]))
            return [[G[g] if g else None,t] for (g,_),t in zip(j[k],v)]
        out.append({'id':r['id'],'translations':{'fr':{'title':r['t'],'description':r['d'],'portions':r['p'],'serving_size':r['s'],'ingredients':lst('ingredients','ing'),'steps':lst('steps','st'),'hints':lst('hints','h'),'food_choices':[]}}})
    return out
if __name__=='__main__':
    # merge parts p*.py in jobs order
    allr={}
    for f in sorted(H.glob('p*.py')):
        sp=importlib.util.spec_from_file_location(f.stem,f);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
        for o in build(m.R): allr[o['id']]=o
    res=[allr[i] for i in JOBS]
    json.dump(res,open(H.parent/'out_sfr0.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
    print(len(res))
