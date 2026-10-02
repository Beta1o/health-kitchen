import json,re
P='/mnt/c/WSL/davita/translations/out_a1.json'
out=json.load(open(P,encoding='utf-8'))
def walk(id_, f):
    for o in out:
        if id_ is None or o['id']==id_:
            d=o['translations']['ar']
            for k in ('title','description','portions','serving_size'):
                if d[k]: d[k]=f(d[k],k)
            for k in ('ingredients','steps','hints'):
                d[k]=[[g,f(t,k)] for g,t in d[k]]
rep_all=[('1/2 حبة كرز','½ حبة كرز'),('½ حبة كرز مسكّر لتكون','½ حبة كرز مسكّر لتكون'),
 ('واحدة (1)','واحدة')]
salt={3817521:[('صلصة صويا قليلة الملح','صلصة صويا مخفّضة الملح')],
 5122504:[('صلصة صويا قليلة الملح','صلصة صويا مخفّضة الملح')],
 5239891:[('لحم بقري قليل الملح','لحم بقري مخفّض الملح')],
 5219021:[('صلصة الصويا قليلة الملح','صلصة الصويا مخفّضة الملح')]}
def g(t,k):
    for a,b in rep_all: t=t.replace(a,b)
    if k in ('steps','hints'):
        for a,b in [('حتى 2 يوم','حتى يومين'),('حتى 2 شهر','حتى شهرين'),('في 2 طبق','في طبقين'),('إلى 2 حصة','إلى حصتين'),
                    ('لمدة 2 دقيقة','لمدة دقيقتين'),('2 دقيقة أخرى','دقيقتين أخريين'),('على شكل 2 قرن','على شكل قرنين'),('بين 2 ورقة زبدة','بين ورقتي زبدة'),
                    ('أضف 2 عين','أضف عينين'),('قشّر 2 جزرة','قشّر جزرتين'),('قشّر 2 حبة كمثرى','قشّر حبتي كمثرى'),('و2 ملعقة كبيرة من الماء','وملعقتين كبيرتين من الماء'),
                    ('مع إضافة 2 ملعقة كبيرة من التتبيلة','مع إضافة ملعقتين كبيرتين من التتبيلة'),('أضف 2 ملعقة كبيرة من التتبيلة','أضف ملعقتين كبيرتين من التتبيلة'),('في 2 ملعقة كبيرة من الزيت','في ملعقتين كبيرتين من الزيت'),('أضف 2 فلفل حار','أضف حبتين من فلفل')]:
            t=t.replace(a,b)
    return t
walk(None,g)
for i,rs in salt.items():
    def h(t,k,rs=rs):
        for a,b in rs: t=t.replace(a,b)
        return t
    walk(i,h)
json.dump(out,open(P,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
# scans
for o in out:
    d=o['translations']['ar']
    texts=[d['title'],d['description'] or '']+[t for k in ('ingredients','steps','hints') for _,t in d[k]]+[g for k in ('ingredients','steps','hints') for g,_ in d[k] if g]
    for t in texts:
        w=set(re.findall(r'[A-Za-z]{3,}',t))-{'Renastep','Vitabite','Quorn','Nutritics','Nutrimen','Kidney','Friendly','Cookbook'}
        if w: print(o['id'],w)
        if re.search('[کیۀ]',t): print(o['id'],'persian',t[:60])
        if re.search(r'\b2 (يوم|شهر|طبق|حصة|دقيقة|قرن|ورقة)',t): print(o['id'],'dual?',t[:80])
