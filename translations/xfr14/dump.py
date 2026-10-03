import json,sys
d=json.load(open('jobs_xfr14.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for i in range(a,min(b,len(d))):
    r=d[i]
    print('##',i,r['id'],r['source_lang'],r['translate_to'])
    print('T:',r['title']);print('D:',r['description']);print('P:',r['portions'],'|',r['serving_size'])
    for k in('ingredients','steps','hints'):
        for j,(g,t) in enumerate(r[k]):print(f'{k[0]}{j}',f'[{g}]' if g else '',t)
    print('FC:',json.dumps(r['food_choices'],ensure_ascii=False))
