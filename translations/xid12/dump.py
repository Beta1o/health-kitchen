import json,sys
a,b=int(sys.argv[1]),int(sys.argv[2])
d=json.load(open('../jobs_xid12.json'))[a:b]
for r in d:
    print('#',r['id'],'|',r['title'],'|',r['description'],'|',r['portions'],'|',r['serving_size'])
    for k in('ingredients','steps','hints'):
        print(' ',k.upper())
        for g,t in r[k]: print('   ',('['+g+'] ') if g else '',t,sep='')
    print('  FC',r['food_choices'])
