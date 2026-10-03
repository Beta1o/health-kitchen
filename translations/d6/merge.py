import json
from pathlib import Path
R = Path(__file__).resolve().parent.parent
out = []
for i in range(1, 5):
    out += json.loads((R/f"out_d6_part{i}.json").read_text(encoding="utf-8"))
(R/"out_d6.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(out))
