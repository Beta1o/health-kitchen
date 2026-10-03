import json,sys
J=json.load(open('/mnt/c/WSL/davita/translations/jobs_xfr13.json'))
def pairs(orig,txt,labels):
    assert len(orig)==len(txt),(len(orig),len(txt),orig[0])
    o=[]
    for (l,_),t in zip(orig,txt):
        o.append([None if l is None else labels[l],t])
    return o
def mk(i,title,desc,portions,serving,ing,steps,hints,fc,labels={}):
    r=J[i]
    assert (desc is None)==(r['description'] is None)
    assert len(fc)==len(r['food_choices']),(i,'fc')
    return {"id":r['id'],"translations":{"fr":{"title":title,"description":desc,"portions":portions,"serving_size":serving,
      "ingredients":pairs(r['ingredients'],ing,labels),"steps":pairs(r['steps'],steps,labels),
      "hints":pairs(r['hints'],hints,labels),"food_choices":fc}}}
def save(name,items):
    json.dump(items,open('/mnt/c/WSL/davita/translations/out_xfr13_%s.json'%name,'w'),ensure_ascii=False)
PN="À NOTER : cette recette est plus riche en potassium et la taille de la portion est importante. Vérifiez avec votre diététiste-nutritionniste agréé comment cette recette peut être intégrée à votre alimentation."
