import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_hi2.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for j in d[a:b]:
    print('#',j['id'])
    print('T:',j['title']);print('D:',j['description']);print('P:',j['portions']);print('S:',j['serving_size'])
    for k,c in (('ingredients','I'),('steps','X'),('hints','H')):
        for g,t in j[k]:
            print(f'{c}{"["+g+"]" if g else ""}:',t)
    print('F:',' | '.join(j['food_choices']))
