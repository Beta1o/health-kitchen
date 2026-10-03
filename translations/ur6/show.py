import json,sys
d=json.load(open('jobs_ur6.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for j in d[a:b]:
    j.pop('translate_to');j.pop('source_lang')
    print(json.dumps(j,ensure_ascii=False,separators=(',',':')))
