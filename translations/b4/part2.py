import sys; sys.path.insert(0, '/mnt/c/WSL/davita/translations/b4')
from common import rec, dump, N

R = []

# 11 Grilled Pineapple
GF_ES = "El verano es un excelente momento para probar nuevas formas de preparar la fruta. Considere asar fruta a la parrilla para crear sabores y texturas únicos. Lo mejor es que puede asar casi cualquier cosa. Elija frutas más bajas en potasio, como piña, peras, manzanas, limón amarillo, limón verde, ciruelas y sandía. Sin importar qué fruta elija, hay algunas técnicas básicas para crear el complemento perfecto de una comida a la parrilla. • Elija fruta madura, pero no demasiado. El calor debilita la estructura de la fruta, por lo que la fruta demasiado madura probablemente se deshará al asarla. • Corte la fruta en trozos grandes para evitar que caiga entre las rejillas de la parrilla. • Antes de asarla, barnice ligeramente la fruta con un aceite que resista altas temperaturas. Algunas buenas opciones son el aceite de canola y el de cártamo. El aceite de oliva y la mantequilla también son una opción cuando se usan temperaturas más bajas. • Una vez que coloque la fruta en la parrilla, no la mueva. Debe quedarse sobre la parrilla caliente unos minutos antes de revisar si ya tiene las marcas de la parrilla, aproximadamente 2 a 3 minutos. La superficie de la fruta necesita tiempo para sellarse y así no se pegará a la parrilla. Sea creativo al planificar sus comidas. La fruta asada es deliciosa tanto con platillos salados como dulces, así que disfrute experimentando con distintas combinaciones."
GF_AR = "الصيف وقت رائع لتجربة طرق جديدة لتحضير الفاكهة. جرّب شوي الفاكهة لابتكار نكهات وقوامات مميزة. والأجمل أنه يمكنك شوي أي شيء تقريبًا. اختر الفواكه الأقل في البوتاسيوم مثل الأناناس والكمثرى والتفاح والليمون والليمون الأخضر والبرقوق والبطيخ. وأيًا كانت الفاكهة التي تختارها، هناك بعض الأساليب الأساسية اللازمة لتحضير الطبق المثالي المرافق لوجبة مشوية. • اختر فاكهة ناضجة، لكن ليست مفرطة النضج. فالحرارة تُضعف بنية الفاكهة، لذا فمن المرجح أن تتفكك الفاكهة المفرطة النضج أثناء الشوي. • قطّع الفاكهة إلى قطع كبيرة لمنعها من السقوط بين قضبان الشواية. • قبل الشوي، ادهن الفاكهة قليلًا بزيت يتحمل درجات الحرارة العالية، ومن الخيارات الجيدة زيت الكانولا وزيت العصفر. ويمكن أيضًا استخدام زيت الزيتون والزبدة عند الشوي على درجات حرارة أقل. • بعد وضع الفاكهة على الشواية، لا تحرّكها. فهي تحتاج إلى البقاء على الشواية الساخنة بضع دقائق، حوالي 2 إلى 3 دقائق، قبل التحقق من ظهور علامات الشواء. ويحتاج سطح الفاكهة إلى وقت ليتحمّر حتى لا يلتصق بالشواية. كن مبدعًا في تخطيط وجباتك، فالفاكهة المشوية لذيذة مع الأطباق المالحة والحلوة على حد سواء، لذا استمتع بتجربة مجموعة متنوعة من التوليفات."
R.append(rec(4882636, {
 "title": "Piña a la parrilla", "description": N, "portions": "4", "serving_size": "¼ de la receta",
 "ingredients": ["1 cucharada de mantequilla derretida", "1/2 cucharadita de extracto artificial de coco*",
   "4 rodajas de piña (de preferencia fruta fresca)", "1/2 taza de frambuesas, frescas o congeladas"],
 "steps": ["Precaliente la parrilla a fuego medio-alto.",
   "En un tazón pequeño, mezcle la mantequilla derretida con el extracto de coco.",
   "Con una brocha, barnice cada rodaja de piña por ambos lados con la mantequilla saborizada.",
   "Baje el fuego de la parrilla a medio. Coloque las rodajas directamente sobre la parrilla y cocine 2 minutos por cada lado.",
   "Sirva con las frambuesas y ¡disfrute!"],
 "hints": ["* El coco es muy alto en potasio y fósforo, pero para conservar su sabor puede usar extracto con moderación, como lo hicimos en esta receta.",
   "En lugar de la parrilla, puede usar una sartén con rayas (plancha acanalada) y preparar la receta en la estufa.",
   ("Descubra la fruta a la parrilla", GF_ES)],
 "food_choices": ["1 fruta baja en potasio", "½ grasa"]},
{
 "title": "أناناس مشوي", "description": N, "portions": "4", "serving_size": "¼ الوصفة",
 "ingredients": ["1 ملعقة كبيرة زبدة مذابة", "½ ملعقة صغيرة خلاصة جوز الهند الصناعية*",
   "4 شريحة أناناس (يُفضّل أن تكون طازجة)", "½ كوب توت العليق (فرامبواز)، طازج أو مجمد"],
 "steps": ["سخّن الشواية مسبقًا على حرارة متوسطة إلى عالية.",
   "في وعاء صغير، اخلط الزبدة المذابة مع خلاصة جوز الهند.",
   "باستخدام فرشاة، ادهن كل شريحة أناناس من الجانبين بالزبدة المنكّهة.",
   "اخفض حرارة الشواية إلى متوسطة. ضع الشرائح مباشرة على الشواية واشوِها لمدة 2 دقيقة لكل جانب.",
   "قدّمها مع توت العليق واستمتع!"],
 "hints": ["* جوز الهند مرتفع جدًا في البوتاسيوم والفوسفور، لكن للحصول على نكهته يمكنك استخدام خلاصته باعتدال كما فعلنا في هذه الوصفة.",
   "بدلًا من الشواية، يمكنك استخدام مقلاة شواء مخططة وتحضير الوصفة على الموقد.",
   ("اكتشف الفاكهة المشوية", GF_AR)],
 "food_choices": ["1 فاكهة منخفضة البوتاسيوم", "½ دهون"]}))

# 12 Almond Cake
TR_ES = """A todos nos gusta darnos un gusto. Cuando se eligen con cuidado, los dulces ocasionales pueden formar parte de una alimentación saludable. Por desgracia, muchos de los dulces que solemos elegir son alimentos muy procesados, como pasteles empaquetados, donas, magdalenas, galletas y barras de postre. Estos alimentos contienen ingredientes refinados o procesados y, por lo general, tienen mayores cantidades de grasa saturada, azúcar añadida, sodio y aditivos de tipo fosfato, con pocos o ningún alimento integral. Estos alimentos “ultraprocesados” por lo general no son adecuados para los riñones y pueden contribuir a muchas enfermedades crónicas.

Es comprensible que elijamos estos alimentos, porque son prácticos, económicos y sabrosos. En su lugar, considere hornear en casa. Cuando hornea usted mismo, puede usar harinas integrales e incluso reemplazar parte de la harina con frutos secos finamente molidos para aumentar el valor nutritivo. Este cambio aumenta la fibra de su postre y reduce el contenido de carbohidratos, lo que puede ayudar a controlar la glucosa en la sangre cuando sea necesario. Por lo general, puede reemplazar hasta la mitad de la harina total con frutos secos molidos. Puede comprar frutos secos molidos o molerlos usted mismo en un procesador de alimentos. Tostarlos primero facilita molerlos y realza su sabor; use la función de pulso para que no se conviertan en pasta. Otros cambios saludables incluyen usar menos sal y azúcar en la receta."""
TR_AR = """الجميع يحب الحلويات. وعند اختيارها بعناية، يمكن أن تكون الحلوى بين الحين والآخر جزءًا من نظام غذائي صحي. لكن للأسف، كثير من الحلويات التي نتناولها أطعمة عالية المعالجة مثل الكعك المعبأ والدونات والمافن والبسكويت وألواح الحلوى. تحتوي هذه الأطعمة على مكونات مكررة أو معالجة، وعادةً ما تحتوي على كميات أعلى من الدهون المشبعة والسكر المضاف والصوديوم والإضافات من نوع الفوسفات، مع قليل من الأطعمة الكاملة أو بدونها. وهذه الأطعمة “فائقة المعالجة” غالبًا لا تكون مناسبة لمرضى الكلى، وقد تسهم في الإصابة بكثير من الأمراض المزمنة.

من المفهوم أن نختار هذه الأطعمة لأنها مريحة ورخيصة ولذيذة. لكن بدلًا من ذلك، فكّر في الخَبز في المنزل. فعندما تخبز بنفسك، يمكنك استخدام دقيق الحبوب الكاملة، بل واستبدال جزء من الدقيق بالمكسرات المطحونة ناعمًا لزيادة القيمة الغذائية. يزيد هذا التغيير من الألياف في الحلوى ويقلل محتواها من الكربوهيدرات، مما قد يساعد على التحكم في سكر الدم عند الحاجة. ويمكنك عادةً استبدال ما يصل إلى نصف كمية الدقيق الإجمالية بالمكسرات المطحونة. ويمكنك شراء المكسرات المطحونة أو طحنها بنفسك في محضرة الطعام. وتحميص المكسرات أولًا يسهّل طحنها ويعزز نكهتها؛ استخدم وضع النبض حتى لا تتحول إلى عجينة. ومن التغييرات الصحية الأخرى استخدام كمية أقل من الملح والسكر في الوصفة."""
R.append(rec(4891483, {
 "title": "Pastel de almendras", "description": N, "portions": "12", "serving_size": "1/12 de la receta",
 "ingredients": ["¾ taza de almendras molidas", "½ taza de harina de trigo común", "¼ cucharadita de bicarbonato de sodio",
   "½ cucharadita de crémor tártaro", "½ taza de azúcar", "¼ taza de mantequilla sin sal, suavizada", "2 cucharadas de aceite de canola",
   "3 huevos", "1 cucharadita de extracto de almendra", "¼ taza de yogur griego de vainilla", "2 cucharadas de almendras fileteadas",
   ("Para decorar", "¾ taza de yogur griego de vainilla"), ("Para decorar", "¾ taza de almendras fileteadas")],
 "steps": ["Precaliente el horno a 350°F.",
   "Forre con papel pergamino un molde desmontable o un molde normal de 8 pulgadas.",
   "En un tazón mediano, mezcle las almendras molidas, la harina, el bicarbonato de sodio y el crémor tártaro. Reserve.",
   "En otro tazón, con una batidora eléctrica a velocidad media, bata el azúcar, la mantequilla suavizada y el aceite hasta obtener una crema (1–2 minutos). Agregue los huevos uno por uno y mezcle hasta que quede homogéneo. Agregue el extracto de almendra.",
   "Batiendo a velocidad baja, incorpore los ingredientes secos alternando con el yogur hasta que la masa quede homogénea. Vierta en el molde y espolvoree las almendras fileteadas por encima.",
   "Hornee unos 30 minutos o hasta que al insertar un cuchillo en el centro salga limpio. Deje enfriar.",
   "Desmolde y sirva cada rebanada con 1 cucharada de yogur y 1 cucharada de almendras fileteadas.",
   "cucharadas de café instantáneo en 1 cucharada de agua y mézclelo con la masa en el paso 4, junto con el extracto de almendra."],
 "hints": ["Nota: Para dar sabor a café, disuelva",
   ("Pruebe una versión saludable de los postres", TR_ES)],
 "food_choices": ["½ carne", "1 lácteos", "1 carbohidrato", "2 grasa"]},
{
 "title": "كيكة اللوز", "description": N, "portions": "12", "serving_size": "1/12 الوصفة",
 "ingredients": ["¾ كوب لوز مطحون", "½ كوب دقيق متعدد الاستخدامات", "¼ ملعقة صغيرة بيكربونات الصوديوم",
   "½ ملعقة صغيرة كريمة الترتار", "½ كوب سكر", "¼ كوب زبدة غير مملحة، طرية", "2 ملعقة كبيرة زيت الكانولا",
   "3 بيضات", "1 ملعقة صغيرة خلاصة اللوز", "¼ كوب زبادي يوناني بالفانيليا", "2 ملعقة كبيرة لوز مقطع شرائح",
   ("للتزيين", "¾ كوب زبادي يوناني بالفانيليا"), ("للتزيين", "¾ كوب لوز مقطع شرائح")],
 "steps": ["سخّن الفرن مسبقًا على 350° فهرنهايت (175° مئوية).",
   "بطّن قالبًا قابلًا للفك أو قالبًا عاديًا قطره 8 بوصات بورق الزبدة.",
   "في وعاء متوسط، اخلط اللوز المطحون والدقيق وبيكربونات الصوديوم وكريمة الترتار. ضعه جانبًا.",
   "في وعاء آخر، اخفق السكر والزبدة الطرية والزيت بالخلاط الكهربائي على سرعة متوسطة حتى يصبح الخليط كريميًا (1–2 دقيقة). أضف البيض واحدة تلو الأخرى واخلط حتى يصبح الخليط ناعمًا. أضف خلاصة اللوز.",
   "مع الخلط على سرعة منخفضة، أضف المكونات الجافة بالتناوب مع الزبادي حتى يصبح الخليط ناعمًا. اسكبه في القالب وانثر شرائح اللوز على الوجه.",
   "اخبز لمدة 30 دقيقة تقريبًا أو حتى تخرج السكين نظيفة عند غرزها في المنتصف. اتركها لتبرد.",
   "أخرجها من القالب وقدّم كل شريحة مع 1 ملعقة كبيرة زبادي و1 ملعقة كبيرة لوز مقطع شرائح.",
   "ملاعق كبيرة من القهوة سريعة الذوبان في 1 ملعقة كبيرة ماء وإضافتها إلى الخليط في الخطوة 4 مع خلاصة اللوز."],
 "hints": ["ملاحظة: أضف نكهة القهوة عن طريق إذابة",
   ("جرّب لمسة صحية على الحلويات", TR_AR)],
 "food_choices": ["½ لحوم", "1 ألبان", "1 كربوهيدرات", "2 دهون"]}))

# 13 Spicy Porcini Mushroom Pasta
R.append(rec(4892893, {
 "title": "Pasta picante con hongos porcini", "description": N, "portions": "6", "serving_size": "1/6 de la receta",
 "ingredients": ["1 paquete pequeño de hongos porcini secos (1 onza)", "1/2 taza de agua hirviendo", "1/3 taza de aceite de oliva",
   "2 dientes de ajo, finamente picados", "1 pizca de hojuelas de chile picante seco", "1/2 pinta de champiñones blancos, cortados en cuartos",
   "1/4 cucharadita de salvia seca o 2 hojas frescas, picadas", "1/2 taza de mini bocconcini de mozzarella",
   "1/3 taza de perejil fresco picado", "1/2 libra de cualquier pasta seca (de preferencia pasta corta)"],
 "steps": ["Rehidrate los hongos porcini con 1/2 taza de agua hirviendo.",
   "Ponga a hervir 3 cuartos de galón de agua para la pasta.",
   "Mientras tanto, prepare la salsa calentando el aceite a fuego medio en una sartén grande. La sartén debe ser lo bastante grande para que quepa la pasta una vez cocida.",
   "Agregue el ajo y las hojuelas de chile y cocínelos hasta que el ajo se dore.",
   "Agregue los champiñones blancos, suba el fuego a medio-alto y siga cocinando.",
   "Cocine la pasta en el agua hirviendo según las instrucciones del paquete.",
   "Exprima el líquido de los porcini y resérvelo para la salsa. Pique los porcini y agréguelos a la sartén.",
   "Vierta el líquido de remojo en la sartén pasándolo por un colador fino.",
   "Agregue la salvia y cocine 5 minutos. (10) Escurra la pasta (NO LA ENJUAGUE) y mézclela en la sartén con la salsa de hongos mientras esté caliente. Agregue el queso bocconcini y el perejil, y sirva."],
 "hints": ["Prepárela con anticipación o congélela en porciones. La receta se puede duplicar fácilmente. Las sobras se congelan bien. Descongélelas en el refrigerador durante la noche, caliéntelas agregando 2 cucharadas de agua y sirva."],
 "food_choices": ["1 carne", "2 almidón", "1 verdura", "2 grasa"]},
{
 "title": "معكرونة حارة بفطر البورشيني", "description": N, "portions": "6", "serving_size": "1/6 الوصفة",
 "ingredients": ["1 عبوة صغيرة فطر بورشيني مجفف (1 أونصة)", "½ كوب ماء مغلي", "⅓ كوب زيت زيتون",
   "2 فص ثوم، مفروم ناعمًا", "1 رشة رقائق فلفل حار مجفف", "½ باينت فطر أبيض، مقطع أرباعًا",
   "¼ ملعقة صغيرة مريمية مجففة أو 2 ورقة طازجة مفرومة", "½ كوب جبن موزاريلا بوكونتشيني صغير",
   "⅓ كوب بقدونس طازج مفروم", "½ رطل من أي نوع معكرونة جافة (يُفضّل المعكرونة القصيرة)"],
 "steps": ["انقع فطر البورشيني في ½ كوب ماء مغلي ليستعيد رطوبته.",
   "اغلِ 3 كوارت من الماء لسلق المعكرونة.",
   "في هذه الأثناء، حضّر الصلصة بتسخين الزيت على نار متوسطة في مقلاة كبيرة. يجب أن تكون المقلاة كبيرة بما يكفي لتتسع للمعكرونة بعد طهيها.",
   "أضف الثوم ورقائق الفلفل الحار، واطهُها حتى يصبح لون الثوم ذهبيًا.",
   "أضف الفطر الأبيض، وارفع الحرارة إلى متوسطة إلى عالية، واستمر في الطهي.",
   "اسلق المعكرونة في الماء المغلي حسب التعليمات المدونة على العبوة.",
   "اعصر السائل من فطر البورشيني واحتفظ به للصلصة. افرم البورشيني وأضفه إلى المقلاة.",
   "اسكب سائل النقع في المقلاة عبر مصفاة ناعمة.",
   "أضف المريمية واطهُ لمدة 5 دقائق. (10) صفِّ المعكرونة (لا تشطفها) واخلطها في المقلاة مع صلصة الفطر وهي ساخنة. أضف جبن البوكونتشيني والبقدونس وقدّمها."],
 "hints": ["حضّرها مسبقًا أو جمّدها في حصص. يمكن مضاعفة الوصفة بسهولة. وتتجمد بقايا الطعام جيدًا. أذبها في الثلاجة طوال الليل، ثم سخّنها مع إضافة 2 ملعقة كبيرة ماء وقدّمها."],
 "food_choices": ["1 لحوم", "2 نشويات", "1 خضار", "2 دهون"]}))

# 14 Chicken Burrito Bowl
PB_ES = "Las recomendaciones para una alimentación adecuada para los riñones han cambiado mucho en los últimos años. Antes se desaconsejaban alimentos como los frijoles, las legumbres, los frutos secos, las cremas de frutos secos, las semillas y los granos integrales debido a su alto contenido de fósforo. Hemos aprendido que, aunque estos alimentos contienen más fósforo, la cantidad que su cuerpo absorbe de ellos es bastante baja. Esto se llama biodisponibilidad del fósforo. En otras palabras, cuando usted come estos alimentos, no el 100% del fósforo llega a su sangre, sino un porcentaje mucho menor, del 40% o menos. Como la absorción del fósforo de estos alimentos es baja, pueden formar parte de una alimentación adecuada para los riñones. Esto no solo es una buena noticia porque agrega más variedad a la alimentación, sino que también es saludable. La proteína de origen vegetal aporta fibra y micronutrientes, que ayudan a retrasar el avance de la enfermedad renal. Hay varias maneras de agregar estos alimentos a su alimentación. Puede reducir la cantidad de proteína animal en las recetas reemplazando todo o parte de ese ingrediente con tofu, frijoles o legumbres. También puede preparar en casa tazones de granos con una base de arroz integral, bulgur o quinoa, y cubrirlos con tofu, frijoles o legumbres y verduras saludables."
PB_AR = "تغيرت التوصيات الخاصة بالنظام الغذائي المناسب لمرضى الكلى كثيرًا في السنوات الأخيرة. ففي الماضي، كان يُنصح بتجنب أطعمة مثل الفاصوليا والبقوليات والمكسرات وزبدة المكسرات والبذور والحبوب الكاملة بسبب ارتفاع محتواها من الفوسفور. لكننا عرفنا أنه رغم احتواء هذه الأطعمة على كمية أكبر من الفوسفور، فإن الكمية التي يمتصها جسمك منها منخفضة جدًا. ويُسمى هذا التوافر الحيوي للفوسفور. وبعبارة أخرى، عندما تتناول هذه الأطعمة لا يصل 100% من الفوسفور إلى دمك، بل نسبة أقل بكثير تبلغ 40% أو أقل. ونظرًا لانخفاض امتصاص الفوسفور من هذه الأطعمة، يمكن أن تكون جزءًا من نظام غذائي مناسب لمرضى الكلى. وهذا ليس خبرًا سارًا لأنه يضيف مزيدًا من التنوع إلى النظام الغذائي فحسب، بل إنه صحي أيضًا. فالبروتين النباتي يضيف الألياف والمغذيات الدقيقة التي تساعد على إبطاء تقدم مرض الكلى. وهناك عدة طرق لإضافة هذه الأطعمة إلى نظامك الغذائي. يمكنك تقليل كمية البروتين الحيواني في الوصفات باستبدال هذا المكون كليًا أو جزئيًا بالتوفو أو الفاصوليا أو البقوليات. ويمكنك أيضًا تحضير أطباق الحبوب في المنزل باستخدام قاعدة من الأرز البني أو البرغل أو الكينوا، ثم إضافة التوفو أو الفاصوليا أو البقوليات والخضار الصحية فوقها."
CS_ES, CK_ES, BW_ES = "Salsa cremosa de chipotle", "Pollo", "Tazón"
CS_AR, CK_AR, BW_AR = "صلصة الشيبوتلي الكريمية", "الدجاج", "الطبق"
R.append(rec(4893714, {
 "title": "Tazón de burrito con pollo", "description": N, "portions": "6", "serving_size": "1/6 de la receta",
 "ingredients": [(CS_ES, "1 taza de yogur griego natural 0% grasa"), (CS_ES, "1 cucharada de jugo de limón verde recién exprimido"),
   (CS_ES, "1 cucharadita de chile chipotle en polvo"), (CS_ES, "1 diente de ajo picado finamente"),
   (CK_ES, "3/4 libra de muslos de pollo (sin piel y sin hueso)"), (CK_ES, "1 cucharada de aceite de oliva"),
   (CK_ES, "½ cucharadita de chile en polvo"), (CK_ES, "½ cucharadita de ajo en polvo"),
   (CK_ES, "½ cucharadita de pimienta negra recién molida"), (CK_ES, "¼ cucharadita de pimentón (paprika)"),
   (BW_ES, "1 taza de arroz blanco crudo (2 tazas cocido)"), (BW_ES, "1 taza de frijoles negros enlatados, escurridos y enjuagados"),
   (BW_ES, "1 taza de maíz congelado"), (BW_ES, "½ taza de tomates uva, cortados en cuartos"),
   (BW_ES, "Jugo de 1 limón verde"), (BW_ES, "½ taza de cilantro fresco picado"), (BW_ES, "Gajos de limón verde para servir")],
 "steps": ["En un tazón pequeño, prepare la salsa cremosa de chipotle batiendo el yogur, el jugo de limón, el chile chipotle en polvo y el ajo. Reserve.",
   "Frote los muslos de pollo con aceite de oliva y espolvoréelos con el chile en polvo, el ajo en polvo, la pimienta molida y el pimentón. Caliente la parrilla o una sartén para asar en la estufa a fuego medio. Ase el pollo hasta que alcance una temperatura interna de 165°F. Deje enfriar.",
   "En una cacerola grande, cocine el arroz según las instrucciones del paquete y deje enfriar.",
   "Reparta el arroz en 6 tazones. Cubra con el pollo en rebanadas, los frijoles negros, el maíz y los tomates. Rocíe el jugo de limón por encima. Rocíe con la salsa cremosa de chipotle y cubra con el cilantro picado. Sirva con gajos de limón adicionales."],
 "hints": ["Consejo: Para variar, pruebe esta receta con cebollín picado, chiles jalapeños o pimiento rojo.",
   ("Maneras de aumentar la proteína de origen vegetal", PB_ES)],
 "food_choices": ["2 1/2 carne magra", "2 almidón", "1/2 verdura feculenta baja en potasio"]},
{
 "title": "طبق بوريتو بالدجاج", "description": N, "portions": "6", "serving_size": "1/6 الوصفة",
 "ingredients": [(CS_AR, "1 كوب زبادي يوناني سادة خالٍ من الدسم 0%"), (CS_AR, "1 ملعقة كبيرة عصير ليمون أخضر طازج"),
   (CS_AR, "1 ملعقة صغيرة مسحوق فلفل الشيبوتلي"), (CS_AR, "1 فص ثوم مفروم ناعمًا"),
   (CK_AR, "¾ رطل أفخاذ دجاج (منزوعة الجلد والعظم)"), (CK_AR, "1 ملعقة كبيرة زيت زيتون"),
   (CK_AR, "½ ملعقة صغيرة مسحوق الفلفل الحار"), (CK_AR, "½ ملعقة صغيرة ثوم بودرة"),
   (CK_AR, "½ ملعقة صغيرة فلفل أسود مطحون طازجًا"), (CK_AR, "¼ ملعقة صغيرة بابريكا"),
   (BW_AR, "1 كوب أرز أبيض غير مطبوخ (2 كوب مطبوخ)"), (BW_AR, "1 كوب فاصوليا سوداء معلبة، مصفاة ومغسولة"),
   (BW_AR, "1 كوب ذرة مجمدة"), (BW_AR, "½ كوب طماطم كرزية صغيرة (عنبية)، مقطعة أرباعًا"),
   (BW_AR, "عصير 1 ليمونة خضراء"), (BW_AR, "½ كوب كزبرة خضراء طازجة مفرومة"), (BW_AR, "شرائح ليمون أخضر للتقديم")],
 "steps": ["في وعاء صغير، حضّر صلصة الشيبوتلي الكريمية بخفق الزبادي وعصير الليمون ومسحوق فلفل الشيبوتلي والثوم معًا. ضعها جانبًا.",
   "افرك أفخاذ الدجاج بزيت الزيتون وانثر عليها مسحوق الفلفل الحار والثوم البودرة والفلفل المطحون والبابريكا. سخّن الشواية أو مقلاة الشواء على الموقد على نار متوسطة. اشوِ الدجاج حتى تصل حرارته الداخلية إلى 165° فهرنهايت (75° مئوية). اتركه ليبرد.",
   "في قدر كبير، اطهُ الأرز حسب التعليمات المدونة على العبوة واتركه ليبرد.",
   "وزّع الأرز على 6 أطباق. ضع فوقه شرائح الدجاج والفاصوليا السوداء والذرة والطماطم. رشّ عصير الليمون على الوجه. ثم رشّ صلصة الشيبوتلي الكريمية وزيّن بالكزبرة المفرومة. قدّمه مع شرائح ليمون إضافية."],
 "hints": ["نصيحة: للتنويع، جرّب هذه الوصفة مع البصل الأخضر المفروم أو فلفل الهالبينو أو الفلفل الرومي الأحمر.",
   ("طرق لزيادة البروتين النباتي", PB_AR)],
 "food_choices": ["2½ لحوم قليلة الدهون", "2 نشويات", "½ خضار نشوية منخفضة البوتاسيوم"]}))

# 15 Summer Fresh Pizza
PZ_ES, RS_ES = "Pizza", "Salsa de pimiento rojo (rinde 2 tazas)"
PZ_AR, RS_AR = "البيتزا", "صلصة الفلفل الأحمر (تكفي 2 كوب)"
R.append(rec(4893996, {
 "title": "Pizza fresca de verano", "description": N, "portions": "1 pizza", "serving_size": "1 pizza",
 "ingredients": [(PZ_ES, "Cualquier pan plano o pan pita de harina blanca (de 7 pulgadas de diámetro)"), (PZ_ES, "1/4 taza de salsa de pimiento rojo"),
   (PZ_ES, "1/4 taza de calabacín rallado (exprimido para quitar el exceso de líquido)"), (PZ_ES, "1/4 taza de champiñones en láminas finas"),
   (PZ_ES, "1 cebolla amarilla pequeña, en rodajas"), (PZ_ES, "2 onzas de queso Brie, en rebanadas delgadas, sin corteza"),
   (PZ_ES, "1 cucharadita de aceite de oliva"),
   (RS_ES, "1/3 taza de aceite de oliva"), (RS_ES, "4 dientes de ajo"), (RS_ES, "3/4 taza de cebolla picada"),
   (RS_ES, "2 tazas de pimiento rojo, sin semillas y picado"), (RS_ES, "1/2 taza de tomate picado en cubitos"),
   (RS_ES, "1/2 cucharadita de chile triturado"), (RS_ES, "2 cucharaditas de ralladura de limón (1 limón)"),
   (RS_ES, "1/2 taza de agua"), (RS_ES, "2/3 taza de albahaca fresca picada (o 3 cucharadas de albahaca seca)")],
 "steps": ["Precaliente el horno a 400°F (horno convencional).",
   "A fuego medio, caliente el aceite y agregue el ajo, la cebolla, el pimiento, el tomate y el chile; cocine hasta que estén blandos.",
   "Agregue 1/2 taza de agua, la albahaca y la ralladura de limón; tape y cocine durante 20 minutos.",
   "Deje que la mezcla se enfríe un poco y licúela.",
   "Coloque el pan pita en una bandeja para hornear. Unte la salsa de pimiento sobre el pan y cubra con las verduras y el queso. Rocíe con aceite de oliva.",
   "Hornee durante 10–12 minutos. Disfrútela con una ensalada."],
 "hints": ["La salsa sobrante se puede congelar en cubeteras para hielo. Una vez congelados, asegúrese de pasar los cubos a bolsas de plástico con cierre hermético para conservar su frescura.",
   "Esta salsa de pimiento rojo reemplaza la pasta de tomate y da un sabor delicioso al mezclarla en sopas y guisos."],
 "food_choices": ["2 carne", "2 verdura", "3 grasa"]},
{
 "title": "بيتزا الصيف الطازجة", "description": N, "portions": "1 بيتزا", "serving_size": "1 بيتزا",
 "ingredients": [(PZ_AR, "أي خبز مسطح أو خبز بيتا من الدقيق الأبيض (قطره 7 بوصات)"), (PZ_AR, "¼ كوب صلصة الفلفل الأحمر"),
   (PZ_AR, "¼ كوب كوسا مبشورة (معصورة للتخلص من السائل الزائد)"), (PZ_AR, "¼ كوب فطر مقطع شرائح رفيعة"),
   (PZ_AR, "1 بصلة صفراء صغيرة، مقطعة شرائح"), (PZ_AR, "2 أونصة جبن بري، مقطع شرائح رفيعة ومنزوع القشرة"),
   (PZ_AR, "1 ملعقة صغيرة زيت زيتون"),
   (RS_AR, "⅓ كوب زيت زيتون"), (RS_AR, "4 فص ثوم"), (RS_AR, "¾ كوب بصل مفروم"),
   (RS_AR, "2 كوب فلفل رومي أحمر، منزوع البذور ومفروم"), (RS_AR, "½ كوب طماطم مقطعة مكعبات صغيرة"),
   (RS_AR, "½ ملعقة صغيرة فلفل حار مجروش"), (RS_AR, "2 ملعقة صغيرة برش قشر الليمون (1 ليمونة)"),
   (RS_AR, "½ كوب ماء"), (RS_AR, "⅔ كوب ريحان طازج مفروم (أو 3 ملعقة كبيرة ريحان مجفف)")],
 "steps": ["سخّن الفرن مسبقًا على 400° فهرنهايت (200° مئوية) (فرن تقليدي).",
   "على نار متوسطة، سخّن الزيت وأضف الثوم والبصل والفلفل الرومي والطماطم والفلفل الحار، واطهُها حتى تطرى.",
   "أضف ½ كوب ماء والريحان وبرش قشر الليمون، وغطِّ القدر واطهُ لمدة 20 دقيقة.",
   "اترك الخليط ليبرد قليلًا ثم اخلطه في الخلاط.",
   "ضع خبز البيتا على صينية خبز. افرد صلصة الفلفل على الخبز ثم ضع فوقها الخضار والجبن. رشّ عليها زيت الزيتون.",
   "اخبزها في الفرن لمدة 10–12 دقيقة. استمتع بها مع السلطة."],
 "hints": ["يمكن تجميد الصلصة المتبقية في قوالب مكعبات الثلج. واحرص على نقل المكعبات بعد تجمدها إلى أكياس بلاستيكية محكمة الإغلاق للحفاظ على طزاجتها.",
   "تحل صلصة الفلفل الأحمر هذه محل معجون الطماطم، وتضفي مذاقًا رائعًا عند إضافتها إلى الحساء واليخنات."],
 "food_choices": ["2 لحوم", "2 خضار", "3 دهون"]}))

# 16 Sweet Corn and Zucchini Quiche
SQ_ES = "Las verduras forman parte de una alimentación saludable para todos. Sin embargo, para las personas con enfermedad renal crónica, algunas verduras pueden contener demasiado potasio para comerlas a diario. En el caso de la calabaza, el contenido de potasio puede variar muchísimo. Las calabazas de pulpa de color más intenso, como la calabaza bellota, la calabaza moscada (butternut) y la calabaza hubbard, son muy altas en potasio y deben usarse en cantidades muy limitadas. En general, las calabazas de pulpa más clara, como la de cuello torcido o cuello recto, la calabaza bonetera (scallop) y la calabaza espagueti, son más bajas en potasio y pueden formar parte de una alimentación con control de potasio. Sin embargo, el calabacín es una excepción a esta regla, ya que en realidad es más alto en potasio. Pregunte a su dietista qué cantidad de calabaza es adecuada para usted. Las calabazas de cuello torcido o recto, la bonetera y el calabacín se cosechan en verano y son mejores cuando se recogen pequeñas y tiernas. Se pueden asar a la parrilla, cocinar al vapor, hervir, saltear, freír o usar en recetas salteadas al estilo oriental. La calabaza espagueti se cosecha a fines del verano o a principios del otoño. Se puede hornear, hervir, cocinar al vapor y en el microondas. Incluso puede usarla como sustituto de la pasta."
SQ_AR = "الخضار جزء من النظام الغذائي الصحي للجميع. لكن بالنسبة لمرضى الكلى المزمن، قد تحتوي بعض الخضار على كمية كبيرة جدًا من البوتاسيوم تمنع تناولها يوميًا. وفيما يخص القرع، فإن محتواه من البوتاسيوم قد يختلف اختلافًا كبيرًا. فأنواع القرع ذات اللب الأغمق لونًا، مثل قرع البلوط والقرع العسلي (بترنت) وقرع الهبارد، مرتفعة جدًا في البوتاسيوم وينبغي استخدامها بكميات محدودة جدًا. وبوجه عام، فإن أنواع القرع ذات اللب الأفتح لونًا، مثل القرع الأصفر ذي العنق المعقوف أو المستقيم، والقرع الصدفي (سكالوب)، وقرع الإسباغيتي، أقل في البوتاسيوم ويمكن أن تكون جزءًا من نظام غذائي مضبوط البوتاسيوم. أما الكوسا فهي استثناء من هذه القاعدة، إذ إنها في الواقع أعلى في البوتاسيوم. اسأل أخصائي التغذية عن كمية القرع المناسبة لك. ويُحصد القرع ذو العنق المعقوف أو المستقيم والقرع الصدفي والكوسا في الصيف، وتكون في أفضل حالاتها عند قطفها وهي صغيرة وطرية. ويمكن شويها أو طهيها على البخار أو سلقها أو تقليبها في قليل من الزيت أو قليها أو استخدامها في وصفات التقليب السريع. أما قرع الإسباغيتي فيُحصد في أواخر الصيف أو أوائل الخريف، ويمكن خبزه أو سلقه أو طهيه على البخار أو في الميكروويف. بل يمكنك استخدامه بديلًا عن المعكرونة."
R.append(rec(4897121, {
 "title": "Quiche de maíz dulce y calabacín", "description": N, "portions": "4", "serving_size": "1/4 de la receta",
 "ingredients": ["1 base de pay congelada estándar, de 9 pulgadas de diámetro", "1 cucharada de aceite de oliva",
   "½ taza de cebolla morada en aros", "1 taza de maíz congelado", "1 ½ taza de calabacín en rodajas", "3 huevos grandes",
   "½ taza de leche descremada", "¼ taza de queso de cabra", "3 cucharadas de albahaca fresca en chiffonade*"],
 "steps": ["Precaliente el horno a 400°F. Hornee la base de pay congelada aproximadamente 15 minutos o hasta que esté ligeramente dorada.",
   "Saque la base de pay del horno y baje la temperatura del horno a 350°F.",
   "Caliente el aceite de oliva en una sartén a fuego medio-alto. Saltee la cebolla, el maíz y el calabacín hasta que estén cocidos. Retire del fuego.",
   "En un tazón, bata los huevos y la leche.",
   "Extienda las verduras cocidas de manera uniforme en la base de pay horneada. Espolvoree con el queso de cabra y la albahaca.",
   "Vierta la mezcla de huevo y leche por encima.",
   "Coloque la quiche en una bandeja para hornear y hornee aproximadamente 35–40 minutos o hasta que la quiche esté firme al tacto (temperatura interna de 160°F). Sirva tibia."],
 "hints": ["* Técnica de corte en la que las hierbas o las verduras de hoja verde (como la espinaca y la albahaca) se cortan en tiras largas y delgadas.",
   ("Qué tipo de calabaza elegir", SQ_ES)],
 "food_choices": ["1 carne", "2 almidón", "1 verdura baja en potasio", "3 grasa"]},
{
 "title": "كيش الذرة الحلوة والكوسا", "description": N, "portions": "4", "serving_size": "¼ الوصفة",
 "ingredients": ["1 قاعدة فطيرة مجمدة عادية، قطرها 9 بوصات", "1 ملعقة كبيرة زيت زيتون",
   "½ كوب بصل أحمر مقطع حلقات", "1 كوب ذرة مجمدة", "1½ كوب كوسا مقطعة دوائر", "3 بيضات كبيرة",
   "½ كوب حليب خالي الدسم", "¼ كوب جبن الماعز", "3 ملعقة كبيرة ريحان طازج مقطع شرائط رفيعة (شيفوناد)*"],
 "steps": ["سخّن الفرن مسبقًا على 400° فهرنهايت (200° مئوية). اخبز قاعدة الفطيرة المجمدة لمدة 15 دقيقة تقريبًا أو حتى يصبح لونها ذهبيًا فاتحًا.",
   "أخرج قاعدة الفطيرة من الفرن واخفض حرارة الفرن إلى 350° فهرنهايت (175° مئوية).",
   "سخّن زيت الزيتون في مقلاة على نار متوسطة إلى عالية. قلّب البصل والذرة والكوسا حتى تنضج. ارفعها عن النار.",
   "في وعاء الخلط، اخفق البيض والحليب معًا.",
   "افرد الخضار المطبوخة بالتساوي في قاعدة الفطيرة المخبوزة. انثر عليها جبن الماعز والريحان.",
   "اسكب خليط البيض والحليب على الوجه.",
   "ضع الكيش على صينية خبز واخبزه لمدة 35–40 دقيقة تقريبًا أو حتى يصبح متماسكًا عند لمسه (حرارة داخلية 160° فهرنهايت (70° مئوية)). قدّمه دافئًا."],
 "hints": ["* أسلوب تقطيع تُقطع فيه الأعشاب أو الخضار الورقية الخضراء (مثل السبانخ والريحان) إلى شرائط طويلة ورفيعة.",
   ("أي نوع من القرع تختار", SQ_AR)],
 "food_choices": ["1 لحوم", "2 نشويات", "1 خضار منخفضة البوتاسيوم", "3 دهون"]}))

# 17 Curried Tilapia with Rice Noodles
FI_ES = """La proteína es una parte necesaria de su alimentación y es importante que la consuma incluso cuando tiene enfermedad renal crónica. La proteína puede provenir de plantas o de animales. Al elegir una fuente de proteína animal, se recomiendan las fuentes magras. El pescado es una excelente fuente de proteína magra que puede formar parte de su alimentación adecuada para los riñones. La tilapia es un pescado más bajo en potasio y, con la combinación de sabores adecuada, puede usarla en una gran variedad de platillos.

Simplemente hornear la tilapia con aceite puede ser una comida fácil y rápida. La tilapia también se puede asar a la parrilla y usar en tacos, agregando cebolla, pimiento verde y un condimento sin sal. Si prefiere adobarla, planifique el tiempo adicional necesario y deseche siempre el adobo sobrante. Asegúrese de incluir ingredientes más bajos en sodio y potasio para mantenerse dentro de las metas de su alimentación renal."""
FI_AR = """البروتين جزء ضروري من نظامك الغذائي، ومن المهم أن تتناوله حتى عندما تكون مصابًا بمرض الكلى المزمن. ويمكن أن يأتي البروتين من مصادر نباتية أو حيوانية. وعند اختيار مصدر حيواني للبروتين، يُنصح بالمصادر قليلة الدهون. والسمك مصدر ممتاز للبروتين قليل الدهون ويمكن تناوله ضمن نظامك الغذائي المناسب لمرضى الكلى. والبلطي سمك أقل في البوتاسيوم، ومع التوليفة المناسبة من النكهات يمكنك استخدامه في أطباق متنوعة.

إن خَبز البلطي بالزيت ببساطة يمكن أن يكون وجبة سهلة وسريعة. ويمكن أيضًا شوي البلطي واستخدامه في التاكو مع إضافة البصل والفلفل الرومي الأخضر وتوابل خالية من الملح. وإذا كنت تفضل التتبيل، فخطط مسبقًا للوقت الإضافي اللازم، وتخلص دائمًا من التتبيلة المتبقية. واحرص على استخدام مكونات أقل في الصوديوم والبوتاسيوم لتبقى ضمن أهداف نظامك الغذائي الخاص بالكلى."""
R.append(rec(4898788, {
 "title": "Tilapia al curry con fideos de arroz", "description": N, "portions": "4", "serving_size": "¼ de la receta",
 "ingredients": ["7 onzas de fideos de arroz, secos", "1 libra de tilapia congelada (4 filetes), descongelada", "2 cucharadas de aceite de canola",
   "1 cucharada de curry en polvo", "1 cucharadita de ajo en polvo", "1 cucharada de aceite de ajonjolí", "1 cucharada de mantequilla sin sal",
   "3 cucharadas de jengibre picado finamente", "1 cucharada de ajo picado finamente", "1 taza de repollo morado en tiras finas",
   "1 taza de chícharos chinos (snow peas)", "1 taza de cebolla amarilla en rodajas", "¼ taza de caldo de pollo sin sal añadida",
   "2 cucharadas de vinagre de vino de arroz", "¼ taza de cilantro finamente picado"],
 "steps": ["Para cocinar los fideos de arroz, ponga a hervir una olla grande con agua. Agregue los fideos y retire la olla del fuego. Deje remojar los fideos 5 minutos o hasta que estén suaves.",
   "Rocíe el aceite de canola sobre los filetes y espolvoréelos con el curry y el ajo en polvo.",
   "En una sartén a fuego medio-alto, caliente el aceite de ajonjolí y la mantequilla. Fría la tilapia de 2 a 3 minutos por cada lado. Retire el pescado de la sartén, páselo a un plato y cúbralo con papel de aluminio para mantenerlo caliente.",
   "En la misma sartén a fuego medio-alto, saltee el jengibre, el ajo, el repollo, los chícharos chinos y la cebolla de 2 a 3 minutos, hasta que estén tiernos pero crujientes.",
   "Agregue los fideos de arroz cocidos, el caldo de pollo y el vinagre. Cocine de 2 a 3 minutos más.",
   "Retire del fuego. Agregue el cilantro y mezcle para integrar. Sirva los fideos con la tilapia al curry."],
 "hints": [("Pescado adecuado para los riñones", FI_ES)],
 "food_choices": ["3 carne", "3 almidón", "1 verdura de potasio medio", "1 grasa"]},
{
 "title": "بلطي بالكاري مع نودلز الأرز", "description": N, "portions": "4", "serving_size": "¼ الوصفة",
 "ingredients": ["7 أونصة نودلز أرز جافة", "1 رطل سمك بلطي مجمد (4 فيليه)، مذاب", "2 ملعقة كبيرة زيت الكانولا",
   "1 ملعقة كبيرة مسحوق الكاري", "1 ملعقة صغيرة ثوم بودرة", "1 ملعقة كبيرة زيت السمسم", "1 ملعقة كبيرة زبدة غير مملحة",
   "3 ملعقة كبيرة زنجبيل مفروم ناعمًا", "1 ملعقة كبيرة ثوم مفروم ناعمًا", "1 كوب ملفوف أحمر مقطع شرائح رفيعة",
   "1 كوب بازلاء صينية (بازلاء الثلج)", "1 كوب بصل أصفر مقطع شرائح", "¼ كوب مرق دجاج بدون ملح مضاف",
   "2 ملعقة كبيرة خل نبيذ الأرز", "¼ كوب كزبرة خضراء مفرومة ناعمًا"],
 "steps": ["لطهي نودلز الأرز، اغلِ قدرًا كبيرًا من الماء. أضف النودلز وارفع القدر عن النار. اترك النودلز منقوعة لمدة 5 دقائق أو حتى تطرى.",
   "رشّ زيت الكانولا على شرائح الفيليه وانثر عليها مسحوق الكاري والثوم البودرة.",
   "في مقلاة على نار متوسطة إلى عالية، سخّن زيت السمسم والزبدة. اقلِ البلطي لمدة 2 إلى 3 دقائق لكل جانب. أخرج السمك من المقلاة وانقله إلى طبق وغطّه بورق الألومنيوم ليبقى دافئًا.",
   "في المقلاة نفسها على نار متوسطة إلى عالية، قلّب الزنجبيل والثوم والملفوف والبازلاء الصينية والبصل لمدة 2 إلى 3 دقائق حتى تطرى مع بقائها مقرمشة.",
   "أضف نودلز الأرز المطبوخة ومرق الدجاج والخل. اطهُ لمدة 2 إلى 3 دقائق أخرى.",
   "ارفعها عن النار. أضف الكزبرة وقلّب لتمتزج. قدّم النودلز مع البلطي بالكاري."],
 "hints": [("سمك مناسب لمرضى الكلى", FI_AR)],
 "food_choices": ["3 لحوم", "3 نشويات", "1 خضار متوسطة البوتاسيوم", "1 دهون"]}))

# 18 Easy Summer Pasta
R.append(rec(4901925, {
 "title": "Pasta fácil de verano", "description": "Ligera y saludable", "portions": "4", "serving_size": N,
 "ingredients": ["2 tazas de pasta rotini (cruda)", "1 pimiento (de cualquier color), picado en cubitos", "1 cebolla picada en cubitos",
   "1 calabacín o calabaza de verano, picado", "1 cucharada de aceite de canola", "¼ taza de queso parmesano vegano",
   "(como Daiya)", "Pimienta negra al gusto"],
 "steps": ["Ponga a hervir una olla grande con agua. Agregue la pasta rotini y cocine 8-10 minutos, hasta que esté tierna.",
   "En una sartén, agregue el aceite y saltee el pimiento, la cebolla y el calabacín hasta que estén blandos.",
   "Escurra la pasta y agréguela a la sartén con las verduras.",
   "Agregue pimienta negra y cubra con queso parmesano vegano al gusto."],
 "hints": [], "food_choices": []},
{
 "title": "معكرونة الصيف السهلة", "description": "خفيفة وصحية", "portions": "4", "serving_size": N,
 "ingredients": ["2 كوب معكرونة روتيني (غير مطبوخة)", "1 فلفل رومي (أي لون)، مقطع مكعبات صغيرة", "1 بصلة مقطعة مكعبات صغيرة",
   "1 كوسا أو قرع صيفي، مقطع", "1 ملعقة كبيرة زيت الكانولا", "¼ كوب جبن بارميزان نباتي",
   "(مثل Daiya)", "فلفل أسود حسب الرغبة"],
 "steps": ["اغلِ قدرًا كبيرًا من الماء. أضف معكرونة الروتيني واسلقها لمدة 8-10 دقائق حتى تطرى.",
   "في مقلاة، ضع الزيت وقلّب الفلفل والبصل والكوسا حتى تطرى.",
   "صفِّ المعكرونة وأضفها إلى المقلاة مع الخضار.",
   "أضف الفلفل الأسود وانثر جبن البارميزان النباتي على الوجه حسب الرغبة."],
 "hints": [], "food_choices": []}))

# 19 Grandma's Blueberry Cupcakes
CC_ES, FR_ES = "Pastelitos", "Glaseado (opcional)"
CC_AR, FR_AR = "الكب كيك", "الكريمة (اختيارية)"
R.append(rec(4902938, {
 "title": "Pastelitos de arándanos de la abuela", "description": "Una tradición familiar", "portions": "18", "serving_size": N,
 "ingredients": [(CC_ES, "1/3 taza de manteca vegetal"), (CC_ES, "½ cucharadita de sal"), (CC_ES, "1 cucharadita de vainilla"),
   (CC_ES, "1 taza de azúcar"), (CC_ES, "1 huevo"), (CC_ES, "2½ cucharaditas de polvo"), (CC_ES, "para hornear"),
   (CC_ES, "2 tazas de harina, cernida"), (CC_ES, "¾ taza de leche"), (CC_ES, "1 taza de arándanos azules"),
   (CC_ES, "Capacillos para pastelitos (opcional)"), (CC_ES, "2 moldes para magdalenas de 12 cavidades"),
   (FR_ES, "3 tazas de azúcar glas"), (FR_ES, "½ taza de mantequilla sin sal, suavizada"), (FR_ES, "1 cucharadita de extracto de vainilla"),
   (FR_ES, "1 cucharada de leche de almendra"), (FR_ES, "sabor vainilla")],
 "steps": ["Precaliente el horno a 400°F. Coloque capacillos en un molde para magdalenas de 12 cavidades y 6 capacillos en un segundo molde (o puede hornearlos en dos tandas si solo tiene un molde).",
   "Bata la manteca vegetal, la sal, la vainilla, el huevo y el azúcar a velocidad alta con una batidora. En otro tazón, mezcle el polvo para hornear y la harina. Agregue la mezcla seca y la leche a la mezcla de manteca, alternándolas (agregue aproximadamente un tercio de cada una a la vez). Luego incorpore los arándanos a la masa con movimientos envolventes, a mano.",
   "Vierta la masa en los capacillos. Hornee durante 15-18 minutos. Glaseado (opcional): Bata el azúcar glas y la mantequilla a velocidad alta con una batidora de mano. Agregue la vainilla y la leche de almendra y siga batiendo hasta que quede homogéneo. Unte el glaseado sobre los pastelitos de arándanos ya fríos."],
 "hints": ["La información nutricional corresponde al pastelito sin el glaseado opcional."],
 "food_choices": []},
{
 "title": "كب كيك التوت الأزرق على طريقة الجدة", "description": "تقليد عائلي", "portions": "18", "serving_size": N,
 "ingredients": [(CC_AR, "⅓ كوب سمن نباتي صلب (شورتنينج)"), (CC_AR, "½ ملعقة صغيرة ملح"), (CC_AR, "1 ملعقة صغيرة فانيليا"),
   (CC_AR, "1 كوب سكر"), (CC_AR, "1 بيضة"), (CC_AR, "2½ ملعقة صغيرة بيكنج"), (CC_AR, "بودر"),
   (CC_AR, "2 كوب دقيق منخول"), (CC_AR, "¾ كوب حليب"), (CC_AR, "1 كوب توت أزرق"),
   (CC_AR, "قوالب ورقية للكب كيك (اختياري)"), (CC_AR, "2 صينية مافن من 12 تجويفًا"),
   (FR_AR, "3 كوب سكر بودرة"), (FR_AR, "½ كوب زبدة غير مملحة، طرية"), (FR_AR, "1 ملعقة صغيرة خلاصة الفانيليا"),
   (FR_AR, "1 ملعقة كبيرة حليب اللوز"), (FR_AR, "بنكهة الفانيليا")],
 "steps": ["سخّن الفرن مسبقًا على 400° فهرنهايت (200° مئوية). ضع قوالب ورقية في صينية مافن من 12 تجويفًا، و6 قوالب ورقية في صينية مافن ثانية (أو يمكنك الخَبز على دفعتين إذا كانت لديك صينية واحدة فقط).",
   "اخفق السمن النباتي والملح والفانيليا والبيض والسكر بالخلاط على سرعة عالية. وفي وعاء منفصل، اخلط البيكنج بودر والدقيق. أضف الخليط الجاف والحليب بالتناوب إلى خليط السمن المخفوق (أضف نحو ثلث كل منهما في كل مرة). ثم أدخل التوت الأزرق في الخليط برفق باليد.",
   "اسكب الخليط في القوالب الورقية. اخبز لمدة 15-18 دقيقة. الكريمة (اختيارية): اخفق السكر البودرة والزبدة على سرعة عالية بالخلاط اليدوي. أضف الفانيليا وحليب اللوز واستمر في الخفق حتى يصبح الخليط ناعمًا. افرد الكريمة على كب كيك التوت الأزرق بعد أن يبرد."],
 "hints": ["المعلومات الغذائية خاصة بقطعة الكب كيك بدون الكريمة الاختيارية."],
 "food_choices": []}))

# 20 Chicken Chili Stew
CH_ES = """La proteína es una parte necesaria de su alimentación cuando tiene enfermedad renal crónica (ERC). En las primeras etapas de la ERC, su consumo de proteína debe ser aproximadamente del 12 al 15% del total de calorías. A medida que avanza la ERC, es posible que su dietista le recomiende reducir el consumo de proteína. Reunirse con un dietista renal puede ayudarle a determinar la cantidad de proteína que su cuerpo necesita. El pollo es una buena fuente de proteína y además es bajo en potasio, lo que lo convierte en una buena opción para las personas con ERC.

El pollo fresco se consigue fácilmente en el supermercado. Se puede cortar en cubitos y cocinar como parte de un omelet, asar a la parrilla como plato principal, o cocinar y deshebrar para ensaladas. El pollo congelado es una segunda opción. Aunque es práctico para recetas con poco tiempo de cocción, lea las etiquetas para evitar conservadores altos en sodio o en potasio. El pollo enlatado es una tercera opción. Es importante recordar que el líquido de la carne enlatada suele ser alto en sodio. Las carnes enlatadas bajas en sodio pueden ser altas en potasio, por lo que siempre es importante leer la etiqueta de información nutricional y la lista de ingredientes."""
CH_AR = """البروتين جزء ضروري من نظامك الغذائي عند الإصابة بمرض الكلى المزمن. وفي المراحل المبكرة من مرض الكلى المزمن، ينبغي أن يشكل البروتين نحو 12 إلى 15% من إجمالي السعرات الحرارية التي تتناولها. ومع تقدم المرض، قد يوصيك أخصائي التغذية بتقليل كمية البروتين. ويمكن أن يساعدك لقاء أخصائي تغذية الكلى على تحديد كمية البروتين التي يحتاجها جسمك. والدجاج مصدر جيد للبروتين، كما أنه منخفض البوتاسيوم، مما يجعله خيارًا جيدًا لمرضى الكلى المزمن.

يتوفر الدجاج الطازج بسهولة في متجر البقالة. ويمكن تقطيعه مكعبات صغيرة وطهيه ضمن الأومليت، أو شويه كطبق رئيسي، أو طهيه وتقطيعه إلى شرائح رفيعة لإضافته إلى السلطات. والدجاج المجمد خيار ثانٍ؛ ورغم أنه عملي في الوصفات التي يكون وقت طهيها محدودًا، اقرأ الملصقات لتجنب أي مواد حافظة مرتفعة الصوديوم أو البوتاسيوم. والدجاج المعلب خيار ثالث. ومن المهم أن تتذكر أن السائل الموجود في اللحوم المعلبة يكون عادةً مرتفع الصوديوم. كما أن اللحوم المعلبة قليلة الصوديوم قد تكون مرتفعة البوتاسيوم، لذا من المهم دائمًا قراءة ملصق الحقائق الغذائية وقائمة المكونات."""
R.append(rec(4909485, {
 "title": "Guiso de pollo con chile", "description": N, "portions": "6", "serving_size": "1/6 de la receta",
 "ingredients": ["1 libra de muslos de pollo sin hueso y sin piel, en cubos de ½ pulgada", "2 cucharadas de chiles jalapeños picados finamente",
   "1 cucharada de ajo picado finamente", "½ taza de apio en cubos de ½ pulgada", "1 taza de cebolla en cubos de ½ pulgada",
   "1 taza de pimiento rojo en cubos de ½ pulgada", "1 taza de maíz congelado", "2 tazas de caldo de pollo sin sal añadida*",
   "1 cucharada de harina de trigo común", "1 cucharada de comino en polvo", "2 cucharaditas de chile en polvo",
   "½ cucharadita de orégano seco", "2 cucharadas de jugo de limón verde", "¼ taza de cilantro finamente picado",
   "1 taza de arroz blanco de grano largo, crudo", "½ taza de crema agria reducida en grasa"],
 "steps": ["Ponga la olla de cocción lenta en temperatura baja. Coloque el pollo en el fondo de la olla. Agregue los jalapeños, el ajo picado, el apio, la cebolla, el pimiento rojo y el maíz.",
   "En una taza medidora, bata el caldo de pollo, la harina, el comino, el chile en polvo y el orégano. Vierta sobre la mezcla de pollo y verduras. Agregue el jugo de limón y el cilantro.",
   "Tape y cocine a temperatura baja de 4 a 6 horas, hasta que el pollo esté cocido y tierno y el guiso se haya espesado ligeramente. Si prefiere usar el horno: precaliéntelo a 225°F y cocine durante 4 horas. Si lo desea, deje más tiempo para que quede más tierno.",
   "Al terminar la cocción, retire el guiso de la fuente de calor.",
   "Cocine el arroz según las instrucciones del paquete.",
   "Incorpore el arroz blanco cocido y la crema agria al guiso. Sirva de inmediato."],
 "hints": ["* Busque caldo bajo o reducido en sodio que contenga 200 mg de sodio o menos por porción de 1 taza. Evite el caldo bajo en sodio que contenga cloruro de potasio, porque es muy alto en potasio.",
   "TENGA EN CUENTA: Esta receta es más alta en potasio y el tamaño de la porción es importante. Consulte con su dietista registrado para saber cómo puede incluir esta receta en su alimentación.",
   ("El pollo como opción de proteína", CH_ES)],
 "food_choices": ["2 carne", "1 almidón", "1 verdura alta en potasio"]},
{
 "title": "يخنة الدجاج بالفلفل الحار", "description": N, "portions": "6", "serving_size": "1/6 الوصفة",
 "ingredients": ["1 رطل أفخاذ دجاج منزوعة العظم والجلد، مقطعة مكعبات ½ بوصة", "2 ملعقة كبيرة فلفل هالبينو مفروم ناعمًا",
   "1 ملعقة كبيرة ثوم مفروم ناعمًا", "½ كوب كرفس مقطع مكعبات ½ بوصة", "1 كوب بصل مقطع مكعبات ½ بوصة",
   "1 كوب فلفل رومي أحمر مقطع مكعبات ½ بوصة", "1 كوب ذرة مجمدة", "2 كوب مرق دجاج بدون ملح مضاف*",
   "1 ملعقة كبيرة دقيق متعدد الاستخدامات", "1 ملعقة كبيرة كمون مطحون", "2 ملعقة صغيرة مسحوق الفلفل الحار",
   "½ ملعقة صغيرة أوريجانو مجفف", "2 ملعقة كبيرة عصير ليمون أخضر", "¼ كوب كزبرة خضراء مفرومة ناعمًا",
   "1 كوب أرز أبيض طويل الحبة، غير مطبوخ", "½ كوب قشدة حامضة قليلة الدسم"],
 "steps": ["اضبط قدر الطهي البطيء على درجة الحرارة المنخفضة. ضع الدجاج في قاع القدر. أضف الهالبينو والثوم المفروم والكرفس والبصل والفلفل الأحمر والذرة.",
   "في كوب قياس، اخفق مرق الدجاج والدقيق والكمون ومسحوق الفلفل الحار والأوريجانو معًا. اسكب الخليط فوق الدجاج والخضار. أضف عصير الليمون والكزبرة.",
   "غطِّ القدر واطهُ على درجة منخفضة لمدة 4 إلى 6 ساعات، حتى ينضج الدجاج ويطرى وتتكثف اليخنة قليلًا. إذا اخترت استخدام الفرن: سخّنه مسبقًا على 225° فهرنهايت (105° مئوية) واطهُ لمدة 4 ساعات. ويمكنك زيادة مدة الطهي لمزيد من الطراوة إن أردت.",
   "بعد انتهاء الطهي، ارفع اليخنة عن مصدر الحرارة.",
   "اطهُ الأرز حسب التعليمات المدونة على العبوة.",
   "أضف الأرز الأبيض المطبوخ والقشدة الحامضة إلى اليخنة وقلّب برفق. قدّمها فورًا."],
 "hints": ["* ابحث عن مرق قليل الصوديوم أو مخفض الصوديوم يحتوي على 200 مليغرام صوديوم أو أقل لكل حصة مقدارها 1 كوب. وتجنب المرق قليل الصوديوم الذي يحتوي على كلوريد البوتاسيوم لأنه مرتفع جدًا في البوتاسيوم.",
   "يرجى الانتباه: هذه الوصفة أعلى في البوتاسيوم، وحجم الحصة مهم. استشر أخصائي التغذية المعتمد لمعرفة كيف يمكن إدراج هذه الوصفة في نظامك الغذائي.",
   ("الدجاج كخيار للبروتين", CH_AR)],
 "food_choices": ["2 لحوم", "1 نشويات", "1 خضار عالية البوتاسيوم"]}))

dump(2, R)
