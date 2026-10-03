import json,sys,glob
# usage: build.py N  -> reads p{N}.json (compact) writes ../out_yhi0_part{N}.json
n=sys.argv[1]
src=json.load(open(f'p{n}.json',encoding='utf-8'))
def pairs(l):
    return [[None,x] if isinstance(x,str) else list(x) for x in l]
out=[]
for r in src:
    out.append({"id":r["id"],"translations":{"hi":{"title":r["title"],"description":r["description"],"portions":r["portions"],"serving_size":r["serving_size"],"ingredients":pairs(r["ing"]),"steps":pairs(r["steps"]),"hints":pairs(r["hints"]),"food_choices":r["fc"]}}})
json.dump(out,open(f'../out_yhi0_part{n}.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
