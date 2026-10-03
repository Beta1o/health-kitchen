import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_xhi14.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for j in d[a:b]:
    print('#',j['id'])
    for k,c in (('title','T'),('description','D'),('portions','P'),('serving_size','V')):
        if j[k] is not None: print(f'{c}: {j[k]}')
    for k,c in (('ingredients','I'),('steps','S'),('hints','H')):
        for g,t in j[k] or []:
            print(f'{c}[{g}]: {t}' if g else f'{c}: {t}')
    for f in j['food_choices']: print('F:',f)
