import json
from pathlib import Path
HERE = Path(__file__).resolve().parent.parent
jobs = json.loads((HERE / "jobs_b3.json").read_text(encoding="utf-8"))
out = []
for i in range(1, 5):
    out += json.loads((HERE / f"out_b3_part{i}.json").read_text(encoding="utf-8"))
assert [o["id"] for o in out] == [j["id"] for j in jobs]
(HERE / "out_b3.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print("merged", len(out))
