import json,sys
def G(label, items): return [(label,t) for t in items]
def _p(x): return list(x) if isinstance(x,(tuple,list)) else [None,x]
def R(id,title,desc,portions,serving,ing,steps,hints,fc):
    return {"id":id,"translations":{"ur":{"title":title,"description":desc,"portions":portions,"serving_size":serving,
      "ingredients":[_p(x) for x in ing],"steps":[_p(x) for x in steps],"hints":[_p(x) for x in hints],"food_choices":list(fc)}}}
FV="پھل/سبزیوں کے حصے"
def FVH(n): return (FV, f"فی سرونگ پھل/سبزیوں کے حصے: {n}")
def save(n,recs):
    json.dump(recs,open(f"/mnt/c/WSL/davita/translations/out_sur1_part{n}.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
    print(n,len(recs))
FRZ="منجمد کرنے کی ہدایات: پکانے کے بعد منجمد کرنے کے لیے موزوں ہے۔ فریج یا مائیکرو ویو میں پگھلائیں اور اتنا گرم کریں کہ اندر تک بھاپ نکلنے لگے۔"
WC="کیا تبدیل کیا گیا: "
KT="گردے کے لیے مشورہ: "
DT="ذیابیطس کے لیے مشورہ: "
SF="موزوں برائے: "
RF="حوالہ جات: "
