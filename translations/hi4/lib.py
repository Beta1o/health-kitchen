import json,sys
J=json.load(open('/mnt/c/WSL/davita/translations/jobs_hi4.json'))
def flat(j):
    s=[]
    for k in ('title','description','portions','serving_size'):
        if j[k] is not None: s.append(j[k])
    for k in ('ingredients','steps','hints'):
        for g,t in j[k]:
            if g is not None: s.append(g)
            s.append(t)
    s+=j['food_choices']
    return s
def part(n,size=20): return J[n*size:(n+1)*size]
if __name__=='__main__':
    n=int(sys.argv[1])
    for j in part(n):
        print('##',j['id'])
        for i,t in enumerate(flat(j)): print(i,t)
