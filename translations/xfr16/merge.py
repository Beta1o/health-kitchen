import json
o=[]
for i in range(1,8): o+=json.load(open(f"/mnt/c/WSL/davita/translations/out_xfr16_part{i}.json"))
import re
t=json.dumps(o,ensure_ascii=False)
t=re.sub(r"(?<=\d),(?=\d)",".",t)
open("/mnt/c/WSL/davita/translations/out_xfr16.json","w").write(t)
#json.dump(o,open("/mnt/c/WSL/davita/translations/out_xfr16.json","w"),ensure_ascii=False)
