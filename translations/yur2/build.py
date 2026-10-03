import json,sys
JOBS=json.load(open('/mnt/c/WSL/davita/translations/jobs_yur2.json'))
LABELS={None:None,'Fruit/veg portions':'پھل/سبزیوں کے حصے','For the meatballs':'میٹ بالز کے لیے','To make the eyeballs':'آنکھیں بنانے کے لیے','For the parsnip crisps':'پارسنپ کرسپس کے لیے','For the relish':'ریلش کے لیے','For the sesame yoghurt':'تل والے دہی کے لیے','For the cheesy garlic popcorn topping':'پنیر اور لہسن والے پاپ کارن کی ٹاپنگ کے لیے','For the chilli lemon popcorn topping':'مرچ اور لیموں والے پاپ کارن کی ٹاپنگ کے لیے','For the sauce':'چٹنی کے لیے','For the dressing':'ڈریسنگ کے لیے','For the greens':'ساگ/پتوں والی سبزیوں کے لیے','For the pastry':'پیسٹری کے لیے','For the filling':'بھرائی کے لیے','For the toppings':'اوپر سجانے کے لیے','For the topping':'اوپر سجانے کے لیے','For the vegetables':'سبزیوں کے لیے','For the dip':'ڈپ کے لیے','For the batter':'بیٹر (گھول) کے لیے','For the satay sauce':'ساتے چٹنی کے لیے','For the salsa':'سالسا کے لیے','For the side salad':'ساتھ کے سلاد کے لیے'}
def build(start,items,part):
    out=[]
    assert start+len(items)<=len(JOBS)
    for off,it in enumerate(items):
        j=JOBS[start+off]
        t,d,p,s,ing,st,h,fc=it
        def pair(key,tx):
            src=j[key] or []
            assert len(src)==len(tx),(j['id'],key,len(src),len(tx))
            return [[LABELS[g[0]],x] for g,x in zip(src,tx)]
        assert len(fc)==len(j['food_choices']),(j['id'],'fc')
        out.append({"id":j['id'],"translations":{"ur":{"title":t,"description":d if j['description'] is not None else None,
          "portions":p if j['portions'] is not None else None,"serving_size":s if j['serving_size'] is not None else None,
          "ingredients":pair('ingredients',ing),"steps":pair('steps',st),"hints":pair('hints',h),"food_choices":fc}}})
    json.dump(out,open(f'/mnt/c/WSL/davita/translations/out_yur2_part{part}.json','w'),ensure_ascii=False,indent=1)
