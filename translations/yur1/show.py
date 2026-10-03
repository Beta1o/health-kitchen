import json,sys
d=json.load(open('jobs_yur1.json'));a,b=int(sys.argv[1]),int(sys.argv[2])
for j in d[a:b]:
    j.pop('source_lang');j.pop('translate_to')
    print(json.dumps(j,ensure_ascii=False,separators=(',',':')))
