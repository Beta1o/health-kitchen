import json,sys
src=json.load(open('/mnt/c/WSL/davita/translations/jobs_xid4.json'))
def parse(path):
    out=[];cur=None
    for line in open(path,encoding='utf-8'):
        line=line.rstrip('\n')
        if not line.strip(): continue
        if line.startswith('# '):
            cur={'id':int(line[2:]),'T':None,'D':None,'P':None,'S':None,'I':[],'M':[],'H':[],'F':[]};out.append(cur);continue
        k,v=line.split(': ',1) if ': ' in line else (line[:-1],'')
        if k in('T','D','P','S'): cur[k]=None if v=='None' else v
        elif k in('I','M','H'):
            g=None
            if '||' in v: g,v=v.split('||',1)
            cur[k].append([g,v])
        elif k=='F': cur['F']=[x.strip() for x in v.split(' ;; ')] if v else []
        else: raise Exception(line)
    return out
def conv(c):
    return {"id":c['id'],"translations":{"id":{"title":c['T'],"description":c['D'],"portions":c['P'],"serving_size":c['S'],"ingredients":c['I'],"steps":c['M'],"hints":c['H'],"food_choices":c['F']}}}
if __name__=='__main__':
    n=sys.argv[1]
    res=[conv(c) for c in parse(f'/mnt/c/WSL/davita/translations/xid4/p{n}.txt')]
    json.dump(res,open(f'/mnt/c/WSL/davita/translations/out_xid4_part{n}.json','w'),ensure_ascii=False)
    print(len(res))
