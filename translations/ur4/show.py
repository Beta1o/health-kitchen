import json,sys
d=json.load(open('jobs_ur4.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for i,j in enumerate(d[a:b],a):
    print('#',i,j['id'],'|',j['title'],'|',j['portions'],'|',j['serving_size'])
    print('D:',j['description'])
    for k in('ingredients','steps','hints'):
        print(k[0].upper()+':',[ (g,t) if g else t for g,t in j[k]])
    print('F:',j['food_choices'])
