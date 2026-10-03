import json,sys
d=json.load(open('jobs_xhi13.json'))
seen={};order=[]
def strs(r):
    for k in ['title','description','portions','serving_size']:
        if r[k]: yield r[k]
    for k in ['ingredients','steps','hints']:
        for g,t in r[k]:
            if g: yield g
            yield t
    yield from r['food_choices']
rec_new=[]
for i,r in enumerate(d):
    new=[]
    for s in strs(r):
        if s not in seen:
            seen[s]=len(order);order.append(s);new.append(seen[s])
    rec_new.append(new)
json.dump(order,open('xhi13/uniq.json','w'))
if __name__=='__main__':
    a,b=int(sys.argv[1]),int(sys.argv[2])
    for i in range(a,b):
        for n in rec_new[i]:
            print(n,order[n].replace('\n','\\n'))
