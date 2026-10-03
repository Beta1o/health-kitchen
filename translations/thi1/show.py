import json,sys
n=int(sys.argv[1]);d=json.load(open('/mnt/c/WSL/davita/translations/jobs_thi1.json'))[(n-1)*8:n*8]
for j in d:
    print(json.dumps({k:v for k,v in j.items() if k not in('source_lang','translate_to')},ensure_ascii=False))
