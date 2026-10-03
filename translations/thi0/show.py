import json,sys
n=int(sys.argv[1]);jobs=json.load(open('/mnt/c/WSL/davita/translations/jobs_thi0.json'))
f=lambda l:[(g+'::' if g else '')+t for g,t in l]
for j in jobs[(n-1)*7:n*7]:
    print(json.dumps([j['id'],j['title'],j['description'],j['portions'],j['serving_size'],f(j['ingredients']),f(j['steps']),f(j['hints']),j['food_choices']],ensure_ascii=False))
