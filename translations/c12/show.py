import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_c12.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for j in d[a:b]:
    print(j['id'],j['source_lang'],j['translate_to'])
    for k in ('title','description','portions','serving_size'): print(' ',k,'=',json.dumps(j[k],ensure_ascii=False))
    for k in ('ingredients','steps','hints','food_choices'):
        print(' ',k, json.dumps(j[k],ensure_ascii=False))
