import json
S=11
GROUPS={'For the kebab':'कबाब के लिए','For cooking and serving':'पकाने और परोसने के लिए','For the broth':'शोरबे के लिए','For the qursan bread':'कुर्सान ब्रेड के लिए','For the dill yoghurt salad':'सोया (डिल) दही सलाद के लिए','For the vegetables':'सब्जियों के लिए','For the hunaini':'हुनैनी के लिए','For the dagoos (salsa)':'दगूस (सालसा) के लिए','For the kushna':'कुशना के लिए','For the jamriyya':'जमरिय्या के लिए','Bulool (spiced syrup)':'बलूल (मसालेदार शरबत)','For the kashna':'कशना के लिए','For the stew':'स्ट्यू के लिए','For the jareesh':'जरीश के लिए','For the fish':'मछली के लिए','For the garlic yoghurt sauce':'लहसुन-दही की चटनी के लिए','For the onion topping':'प्याज की टॉपिंग के लिए','For brushing and topping':'ब्रश करने और ऊपर डालने के लिए','For the top':'ऊपर के लिए','For the bottom of the pot':'बर्तन की तली के लिए','For the dakous':'दकूस के लिए','For the stock':'स्टॉक के लिए','For the marag and idam':'मरग और इदाम के लिए','For the batter':'घोल के लिए','For the tahini salad':'तहीनी सलाद के लिए','For brushing':'ब्रश करने के लिए','For the beans':'फलियों के लिए','For the rice':'चावल के लिए','For the fish and broth':'मछली और शोरबे के लिए','To serve':'परोसने के लिए','For the humar (tamarind) sauce':'हुमर (इमली) सॉस के लिए','For the meat':'मांस के लिए','To garnish and serve':'सजाने और परोसने के लिए','For the bread':'ब्रेड के लिए','For the potatoes':'आलू के लिए','For the topping':'टॉपिंग के लिए','For the yogurt finish':'दही की अंतिम परत के लिए','For the filling and top':'भरावन और ऊपर के लिए','For the chicken':'चिकन के लिए','For the dough':'आटे के लिए','Dough':'आटा','For the filling':'भरावन के लिए'}
def P(n,recs):
    jobs=json.load(open('/mnt/c/WSL/davita/translations/jobs_shi0.json'))
    s=(n-1)*S; exp=jobs[s:s+S]
    assert len(recs)==len(exp),(len(recs),len(exp))
    out=[]
    for j,r in zip(exp,recs):
        assert r[0]==j['id'],(r[0],j['id'])
        def pairs(key,items):
            o=j[key]; assert len(o)==len(items),(j['id'],key,len(o),len(items))
            res=[]
            for oo,t in zip(o,items):
                g=GROUPS[oo[0]] if oo[0] is not None else None
                res.append([g,t])
            return res
        _,title,desc,por,serv,ing,st,hi,fc=r
        assert len(j['food_choices'])==len(fc),(j['id'],'fc')
        out.append({"id":j['id'],"translations":{"hi":{"title":title,"description":desc,"portions":por,"serving_size":serv,"ingredients":pairs('ingredients',ing),"steps":pairs('steps',st),"hints":pairs('hints',hi),"food_choices":fc}}})
    json.dump(out,open(f'/mnt/c/WSL/davita/translations/shi0/part{n}.json','w'),ensure_ascii=False,indent=0)
    print('ok',n,len(out))
