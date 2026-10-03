import json,sys
n=int(sys.argv[1]);S=10
for j in json.load(open('/mnt/c/WSL/davita/translations/jobs_thi2.json'))[(n-1)*S:n*S]:
    print('###',j['id'],'|',j['title']);print('D:',j['description']);print('P:',j['portions'],'| S:',j['serving_size'])
    for k in('ingredients','steps','hints'):
        print(k[0].upper()+':');
        for g,t in j[k]:print('  ',(g+'::') if g else '',t,sep='')
    print('FC:',j['food_choices'])
