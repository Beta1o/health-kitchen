import json,re,sys
MAC={
'a':"Renastep एक विशेष चिकित्सीय उद्देश्यों के लिए खाद्य उत्पाद (Food for Special Medical Purposes) है और इसका उपयोग केवल चिकित्सकीय निगरानी में ही करना चाहिए।",
'b':"Renastep 3 वर्ष और उससे अधिक आयु के लिए गुर्दे की बीमारी के आहार प्रबंधन हेतु उपयोग के लिए तैयार (रेडी-टू-यूज़) फ़ीड है।",
'c':"Renastep में दूध और मछली होती है।",
'd':"एलर्जी और अन्य उत्पाद संबंधी जानकारी के लिए लेबल देखें।",
'e':"यह रेसिपी विशेष रूप से गुर्दे की बीमारी के आहार प्रबंधन के लिए तैयार की गई है।",
'f':"हमेशा अपने आहार विशेषज्ञ या डॉक्टर से पूछ लें कि यह रेसिपी आपके लिए उपयुक्त है।",
'enm':"यह रेसिपी विशेष रूप से गुर्दे की बीमारी के आहार प्रबंधन के लिए तैयार की गई है और इसका विश्लेषण Nutrimen डाइटरी विश्लेषण सॉफ़्टवेयर से किया गया है।",
'ent':"यह रेसिपी विशेष रूप से गुर्दे की बीमारी के आहार प्रबंधन के लिए तैयार की गई है और इसका विश्लेषण Nutritics डाइटरी विश्लेषण सॉफ़्टवेयर से किया गया है।",
}
EXTRA={}
exec(open('/mnt/c/WSL/davita/translations/xhi14/macros_extra.py').read()) if __import__('os').path.exists('/mnt/c/WSL/davita/translations/xhi14/macros_extra.py') else None
MAC.update(EXTRA)
def sub(t):
    for _ in range(3): t=re.sub(r'\{(\w+)\}',lambda m:MAC[m.group(1)],t)
    return t
def build(src,dst):
    out=[];cur=None
    for ln in open(src,encoding='utf-8').read().split('\n'):
        if not ln.strip(): continue
        if ln.startswith('# '):
            cur={"id":int(ln[2:]),"translations":{"hi":{"title":None,"description":None,"portions":None,"serving_size":None,"ingredients":[],"steps":[],"hints":[],"food_choices":[]}}}
            out.append(cur);continue
        m=re.match(r'^([TDPVISHF])(?:\[(.*?)\])?: (.*)$',ln)
        assert m,ln
        c,g,t=m.groups();t=sub(t);h=cur["translations"]["hi"]
        if c=='T':h['title']=t
        elif c=='D':h['description']=t
        elif c=='P':h['portions']=t
        elif c=='V':h['serving_size']=t
        elif c=='F':h['food_choices'].append(t)
        else:h[{'I':'ingredients','S':'steps','H':'hints'}[c]].append([g,t])
    json.dump(out,open(dst,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
if __name__=='__main__':
    build(sys.argv[1],sys.argv[2])
