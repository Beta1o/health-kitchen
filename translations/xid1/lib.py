import json,re
JOBS={j['id']:j for j in json.load(open('/mnt/c/WSL/davita/translations/jobs_xid1.json'))}
def P(x): return [None,x] if isinstance(x,str) else list(x)
U=[("tablespoons","sendok makan"),("tablespoon","sendok makan"),("teaspoons","sendok teh"),("teaspoon","sendok teh"),("cups","cangkir"),("cup","cangkir"),("ounces","ons"),("ounce","ons"),("pounds","pon"),("pound","pon"),("slices","potong"),("slice","potong"),("pieces","potong"),("piece","potong"),("recipe","resep"),("sandwich","sandwich"),("mug","mug"),("muffins","muffin"),("muffin","muffin")]
def unit(s):
    if s is None: return None
    for a,b in U: s=re.sub(r'\b'+a+r'\b',b,s)
    return s
FC=[("high-calorie","tinggi kalori"),("high calorie","tinggi kalori"),("low-potassium vegetable","sayuran rendah kalium"),("nondairy milk substitute","pengganti susu nonsusu"),("milk substitute","pengganti susu"),("vegetables","sayuran"),("vegetable","sayuran"),("starch","pati"),("fat","lemak"),("meat","daging"),("protein","protein"),("fruit","buah"),("milk","susu"),("dairy","produk susu"),("low potassium","rendah kalium"),("medium potassium","kalium sedang"),("high potassium","kalium tinggi")]
def fc(s):
    if s is None: return None
    if s.lower()=="none": return "tidak ada"
    for a,b in FC: s=s.replace(a,b)
    return s
def R(id,title,desc,ings,steps,hints=(),portions=None,serving=None):
    j=JOBS[id]
    return {"id":id,"translations":{"id":{"title":title,"description":desc,
      "portions":j['portions'] if portions is None else portions,
      "serving_size":unit(j['serving_size']) if serving is None else serving,
      "ingredients":[P(x) for x in ings],"steps":[P(x) for x in steps],"hints":[P(x) for x in hints],
      "food_choices":[fc(x) for x in j['food_choices']]}}}
def save(n,recs):
    json.dump(recs,open(f'/mnt/c/WSL/davita/translations/out_xid1_part{n}.json','w'),ensure_ascii=False,indent=0)
