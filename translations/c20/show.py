import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_c20.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for i,r in enumerate(d[a:b],a):
    print(i,r['id'],r['source_lang'],r['translate_to']);print('T:',r['title']);print('D:',r['description']);print('P:',r['portions'],'| S:',r['serving_size'])
    for k in('ingredients','steps','hints','food_choices'):
        for x in r[k]:print(' ',k[:1],x)
    print()
