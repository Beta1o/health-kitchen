import json,sys,re
J=json.load(open('../jobs_yhi4.json'))
LBL={"Fruit/veg portions":"फल/सब्ज़ी की मात्राएँ","For the topping":"टॉपिंग के लिए","For the filling":"फिलिंग के लिए","For the chilli dipping sauce":"मिर्च वाली डिपिंग सॉस के लिए","For the stew":"स्ट्यू के लिए","For the colcannon":"कोलकैनन के लिए","To serve":"परोसने के लिए","For the marinade":"मैरिनेड के लिए","For the kebabs":"कबाब के लिए","For the dressing":"ड्रेसिंग के लिए","For the croutons":"क्राउटन के लिए","For the salad":"सलाद के लिए","For the berry sauce (optional)":"बेरी सॉस के लिए (वैकल्पिक)","For the lentils":"दाल के लिए","For the salsa":"सालसा के लिए","For the topping":"टॉपिंग के लिए"}
def lab(l):
    if l is None: return None
    if l not in LBL: raise SystemExit("missing label: "+l)
    return LBL[l]
def build(start,R):
    out=[]
    for k,r in enumerate(R):
        j=J[start+k]
        t,d,p,s,ing,st,h,f=r
        def pairs(src,tx,key):
            if len(src)!=len(tx): raise SystemExit(f"{j['id']} {key} count {len(tx)} vs {len(src)}")
            res=[]
            for (l,e),x in zip(src,tx):
                if x=="AUTO":
                    n=re.search(r'(\d+)\s*$',e).group(1)
                    x="प्रति सर्विंग फल/सब्ज़ी की मात्राएँ: "+n
                res.append([lab(l),x])
            return res
        if len(f)!=len(j['food_choices']): raise SystemExit(f"{j['id']} fc")
        out.append({"id":j['id'],"translations":{"hi":{"title":t,"description":d if j['description'] is not None else None,"portions":p,"serving_size":s,"ingredients":pairs(j['ingredients'],ing,'ing'),"steps":pairs(j['steps'],st,'steps'),"hints":pairs(j['hints'],h,'hints'),"food_choices":f}}})
    return out
def save(n,start,R):
    json.dump(build(start,R),open(f'../out_yhi4_part{n}.json','w'),ensure_ascii=False,indent=1)
