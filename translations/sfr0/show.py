import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_sfr0.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for x in d[a:b]:
    print('##',x['id'],'|',x['title'],'|',x['description'],'|',x['portions'],'|',x['serving_size'])
    for k in('ingredients','steps','hints'):
        print(k[:2].upper(),[ (g[:4] if g else '')+'§'+t if g else t for g,t in x[k]] if False else [t for g,t in x[k]])
