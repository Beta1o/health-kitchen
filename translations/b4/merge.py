import json, os
B = '/mnt/c/WSL/davita/translations/'
out = []
for i in range(1, 5):
    out += json.load(open(f'{B}out_b4_part{i}.json', encoding='utf-8'))
jobs = json.load(open(B + 'jobs_b4.json'))
assert [o['id'] for o in out] == [j['id'] for j in jobs]
json.dump(out, open(B + 'out_b4.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('merged', len(out))
