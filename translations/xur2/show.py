import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_xur2.json'))
n=int(sys.argv[1])
for j in d[(n-1)*15:n*15]:
    print('##',j['id'],'|',j['title']);print('D:',j['description']);print('P:',j['portions'],'| S:',j['serving_size'])
    for k in('ingredients','steps','hints'):
        print(k[0].upper()+':',json.dumps([x[1] for x in j[k] or []],ensure_ascii=False))
    print('F:',json.dumps(j['food_choices'],ensure_ascii=False))
