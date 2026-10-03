import json,sys
d=json.load(open('../jobs_xhi8.json'))
n=int(sys.argv[1]);
for r in d[(n-1)*15:n*15]:
    print('###',r['id'])
    print('T:',r['title']);print('D:',r['description']);print('P:',r['portions']);print('S:',r['serving_size'])
    for k,c in(('ingredients','I'),('steps','W'),('hints','H')):
        for a,b in r[k] or []: print(c+':',b)
    for f in r['food_choices']: print('F:',f)
