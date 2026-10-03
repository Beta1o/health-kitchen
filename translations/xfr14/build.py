import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_xfr14.json'))
def build(mod,start):
    ns={};exec(open('/mnt/c/WSL/davita/translations/xfr14/common.py',encoding='utf-8').read(),ns);exec(open(mod,encoding='utf-8').read(),ns)
    ns['G']={**ns['G0'],**ns['G']}
    R=ns['R'];G=ns['G'];out=[]
    for k,x in enumerate(R):
        r=d[start+k]
        def pairs(key,tx):
            src=r[key]
            assert len(src)==len(tx),(r['id'],key,len(src),len(tx))
            return [[ (G[g] if g is not None else None),t] for (g,_),t in zip(src,tx)]
        assert len(r['food_choices'])==len(x.get('fc',[])),(r['id'],'fc')
        out.append({"id":r['id'],"translations":{"fr":{"title":x['t'],"description":x['d'],"portions":x['p'],"serving_size":x.get('s'),
          "ingredients":pairs('ingredients',x['i']),"steps":pairs('steps',x['st']),"hints":pairs('hints',x.get('h',[])),"food_choices":x.get('fc',[])}}})
    return out
if __name__=='__main__':
    n=int(sys.argv[1]);start=(n-1)*15
    o=build(f'/mnt/c/WSL/davita/translations/xfr14/part{n}.py',start)
    json.dump(o,open(f'/mnt/c/WSL/davita/translations/out_xfr14_part{n}.json','w'),ensure_ascii=False,indent=1)
    print(len(o))
