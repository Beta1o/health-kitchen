import json,sys
j=json.load(open('/mnt/c/WSL/davita/translations/jobs_tid1.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for r in j[a:b]:
    print("###",r['id'],"|",r['title'],"|",r['description'],"|",r['portions'],"|",r['serving_size'])
    for k in('ingredients','steps','hints'):
        print(k[:3].upper(),json.dumps(r[k],ensure_ascii=False))
    print("FC",json.dumps(r['food_choices'],ensure_ascii=False))
