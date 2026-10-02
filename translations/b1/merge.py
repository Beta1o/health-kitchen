import json
from pathlib import Path
R=Path('/mnt/c/WSL/davita/translations')
out=[]
for i in range(1,5): out+=json.loads((R/f'out_b1_part{i}.json').read_text(encoding='utf-8'))
(R/'out_b1.json').write_text(json.dumps(out,ensure_ascii=False,indent=1),encoding='utf-8')
print(len(out))
