import sys; sys.path.insert(0, '/mnt/c/WSL/davita/translations/b4')
from common import rec, dump, N

R = []

# 30 Spiced Pear and Raspberry Loaf
RB_ES = """Las frambuesas son una fruta deliciosa con muchos beneficios para la salud y un alimento básico durante los meses de verano. Por suerte, para las personas con enfermedad renal crónica (ERC) que deben cuidar el potasio, también son más bajas en potasio que muchas otras frutas. Con solo 186 miligramos de potasio por porción de 1 taza, por lo general se pueden disfrutar todos los días si lo desea. Pregunte a su dietista qué cantidad de fruta es adecuada para usted.

Las frambuesas también son una excelente fuente de fibra dietética y de antioxidantes que combaten enfermedades. Mientras que otras frutas suelen contener 2–4 gramos de fibra por porción, 1 taza de frambuesas frescas contiene 8 gramos de fibra.

Para aprovechar al máximo los beneficios de las frambuesas, agréguelas a su cereal o a sus magdalenas, añádalas a una ensalada o disfrútelas como refrigerio o postre saludable. Cuando ya no sea temporada de bayas, compre frambuesas congeladas sin azúcar para disfrutarlas todo el año."""
RB_AR = """توت العليق (الفرامبواز) فاكهة لذيذة لها فوائد صحية كثيرة، وهو من الأطعمة الأساسية خلال أشهر الصيف. ولحسن حظ مرضى الكلى المزمن الذين يحتاجون إلى الانتباه للبوتاسيوم، فهو أيضًا أقل في البوتاسيوم من كثير من الفواكه الأخرى. فمع احتوائه على 186 مليغرامًا فقط من البوتاسيوم لكل حصة مقدارها 1 كوب، يمكن عادةً الاستمتاع به يوميًا إن رغبت. اسأل أخصائي التغذية عن كمية الفاكهة المناسبة لك.

ويُعد توت العليق أيضًا مصدرًا ممتازًا للألياف الغذائية ومضادات الأكسدة التي تساعد على مقاومة الأمراض. فبينما تحتوي الفواكه الأخرى عادةً على 2–4 غرامات من الألياف لكل حصة، يحتوي 1 كوب من توت العليق الطازج على 8 غرامات من الألياف.

وللاستفادة الكاملة من فوائد توت العليق الصحية، أضفه إلى حبوب الإفطار أو المافن، أو إلى السلطة، أو استمتع به كوجبة خفيفة أو حلوى صحية. وعندما ينتهي موسم التوت، اشترِ توت العليق المجمد غير المحلى لتستمتع به طوال العام."""
R.append(rec(4965971, {
 "title": "Pan especiado de pera y frambuesa", "description": N, "portions": "12", "serving_size": "1/12 de la receta",
 "ingredients": ["1 taza de harina de trigo común", "1/2 cucharadita de jengibre molido", "1/2 cucharadita de nuez moscada molida",
   "1 cucharadita de canela molida", "1 cucharadita de bicarbonato de sodio", "1/4 cucharadita de polvo de hornear",
   "1 cucharadita de ralladura de limón", "2 huevos grandes", "1/2 taza de azúcar blanca*", "1/3 taza de aceite vegetal",
   "1 cucharadita de vainilla", "2 peras, peladas y ralladas", "1 taza de frambuesas"],
 "steps": ["Precaliente el horno a 350°F.",
   "Cierna juntos los ingredientes secos: la harina, las especias, el bicarbonato de sodio, el polvo de hornear y la ralladura de limón.",
   "En otro tazón, prepare la mezcla de huevo: bata los huevos, el azúcar, el aceite y la vainilla.",
   "Agregue los ingredientes secos a la mezcla de huevo.",
   "Incorpore las frutas con movimientos envolventes.",
   "Vierta en un molde para pan antiadherente y hornee aproximadamente 45 minutos o hasta que el pan recupere su forma al tocarlo."],
 "hints": ["* Para reducir el contenido de carbohidratos, puede usar un sustituto de azúcar apto para hornear.",
   "Una vez frío, puede cortar el pan en rebanadas. Póngalas en bolsas para congelador y congélelas para usarlas más adelante.",
   ("Frambuesas: fruta más baja en potasio", RB_ES)],
 "food_choices": ["1 ½ almidón", "1 grasa"]},
{
 "title": "كيك الكمثرى وتوت العليق بالتوابل", "description": N, "portions": "12", "serving_size": "1/12 الوصفة",
 "ingredients": ["1 كوب دقيق متعدد الاستخدامات", "½ ملعقة صغيرة زنجبيل مطحون", "½ ملعقة صغيرة جوزة الطيب المطحونة",
   "1 ملعقة صغيرة قرفة مطحونة", "1 ملعقة صغيرة بيكربونات الصوديوم", "¼ ملعقة صغيرة بيكنج بودر",
   "1 ملعقة صغيرة برش قشر الليمون", "2 بيضة كبيرة", "½ كوب سكر أبيض*", "⅓ كوب زيت نباتي",
   "1 ملعقة صغيرة فانيليا", "2 كمثرى، مقشرة ومبشورة", "1 كوب توت العليق"],
 "steps": ["سخّن الفرن مسبقًا على 350° فهرنهايت (175° مئوية).",
   "انخل المكونات الجافة معًا: الدقيق والتوابل وبيكربونات الصوديوم والبيكنج بودر وبرش قشر الليمون.",
   "في وعاء منفصل، حضّر خليط البيض: اخفق البيض والسكر والزيت والفانيليا معًا.",
   "أضف المكونات الجافة إلى خليط البيض.",
   "أدخل الفاكهة في الخليط برفق.",
   "اسكب الخليط في قالب كيك مستطيل غير لاصق واخبزه لمدة 45 دقيقة تقريبًا أو حتى يرتد سطح الكيك عند لمسه."],
 "hints": ["* لتقليل محتوى الكربوهيدرات، يمكنك استخدام بديل سكر مناسب للخَبز.",
   "بعد أن يبرد، يمكنك تقطيع الكيك إلى شرائح. ضعها في أكياس التجميد وجمّدها لاستخدامها لاحقًا.",
   ("توت العليق: فاكهة أقل في البوتاسيوم", RB_AR)],
 "food_choices": ["1½ نشويات", "1 دهون"]}))

# 31 Pear and Ginger Upside Down Cake
GI_ES = """Elegir un postre que encaje en una alimentación baja en potasio para la enfermedad renal crónica puede ser un reto. Sin embargo, es importante encontrar un dulce que pueda disfrutar. Muchos postres contienen ingredientes ricos en potasio, como chocolate, frutos secos o lácteos. Preparar una receta desde cero le permite mantener ingredientes bajos en potasio. El tamaño de la porción también influye para limitar el potasio que consume. Se puede mantener el dulzor de los postres con frutas y especias más bajas en potasio.

El jengibre es una especia que puede realzar el sabor de los postres. Su intenso sabor proviene de compuestos llamados gingeroles. El jengibre no solo da sabor a una alimentación baja en potasio, sino que también es beneficioso para la presión arterial, el colesterol en la sangre y el sistema inmunitario. Al elegir jengibre fresco, escoja un trozo de piel lisa y no arrugada, ya que la piel arrugada indica que está menos fresco. No lo pele hasta justo antes de usarlo para aprovechar al máximo su sabor. El jengibre se puede guardar a corto plazo sobre la encimera o, por más tiempo, envuelto en el congelador."""
GI_AR = """قد يكون اختيار حلوى تناسب النظام الغذائي منخفض البوتاسيوم لمرضى الكلى المزمن أمرًا صعبًا. ومع ذلك، من المهم أن تجد حلوى يمكنك الاستمتاع بها. فكثير من الحلويات تحتوي على مكونات غنية بالبوتاسيوم مثل الشوكولاتة أو المكسرات أو منتجات الألبان. ويتيح لك تحضير الوصفة من البداية الحفاظ على مكونات منخفضة البوتاسيوم. كما يُحدث حجم الحصة فرقًا في الحد من البوتاسيوم الذي تتناوله. ويمكن الحفاظ على حلاوة الحلويات باستخدام فواكه وتوابل أقل في البوتاسيوم.

والزنجبيل من التوابل التي يمكن أن تعزز مذاق الحلوى. وتأتي نكهة الزنجبيل الغنية من مركبات تُسمى الجينجيرولات. ولا يضيف الزنجبيل النكهة إلى النظام الغذائي منخفض البوتاسيوم فحسب، بل إنه مفيد أيضًا لضغط الدم وكوليسترول الدم وجهاز المناعة في جسمك. وعند اختيار الزنجبيل الطازج، اختر قطعة ذات قشرة ناعمة لا مجعدة، لأن التجاعيد تدل على أنه أقل طزاجة. وتجنب تقشيره إلا قبل استخدامه مباشرة للحصول على أفضل نكهة. ويمكن حفظ الزنجبيل لفترة قصيرة على سطح المطبخ، أو لفترة أطول ملفوفًا في الفريزر."""
SY_ES, CA_ES = "Almíbar", "Pastel"
SY_AR, CA_AR = "الشراب", "الكيك"
R.append(rec(4973268, {
 "title": "Pastel invertido de pera y jengibre", "description": N, "portions": "12", "serving_size": "1/12 de la receta",
 "ingredients": [(SY_ES, "3 rodajas de jengibre fresco"), (SY_ES, "½ taza de azúcar granulada"), (SY_ES, "2 cucharadas de jugo de limón"),
   (SY_ES, "2 cucharadas de agua"),
   (CA_ES, "1 lata (15 onzas) de mitades de pera en su jugo, escurridas y rebanadas"), (CA_ES, "1 1/3 taza de harina de trigo común"),
   (CA_ES, "1 cucharadita de crémor tártaro"), (CA_ES, "½ cucharadita de bicarbonato de sodio"),
   (CA_ES, "½ taza de mantequilla sin sal, suavizada"), (CA_ES, "½ taza de azúcar granulada"), (CA_ES, "2 huevos"),
   (CA_ES, "1 cucharadita de vainilla"), (CA_ES, "1 cucharada de ralladura de limón"), (CA_ES, "1 cucharada de jengibre fresco rallado"),
   (CA_ES, "½ taza de leche (1% de grasa)")],
 "steps": ["Precaliente el horno a 375°F.",
   "En un tazón hondo o taza medidora apta para microondas, prepare el almíbar. Machaque las rodajas de jengibre con una cuchara de madera; así se libera el sabor del jengibre. Agregue el azúcar, el jugo de limón y el agua. Caliente en el microondas durante 2 minutos. Luego revuelva para disolver el azúcar. Si el azúcar no se ha disuelto por completo, caliente un poco más en el microondas. Vierta la mezcla en un molde para pastel de 9 pulgadas. Coloque encima las rebanadas de pera y reserve.",
   "En un tazón pequeño, mezcle la harina, el crémor tártaro y el bicarbonato de sodio. Reserve.",
   "En un tazón más grande, con ayuda de una batidora eléctrica, bata la mantequilla y el azúcar durante unos 2 minutos, hasta que la mezcla quede homogénea. Agregue los huevos y siga batiendo durante 2 minutos. Agregue la vainilla, la ralladura de limón y el jengibre rallado.",
   "Con ayuda de una cuchara de madera, agregue poco a poco los ingredientes secos del paso 3 y la leche, alternándolos.",
   "Vierta la mezcla en el molde sobre las rebanadas de pera. Use una cuchara para distribuir la mezcla suavemente y de manera uniforme. Hornee durante 40 minutos o hasta que al insertar un palillo en el centro salga limpio. Saque del horno y deje enfriar durante 10 minutos.",
   "Pase un cuchillo alrededor del borde del pastel, coloque un plato grande encima y voltee el pastel para desmoldarlo."],
 "hints": ["Consejo: Usar peras enlatadas en lugar de frescas puede reducir el potasio de una receta.",
   ("El jengibre y los postres bajos en potasio", GI_ES)],
 "food_choices": ["2 almidón", "1 fruta baja en potasio", "1 grasa"]},
{
 "title": "كيكة الكمثرى والزنجبيل المقلوبة", "description": N, "portions": "12", "serving_size": "1/12 الوصفة",
 "ingredients": [(SY_AR, "3 شريحة زنجبيل طازج"), (SY_AR, "½ كوب سكر محبب"), (SY_AR, "2 ملعقة كبيرة عصير ليمون"),
   (SY_AR, "2 ملعقة كبيرة ماء"),
   (CA_AR, "1 علبة (15 أونصة) أنصاف كمثرى في عصيرها، مصفاة ومقطعة شرائح"), (CA_AR, "1⅓ كوب دقيق متعدد الاستخدامات"),
   (CA_AR, "1 ملعقة صغيرة كريمة الترتار"), (CA_AR, "½ ملعقة صغيرة بيكربونات الصوديوم"),
   (CA_AR, "½ كوب زبدة غير مملحة، طرية"), (CA_AR, "½ كوب سكر محبب"), (CA_AR, "2 بيضة"),
   (CA_AR, "1 ملعقة صغيرة فانيليا"), (CA_AR, "1 ملعقة كبيرة برش قشر الليمون"), (CA_AR, "1 ملعقة كبيرة زنجبيل طازج مبشور"),
   (CA_AR, "½ كوب حليب (1% دسم)")],
 "steps": ["سخّن الفرن مسبقًا على 375° فهرنهايت (190° مئوية).",
   "في وعاء عميق أو كوب قياس مناسب للميكروويف، حضّر الشراب. اهرس شرائح الزنجبيل بملعقة خشبية، فهذا يُطلق نكهة الزنجبيل. أضف السكر وعصير الليمون والماء. سخّنه في الميكروويف لمدة 2 دقيقة. ثم قلّب لإذابة السكر. وإذا لم يذب السكر تمامًا، فسخّنه في الميكروويف لمدة أطول. اسكب الخليط في قالب كيك قطره 9 بوصات. رصّ شرائح الكمثرى فوقه وضعه جانبًا.",
   "في وعاء صغير، اخلط الدقيق وكريمة الترتار وبيكربونات الصوديوم. ضعه جانبًا.",
   "في وعاء أكبر، اخلط الزبدة والسكر بالخلاط الكهربائي لمدة 2 دقيقة تقريبًا حتى يصبح الخليط ناعمًا. أضف البيض واستمر في الخلط لمدة 2 دقيقة. أضف الفانيليا وبرش قشر الليمون والزنجبيل المبشور.",
   "باستخدام ملعقة خشبية، أضف تدريجيًا المكونات الجافة من الخطوة 3 والحليب بالتناوب.",
   "اسكب الخليط في القالب فوق شرائح الكمثرى. استخدم ملعقة لتوزيع الخليط برفق وبالتساوي. اخبزه في الفرن لمدة 40 دقيقة أو حتى يخرج عود الأسنان نظيفًا عند غرزه في المنتصف. أخرجه من الفرن واتركه ليبرد لمدة 10 دقائق.",
   "مرّر سكينًا حول حافة الكيكة، وضع طبقًا كبيرًا فوقها، واقلب الكيكة رأسًا على عقب لإخراجها من القالب."],
 "hints": ["نصيحة: استخدام الكمثرى المعلبة بدلًا من الطازجة يمكن أن يقلل البوتاسيوم في الوصفة.",
   ("الزنجبيل والحلويات منخفضة البوتاسيوم", GI_AR)],
 "food_choices": ["2 نشويات", "1 فاكهة منخفضة البوتاسيوم", "1 دهون"]}))

# 32 Summer Berry Semifreddo
LF_ES = """Comer fruta todos los días es parte de una alimentación saludable. Las frutas aportan fibra y vitaminas, además de antioxidantes y fitoquímicos, que son nutrientes que ayudan a protegerle de diversas enfermedades. Sin embargo, también pueden ser una fuente abundante de minerales como el potasio. El potasio es un mineral que puede ser dañino si consume más del que sus riñones pueden manejar. Cuando esto ocurre, el nivel de potasio en la sangre puede subir a un nivel peligrosamente alto.

Afortunadamente, hay varias frutas más bajas en potasio, así que si tiene enfermedad renal crónica y debe vigilar la cantidad de potasio en su alimentación, estas son las frutas que debe elegir a diario. En porciones limitadas a ½ taza, las frutas más bajas en potasio incluyen manzanas, bayas, cerezas, clementinas, coctel de frutas, uvas, kiwi, limón amarillo o verde, mandarinas, peras, piña, ciruelas, mandarinas tangerinas y sandía. Los jugos de estas frutas también se consideran una buena opción para usted. Pregunte a su dietista qué cantidad de estos alimentos debe comer cada día para mantener una buena salud y evitar niveles altos de potasio."""
LF_AR = """تناول الفاكهة يوميًا جزء من النظام الغذائي الصحي. فالفواكه توفر الألياف والفيتامينات، إلى جانب مضادات الأكسدة والمركبات الكيميائية النباتية، وهي عناصر غذائية تساعد على حمايتك من أمراض متنوعة. لكنها قد تكون أيضًا مصدرًا غنيًا بالمعادن مثل البوتاسيوم. والبوتاسيوم معدن قد يكون ضارًا إذا تناولت منه أكثر مما تستطيع كليتاك التعامل معه. وعندما يحدث ذلك، قد يرتفع مستوى البوتاسيوم في دمك إلى مستوى مرتفع بشكل خطير.

ولحسن الحظ، هناك عدد من الفواكه الأقل في البوتاسيوم، فإذا كنت مصابًا بمرض الكلى المزمن وعليك مراقبة كمية البوتاسيوم في نظامك الغذائي، فهذه هي الفواكه التي ينبغي أن تختارها يوميًا. وعند الاقتصار على حصص مقدارها ½ كوب، تشمل الفواكه الأقل في البوتاسيوم: التفاح والتوت بأنواعه والكرز والكليمنتينا وكوكتيل الفواكه والعنب والكيوي والليمون أو الليمون الأخضر واليوسفي والكمثرى والأناناس والبرقوق واليوسفي (تانجرين) والبطيخ. وتُعد عصائر هذه الفواكه أيضًا خيارًا جيدًا لك. اسأل أخصائي التغذية عن الكمية التي ينبغي أن تتناولها من هذه الأطعمة يوميًا للحفاظ على صحة جيدة وتجنب ارتفاع مستويات البوتاسيوم."""
R.append(rec(4978734, {
 "title": "Semifreddo de frutos rojos de verano", "description": N, "portions": "8", "serving_size": "⅛ de la receta",
 "ingredients": ["1 taza de fresas frescas", "1 taza de zarzamoras frescas", "2 cucharadas de agua", "¼ taza de azúcar blanca*",
   "¼ taza de claras de huevo pasteurizadas", "¼ taza de azúcar blanca", "1 cucharada de jugo de limón", "1 cucharadita de vainilla",
   "1 taza de Cool Whip®"],
 "steps": ["Ponga las bayas y el agua con el azúcar en una cacerola y deje que hiervan. Cocine a fuego lento hasta que las bayas se ablanden (5–10 minutos).",
   "Deje enfriar la mezcla de bayas y licúela bien. Pase las bayas por un colador fino para quitar las semillas.",
   "En otro tazón, bata las claras de huevo hasta que estén espumosas. Agregue poco a poco el azúcar y bata hasta que se formen picos suaves.",
   "Agregue el jugo de limón y la vainilla a la mezcla de bayas. Incorpore el Cool Whip® y las claras batidas con una cuchara, con movimientos envolventes.",
   "Pase la mezcla a los platos de postre que prefiera. Cubra con envoltura plástica y congele al menos 4 horas.",
   "Decore con bayas frescas y sirva."],
 "hints": ["* Para reducir el contenido de carbohidratos, puede usar un sustituto de azúcar como Splenda®",
   "También puede congelar el semifreddo en un solo recipiente, como un molde cuadrado o un molde para magdalenas. Para desmoldarlo fácilmente después de congelarlo, forre el molde o las cavidades con envoltura plástica. Cubra siempre con envoltura plástica antes de congelar.",
   "Este postre se puede preparar uno o dos días antes de servirlo.",
   "¡Pruébelo con otros tipos de bayas frescas!",
   ("Disfrute las frutas bajas en potasio", LF_ES)],
 "food_choices": ["1 fruta baja en potasio"]},
{
 "title": "سميفريدو التوت الصيفي", "description": N, "portions": "8", "serving_size": "⅛ الوصفة",
 "ingredients": ["1 كوب فراولة طازجة", "1 كوب توت أسود (عُليق) طازج", "2 ملعقة كبيرة ماء", "¼ كوب سكر أبيض*",
   "¼ كوب بياض بيض مبستر", "¼ كوب سكر أبيض", "1 ملعقة كبيرة عصير ليمون", "1 ملعقة صغيرة فانيليا",
   "1 كوب Cool Whip®"],
 "steps": ["ضع التوت والماء مع السكر في قدر واتركه حتى يغلي. اتركه على نار هادئة حتى يطرى التوت (5–10 دقائق).",
   "اترك خليط التوت ليبرد ثم اخلطه جيدًا في الخلاط. مرّر التوت عبر مصفاة ناعمة للتخلص من البذور.",
   "في وعاء منفصل، اخفق بياض البيض حتى يصبح رغويًا. أضف السكر تدريجيًا واستمر في الخفق حتى تتكون قمم طرية.",
   "أضف عصير الليمون والفانيليا إلى خليط التوت. أدخل Cool Whip® وبياض البيض المخفوق برفق باستخدام ملعقة.",
   "انقل الخليط إلى أطباق الحلوى التي تختارها. غطّها بغلاف بلاستيكي وجمّدها لمدة 4 ساعات على الأقل.",
   "زيّنها بالتوت الطازج وقدّمها."],
 "hints": ["* لتقليل محتوى الكربوهيدرات، يمكنك استخدام بديل سكر مثل Splenda®",
   "يمكنك أيضًا تجميد السميفريدو في وعاء واحد، مثل قالب مربع أو صينية مافن. ولتسهيل إخراجه بعد التجميد، بطّن القالب أو تجاويف صينية المافن بغلاف بلاستيكي. وغطّه دائمًا بغلاف بلاستيكي قبل التجميد.",
   "يمكن تحضير هذه الحلوى قبل تقديمها بيوم أو يومين.",
   "جرّبها مع أنواع أخرى من التوت الطازج!",
   ("استمتع بالفواكه منخفضة البوتاسيوم", LF_AR)],
 "food_choices": ["1 فاكهة منخفضة البوتاسيوم"]}))

# 33 Mango Lime Cream
AD_ES = """Cuando se sigue una alimentación adecuada para los riñones, es importante consumir la cantidad justa de fósforo. Hay que consumir lo suficiente para mantener dientes y huesos sanos y ayudar a que los nervios y los músculos funcionen, pero no demasiado, porque puede causar complicaciones de la enfermedad renal. Consumir demasiado fósforo aumenta su nivel en la sangre. Con el tiempo, esto extrae calcio de los huesos y los debilita. Esto, a su vez, provoca depósitos de calcio en los vasos sanguíneos, el corazón y los pulmones, lo que aumenta el riesgo de enfermedades del corazón.

Evitar los aditivos de fosfato siempre que sea posible es la mejor manera de prevenir niveles altos de fósforo en la sangre. Lea la lista de ingredientes de los alimentos para saber si contienen aditivos de fosfato. Los ingredientes que contienen las letras “fos” (en inglés, “phos”) son aditivos de fosfato.

Revise la lista de ingredientes de todos los alimentos empaquetados. Algunos alimentos pueden ser engañosos, ya que una versión del alimento contiene aditivos y otras no. Por ejemplo, el queso crema normal por lo general no contiene aditivos de fosfato, pero es probable que la versión sin grasa contenga tripolifosfato de sodio o un aditivo similar. Otro ejemplo es la mezcla de leche y crema (half and half) sin grasa, que puede contener fosfato disódico, mientras que la versión normal no tiene aditivos. Puede ser mejor comprar la versión normal y usar una porción más pequeña para reducir el total de calorías y grasa y así evitar consumir los aditivos. Pregunte a su dietista registrado cuál es la mejor opción para usted."""
AD_AR = """عند اتباع نظام غذائي مناسب لمرضى الكلى، من المهم تناول الكمية المناسبة تمامًا من الفوسفور. فيجب تناول ما يكفي منه للحفاظ على صحة الأسنان والعظام ومساعدة الأعصاب والعضلات على أداء وظائفها، ولكن دون إفراط لأن ذلك قد يؤدي إلى مضاعفات مرض الكلى. فالإفراط في تناول الفوسفور يرفع مستواه في الدم. ومع مرور الوقت، يسحب ذلك الكالسيوم من العظام ويجعلها ضعيفة. ثم يؤدي ذلك إلى ترسب الكالسيوم في الأوعية الدموية والقلب والرئتين، مما يزيد خطر الإصابة بأمراض القلب.

إن تجنب إضافات الفوسفات قدر الإمكان هو أفضل طريقة للوقاية من ارتفاع مستوى الفوسفور في الدم. اقرأ قائمة المكونات على الأطعمة لتعرف ما إذا كانت تحتوي على إضافات الفوسفات. فالمكونات التي تحتوي أسماؤها على الأحرف “phos” (فوس) هي إضافات فوسفات.

تحقق من قائمة مكونات جميع الأطعمة المعبأة. فبعض الأطعمة قد تكون مضللة، إذ يحتوي أحد أشكال الطعام على إضافات بينما لا تحتوي عليها أشكاله الأخرى. فعلى سبيل المثال، لا يحتوي الجبن الكريمي العادي عادةً على إضافات الفوسفات، لكن من المرجح أن تحتوي النسخة الخالية من الدسم على ثلاثي فوسفات الصوديوم أو إضافة مشابهة. ومثال آخر هو خليط الحليب والقشدة (هاف آند هاف) الخالي من الدسم، الذي قد يحتوي على فوسفات ثنائي الصوديوم بينما لا تحتوي النسخة العادية على أي إضافات. وقد يكون من الأفضل شراء النسخة العادية واستخدام حصة أصغر لتقليل إجمالي السعرات والدهون وتجنب تناول الإضافات. اسأل أخصائي التغذية المعتمد عن الخيار الأفضل لك."""
MC_ES, VC_ES = "Crema de mango", "Crema de vainilla"
MC_AR, VC_AR = "كريمة المانجو", "كريمة الفانيليا"
R.append(rec(4979488, {
 "title": "Crema de mango y limón", "description": N, "portions": "4", "serving_size": "¼ de la receta",
 "ingredients": ["2 láminas de galletas Graham, trituradas",
   (MC_ES, "2 tazas (10 onzas) de trozos de mango congelado, descongelados"), (MC_ES, "2 cucharadas de jugo de limón verde"),
   (MC_ES, "Ralladura de 1 limón verde (reserve un poco para decorar)"), (MC_ES, "⅓ taza de leche condensada azucarada*"),
   (VC_ES, "3 cucharadas de crema para batir"), (VC_ES, "2 cucharadas de queso crema batido"),
   (VC_ES, "1 cucharadita de azúcar glas"), (VC_ES, "¼ cucharadita de extracto de vainilla")],
 "steps": ["En un tazón grande, prepare la crema de mango. Con ayuda de una batidora eléctrica o licuadora, mezcle todos los ingredientes hasta obtener una consistencia cremosa.",
   "En otro tazón, prepare la crema de vainilla. Con ayuda de una batidora eléctrica o licuadora, mezcle todos los ingredientes. Se necesitan aproximadamente 1–2 minutos de batido para que el azúcar se disuelva y se formen picos.",
   "Reparta las galletas Graham trituradas en 4 copas de postre. Agregue la crema de mango y cubra con la crema de vainilla.",
   "Cubra con envoltura plástica y refrigere durante 1 hora antes de servir. Decore con ralladura de limón."],
 "hints": ["* Puede congelar la leche condensada que le sobre.",
   "Consejo: Este postre se puede congelar. Descongélelo en el refrigerador dos horas antes de servir.",
   "* Para trasplante: Esta receta es más alta en grasa saturada. Consulte con su dietista registrado para saber cómo puede incluir esta receta en su alimentación.",
   ("Cuidado con los aditivos en los lácteos bajos en grasa", AD_ES)],
 "food_choices": ["2 fruta baja en potasio", "2 grasa"]},
{
 "title": "كريمة المانجو والليمون الأخضر", "description": N, "portions": "4", "serving_size": "¼ الوصفة",
 "ingredients": ["2 لوح بسكويت غراهام، مطحون",
   (MC_AR, "2 كوب (10 أونصة) قطع مانجو مجمدة، مذابة"), (MC_AR, "2 ملعقة كبيرة عصير ليمون أخضر"),
   (MC_AR, "برش قشر 1 ليمونة خضراء (احتفظ بجزء منه للتزيين)"), (MC_AR, "⅓ كوب حليب مكثف محلى*"),
   (VC_AR, "3 ملعقة كبيرة كريمة خفق"), (VC_AR, "2 ملعقة كبيرة جبن كريمي مخفوق"),
   (VC_AR, "1 ملعقة صغيرة سكر بودرة"), (VC_AR, "¼ ملعقة صغيرة خلاصة الفانيليا")],
 "steps": ["في وعاء كبير، حضّر كريمة المانجو. باستخدام خلاط كهربائي أو خلاط عادي، اخلط جميع المكونات حتى يصبح القوام كريميًا.",
   "في وعاء آخر، حضّر كريمة الفانيليا. باستخدام خلاط كهربائي أو خلاط عادي، اخلط جميع المكونات. يستغرق الخلط نحو 1–2 دقيقة حتى يذوب السكر وتتكون القمم.",
   "وزّع بسكويت غراهام المطحون على 4 كؤوس حلوى. أضف كريمة المانجو ثم ضع فوقها كريمة الفانيليا.",
   "غطّها بغلاف بلاستيكي وضعها في الثلاجة لمدة 1 ساعة قبل التقديم. زيّنها ببرش قشر الليمون الأخضر."],
 "hints": ["* يمكنك تجميد الحليب المكثف المتبقي.",
   "نصيحة: يمكن تجميد هذه الحلوى. أذبها في الثلاجة قبل التقديم بساعتين.",
   "* لمرضى زراعة الكلى: هذه الوصفة أعلى في الدهون المشبعة. استشر أخصائي التغذية المعتمد لمعرفة كيف يمكن إدراج هذه الوصفة في نظامك الغذائي.",
   ("انتبه للإضافات في منتجات الألبان قليلة الدسم", AD_AR)],
 "food_choices": ["2 فاكهة منخفضة البوتاسيوم", "2 دهون"]}))

# 34 Turkey Red Pepper Strata
SS_ES = """Cuando necesita limitar la sal en su alimentación, busque otras formas de sazonar los alimentos. En su búsqueda de nuevos sabores, puede encontrar productos llamados sustitutos de sal. Estos productos suelen parecerse a la sal de mesa, pero afirman ser bajos en sodio. Por desgracia, cuando se quita el sodio de la sal, por lo general se agrega potasio en su lugar. Cuando se quita el sodio y se reemplaza con potasio, el producto pasa a ser cloruro de potasio, o KCL. Es importante leer la lista de ingredientes de todos los sustitutos de sal para asegurarse de no elegir uno que contenga cloruro de potasio.

La cantidad de potasio de un sustituto de sal varía de un producto a otro, pero en general es muy alta cuando contiene cloruro de potasio. Una sola cucharadita puede contener de 2,400 a 3,000 miligramos de potasio, lo que equivale a la cantidad permitida para todo un día en una alimentación baja en potasio. Los sustitutos de sal también pueden encontrarse en alimentos etiquetados como “bajo en sodio” o “sin sodio”. Lea con atención los ingredientes de estos alimentos para ver si se les ha agregado cloruro de potasio.

La mejor manera de dar sabor a los alimentos es usar hierbas y especias, sin agregar sodio ni potasio no deseados. Si no sabe bien cómo usar hierbas y especias, pida sugerencias a su dietista."""
SS_AR = """عندما تحتاج إلى الحد من الملح في نظامك الغذائي، ابحث عن طرق أخرى لتتبيل الطعام. وفي أثناء بحثك عن نكهات جديدة، قد تصادف منتجات تُسمى بدائل الملح. تبدو هذه المنتجات عادةً مثل ملح الطعام، لكنها تدّعي أنها قليلة الصوديوم. وللأسف، عند إزالة الصوديوم من الملح، يُضاف البوتاسيوم عادةً مكانه. وعندما يُزال الصوديوم ويُستبدل بالبوتاسيوم، يصبح المنتج كلوريد البوتاسيوم (KCL). ومن المهم قراءة قائمة المكونات على جميع بدائل الملح للتأكد من أنك لا تختار بديلًا يحتوي على كلوريد البوتاسيوم.

تختلف كمية البوتاسيوم في بدائل الملح من منتج لآخر، لكنها عمومًا مرتفعة جدًا عندما تحتوي على كلوريد البوتاسيوم. فقد تحتوي ملعقة صغيرة واحدة على 2,400 إلى 3,000 مليغرام من البوتاسيوم، وهو ما يعادل الكمية المسموح بها ليوم كامل في النظام الغذائي منخفض البوتاسيوم. كما يمكن أن توجد بدائل الملح في الأطعمة المكتوب عليها “قليل الصوديوم” أو “خالٍ من الصوديوم”. اقرأ مكونات هذه الأطعمة بعناية لمعرفة ما إذا كان قد أُضيف إليها كلوريد البوتاسيوم.

أفضل طريقة لإضافة النكهة إلى الطعام هي استخدام الأعشاب والبهارات دون إضافة صوديوم أو بوتاسيوم غير مرغوب فيهما. وإذا لم تكن متأكدًا من طريقة استخدام الأعشاب والبهارات، فاطلب اقتراحات من أخصائي التغذية."""
R.append(rec(4980045, {
 "title": "Strata de pavo y pimiento rojo", "description": N, "portions": "6", "serving_size": "1/6 de la receta",
 "ingredients": ["6 huevos", "1 ½ tazas de bebida de arroz", "1 cucharadita de condimento para aves", "¼ cucharadita de pimienta negra molida",
   "1 cucharada de mostaza Dijon", "4 tazas de pan de corteza crujiente, en cubos", "½ taza de queso suizo rallado",
   "1 taza de cebollín picado", "2 tazas (8.8 onzas) de pavo o pollo sobrante, en cubitos", "1 taza de pimiento rojo picado en cubitos",
   "2 cucharadas de perejil fresco"],
 "steps": ["Precaliente el horno a 350°F.",
   "En un tazón, bata los huevos, la bebida de arroz y las especias.",
   "En otro tazón, mezcle el pan con el queso, el cebollín, el pavo y el pimiento rojo. Páselo a un molde cuadrado antiadherente de 9 pulgadas o a su fuente para hornear favorita, previamente engrasada.",
   "Vierta la mezcla de huevo sobre la mezcla de pan. Presione el pan para asegurarse de que todo quede cubierto con el líquido.",
   "Coloque la strata sin tapar en el horno y hornee de 50 a 60 minutos. La strata está lista cuando se ha inflado y está firme al tacto.",
   "Sirva tibia. Excelente para el desayuno o el almuerzo."],
 "hints": ["La strata se puede armar la noche anterior, cubrir con envoltura plástica y refrigerar. Hornéela a la mañana siguiente en el horno precalentado para disfrutar de un brunch fácil.",
   ("Los peligros de los sustitutos de sal", SS_ES)],
 "food_choices": ["3 carne", "1 almidón"]},
{
 "title": "ستراتا الديك الرومي والفلفل الأحمر", "description": N, "portions": "6", "serving_size": "1/6 الوصفة",
 "ingredients": ["6 بيضات", "1½ كوب مشروب الأرز", "1 ملعقة صغيرة توابل الدواجن", "¼ ملعقة صغيرة فلفل أسود مطحون",
   "1 ملعقة كبيرة خردل ديجون", "4 كوب خبز مقرمش القشرة، مقطع مكعبات", "½ كوب جبن سويسري مبشور",
   "1 كوب بصل أخضر مفروم", "2 كوب (8.8 أونصة) ديك رومي أو دجاج متبقٍ، مقطع مكعبات صغيرة", "1 كوب فلفل رومي أحمر مقطع مكعبات صغيرة",
   "2 ملعقة كبيرة بقدونس طازج"],
 "steps": ["سخّن الفرن مسبقًا على 350° فهرنهايت (175° مئوية).",
   "في وعاء الخلط، اخفق البيض ومشروب الأرز والتوابل معًا.",
   "في وعاء خلط منفصل، اخلط الخبز مع الجبن والبصل الأخضر والديك الرومي والفلفل الأحمر. انقل الخليط إلى قالب مربع غير لاصق مقاسه 9 بوصات أو إلى طبق الفرن المفضل لديك بعد دهنه.",
   "اسكب خليط البيض فوق خليط الخبز. اضغط على الخبز للتأكد من أن السائل يغطيه كله.",
   "ضع الستراتا في الفرن دون غطاء واخبزها لمدة 50 إلى 60 دقيقة. تكون الستراتا جاهزة عندما تنتفخ وتصبح متماسكة عند لمسها.",
   "قدّمها دافئة. ممتازة للإفطار أو الغداء."],
 "hints": ["يمكن تجهيز الستراتا في الليلة السابقة وتغطيتها بغلاف بلاستيكي ووضعها في الثلاجة. اخبزها في الفرن المسخّن مسبقًا في صباح اليوم التالي لوجبة فطور متأخر سهلة!",
   ("مخاطر بدائل الملح", SS_AR)],
 "food_choices": ["3 لحوم", "1 نشويات"]}))

# 35 Roasted Eggplant Dip
DP_ES, TC_ES = "Dip", "Totopos de tortilla"
DP_AR, TC_AR = "الغموس", "رقائق التورتيا المقرمشة"
R.append(rec(4982271, {
 "title": "Dip de berenjena asada", "description": N, "portions": "8", "serving_size": "4 totopos con 1/4 taza de dip",
 "ingredients": [(DP_ES, "1 berenjena mediana (~1 1/2 libras)"), (DP_ES, "1 cabeza de ajo"), (DP_ES, "1/2 cucharadita de comino en polvo"),
   (DP_ES, "2 cucharadas de perejil fresco picado"), (DP_ES, "1/8 cucharadita de pimienta negra molida"),
   (DP_ES, "2 cucharadas de jugo de limón"), (DP_ES, "1 cucharada de aceite de oliva"),
   (TC_ES, "4 tortillas de harina blanca (de 6 pulgadas de diámetro)"), (TC_ES, "1 cucharada de aceite de oliva o aceite en aerosol"),
   (TC_ES, "1/2 cucharadita de chile en polvo (opcional)"), (TC_ES, "1/2 cucharadita de comino en polvo (opcional)")],
 "steps": ["Precaliente el horno a 400°F.",
   "Corte la berenjena por la mitad a lo largo y colóquela con la piel hacia arriba en una bandeja para hornear forrada o antiadherente.",
   "Corte la parte superior de la cabeza de ajo. Envuélvala en papel de aluminio y colóquela en la misma bandeja que la berenjena. Hornee durante 40 minutos o hasta que la berenjena y el ajo se ablanden y suelten su aroma.",
   "Una vez que la berenjena y el ajo estén asados y fríos, puede preparar el dip. Saque con una cuchara la pulpa blanda de la berenjena y exprima los dientes de ajo de la cabeza en un tazón o en un procesador de alimentos. Agregue todos los demás ingredientes del dip. Haga un puré en el procesador de alimentos o con una licuadora de inmersión.",
   "Para preparar los totopos de tortilla, precaliente el horno a 400°F.",
   "Corte cada tortilla en ocho triángulos y extiéndalos en una bandeja para hornear forrada o antiadherente. Barnice las tortillas con aceite de oliva (o rocíelas con aceite). Si lo desea, espolvoréelas con una mezcla de chile en polvo y comino. Hornee aproximadamente 8 minutos o hasta que estén crujientes."],
 "hints": [], "food_choices": ["1 almidón", "1 verdura", "1 grasa"]},
{
 "title": "غموس الباذنجان المشوي", "description": N, "portions": "8", "serving_size": "4 رقائق مع ¼ كوب من الغموس",
 "ingredients": [(DP_AR, "1 باذنجانة متوسطة (~1½ رطل)"), (DP_AR, "1 رأس ثوم"), (DP_AR, "½ ملعقة صغيرة كمون مطحون"),
   (DP_AR, "2 ملعقة كبيرة بقدونس طازج مفروم"), (DP_AR, "⅛ ملعقة صغيرة فلفل أسود مطحون"),
   (DP_AR, "2 ملعقة كبيرة عصير ليمون"), (DP_AR, "1 ملعقة كبيرة زيت زيتون"),
   (TC_AR, "4 تورتيا من الدقيق الأبيض (قطرها 6 بوصات)"), (TC_AR, "1 ملعقة كبيرة زيت زيتون أو رذاذ زيت للطهي"),
   (TC_AR, "½ ملعقة صغيرة مسحوق الفلفل الحار (اختياري)"), (TC_AR, "½ ملعقة صغيرة كمون مطحون (اختياري)")],
 "steps": ["سخّن الفرن مسبقًا على 400° فهرنهايت (200° مئوية).",
   "قطّع الباذنجانة إلى نصفين بالطول وضعها بحيث يكون القشر للأعلى على صينية خبز مبطنة أو غير لاصقة.",
   "اقطع الجزء العلوي من رأس الثوم. لُفّ رأس الثوم بورق الألومنيوم وضعه على صينية الباذنجان نفسها. اخبزهما لمدة 40 دقيقة أو حتى يطرى الباذنجان والثوم وتفوح رائحتهما.",
   "بعد شوي الباذنجان والثوم وتبريدهما، يمكن تحضير الغموس. استخرج لب الباذنجان الطري من قشره بالملعقة، واعصر فصوص الثوم من الرأس في وعاء الخلط أو محضرة الطعام. أضف جميع مكونات الغموس الأخرى. اهرس الخليط في محضرة الطعام أو بالخلاط اليدوي حتى يصبح ناعمًا.",
   "لتحضير رقائق التورتيا، سخّن الفرن مسبقًا على 400° فهرنهايت (200° مئوية).",
   "قطّع كل تورتيا إلى ثمانية مثلثات وافردها على صينية خبز مبطنة أو غير لاصقة. ادهن التورتيا بزيت الزيتون (أو رشّها بالزيت). انثر عليها خليط مسحوق الفلفل الحار والكمون إن رغبت. اخبزها لمدة 8 دقائق تقريبًا أو حتى تصبح مقرمشة."],
 "hints": [], "food_choices": ["1 نشويات", "1 خضار", "1 دهون"]}))

# 36 Chicken Soba Noodle Salad
AN_ES = """Los fideos asiáticos se cocinan rápido y son fáciles de usar en una gran variedad de platillos. Se consiguen fácilmente, frescos o secos, en tiendas de productos asiáticos. Se han vuelto tan populares que incluso puede encontrar muchas de sus variedades en su supermercado local. Con tantas opciones, son bastante fáciles de usar en la cocina diaria. Puede agregarlos a sopas, ensaladas, salteados y rollitos primavera.

Al igual que los fideos tradicionales de trigo, como el espagueti o los coditos, los fideos asiáticos vienen en numerosas formas y tamaños. Sin embargo, a diferencia de los fideos de trigo, la textura de los fideos asiáticos puede variar muchísimo según el ingrediente con que se elaboren.

Los fideos asiáticos suelen elaborarse con harina de arroz, harina de alforfón (trigo sarraceno), almidones de tubérculos y de frijol mungo, harina de tapioca o algas. Según sus ingredientes principales, los fideos asiáticos pueden variar enormemente en su contenido de potasio y fósforo. Por ejemplo, los fideos de celofán se elaboran con agua y almidón de frijol, por lo que son muy bajos en potasio y fósforo en comparación con los fideos de harina de arroz o de alforfón. Hable con su dietista registrado sobre cómo puede incluir los fideos asiáticos en su alimentación."""
AN_AR = """تُطهى النودلز الآسيوية بسرعة ويسهل استخدامها في أطباق متنوعة. وهي متوفرة بسهولة، طازجة أو مجففة، في متاجر الأطعمة الآسيوية. وقد أصبحت شائعة جدًا لدرجة أنك قد تجد كثيرًا من أنواعها في متجر البقالة المحلي. ومع تعدد الخيارات، يسهل استخدامها في الطهي اليومي. ويمكنك إضافتها إلى الحساء والسلطات وأطباق التقليب السريع ولفائف الربيع.

وكما هو الحال مع المعكرونة التقليدية المصنوعة من القمح، مثل السباغيتي أو المعكرونة المقوسة، تأتي النودلز الآسيوية بأشكال وأحجام عديدة. لكن على عكس معكرونة القمح، قد يختلف قوام النودلز الآسيوية اختلافًا كبيرًا حسب المادة المصنوعة منها.

تُصنع النودلز الآسيوية عادةً من دقيق الأرز، أو دقيق الحنطة السوداء، أو نشا الخضار الجذرية والماش، أو دقيق التابيوكا، أو الأعشاب البحرية. وحسب مكوناتها الأساسية، قد تختلف النودلز الآسيوية اختلافًا هائلًا في محتواها من البوتاسيوم والفوسفور. فعلى سبيل المثال، تُصنع نودلز السيلوفان (الشفافة) من الماء ونشا البقول، ولذلك فهي منخفضة جدًا في البوتاسيوم والفوسفور مقارنة بالنودلز المصنوعة من دقيق الأرز أو الحنطة السوداء. تحدث إلى أخصائي التغذية المعتمد حول كيفية إدراج النودلز الآسيوية في نظامك الغذائي."""
R.append(rec(4990756, {
 "title": "Ensalada de pollo con fideos soba", "description": N, "portions": "4", "serving_size": "1/4 de la receta",
 "ingredients": ["12 onzas de pechuga de pollo sin piel", "1 cucharada de aceite de canola", "1 paquete (9.5 onzas) de fideos soba, secos",
   ("Vinagreta", "¼ taza de vinagre de vino de arroz"), ("Vinagreta", "1 cucharada de miel"), ("Vinagreta", "¼ taza de aceite de canola"),
   ("Vinagreta", "1 cucharada de jengibre rallado"), ("Vinagreta", "1 taza de repollo morado rallado"),
   ("Vinagreta", "1 taza de chícharos dulces (snap peas), cortados en diagonal en rodajas de ¼\""),
   ("Vinagreta", "¼ taza de cebollín, cortado en diagonal en rodajas de ¼\""), ("Vinagreta", "¼ taza de cilantro picado")],
 "steps": ["Precaliente el horno a 400°F.",
   "Frote el pollo con aceite de canola. Colóquelo en una bandeja para hornear y hornee durante 20–25 minutos o hasta que alcance una temperatura interna de 165°F. Deje enfriar. Córtelo en trozos de ¼ de pulgada y refrigérelo.",
   "Cocine los fideos soba según las instrucciones del paquete. Escúrralos y enjuáguelos con agua fría. Póngalos en un tazón grande y refrigérelos.",
   "Para preparar la vinagreta, mezcle el vinagre, la miel, el aceite y el jengibre. Refrigere.",
   "Para armar la ensalada, agregue al tazón de fideos soba el repollo, los chícharos, el cebollín, el cilantro y la vinagreta de jengibre. Mezcle bien para integrar.",
   "Decore la ensalada con el pollo en rebanadas."],
 "hints": ["Esta ensalada también se puede servir tibia.",
   "TENGA EN CUENTA: Esta receta es más alta en potasio y el tamaño de la porción es importante. Consulte con su dietista registrado para saber cómo puede incluir esta receta en su alimentación.",
   ("Fósforo y potasio en los fideos asiáticos", AN_ES)],
 "food_choices": ["3 carne", "3 1/2 almidón", "1 verdura baja en potasio", "1 grasa"]},
{
 "title": "سلطة الدجاج بنودلز السوبا", "description": N, "portions": "4", "serving_size": "¼ الوصفة",
 "ingredients": ["12 أونصة صدر دجاج منزوع الجلد", "1 ملعقة كبيرة زيت الكانولا", "1 عبوة (9.5 أونصة) نودلز سوبا جافة",
   ("الفينيغريت", "¼ كوب خل نبيذ الأرز"), ("الفينيغريت", "1 ملعقة كبيرة عسل"), ("الفينيغريت", "¼ كوب زيت الكانولا"),
   ("الفينيغريت", "1 ملعقة كبيرة زنجبيل مبشور"), ("الفينيغريت", "1 كوب ملفوف أحمر مقطع شرائح رفيعة"),
   ("الفينيغريت", "1 كوب بازلاء سكرية (سناب)، مقطعة بشكل مائل شرائح بسمك ¼ بوصة"),
   ("الفينيغريت", "¼ كوب بصل أخضر، مقطع بشكل مائل شرائح بسمك ¼ بوصة"), ("الفينيغريت", "¼ كوب كزبرة خضراء مفرومة")],
 "steps": ["سخّن الفرن مسبقًا على 400° فهرنهايت (200° مئوية).",
   "افرك الدجاج بزيت الكانولا. ضعه على صينية خبز واخبزه لمدة 20–25 دقيقة أو حتى تصل حرارته الداخلية إلى 165° فهرنهايت (75° مئوية). اتركه ليبرد. قطّعه إلى قطع بسمك ¼ بوصة وضعه في الثلاجة.",
   "اسلق نودلز السوبا حسب التعليمات المدونة على العبوة. صفّها واشطفها بالماء البارد. ضعها في وعاء خلط كبير وضعه في الثلاجة.",
   "لتحضير الفينيغريت، اخلط الخل والعسل والزيت والزنجبيل معًا. ضعه في الثلاجة.",
   "لتجميع السلطة، أضف الملفوف والبازلاء والبصل الأخضر والكزبرة وفينيغريت الزنجبيل إلى وعاء نودلز السوبا. اخلط جيدًا لتمتزج المكونات.",
   "زيّن السلطة بشرائح الدجاج."],
 "hints": ["يمكن أيضًا تقديم هذه السلطة دافئة.",
   "يرجى الانتباه: هذه الوصفة أعلى في البوتاسيوم، وحجم الحصة مهم. استشر أخصائي التغذية المعتمد لمعرفة كيف يمكن إدراج هذه الوصفة في نظامك الغذائي.",
   ("الفوسفور والبوتاسيوم في النودلز الآسيوية", AN_AR)],
 "food_choices": ["3 لحوم", "3½ نشويات", "1 خضار منخفضة البوتاسيوم", "1 دهون"]}))

# 37 Cranberry Crumble Coffee Cake
TP_ES, TP_AR = "Cubierta", "طبقة الكرامبل"
R.append(rec(4990973, {
 "title": "Pastel de café con arándanos rojos y crumble", "description": N, "portions": "12", "serving_size": "1/12 de la receta",
 "ingredients": [(CA_ES, "2 huevos"), (CA_ES, "½ taza de azúcar granulada"), (CA_ES, "¼ taza de mantequilla sin sal, derretida"),
   (CA_ES, "1 cucharadita de vainilla"), (CA_ES, "½ taza de yogur griego natural"), (CA_ES, "¼ taza de leche descremada"),
   (CA_ES, "1 ½ tazas de harina de trigo común"), (CA_ES, "1 cucharadita de bicarbonato de sodio"), (CA_ES, "1 cucharadita de canela molida"),
   (CA_ES, "1 ½ tazas de arándanos rojos, frescos o congelados"),
   (TP_ES, "½ taza de harina de trigo común"), (TP_ES, "½ cucharadita de canela molida"), (TP_ES, "2 cucharadas de mantequilla derretida"),
   (TP_ES, "2 cucharadas de jarabe de maple")],
 "steps": ["Precaliente el horno convencional a 350°F. Forre un molde de 9×9 pulgadas con papel pergamino.",
   "En un tazón, prepare los ingredientes húmedos. Bata los huevos, el azúcar, la mantequilla, la vainilla, el yogur y la leche.",
   "En otro tazón, prepare los ingredientes secos. Cierna juntos la harina, el bicarbonato de sodio y la canela.",
   "Agregue los ingredientes secos a los húmedos y mezcle bien.",
   "Incorpore los arándanos a la masa con movimientos envolventes.",
   "En otro tazón, mezcle los ingredientes de la cubierta de crumble.",
   "Vierta la masa en el molde. La masa debe quedar bastante espesa. Cubra con el crumble.",
   "Hornee aproximadamente 40 minutos o hasta que el pastel recupere su forma al tocarlo."],
 "hints": [], "food_choices": ["2 almidón", "1 grasa"]},
{
 "title": "كيكة القهوة بالتوت البري والكرامبل", "description": N, "portions": "12", "serving_size": "1/12 الوصفة",
 "ingredients": [(CA_AR, "2 بيضة"), (CA_AR, "½ كوب سكر محبب"), (CA_AR, "¼ كوب زبدة غير مملحة، مذابة"),
   (CA_AR, "1 ملعقة صغيرة فانيليا"), (CA_AR, "½ كوب زبادي يوناني سادة"), (CA_AR, "¼ كوب حليب خالي الدسم"),
   (CA_AR, "1½ كوب دقيق متعدد الاستخدامات"), (CA_AR, "1 ملعقة صغيرة بيكربونات الصوديوم"), (CA_AR, "1 ملعقة صغيرة قرفة مطحونة"),
   (CA_AR, "1½ كوب توت بري (كرانبيري)، طازج أو مجمد"),
   (TP_AR, "½ كوب دقيق متعدد الاستخدامات"), (TP_AR, "½ ملعقة صغيرة قرفة مطحونة"), (TP_AR, "2 ملعقة كبيرة زبدة مذابة"),
   (TP_AR, "2 ملعقة كبيرة شراب القيقب")],
 "steps": ["سخّن الفرن التقليدي مسبقًا على 350° فهرنهايت (175° مئوية). بطّن قالبًا مقاسه 9×9 بوصات بورق الزبدة.",
   "في وعاء الخلط، حضّر المكونات السائلة. اخفق البيض والسكر والزبدة والفانيليا والزبادي والحليب معًا.",
   "في وعاء آخر، حضّر المكونات الجافة. انخل الدقيق وبيكربونات الصوديوم والقرفة معًا.",
   "أضف المكونات الجافة إلى المكونات السائلة واخلط جيدًا.",
   "أدخل التوت في خليط الكيك برفق.",
   "في وعاء منفصل، اخلط مكونات طبقة الكرامبل.",
   "اسكب خليط الكيك في القالب. يجب أن يكون الخليط كثيفًا نوعًا ما. غطّه بالكرامبل.",
   "اخبزه لمدة 40 دقيقة تقريبًا أو حتى يرتد سطح الكيك عند لمسه."],
 "hints": [], "food_choices": ["2 نشويات", "1 دهون"]}))

# 38 Carne Asada Burritos
R.append(rec(4993661, {
 "title": "Burritos de carne asada", "description": "Un burrito latinoamericano de bistec", "portions": "7", "serving_size": N,
 "ingredients": ["1½ libras de falda de res (skirt steak)", "½ cebolla en rodajas", "2 cucharadas de miel", "1 cucharada de aceite de canola",
   "½ cucharadita de comino", "½ cucharada de chile en polvo", "2 onzas de jugo de manzana sin filtrar (apple cider)", "4 onzas de agua",
   "7 tortillas blancas (de 6”)", "Crema agria, al gusto"],
 "steps": ["Ponga la falda de res, la cebolla, el jugo de manzana, las especias, la miel y el agua en la olla de cocción lenta. Cocine a temperatura baja durante 8 horas.",
   "Deshebre la carne cocida y sírvala en las tortillas. Decore con crema agria."],
 "hints": [], "food_choices": []},
{
 "title": "بوريتو كارني أسادا", "description": "بوريتو ستيك على الطريقة اللاتينية", "portions": "7", "serving_size": N,
 "ingredients": ["1½ رطل ستيك الخاصرة (سكيرت ستيك)", "½ بصلة مقطعة شرائح", "2 ملعقة كبيرة عسل", "1 ملعقة كبيرة زيت الكانولا",
   "½ ملعقة صغيرة كمون", "½ ملعقة كبيرة مسحوق الفلفل الحار", "2 أونصة عصير تفاح (سايدر)", "4 أونصة ماء",
   "7 تورتيا بيضاء (6 بوصات)", "قشدة حامضة حسب الرغبة"],
 "steps": ["ضع ستيك الخاصرة والبصل وعصير التفاح والبهارات والعسل والماء في قدر الطهي البطيء. اطهُه على حرارة منخفضة لمدة 8 ساعات.",
   "فتّت اللحم المطبوخ إلى خيوط وقدّمه في التورتيا، وزيّنه بالقشدة الحامضة."],
 "hints": [], "food_choices": []}))

dump(4, R)
