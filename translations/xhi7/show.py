import json,sys
n=int(sys.argv[1]);d=json.load(open('/mnt/c/WSL/davita/translations/jobs_xhi7.json'))[(n-1)*15:n*15]
for j in d:
    print(j['id'],'|',j['title'],'|',j['description'],'|',j['portions'],'|',j['serving_size'])
    print(' ING',[x[1] for x in j['ingredients']], 'GROUPS' if any(x[0] for x in j['ingredients']+j['steps']+j['hints']) else '')
    print(' ST',[x[1] for x in j['steps']]);print(' HI',[x[1] for x in j['hints']]);print(' FC',j['food_choices'])
