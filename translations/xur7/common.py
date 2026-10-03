import json
J={j['id']:j for j in json.load(open('/mnt/c/WSL/davita/translations/jobs_xur7.json'))}
LABELS={
'Renastep note':'Renastep سے متعلق نوٹ','To make the cupcakes':'کپ کیکس بنانے کے لیے','For the frosting':'فراسٹنگ کے لیے',
'To decorate':'سجانے کے لیے','Cupcakes':'کپ کیکس','Decoration':'سجاوٹ','For the wedges':'ویجز کے لیے','For the aiolo':'ایولی کے لیے',
'To make the dough':'آٹا بنانے کے لیے','To make the filling':'فلنگ بنانے کے لیے','Assembly':'تیاری و ترتیب','Creamy Cheese Sauce':'کریمی پنیر کی چٹنی',
'Dough':'آٹا','Sauce':'چٹنی','Filling':'فلنگ','For the base':'بیس کے لیے','For the topping':'اوپر ڈالنے کے لیے'}
C1='Renastep ایک خاص طبی مقاصد کے لیے غذا ہے اور اسے طبی نگرانی میں ہی استعمال کرنا چاہیے۔'
C2='Renastep گردے کی بیماری کے غذائی انتظام کے لیے تیار شدہ، استعمال کے لیے تیار فیڈ ہے جو 3 سال اور اس سے زیادہ عمر کے افراد کے لیے ہے۔ Renastep میں دودھ اور مچھلی شامل ہیں۔ الرجین اور دیگر مصنوعاتی معلومات کے لیے لیبل دیکھیں۔'
C3='یہ ترکیب خاص طور پر گردے کی بیماری کے غذائی انتظام کے لیے بنائی گئی ہے۔'
C4='یہ ترکیب خاص طور پر گردے کی بیماری کے غذائی انتظام کے لیے بنائی گئی ہے اور Nutrimen غذائی تجزیے کے سافٹ ویئر کے ذریعے اس کا تجزیہ کیا گیا ہے۔'
COMMON={
'Renastep is a Food for Special Medical Purposes and must be used under medical supervision.':C1,
'Renastep is a ready to use feed for the dietary management of kidney disease from 3 years of age onwards. Renastep contains milk and fish. Refer to labels for allergen and other product information.':C2,
'This recipe has been specifically designed for the dietary management of kidney disease.':C3,
'This recipe has been specifically designed for the dietary management of kidney disease and has been analysed using Nutrimen dietary analysis software.':C4,
'Renastep is a Food for Special Medical Purposes and must be used under medical supervision. Renastep is a ready to use feed for the dietary management of kidney disease from 3 years of age onwards. Renastep contains milk and fish. Refer to labels for allergen and other product information. This recipe has been specifically designed for the dietary management of kidney disease and has been analysed using Nutrimen dietary analysis software.':' '.join([C1,C2,C4]),
'Always check with your dietitian or doctor that this recipe is suitable for you.':'ہمیشہ اپنے ڈائیٹیشن یا ڈاکٹر سے تصدیق کریں کہ یہ ترکیب آپ کے لیے موزوں ہے۔',
'Renastep is a food for special medical purposes for the dietary management of kidney disease. Suitable from 3 years of age. Must be used under medical supervision. Renastep contains Milk (milk protein) and Fish (Tuna oil). This recipe has been specifically designed for the dietary management of kidney disease and has been analysed using Nutritics dietary analysis software. Refer to labels for allergen and other product information.':'Renastep گردے کی بیماری کے غذائی انتظام کے لیے خاص طبی مقاصد کی غذا ہے۔ 3 سال اور اس سے زیادہ عمر کے لیے موزوں ہے۔ اسے طبی نگرانی میں ہی استعمال کرنا چاہیے۔ Renastep میں دودھ (دودھ کا پروٹین) اور مچھلی (ٹونا آئل) شامل ہیں۔ یہ ترکیب خاص طور پر گردے کی بیماری کے غذائی انتظام کے لیے بنائی گئی ہے اور Nutritics غذائی تجزیے کے سافٹ ویئر کے ذریعے اس کا تجزیہ کیا گیا ہے۔ الرجین اور دیگر مصنوعاتی معلومات کے لیے لیبل دیکھیں۔',
'Renastep is a food for special medical purposes and must be used under medical supervision. Renastep is for the dietary management of kidney disease and is suitable from 3 years of age onwards.':'Renastep خاص طبی مقاصد کے لیے غذا ہے اور اسے طبی نگرانی میں ہی استعمال کرنا چاہیے۔ Renastep گردے کی بیماری کے غذائی انتظام کے لیے ہے اور 3 سال اور اس سے زیادہ عمر کے افراد کے لیے موزوں ہے۔',
'Renastep contains Milk (milk protein) and Fish (Tuna Oils). This recipe has been specifically designed for the dietary management of kidney disease and has been analysed using Nutrimen dietary analysis software.':'Renastep میں دودھ (دودھ کا پروٹین) اور مچھلی (ٹونا آئل) شامل ہیں۔ یہ ترکیب خاص طور پر گردے کی بیماری کے غذائی انتظام کے لیے بنائی گئی ہے اور Nutrimen غذائی تجزیے کے سافٹ ویئر کے ذریعے اس کا تجزیہ کیا گیا ہے۔',
'Refer to labels for allergen and other product information':'الرجین اور دیگر مصنوعاتی معلومات کے لیے لیبل دیکھیں۔',
'This recipe has been specifically designed for the dietary management of kidney disease and has been analysed using Nutritics dietary analysis software. Refer to labels for allergen and other product information.':'یہ ترکیب خاص طور پر گردے کی بیماری کے غذائی انتظام کے لیے بنائی گئی ہے اور Nutritics غذائی تجزیے کے سافٹ ویئر کے ذریعے اس کا تجزیہ کیا گیا ہے۔ الرجین اور دیگر مصنوعاتی معلومات کے لیے لیبل دیکھیں۔',
'Serve and enjoy!':'پیش کریں اور لطف اٹھائیں!',
}
def conv(src,texts,kind):
    # texts: list of str or '=' (use COMMON)
    assert len(src)==len(texts),(kind,len(src),len(texts))
    out=[]
    for (g,t),u in zip(src,texts):
        if u=='=': u=COMMON[t]
        out.append([LABELS[g] if g else None,u])
    return out
def build(n,entries):
    res=[]
    for (i,title,desc,por,serv,ings,steps,hints) in entries:
        j=J[i]
        assert (j['description'] is None)==(desc is None),i
        assert (j['portions'] is None)==(por is None),i
        assert (j['serving_size'] is None)==(serv is None),i
        res.append({'id':i,'translations':{'ur':{'title':title,'description':desc,'portions':por,'serving_size':serv,
          'ingredients':conv(j['ingredients'],ings,'ing'),'steps':conv(j['steps'],steps,'steps'),
          'hints':conv(j['hints'],hints,'hints'),'food_choices':[]}}})
    json.dump(res,open(f'/mnt/c/WSL/davita/translations/out_xur7_part{n}.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
    print('part',n,len(res))
