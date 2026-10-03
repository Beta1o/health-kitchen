import json
d=json.load(open('in_0.json'))
P='Pizza & Sandwiches';S='Sauces & Seasonings';BR='Breakfast & Brunch';SO='Soups & Stews';SA='Salads & Dressings'
ch={14:P,17:SA,30:'Breads',42:SA,45:BR,59:S,65:BR,81:S,88:P,101:P,134:S,137:S,142:S,146:P,83:P,158:P,249:BR,250:S,253:P,262:S,314:P,328:'Beef, Lamb & Pork',29:SO,37:SO,54:P}
ch.update({336:BR,338:'Appetizers & Snacks',344:'Vegetables',346:S,347:S,364:P,366:P,376:'Fish & Seafood',409:'Vegetables',98:'Desserts',84:'Desserts',131:'Desserts',424:SO,440:'Desserts',479:BR,497:'Desserts',508:SA,515:S,538:P,544:'Vegetables',545:'Chicken & Turkey',559:'Breads',562:'Chicken & Turkey',573:'Vegetables',598:'Desserts',605:S,626:S,641:'Vegetables',649:'Vegetables',652:S})
cats={"Appetizers & Snacks","Beef, Lamb & Pork","Beverages","Breads","Breakfast & Brunch","Chicken & Turkey","Desserts","Fish & Seafood","Pasta, Rice & Grains","Pizza & Sandwiches","Salads & Dressings","Sauces & Seasonings","Soups & Stews","Vegetables"}
out={str(d[i]['id']):c for i,c in ch.items() if c!=d[i]['category']}
assert all(v in cats for v in out.values())
json.dump(out,open('out_0.json','w'),ensure_ascii=False,indent=1)
print(len(d),len(out))
for i in [14,30,59,545,562]:print(d[i]['title'],'->',ch[i])
