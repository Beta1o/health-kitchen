import sys; sys.path.insert(0, '/mnt/c/WSL/davita/translations/b4')
from common import rec, dump, N

R = []

# 21 Tropical Mocktail
CI_ES = """Una variedad de frutas aporta vitaminas, minerales y fibra valiosos a cualquier alimentación para los riñones. En las primeras etapas de la enfermedad renal crónica, la fruta tiene un papel importante en una alimentación saludable, y las investigaciones sugieren que estos alimentos benefician la salud renal en general. A medida que avanza la enfermedad renal, es posible que deba ajustar la cantidad y el tipo de fruta que elige como parte de una alimentación baja en potasio.

Según la variedad, los cítricos pueden contener distintas cantidades de potasio. Trabajar con un dietista nutricionista registrado es una excelente manera de saber qué cítricos puede incluir con seguridad en su alimentación.

Cítricos más altos en potasio (1 fruta entera): toronja, naranjas, jugo de naranja, pomelo

Cítricos moderados y más bajos en potasio: clementina, kumquat, limón amarillo, limón verde, mandarinas enlatadas, piña, mandarina, fruta ugli"""
CI_AR = """تضيف الفواكه المتنوعة فيتامينات ومعادن وأليافًا قيّمة إلى أي نظام غذائي خاص بالكلى. وفي المراحل المبكرة من مرض الكلى المزمن، تؤدي الفاكهة دورًا مهمًا في النظام الغذائي الصحي، إذ تشير الأبحاث إلى أن هذه الأطعمة مفيدة لصحة الكلى بشكل عام. ومع تقدم مرض الكلى، قد تحتاج إلى تعديل كمية الفاكهة ونوعها ضمن نظام غذائي منخفض البوتاسيوم.

تحتوي الحمضيات على كميات مختلفة من البوتاسيوم حسب نوعها. ويُعد العمل مع أخصائي تغذية معتمد طريقة رائعة لمعرفة أنواع الحمضيات التي يمكن إدراجها بأمان في نظامك الغذائي.

حمضيات أعلى في البوتاسيوم (1 ثمرة كاملة): الجريب فروت، البرتقال، عصير البرتقال، البوميلو

حمضيات متوسطة وأقل في البوتاسيوم: الكليمنتينا، الكمكوات، الليمون، الليمون الأخضر، اليوسفي المعلب، الأناناس، اليوسفي (تانجرين)، فاكهة الأوغلي"""
R.append(rec(4910262, {
 "title": "Cóctel tropical sin alcohol", "description": N, "portions": "2", "serving_size": "1 bebida",
 "ingredients": ["½ taza de piña madura, en rodajas de ½ pulgada", "½ taza de mango picado en cubitos", "1 cucharada de jugo de limón verde fresco",
   "¼ cucharadita de extracto de vainilla", "½ taza de hielo picado", "2 cucharadas de hielo picado",
   "4 onzas (½ taza) de agua mineral con gas baja en sodio", "2 rodajas de limón verde para decorar"],
 "steps": ["Ponga en una licuadora la piña, el mango, el jugo de limón, el extracto de vainilla y 1/2 taza de hielo picado.",
   "Licúe hasta obtener una mezcla homogénea.",
   "Ponga en cada vaso 1 cucharada de hielo picado y la mitad de la mezcla de frutas, y agregue 1/4 taza de agua con gas. ¡Revuelva y decore con una rodaja de limón!"],
 "hints": [("Cómo incluir cítricos en una alimentación baja en potasio", CI_ES)],
 "food_choices": ["1 fruta baja en potasio"]},
{
 "title": "موكتيل استوائي", "description": N, "portions": "2", "serving_size": "1 مشروب",
 "ingredients": ["½ كوب أناناس ناضج، مقطع شرائح بسمك ½ بوصة", "½ كوب مانجو مقطعة مكعبات صغيرة", "1 ملعقة كبيرة عصير ليمون أخضر طازج",
   "¼ ملعقة صغيرة خلاصة الفانيليا", "½ كوب ثلج مجروش", "2 ملعقة كبيرة ثلج مجروش",
   "4 أونصة (½ كوب) مياه فوارة قليلة الصوديوم", "2 شريحة ليمون أخضر للتزيين"],
 "steps": ["ضع الأناناس والمانجو وعصير الليمون وخلاصة الفانيليا و½ كوب ثلج مجروش في الخلاط.",
   "اخلطها حتى يصبح المزيج ناعمًا.",
   "املأ كل كأس بـ 1 ملعقة كبيرة ثلج مجروش ونصف خليط الفاكهة، ثم أضف ¼ كوب مياه فوارة. قلّب وزيّن بشريحة ليمون!"],
 "hints": [("كيف تُدرج الحمضيات في نظام غذائي منخفض البوتاسيوم", CI_AR)],
 "food_choices": ["1 فاكهة منخفضة البوتاسيوم"]}))

# 22 Steak Fajita Salad
LV_ES = """Comer verduras todos los días es una parte muy importante de una alimentación saludable. Las verduras aportan fibra y vitaminas, además de antioxidantes que pueden ayudar a proteger las células del cuerpo y posiblemente prevenir ciertas enfermedades. También son ricas en muchos minerales. Uno de esos minerales es el potasio.

El potasio es un mineral que puede ser dañino si consume más del que sus riñones pueden manejar. Cuando esto ocurre, el nivel de potasio en la sangre puede subir mucho y volverse peligroso. Afortunadamente, hay varias verduras más bajas en potasio. Si tiene enfermedad renal crónica y su médico le ha indicado limitar el consumo de potasio, estas son verduras que puede comer a diario.

Entre las verduras más bajas en potasio están los espárragos, el repollo, la zanahoria, el maíz, el pepino, las lechugas de color más claro, la cebolla y los rábanos. Por lo general, las verduras se consideran un “alimento libre”, es decir, que puede comer todas las que quiera cada día. Aunque muchas verduras son más bajas en potasio, es importante prestar atención al tamaño de la porción. Pregunte a su dietista qué cantidad de estos alimentos debe comer cada día para mejorar su salud y evitar consumir demasiado potasio."""
LV_AR = """تناول الخضار يوميًا جزء مهم جدًا من النظام الغذائي الصحي. فالخضار تضيف الألياف والفيتامينات، إلى جانب مضادات الأكسدة التي قد تساعد على حماية خلايا جسمك وربما الوقاية من بعض الأمراض. كما أنها غنية بكثير من المعادن، ومن هذه المعادن البوتاسيوم.

البوتاسيوم معدن قد يكون ضارًا إذا تناولت منه أكثر مما تستطيع كليتاك التعامل معه. وعندما يحدث ذلك، قد يرتفع مستوى البوتاسيوم في دمك إلى مستوى مرتفع جدًا ويصبح خطيرًا. ولحسن الحظ، هناك عدد من الخضار الأقل في البوتاسيوم. فإذا كنت مصابًا بمرض الكلى المزمن وأخبرك طبيبك بالحد من تناول البوتاسيوم، فهذه خضار يمكنك تناولها يوميًا.

من الخضار الأقل في البوتاسيوم: الهليون والملفوف والجزر والذرة والخيار وأنواع الخس الفاتحة اللون والبصل والفجل. وعادةً ما تُعد الخضار “طعامًا حرًا”، أي يمكنك تناول ما تشاء منها كل يوم. ورغم أن كثيرًا من الخضار أقل في البوتاسيوم، من المهم الانتباه إلى حجم الحصة. اسأل أخصائي التغذية عن الكمية التي ينبغي أن تتناولها من هذه الأطعمة يوميًا لتحسين صحتك مع تجنب الإفراط في البوتاسيوم في نظامك الغذائي."""
SR_ES, SA_ES, DR_ES = "Mezcla de especias", "Ensalada", "Aderezo"
SR_AR, SA_AR, DR_AR = "خلطة التتبيل", "السلطة", "الصلصة"
R.append(rec(4913710, {
 "title": "Ensalada de fajitas de res", "description": N, "portions": "4", "serving_size": "¼ de la receta",
 "ingredients": ["1 libra de bistec de lomo (striploin)",
   (SR_ES, "1 cucharada de aceite de oliva"), (SR_ES, "½ cucharadita de ajo en polvo"), (SR_ES, "½ cucharadita de chile en polvo"),
   (SA_ES, "½ taza de arroz de grano largo, crudo"), (SA_ES, "½ taza de granos de maíz congelados, descongelados"),
   (SA_ES, "1 cucharada de aceite de oliva"), (SA_ES, "½ taza de pimiento rojo en tiras cortas y delgadas"),
   (SA_ES, "½ taza de pimiento verde en tiras cortas y delgadas"), (SA_ES, "½ taza de cebolla amarilla en rodajas"),
   (SA_ES, "4 tazas de lechuga iceberg, lavada y troceada"),
   (DR_ES, "¼ taza de cebollín picado"), (DR_ES, "½ taza de hojas de cilantro, lavadas"), (DR_ES, "1 cucharadita de ajo picado finamente"),
   (DR_ES, "2 cucharadas de jugo de limón"), (DR_ES, "¼ taza de aceite de oliva extra virgen")],
 "steps": ["Frote el bistec con el aceite, el ajo y el chile en polvo. Déjelo adobar en el refrigerador por un mínimo de dos horas o durante toda la noche.",
   "En una sartén a fuego medio-alto, cocine el bistec al término deseado. Resérvelo a temperatura ambiente. Córtelo en tiras delgadas. (También puede usar la parrilla).",
   "En una cacerola, cocine el arroz según las instrucciones. Una vez cocido, mézclelo con el maíz y manténgalo a temperatura ambiente.",
   "En una sartén a fuego medio-alto, saltee los pimientos y la cebolla en aceite de oliva. Retire del fuego y reserve.",
   "Para preparar el aderezo, ponga todos sus ingredientes en un procesador de alimentos y procéselos.",
   "Para armar la ensalada, mezcle la lechuga con el aderezo de cilantro y repártala en cuatro tazones. Cubra con el arroz, los frijoles, los pimientos, la cebolla y el bistec."],
 "hints": [("Disfrute las verduras bajas en potasio", LV_ES)],
 "food_choices": ["2 carne", "2 almidón", "1 verdura baja en potasio", "2 grasa"]},
{
 "title": "سلطة فاهيتا الستيك", "description": N, "portions": "4", "serving_size": "¼ الوصفة",
 "ingredients": ["1 رطل ستيك ستريبلوين (لحم الخاصرة)",
   (SR_AR, "1 ملعقة كبيرة زيت زيتون"), (SR_AR, "½ ملعقة صغيرة ثوم بودرة"), (SR_AR, "½ ملعقة صغيرة مسحوق الفلفل الحار"),
   (SA_AR, "½ كوب أرز طويل الحبة، غير مطبوخ"), (SA_AR, "½ كوب حبوب ذرة مجمدة، مذابة"),
   (SA_AR, "1 ملعقة كبيرة زيت زيتون"), (SA_AR, "½ كوب فلفل رومي أحمر مقطع شرائط قصيرة رفيعة"),
   (SA_AR, "½ كوب فلفل رومي أخضر مقطع شرائط قصيرة رفيعة"), (SA_AR, "½ كوب بصل أصفر مقطع شرائح"),
   (SA_AR, "4 كوب خس آيسبرغ، مغسول ومقطع باليد"),
   (DR_AR, "¼ كوب بصل أخضر مفروم"), (DR_AR, "½ كوب أوراق كزبرة خضراء، مغسولة"), (DR_AR, "1 ملعقة صغيرة ثوم مفروم ناعمًا"),
   (DR_AR, "2 ملعقة كبيرة عصير ليمون"), (DR_AR, "¼ كوب زيت زيتون بكر ممتاز")],
 "steps": ["افرك الستيك بالزيت والثوم ومسحوق الفلفل الحار. اتركه في التتبيلة في الثلاجة لمدة ساعتين على الأقل أو طوال الليل.",
   "في مقلاة على نار متوسطة إلى عالية، اطهُ الستيك حتى درجة النضج المرغوبة. اتركه جانبًا في درجة حرارة الغرفة. قطّعه إلى شرائح رفيعة. (يمكنك أيضًا استخدام الشواية.)",
   "في قدر، اطهُ الأرز حسب التعليمات. وبعد أن ينضج، اخلطه مع الذرة واتركه في درجة حرارة الغرفة.",
   "في مقلاة على نار متوسطة إلى عالية، قلّب الفلفل والبصل في زيت الزيتون. ارفعها عن النار وضعها جانبًا.",
   "لتحضير الصلصة، ضع جميع مكوناتها في محضرة الطعام واخلطها.",
   "لتجميع السلطة، اخلط الخس مع صلصة الكزبرة ووزّعه على أربعة أطباق. ضع فوقه الأرز والفاصوليا والفلفل والبصل والستيك."],
 "hints": [("استمتع بالخضار منخفضة البوتاسيوم", LV_AR)],
 "food_choices": ["2 لحوم", "2 نشويات", "1 خضار منخفضة البوتاسيوم", "2 دهون"]}))

# 23 Green Bean Slaw
SL_ES, VI_ES = "Ensalada", "Vinagreta"
SL_AR, VI_AR = "السلطة", "صلصة الفينيغريت"
R.append(rec(4934943, {
 "title": "Ensalada crujiente de ejotes", "description": N, "portions": "4", "serving_size": "1/4 de la receta",
 "ingredients": [(SL_ES, "1 taza de repollo morado en tiras finas"), (SL_ES, "2 tazas de ejotes, sin puntas y cortados en trozos de 1 pulgada"),
   (SL_ES, "1/4 taza de chalota en aros finos"), (SL_ES, "1/2 taza de arúgula baby"),
   (VI_ES, "1 cucharada de cebollino finamente picado"), (VI_ES, "1 cucharadita de mostaza Dijon"), (VI_ES, "1 cucharadita de miel"),
   (VI_ES, "1 cucharada de vinagre de sidra"), (VI_ES, "2 cucharadas de aceite de oliva"), (VI_ES, "1/8 cucharadita de pimienta negra molida")],
 "steps": ["En una cacerola, ponga a hervir agua y cocine los ejotes (aproximadamente 5 minutos). Enjuáguelos de inmediato con agua fría para detener la cocción. Los ejotes deben quedar todavía crujientes.",
   "En una ensaladera, mezcle los ingredientes de la ensalada: el repollo, los ejotes, los aros de chalota y la arúgula.",
   "En un tazón pequeño, bata los ingredientes de la vinagreta: el cebollino, la mostaza, la miel, el vinagre, el aceite de oliva y la pimienta negra molida.",
   "Vierta la vinagreta sobre la ensalada de ejotes y mezcle para integrar."],
 "hints": ["Sírvala como guarnición de carnes o pescado.",
   "Agregue una proteína, como bistec en rebanadas o huevo cocido, y conviértala en una comida completa."],
 "food_choices": ["1 verdura", "1 grasa"]},
{
 "title": "سلطة الفاصوليا الخضراء المقرمشة", "description": N, "portions": "4", "serving_size": "¼ الوصفة",
 "ingredients": [(SL_AR, "1 كوب ملفوف أحمر مقطع شرائح رفيعة"), (SL_AR, "2 كوب فاصوليا خضراء، منزوعة الأطراف ومقطعة قطعًا بطول 1 بوصة"),
   (SL_AR, "¼ كوب كراث أندلسي (شالوت) مقطع حلقات رفيعة"), (SL_AR, "½ كوب جرجير صغير"),
   (VI_AR, "1 ملعقة كبيرة ثوم معمّر (ثوم الحلفاء) مفروم ناعمًا"), (VI_AR, "1 ملعقة صغيرة خردل ديجون"), (VI_AR, "1 ملعقة صغيرة عسل"),
   (VI_AR, "1 ملعقة كبيرة خل التفاح"), (VI_AR, "2 ملعقة كبيرة زيت زيتون"), (VI_AR, "⅛ ملعقة صغيرة فلفل أسود مطحون")],
 "steps": ["في قدر، اغلِ الماء واسلق الفاصوليا الخضراء (لمدة 5 دقائق تقريبًا). اشطفها فورًا بالماء البارد لإيقاف الطهي. يجب أن تبقى الفاصوليا مقرمشة.",
   "في وعاء التقديم، اخلط مكونات السلطة: الملفوف والفاصوليا الخضراء وحلقات الشالوت والجرجير.",
   "في وعاء صغير، اخفق مكونات الفينيغريت معًا: الثوم المعمّر والخردل والعسل والخل وزيت الزيتون والفلفل الأسود المطحون.",
   "اسكب الفينيغريت فوق سلطة الفاصوليا الخضراء وقلّب لتمتزج."],
 "hints": ["قدّمها طبقًا جانبيًا مع اللحوم أو السمك.",
   "أضف إليها بروتينًا، مثل شرائح الستيك أو البيض المسلوق، لتصبح وجبة كاملة."],
 "food_choices": ["1 خضار", "1 دهون"]}))

# 24 Low-Phosphorus Pizza
R.append(rec(4936056, {
 "title": "Pizza baja en fósforo", "description": "Ideal para los niños y adecuada para los riñones", "portions": "4", "serving_size": N,
 "ingredients": ["1 taza de queso vegano rallado", "(como Daiya)", "4 panes pita blancos pequeños", "1 pimiento rojo picado en cubitos",
   "8 tomates cherry, cortados en cuartos", "1 cucharada de aceite de oliva"],
 "steps": ["Barnice el pimiento picado y los tomates con aceite de oliva.",
   "Reparta el queso, el pimiento y el tomate de manera uniforme entre los 4 panes pita.",
   "Tueste en el asador del horno (broil) o en un horno tostador durante 5 minutos, o hasta que el queso se derrita."],
 "hints": [], "food_choices": []},
{
 "title": "بيتزا قليلة الفوسفور", "description": "مناسبة للأطفال ولمرضى الكلى", "portions": "4", "serving_size": N,
 "ingredients": ["1 كوب جبن نباتي مبشور", "(مثل Daiya)", "4 خبز بيتا أبيض صغير", "1 فلفل رومي أحمر مقطع مكعبات صغيرة",
   "8 طماطم كرزية، مقطعة أرباعًا", "1 ملعقة كبيرة زيت زيتون"],
 "steps": ["ادهن الفلفل الرومي المقطع والطماطم بزيت الزيتون.",
   "وزّع الجبن والفلفل الرومي والطماطم بالتساوي على 4 أرغفة بيتا.",
   "حمّصها تحت شواية الفرن العلوية أو في فرن التحميص الصغير لمدة 5 دقائق، أو حتى يذوب الجبن."],
 "hints": [], "food_choices": []}))

# 25 General Tao Tofu
SN_ES = """Si anda con prisa, necesita un bocado rápido o le da hambre por la noche, los refrigerios pueden formar parte de su alimentación adecuada para los riñones. La mayor parte del potasio de su alimentación debe provenir del desayuno, el almuerzo y la cena. Tenga a mano refrigerios bajos en potasio para tomar algo rápido sin pasarse de su límite diario. Elija entre los distintos grupos de alimentos para que sus refrigerios sean variados. Tenga en cuenta también que los alimentos muy procesados contienen aditivos, sal y posibles fuentes ocultas de potasio. Asegúrese de leer la etiqueta para identificar estos alimentos.

Tome una pieza de fruta o un puñado de verduras como opción baja en calorías y en potasio. Elija una manzana mediana, media taza de uvas o un puñado pequeño de palitos de zanahoria y pimiento rojo. Si prefiere un refrigerio crujiente, elija una porción de galletas de animalitos, tortitas de arroz o pretzels sin sal. Una porción pequeña de galletas de vainilla, gelatina o una refrescante paleta helada son opciones dulces. Agregue más proteína a su refrigerio eligiendo un huevo duro, una rebanada de carne fría o una malteada nutricional adecuada para los riñones."""
SN_AR = """إذا كنت على عجلة من أمرك، أو تحتاج إلى لقمة سريعة، أو شعرت بالجوع في وقت متأخر من الليل، فيمكن إدراج الوجبات الخفيفة ضمن نظامك الغذائي المناسب لمرضى الكلى. ينبغي أن يأتي معظم البوتاسيوم في نظامك الغذائي من وجبات الإفطار والغداء والعشاء. احتفظ بوجبات خفيفة منخفضة البوتاسيوم في متناول يدك لتتناول شيئًا سريعًا دون تجاوز حدك اليومي. واختر من مجموعات غذائية مختلفة لتبقى وجباتك الخفيفة متنوعة. وتذكر أيضًا أن الأطعمة عالية المعالجة تحتوي على إضافات وملح ومصادر خفية محتملة للبوتاسيوم، لذا احرص على قراءة الملصق للتعرف على هذه الأطعمة.

تناول ثمرة فاكهة أو حفنة من الخضار كخيار منخفض السعرات والبوتاسيوم. اختر تفاحة متوسطة، أو نصف كوب من العنب، أو حفنة صغيرة من أصابع الجزر والفلفل الأحمر. وإذا كنت تفضل وجبة خفيفة مقرمشة، فاكتفِ بحصة من بسكويت الحيوانات، أو كعك الأرز المنفوخ، أو البريتزل غير المملح. وتُعد الحصة الصغيرة من بسكويت الفانيليا الرقيق أو الجيلاتين أو المثلجات المنعشة على عود خيارات حلوة. وأضف مزيدًا من البروتين إلى وجبتك الخفيفة باختيار بيضة مسلوقة، أو شريحة من اللحوم الباردة، أو مشروب غذائي مناسب لمرضى الكلى."""
SC_ES, SF_ES = "Salsa", "Salteado"
SC_AR, SF_AR = "الصلصة", "التقليب السريع"
R.append(rec(4937676, {
 "title": "Tofu del General Tao", "description": N, "portions": "5", "serving_size": "1/5 de la receta",
 "ingredients": [(SC_ES, "¼ taza de caldo de verduras sin sal añadida*"), (SC_ES, "2 cucharadas de azúcar"),
   (SC_ES, "2 cucharadas de salsa de soya baja en sodio"), (SC_ES, "2 cucharadas de vinagre de arroz sin sazonar"),
   (SC_ES, "2 cucharadas de cátsup"), (SC_ES, "1 cucharadita de fécula de maíz"), (SC_ES, "1 cucharadita de salsa Sriracha"),
   (SF_ES, "1 libra de tofu firme, secado con toallas de papel y cortado en cubos pequeños"), (SF_ES, "2 cucharadas de fécula de maíz"),
   (SF_ES, "2 cucharadas de aceite de canola"), (SF_ES, "4 cebollines picados (reserve un poco para decorar)"),
   (SF_ES, "1 cucharadita de jengibre fresco picado finamente"), (SF_ES, "2 dientes de ajo picados finamente")],
 "steps": ["En un tazón pequeño, mezcle todos los ingredientes de la salsa y reserve.",
   "En un tazón grande, mezcle los cubos de tofu con la fécula de maíz. Coloque los cubos en un plato y reserve.",
   "En una sartén antiadherente o wok, caliente el aceite a fuego medio-alto. Fría el tofu por tandas hasta que todos los cubos estén ligeramente dorados.",
   "Cubra un plato con toalla de papel y pase el tofu al plato para que absorba el exceso de aceite.",
   "Agregue el cebollín, el jengibre y el ajo a la sartén o wok y fríalos durante 1–2 minutos. Agregue un poco de aceite si es necesario.",
   "Agregue la salsa y deje que todo hierva, revolviendo constantemente (aproximadamente 2 minutos).",
   "Agregue el tofu y revuelva hasta que todos los ingredientes estén calientes y listos para servir.",
   "Sirva con arroz al vapor."],
 "hints": ["* Busque caldo bajo o reducido en sodio que contenga 200 mg de sodio o menos por porción de 1 taza. Evite el caldo bajo en sodio que contenga cloruro de potasio, porque es muy alto en potasio.",
   "El tofu es una excelente fuente vegetariana de proteína. Puede usar otras verduras y fuentes de proteína permitidas en este salteado. Pruebe con pimientos, ejotes, pollo o camarones.",
   ("Refrigerios bajos en potasio", SN_ES)],
 "food_choices": ["1 carne", "½ almidón", "1 verdura baja en potasio", "1 grasa"]},
{
 "title": "توفو الجنرال تاو", "description": N, "portions": "5", "serving_size": "1/5 الوصفة",
 "ingredients": [(SC_AR, "¼ كوب مرق خضار بدون ملح مضاف*"), (SC_AR, "2 ملعقة كبيرة سكر"),
   (SC_AR, "2 ملعقة كبيرة صلصة صويا قليلة الصوديوم"), (SC_AR, "2 ملعقة كبيرة خل أرز غير متبل"),
   (SC_AR, "2 ملعقة كبيرة كاتشب"), (SC_AR, "1 ملعقة صغيرة نشا الذرة"), (SC_AR, "1 ملعقة صغيرة صلصة Sriracha"),
   (SF_AR, "1 رطل توفو صلب، مجفف بالمناشف الورقية ومقطع مكعبات صغيرة"), (SF_AR, "2 ملعقة كبيرة نشا الذرة"),
   (SF_AR, "2 ملعقة كبيرة زيت الكانولا"), (SF_AR, "4 عود بصل أخضر مفروم (احتفظ بجزء منه للتزيين)"),
   (SF_AR, "1 ملعقة صغيرة زنجبيل طازج مفروم ناعمًا"), (SF_AR, "2 فص ثوم مفروم ناعمًا")],
 "steps": ["في وعاء صغير، اخلط جميع مكونات الصلصة وضعها جانبًا.",
   "في وعاء كبير، اخلط مكعبات التوفو مع نشا الذرة. ضع المكعبات في طبق واتركها جانبًا.",
   "في مقلاة غير لاصقة أو مقلاة ووك، سخّن الزيت على نار متوسطة إلى عالية. اقلِ التوفو على دفعات حتى تكتسب جميع المكعبات لونًا ذهبيًا خفيفًا.",
   "بطّن طبقًا بمنشفة ورقية وانقل التوفو إليه لامتصاص الزيت الزائد.",
   "أضف البصل الأخضر والزنجبيل والثوم إلى المقلاة أو الووك وقلّبها لمدة 1–2 دقيقة. أضف قليلًا من الزيت عند الحاجة.",
   "أضف الصلصة واتركها حتى تغلي مع التقليب المستمر (لمدة 2 دقيقة تقريبًا).",
   "أضف التوفو وقلّب حتى تسخن جميع المكونات وتصبح جاهزة للتقديم.",
   "قدّمه مع الأرز المطهو على البخار."],
 "hints": ["* ابحث عن مرق قليل الصوديوم أو مخفض الصوديوم يحتوي على 200 مليغرام صوديوم أو أقل لكل حصة مقدارها 1 كوب. وتجنب المرق قليل الصوديوم الذي يحتوي على كلوريد البوتاسيوم، فهو مرتفع جدًا في البوتاسيوم.",
   "التوفو مصدر نباتي رائع للبروتين. ويمكنك استخدام خضار ومصادر بروتين أخرى مسموح بها في هذا الطبق. جرّب الفلفل الرومي أو الفاصوليا الخضراء أو الدجاج أو الروبيان.",
   ("وجبات خفيفة منخفضة البوتاسيوم", SN_AR)],
 "food_choices": ["1 لحوم", "½ نشويات", "1 خضار منخفضة البوتاسيوم", "1 دهون"]}))

# 26 Red Pepper Couscous Salad
CO_ES = """Elegir una gran variedad de fuentes de carbohidratos debe formar parte de una alimentación adecuada para los riñones. En promedio, estos alimentos aportan aproximadamente la mitad de sus calorías diarias y son necesarios para producir la energía que su cuerpo necesita. Muchos platillos incluyen granos como arroz, pasta u otros fideos para aportar estos carbohidratos. Estos alimentos pueden contener distintas cantidades de potasio según los ingredientes y condimentos que se usen. Leer las etiquetas y determinar el tamaño de porción correcto puede ayudarle a elegir distintos granos y mantener sus metas de una alimentación más baja en potasio.

El cuscús, que se come caliente o frío, se puede usar en recetas como fuente de granos o de carbohidratos. Aunque su forma puede parecer de arroz o de semilla, el cuscús en realidad es una pasta pequeña. Suele ser de color amarillo y se mezcla bien con otros sabores del platillo o aporta un sabor ligero, con notas a nuez. El cuscús se elabora con sémola y es una buena fuente de fibra y proteína. Además, una porción de ¼ taza de cuscús seco también cabe en una alimentación adecuada para los riñones, ya que aporta solo 150 mg de potasio y 10 mg de sodio. Al probar distintas recetas de cuscús, sírvalo acompañado de una fuente de proteína, mezclado con verduras asadas o como complemento de ensaladas verdes."""
CO_AR = """ينبغي أن يكون اختيار مصادر متنوعة من الكربوهيدرات جزءًا من النظام الغذائي المناسب لمرضى الكلى. ففي المتوسط، توفر هذه الأطعمة نحو نصف سعراتك الحرارية اليومية، وهي ضرورية لإنتاج الطاقة التي يحتاجها جسمك. وتتضمن أطباق كثيرة حبوبًا مثل الأرز أو المعكرونة أو أنواع النودلز الأخرى لتوفير هذه الكربوهيدرات. وقد تحتوي هذه الأطعمة على كميات مختلفة من البوتاسيوم حسب المكونات المستخدمة والتوابل المضافة. ويمكن أن تساعدك قراءة الملصقات وتحديد حجم الحصة الصحيح على اختيار حبوب متنوعة والحفاظ على أهداف نظامك الغذائي الأقل في البوتاسيوم.

يمكن استخدام الكسكس، الذي يؤكل دافئًا أو باردًا، في الوصفات كمصدر للحبوب أو الكربوهيدرات. ورغم أن شكله قد يشبه الأرز أو البذور، فإن الكسكس في الحقيقة نوع من المعكرونة الصغيرة. وغالبًا ما يكون لونه أصفر، ويمتزج جيدًا مع النكهات الأخرى في الطبق أو يضفي مذاقًا خفيفًا يشبه المكسرات. يُصنع الكسكس من السميد، وهو مصدر جيد للألياف والبروتين. كما أن حصة مقدارها ¼ كوب من الكسكس الجاف تناسب النظام الغذائي لمرضى الكلى، إذ لا توفر سوى 150 مليغرامًا من البوتاسيوم و10 مليغرامات من الصوديوم. وعند تجربة وصفات الكسكس المختلفة، قدّمه مع مصدر للبروتين، أو مخلوطًا مع الخضار المشوية، أو كإضافة إلى السلطات الخضراء."""
R.append(rec(4957725, {
 "title": "Ensalada de cuscús con pimiento rojo", "description": N, "portions": "2", "serving_size": "½ de la receta",
 "ingredients": ["½ taza de cuscús perla, crudo", "½ taza de pimientos rojos asados*, cortados en trozos pequeños",
   "¼ taza de perejil liso picado", "2 cucharadas de cebolla morada picada en cubitos", "1 cucharada de ajo picado finamente",
   "1 cucharadita de ralladura de limón", "1 cucharada de jugo de limón", "1 cucharada de aceite de oliva",
   "1/8 cucharadita de pimienta negra"],
 "steps": ["Cocine el cuscús según las instrucciones del paquete, sin agregar la sal. Pase el cuscús cocido (tibio o frío) a un plato y póngalo en el refrigerador para que se enfríe.",
   "En un tazón, mezcle el cuscús, los pimientos, el perejil, la cebolla morada, el ajo, la ralladura de limón, el jugo de limón y el aceite de oliva. Sazone con pimienta al gusto."],
 "hints": ["* Elija el producto con el menor contenido de sodio",
   "Esta guarnición puede convertirse en una comida completa si le agrega una proteína, como pollo, pescado o carne en rebanadas.",
   ("Tipos y usos del cuscús", CO_ES)],
 "food_choices": ["2 ½ almidón", "1 verdura baja en potasio", "1 grasa"]},
{
 "title": "سلطة الكسكس بالفلفل الأحمر", "description": N, "portions": "2", "serving_size": "½ الوصفة",
 "ingredients": ["½ كوب كسكس لؤلؤي (مغربية) غير مطبوخ", "½ كوب فلفل رومي أحمر مشوي*، مقطع قطعًا صغيرة",
   "¼ كوب بقدونس مسطح الأوراق مفروم", "2 ملعقة كبيرة بصل أحمر مقطع مكعبات صغيرة", "1 ملعقة كبيرة ثوم مفروم ناعمًا",
   "1 ملعقة صغيرة برش قشر الليمون", "1 ملعقة كبيرة عصير ليمون", "1 ملعقة كبيرة زيت زيتون",
   "⅛ ملعقة صغيرة فلفل أسود"],
 "steps": ["اطهُ الكسكس حسب التعليمات المدونة على العبوة مع الاستغناء عن الملح. انقل الكسكس المطبوخ (دافئًا أو باردًا) إلى طبق وضعه في الثلاجة ليبرد.",
   "في وعاء، اخلط الكسكس والفلفل والبقدونس والبصل الأحمر والثوم وبرش قشر الليمون وعصير الليمون وزيت الزيتون. تبّل بالفلفل حسب الرغبة."],
 "hints": ["* اختر المنتج الأقل محتوى من الصوديوم",
   "يمكن أن يتحول هذا الطبق الجانبي إلى وجبة كاملة بإضافة بروتين، مثل شرائح الدجاج أو السمك أو اللحم.",
   ("أنواع الكسكس واستخداماته", CO_AR)],
 "food_choices": ["2½ نشويات", "1 خضار منخفضة البوتاسيوم", "1 دهون"]}))

# 27 Basmati Summer Salad
VP_ES = """Hay muchos aspectos a tener en cuenta en una alimentación adecuada para los riñones. Uno de ellos es la cantidad y el tipo de proteína. En general, las personas con enfermedad renal crónica (ERC) en etapas tempranas deben consumir menos proteína para disminuir la carga de trabajo de los riñones. Una buena manera de reducir el consumo de proteína es agregar a su alimentación más proteínas de origen vegetal. Estos alimentos suelen aportar una buena cantidad de calorías con un contenido de proteína mucho menor que la proteína de origen animal. Comer proteínas de origen vegetal también puede ayudar a proteger los riñones y a retrasar el deterioro de la función renal.

Los garbanzos son una excelente fuente de proteína vegetal y de fibra. También son ricos en vitaminas y minerales, como el folato y el hierro. Por lo general son económicos y se consiguen tanto enlatados como secos. Si los compra enlatados, busque los que digan “sin sal añadida” o “bajo en sodio”. Los garbanzos se pueden agregar a una gran variedad de platillos, como ensaladas, sopas, guisos, chili, hamburguesas y tacos. También se pueden machacar para preparar hummus o asar en el horno para obtener un refrigerio crujiente. Al cocinarlos, agregue cebolla, ajo, hierbas y especias para darles más sabor."""
VP_AR = """هناك أمور كثيرة ينبغي مراعاتها في النظام الغذائي المناسب لمرضى الكلى، ومن أهمها كمية البروتين ونوعه. وبوجه عام، ينبغي للمصابين بمرض الكلى المزمن في مراحله المبكرة تناول كمية أقل من البروتين لتخفيف العبء على الكلى. ومن الطرق الجيدة لتقليل البروتين إضافة مزيد من البروتينات النباتية إلى نظامك الغذائي. فهذه الأطعمة توفر عادةً كمية جيدة من السعرات الحرارية مع محتوى أقل بكثير من البروتين مقارنة بالبروتين من المصادر الحيوانية. كما أن تناول البروتينات النباتية قد يساعد على حماية الكلى وإبطاء تراجع وظائفها.

الحمص مصدر رائع للبروتين النباتي والألياف. كما أنه غني بالفيتامينات والمعادن مثل حمض الفوليك والحديد. وهو عادةً رخيص الثمن ومتوفر معلبًا ومجففًا. وعند شرائه معلبًا، ابحث عن العلب المكتوب عليها “بدون ملح مضاف” أو “قليل الصوديوم”. ويمكن إضافة الحمص إلى أطباق متنوعة مثل السلطات والحساء واليخنات وأطباق التشيلي والبرغر والتاكو. ويمكن أيضًا هرسه لتحضير الحمص بالطحينة (هُمُّس) أو تحميصه في الفرن ليصبح وجبة خفيفة مقرمشة. وعند طهيه، أضف البصل والثوم والأعشاب والبهارات لمزيد من النكهة."""
R.append(rec(4958092, {
 "title": "Ensalada de verano con arroz basmati", "description": N, "portions": "4", "serving_size": "¼ de la receta",
 "ingredients": ["1 lata (15.5 onzas) de garbanzos sin sal añadida, escurridos y enjuagados", "1/2 taza de arroz basmati, crudo",
   "1 taza de pepino pelado y en cubos", "1 taza de apio picado", "1 taza de mandarinas*, cortadas en trozos pequeños",
   "1/2 taza de cebolla morada picada finamente", "¼ taza de cilantro fresco picado", "1 cucharada de aceite de oliva",
   "1 cucharada de jugo de limón verde", "1 cucharadita de ralladura de limón verde", "1/2 taza de nueces troceadas",
   "Pimienta negra al gusto"],
 "steps": ["En un tazón grande, remoje los garbanzos en 4 cuartos de galón de agua durante 12 horas para reducir su contenido de potasio. Escúrralos y enjuáguelos con agua una vez más. Reserve.",
   "En una cacerola, cocine el arroz según las instrucciones del paquete. Deje enfriar el arroz en la cacerola destapada.",
   "Mientras se cocina el arroz, mezcle en un tazón grande los ingredientes de la ensalada: los garbanzos, el pepino, el apio, las mandarinas, la cebolla y el cilantro. Agregue el arroz y mezcle suavemente.",
   "En un tazón pequeño, bata los ingredientes del aderezo: el aceite de oliva, el jugo y la ralladura de limón. Vierta el aderezo sobre la ensalada, agregue pimienta al gusto y mezcle suavemente. Decore con las nueces.",
   "Refrigere durante 1 hora antes de servir."],
 "hints": ["* frescas o enlatadas",
   "Consejo: Escurra y enjuague los productos enlatados para reducir el sodio.",
   "* Puede ser más bajo si se remojan",
   ("Proteínas de origen vegetal", VP_ES)],
 "food_choices": ["1 proteína", "2 almidón", "1 fruta baja en potasio", "2 grasa"]},
{
 "title": "سلطة الصيف بأرز البسمتي", "description": N, "portions": "4", "serving_size": "¼ الوصفة",
 "ingredients": ["1 علبة (15.5 أونصة) حمص بدون ملح مضاف، مصفى ومغسول", "½ كوب أرز بسمتي غير مطبوخ",
   "1 كوب خيار مقشر ومقطع مكعبات", "1 كوب كرفس مفروم", "1 كوب يوسفي*، مقطع قطعًا صغيرة",
   "½ كوب بصل أحمر مفروم ناعمًا", "¼ كوب كزبرة خضراء طازجة مفرومة", "1 ملعقة كبيرة زيت زيتون",
   "1 ملعقة كبيرة عصير ليمون أخضر", "1 ملعقة صغيرة برش قشر الليمون الأخضر", "½ كوب جوز (عين الجمل) مجروش",
   "فلفل أسود حسب الرغبة"],
 "steps": ["في وعاء كبير، انقع الحمص في 4 كوارت من الماء لمدة 12 ساعة لتقليل محتواه من البوتاسيوم. صفِّ الحمص واشطفه بالماء مرة أخرى. ضعه جانبًا.",
   "في قدر، اطهُ الأرز حسب التعليمات المدونة على العبوة. اترك الأرز ليبرد في القدر دون غطاء.",
   "أثناء طهي الأرز، اخلط مكونات السلطة في وعاء كبير: الحمص والخيار والكرفس واليوسفي والبصل والكزبرة. أضف الأرز وقلّب برفق.",
   "في وعاء صغير، اخفق مكونات الصلصة معًا: زيت الزيتون وعصير الليمون الأخضر وبرش قشره. اسكب الصلصة فوق السلطة، وأضف الفلفل حسب الرغبة، وقلّب برفق. زيّنها بالجوز.",
   "ضعها في الثلاجة لمدة 1 ساعة قبل التقديم."],
 "hints": ["* طازج أو معلب",
   "نصيحة: صفِّ المنتجات المعلبة واشطفها لتقليل الصوديوم.",
   "* يمكن أن تكون الكمية أقل مع النقع",
   ("البروتينات النباتية", VP_AR)],
 "food_choices": ["1 بروتين", "2 نشويات", "1 فاكهة منخفضة البوتاسيوم", "2 دهون"]}))

# 28 Fine Fish Stew
FM_ES = """Comer la cantidad adecuada de proteína es fundamental para mantener músculos sanos y apoyar muchas funciones del cuerpo. El pescado es una buena fuente de proteína y una excelente alternativa a la carne roja, ya que ofrece una gran variedad de beneficios para la salud de las personas con enfermedad renal crónica. El pescado que contiene ácidos grasos omega-3 es especialmente saludable. La American Heart Association recomienda comer pescado al menos dos veces por semana como parte de una alimentación saludable. Sin embargo, el pescado es rico en potasio, por lo que el tamaño de la porción es importante para evitar consumir demasiado potasio cuando se sigue una alimentación baja en potasio. Trabajar con un dietista nutricionista registrado es una excelente manera de saber qué tipo y qué cantidad de pescado puede incluir con seguridad en su alimentación.

Existen docenas de variedades de pescado, con muchos sabores y formas de preparación que se adaptan a cualquier gusto. Puede comprar el pescado fresco o congelado. El pescado congelado suele costar menos que el fresco y puede ser el más fresco que usted compre, ya que se congela inmediatamente después de pescarlo. El pescado es fácil de preparar y se puede cocinar en el microondas, al horno, asado en el asador, al vapor o en sartén. La pimienta, el limón o un poco de hierbas le dan buen sabor sin agregar mucho potasio. Sirva el pescado acompañado de arroz o pasta, sobre una cama de hojas verdes o como relleno de tacos."""
FM_AR = """إن تناول الكمية المناسبة من البروتين أمر بالغ الأهمية للحفاظ على عضلات سليمة ودعم كثير من وظائف الجسم. والسمك مصدر جيد للبروتين وبديل رائع للحوم الحمراء، إذ يوفر مجموعة واسعة من الفوائد الصحية لمرضى الكلى المزمن. والأسماك التي تحتوي على أحماض أوميغا-3 الدهنية صحية بشكل خاص. وتوصي جمعية القلب الأمريكية (American Heart Association) بتناول السمك مرتين على الأقل في الأسبوع ضمن نظام غذائي صحي. لكن السمك غني بالبوتاسيوم، ولذلك فإن حجم الحصة مهم لتجنب الإفراط في البوتاسيوم عند اتباع نظام غذائي منخفض البوتاسيوم. ويُعد العمل مع أخصائي تغذية معتمد طريقة رائعة لمعرفة نوع السمك وكميته التي يمكن إدراجها بأمان في نظامك الغذائي.

تتوفر عشرات الأنواع من الأسماك بنكهات كثيرة وطرق طهي متعددة تناسب جميع الأذواق. ويمكنك شراء السمك طازجًا أو مجمدًا. وغالبًا ما يكون السمك المجمد أرخص من الطازج، وقد يكون أكثر الأسماك طزاجة يمكنك شراؤها لأنه يُجمَّد فور صيده. والسمك سهل التحضير ويمكن طهيه في الميكروويف أو خبزه في الفرن أو شويه تحت الشواية أو طهيه على البخار أو قليه في المقلاة. ويضفي الفلفل أو الليمون أو رشة من الأعشاب نكهة جيدة دون إضافة الكثير من البوتاسيوم. قدّم السمك المطبوخ مع طبق جانبي من الأرز أو المعكرونة، أو على طبقة من السلطة الخضراء، أو كحشوة للتاكو."""
R.append(rec(4964422, {
 "title": "Guiso fino de pescado", "description": N, "portions": "4", "serving_size": "¼ de la receta",
 "ingredients": ["2 cucharadas de aceite de oliva", "1/2 taza de puerro, lavado y picado", "2 dientes de ajo picados finamente",
   "3/4 taza de calabacín picado en cubitos", "1/2 taza de granos de maíz congelados", "3 tazas de caldo de pollo sin sal añadida*",
   "1 taza de orzo crudo", "2 cucharadas de ralladura de limón", "2 cucharaditas de albahaca seca",
   "1/4 cucharadita de pimienta negra molida", "12 onzas de eglefino congelado, descongelado", "1/4 taza de perejil fresco picado"],
 "steps": ["En una sartén grande, caliente el aceite de oliva a fuego medio. Agregue el puerro y el ajo y saltéelos hasta que el puerro empiece a ablandarse. Agregue el calabacín y el maíz y siga salteando.",
   "Cuando las verduras empiecen a ablandarse, agregue el caldo de pollo y suba el fuego para que la mezcla hierva.",
   "Incorpore el orzo crudo, la ralladura de limón, la albahaca y la pimienta a la mezcla hirviendo.",
   "Coloque el pescado encima y baje el fuego. Cocine el guiso a fuego lento, sin tapar, aproximadamente 12 a 15 minutos o hasta que el pescado y el orzo estén completamente cocidos y se haya absorbido la mayor parte del líquido.",
   "Apague el fuego. Coloque el pescado en los platos. Agregue el perejil fresco a la mezcla de orzo, divida en porciones y sirva de inmediato."],
 "hints": ["* Busque caldo bajo o reducido en sodio que contenga 200 mg de sodio o menos por porción de 1 taza. Evite el caldo bajo en sodio que contenga cloruro de potasio.",
   "TENGA EN CUENTA: Esta receta es más alta en potasio y el tamaño de la porción es importante. Consulte con su dietista registrado para saber cómo puede incluir esta receta en su alimentación.",
   ("Distintas formas de preparar el pescado", FM_ES)],
 "food_choices": ["2 1/2 proteína magra", "3 almidón", "1 verdura baja en potasio"]},
{
 "title": "يخنة السمك الفاخرة", "description": N, "portions": "4", "serving_size": "¼ الوصفة",
 "ingredients": ["2 ملعقة كبيرة زيت زيتون", "½ كوب كراث، مغسول ومفروم", "2 فص ثوم مفروم ناعمًا",
   "¾ كوب كوسا مقطعة مكعبات صغيرة", "½ كوب حبوب ذرة مجمدة", "3 كوب مرق دجاج بدون ملح مضاف*",
   "1 كوب أورزو غير مطبوخ", "2 ملعقة كبيرة برش قشر الليمون", "2 ملعقة صغيرة ريحان مجفف",
   "¼ ملعقة صغيرة فلفل أسود مطحون", "12 أونصة سمك الحدوق (هادوك) مجمد، مذاب", "¼ كوب بقدونس طازج مفروم"],
 "steps": ["في مقلاة كبيرة، سخّن زيت الزيتون على نار متوسطة. أضف الكراث والثوم وقلّبهما حتى يبدأ الكراث في الطراوة. أضف الكوسا والذرة واستمر في التقليب.",
   "عندما تبدأ الخضار في الطراوة، أضف مرق الدجاج وارفع النار حتى يغلي الخليط.",
   "أضف الأورزو غير المطبوخ وبرش قشر الليمون والريحان والفلفل إلى الخليط المغلي وقلّب.",
   "ضع السمك على الوجه واخفض النار. اترك يخنة السمك على نار هادئة دون غطاء لمدة 12 إلى 15 دقيقة تقريبًا أو حتى ينضج السمك والأورزو تمامًا ويُمتص معظم السائل.",
   "أطفئ النار. ضع السمك في أطباق التقديم. أضف البقدونس الطازج إلى خليط الأورزو، ووزّعه في حصص وقدّمه فورًا."],
 "hints": ["* ابحث عن مرق قليل الصوديوم أو مخفض الصوديوم يحتوي على 200 مليغرام صوديوم أو أقل لكل حصة مقدارها 1 كوب. وتجنب المرق قليل الصوديوم الذي يحتوي على كلوريد البوتاسيوم.",
   "يرجى الانتباه: هذه الوصفة أعلى في البوتاسيوم، وحجم الحصة مهم. استشر أخصائي التغذية المعتمد لمعرفة كيف يمكن إدراج هذه الوصفة في نظامك الغذائي.",
   ("طرق مختلفة لتحضير السمك", FM_AR)],
 "food_choices": ["2½ بروتين قليل الدهون", "3 نشويات", "1 خضار منخفضة البوتاسيوم"]}))

# 29 Watermelon Strawberry Sorbet
WM_ES = "Las frutas forman parte de una alimentación saludable para todos. Sin embargo, para las personas con enfermedad renal crónica, muchas frutas contienen demasiado potasio para comerlas a diario. Por lo general, los melones contienen mucho potasio, pero la sandía es la que menos tiene de todos. Para comparar, ½ taza de sandía en cubitos contiene 85 miligramos de potasio, mientras que la misma cantidad de melón cantalupo contiene 208 miligramos y la de melón verde (honeydew) contiene 194 miligramos de potasio.[1] En otras palabras, la sandía contiene menos de la mitad del potasio que otros melones. Recuerde siempre que un alimento más bajo en potasio puede aportar demasiado potasio si come mucho de él, y que un alimento más alto en potasio puede caber en su alimentación si come solo una pequeña cantidad. Pregunte a su dietista qué cantidad de sandía es adecuada para usted."
WM_AR = "الفواكه جزء من النظام الغذائي الصحي للجميع. لكن بالنسبة لمرضى الكلى المزمن، تحتوي فواكه كثيرة على كمية كبيرة جدًا من البوتاسيوم تمنع تناولها يوميًا. وعادةً ما يحتوي الشمام بأنواعه على كمية كبيرة من البوتاسيوم، لكن البطيخ هو الأقل احتواءً عليه من بينها جميعًا. وللمقارنة، يحتوي ½ كوب من البطيخ المقطع مكعبات على 85 مليغرامًا من البوتاسيوم، بينما تحتوي الكمية نفسها من الشمام (الكانتالوب) على 208 مليغرامات، ومن شمام الهوني ديو على 194 مليغرامًا من البوتاسيوم.[1] وبعبارة أخرى، يحتوي البطيخ على أقل من نصف كمية البوتاسيوم مقارنة بأنواع الشمام الأخرى. وتذكّر دائمًا أن الطعام الأقل في البوتاسيوم قد يمدك بكمية كبيرة من البوتاسيوم إذا أكثرت منه، وأن الطعام الأعلى في البوتاسيوم قد يناسب نظامك الغذائي إذا تناولت منه كمية صغيرة فقط. اسأل أخصائي التغذية عن كمية البطيخ المناسبة لك."
R.append(rec(4964931, {
 "title": "Sorbete de sandía y fresa", "description": N, "portions": "5", "serving_size": "1/5 de la receta",
 "ingredients": ["2 tazas de sandía en cubitos de ½ pulgada, congelada", "1 taza de fresas congeladas", "1 cucharada de jugo de limón",
   "¼ taza de agua", "¼ taza de miel*"],
 "steps": ["Corte la sandía en cubos de 1/2 pulgada. Coloque los cubos en una bandeja para hornear, en una sola capa, y congélelos al menos 2 horas o durante toda la noche.",
   "En un procesador de alimentos, ponga la sandía y las fresas congeladas, el jugo de limón, el agua y la miel. Procese hasta obtener una mezcla homogénea.",
   "Póngalo en un recipiente para servir y sirva de inmediato.",
   "Otra opción es taparlo y congelarlo para más tarde. Sáquelo del congelador 5 minutos antes de servir."],
 "hints": ["* Las personas con el sistema inmunitario debilitado no deben comer miel cruda por el riesgo de infección bacteriana o por hongos. La miel filtrada, que se encuentra comúnmente en los supermercados, es una alternativa preferible; sin embargo, consulte siempre con su equipo de atención médica si tiene alguna duda sobre los alimentos.",
   "Puede usar jugo de limón verde en lugar del jugo de limón amarillo.",
   ("Disfrute la sandía como fruta más baja en potasio", WM_ES)],
 "food_choices": ["1 fruta baja en potasio"]},
{
 "title": "سوربيه البطيخ والفراولة", "description": N, "portions": "5", "serving_size": "1/5 الوصفة",
 "ingredients": ["2 كوب بطيخ مقطع مكعبات ½ بوصة ومجمد", "1 كوب فراولة مجمدة", "1 ملعقة كبيرة عصير ليمون",
   "¼ كوب ماء", "¼ كوب عسل*"],
 "steps": ["قطّع البطيخ إلى مكعبات ½ بوصة. ضع المكعبات على صينية خبز في طبقة واحدة، وجمّدها لمدة 2 ساعة على الأقل أو طوال الليل.",
   "في محضرة الطعام، ضع البطيخ والفراولة المجمدين وعصير الليمون والماء والعسل. اخلطها حتى يصبح المزيج ناعمًا.",
   "ضعه في طبق التقديم وقدّمه فورًا.",
   "أو بدلًا من ذلك، غطّه وجمّده لاستخدامه لاحقًا. أخرجه من الفريزر قبل التقديم بـ 5 دقائق."],
 "hints": ["* لا ينبغي لمن يعانون من ضعف جهاز المناعة تناول العسل الخام بسبب خطر الإصابة بعدوى بكتيرية أو فطرية. ويُعد العسل المصفّى، المتوفر عادةً في متاجر البقالة المحلية، بديلًا أفضل، لكن تواصل دائمًا مع فريق الرعاية الصحية إذا كانت لديك أي مخاوف بشأن الطعام.",
   "يمكنك استخدام عصير الليمون الأخضر بدلًا من عصير الليمون.",
   ("استمتع بالبطيخ كفاكهة أقل في البوتاسيوم", WM_AR)],
 "food_choices": ["1 فاكهة منخفضة البوتاسيوم"]}))

dump(3, R)
