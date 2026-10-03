import json,sys
J={j['id']:j for j in json.load(open('/mnt/c/WSL/davita/translations/jobs_sur0.json'))}
GL={}
def load_gl():
    try: GL.update(json.load(open('/mnt/c/WSL/davita/translations/sur0/gl.json')))
    except Exception: pass
load_gl()
OUT=[]
def R(id,title,desc,portions,serving,ings,steps,hints):
    j=J[id]
    assert len(ings)==len(j['ingredients']),(id,'ing',len(ings),len(j['ingredients']))
    assert len(steps)==len(j['steps']),(id,'steps',len(steps),len(j['steps']))
    assert len(hints)==len(j['hints']),(id,'hints',len(hints),len(j['hints']))
    I=[[None if g is None else GL[g],t] for (g,_),t in zip(j['ingredients'],ings)]
    OUT.append({"id":id,"translations":{"ur":{"title":title,"description":desc,"portions":portions,"serving_size":serving,
      "ingredients":I,"steps":[[None,t] for t in steps],"hints":[[None,t] for t in hints],"food_choices":[]}}})
def save(name):
    json.dump(OUT,open('/mnt/c/WSL/davita/translations/sur0/%s.json'%name,'w'),ensure_ascii=False)
