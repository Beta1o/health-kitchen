import json,glob,os
os.chdir('/mnt/c/WSL/davita/translations')
C={}
for jf in glob.glob('jobs_*fr*.json'):
    of='out_'+jf[5:]
    if not os.path.exists(of): continue
    try:
        J={r['id']:r for r in json.load(open(jf))}
        for o in json.load(open(of)):
            f=o['translations'].get('fr'); r=J.get(o['id'])
            if not f or not r: continue
            for k in ('hints','steps','ingredients'):
                if len(f[k])!=len(r[k]): continue
                for (l1,t1),(l2,t2) in zip(r[k],f[k]):
                    if k=='hints' and t1 and t2: C[t1]=t2
                    if l1 and l2: C[l1]=l2
    except Exception as e: print(jf,e)
json.dump(C,open('/mnt/c/WSL/davita/translations/xfr13/cache.json','w'),ensure_ascii=False)
print(len(C))
