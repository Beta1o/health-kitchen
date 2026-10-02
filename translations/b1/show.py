import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_b1.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for i,r in enumerate(d[a:b],a):
    print(f"=== #{i} id={r['id']} src={r['source_lang']}")
    for k in ('title','description','portions','serving_size'): print(k,':',r[k])
    for k in ('ingredients','steps','hints'):
        print(k+':')
        for g,t in r[k]: print('  ',g,'|',t)
    print('fc:',r['food_choices'])
