import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_xhi1.json'))
n=int(sys.argv[1]);s=(n-1)*15
for x in d[s:s+15]:
    print(x['id'],'|',x['title'],'|',x['description'],'|',x['portions'],'|',x['serving_size'])
    for k in('ingredients','steps','hints'):
        print(' ',k[:2].upper(),[t for g,t in x[k]])
    print('  FC',x['food_choices'])
