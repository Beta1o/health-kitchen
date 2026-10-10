UI.tl = {
    navAbout: "Tungkol", footNote: "Para sa pangkalahatang impormasyon; sundin ang payo ng iyong care team.", srcFacet: "Pinagmulan", fitTitle: "Angkop sa aking mga target", fitLine: (sv, kcal, p) => `Ang iyong bahagi: ${sv} serving, humigit-kumulang ${kcal} kcal, pasok sa bahagi ng isang pagkain sa iyong mga limitasyon sa ${p}.`, fitOver: x => `Kahit kalahating serving ay lampas na sa bahagi ng isang pagkain para sa: ${x}. Samahan ito ng mas magagaan na putahe ngayong araw.`, fitScale: sv => `Lutuin lang ang aking bahagi (${sv} serving)`, fitScaled: sv => `iniangkop sa ${sv} serving`, perServing: "bawat serving", myPortionW: "aking bahagi", recTitle: "Mga inirerekomendang pagkain para sa iyo", recAddAll: "Idagdag lahat sa Aking araw", recNote: (k, p) => `Isang araw ng mga pagkaing akma sa iyong target na ${k.toLocaleString()} kcal, pasok sa iyong mga limitasyon sa ${p}. Inaayos ang mga bahagi sa bawat pagkain.`, servX: x => `${x} serving`, fitOnly: "Angkop sa aking pang-araw-araw na target", settings: "Mga Setting", setLang: "Wika", setTheme: "Tema", setAddr: "Kausapin ako bilang", addrM: "Lalaki", addrF: "Babae", setAddrNote: "Binabago nito kung paano ka tinatawag sa mga tagubiling Arabic.", setData: "Aking data", clearSaved: "I-clear ang mga naka-save na recipe", kidneySub: { hd: "Dialysis", ckd: "CKD, walang dialysis", dm: "CKD + diabetes" }, aboutLatest: "Mga pinakabagong update", updates: [["2026-10-02", ["Bagong dashboard na may switcher ng kondisyon, pang-araw-araw na target, payo at mga calculator", "Weight tracker, cook mode na may mga timer at metric na yunit", "Mga recipe mula sa AAKP, Kidney Care UK, My Renal Nutrition at DaVita Saudi Arabia", "Mga meal plan mula 7 araw hanggang isang buong taon", "Maliwanag at madilim na tema, pagbabahagi at PDF export"]], ["2026-10-01", ["Mga recipe sa English, Spanish at Arabic", "Mga health plan para sa sakit sa bato, diabetes, altapresyon at kalusugan ng puso"]]], conds: { kidney: "Bato", t2: "Diabetes", bp: "Presyon ng dugo", heart: "Puso", gen: "Pangkalahatan" },
    aboutWhat: "Ano ang Kusinang Malusog?", aboutWhatP: "Pinagsasama-sama ng Kusinang Malusog sa iisang lugar ang mga recipe mula sa mapagkakatiwalaang organisasyon para sa kalusugan ng bato, diabetes at puso, sa English, Spanish at Arabic. Bawat recipe ay nagpapakita ng nutrisyon bawat serving at may link sa orihinal na pinagmulan, para makapagluto ka nang may kumpiyansa at maibahagi ang iyong mga natuklasan.",
    aboutHow: "Paano ito gumagana", aboutSteps: [["🎯", "Piliin ang iyong kondisyon", "Bato, diabetes, presyon ng dugo, puso o pangkalahatan. Umaangkop dito ang dashboard."], ["🍽️", "Hanapin ang mga angkop na recipe", "Mag-filter ayon sa diyeta, nutrisyon at sangkap, at tingnan ang bahagi ng bawat putahe sa iyong pang-araw-araw na dami."], ["📅", "Magplano at magluto", "Gumawa ng mga meal plan, subaybayan ang iyong araw at timbang, at magluto nang hakbang-hakbang gamit ang mga timer."]],
    aboutSources: "Mga pinagmulan ng recipe", aboutSourcesP: "Binabanggit at nilalagyan ng link ng bawat recipe ang organisasyong naglathala nito.", aboutShare: "Ibahagi ang Kusinang Malusog", shareBtn: "Ibahagi", shareMsg: "Kusinang Malusog: mga recipe para sa kalusugan ng bato, diabetes at puso sa English, Spanish at Arabic.",
    email: "Email", copyLink: "Kopyahin ang link", linkCopied: "Nakopya ang link",
    disclaimer: "Ang Kusinang Malusog ay para sa pangkalahatang impormasyon. Hindi nito pinapalitan ang payo ng iyong doktor, dietitian o dialysis team; sundin ang mga limitasyong ibinigay nila sa iyo.",
    unitsLabel: "Mga yunit", unitsMetric: "Metric na yunit (g, ml, °C)", unitsUS: "US na yunit (oz, cups, °F)",
    dRecTitle: "Ang iyong pang-araw-araw na target", dTipsTitle: "Payo para sa iyong plano", dToolsTitle: "Mga tool at calculator",
    tCalories: "Calories", tPerDay: "bawat araw", tPerMeal: x => `humigit-kumulang ${x} bawat pagkain`, tChoices: n => `humigit-kumulang ${n} choice bawat pagkain`, tSalt: g => `= ${g} g asin`,
    tFluid: "Likido", tFluidNote: "ihi + 750 ml", tBmi: "BMI", tNote: "Mga pagtataya mula sa iyong plano at detalye ng katawan (Mifflin-St Jeor para sa calories, Devine na ideal na timbang). Mas matimbang ang mga target ng iyong care team.",
    bmiCat: b => b < 18.5 ? "Kulang sa timbang" : b < 25 ? "Malusog na timbang" : b < 30 ? "Sobra sa timbang" : "Obesity",
    toolNames: { bmi: "BMI at malusog na timbang", needs: "Pang-araw-araw na calories at protina", fluid: "Limitasyon sa likido (dialysis)", convert: "Converter ng asin, mmol at carb", weight: "Weight tracker" },
    bmiSub: "Body mass index, malusog na saklaw, ideal na timbang", needsSub: "Enerhiya at protina para sa iyong plano", fluidSub: "Batay sa dami ng iyong ihi kada araw", convSub: "Asin ↔ sodium, mmol ↔ mg, carb choices", weightSub: "I-log ang iyong timbang at tingnan ang takbo",
    height: "Taas", age: "Edad", years: "taon", sex: "Kasarian", female: "Babae", male: "Lalaki", activity: "Aktibidad", act: ["Kaunti o walang ehersisyo", "Magaan (1–3 araw/linggo)", "Katamtaman (3–5 araw/linggo)", "Napakaaktibo (6–7 araw/linggo)"],
    healthyRange: "Saklaw ng malusog na timbang", ibw: "Ideal na timbang ng katawan", adjw: "Naiakmang timbang ng katawan (ginagamit sa protina)", bmr: "Enerhiya sa pamamahinga (BMR)", meal: "pagkain", choicesW: "carb choices",
    fluidIntro: "Para sa dialysis, karaniwang panimulang punto ang dami ng iyong ihi kada araw dagdag ang 500–1,000 ml. Ang iyong dialysis unit ang magtatakda ng tunay mong limitasyon.", urine: "Ihi kada araw", cups250: "Baso na 250 ml",
    salt: "Asin", convHint: "Maglagay ng halaga sa alinmang kahon.", date: "Petsa", addWeight: "I-save ang timbang", weightSaved: "Na-save ang timbang", weightEmpty: "Magdagdag ng dalawa o higit pang timbang para makita ang iyong takbo.",
    calcNote: "Gabay lamang. Itanong sa iyong doktor o dietitian ang iyong personal na target.",
    navRecipes: "Mga Recipe", dCats: "Mag-browse ayon sa kategorya", dAll: "Lahat ng recipe", dMore: "Tingnan lahat", dPicks: p => `Mga nangungunang pili para sa ${p}`, dPlanTitle: "Ngayong araw sa iyong meal plan", dOpenPlans: "Buksan ang mga meal plan", dBrowse: "Mag-browse ng lahat ng recipe", greetMorning: "Magandang umaga", greetAfternoon: "Magandang hapon", greetEvening: "Magandang gabi", streak: n => `${n} araw na tuloy-tuloy`, pickPlan: "Para saan ka nagluluto?",
    nextIdea: slot => `Ideya para sa ${slot.toLowerCase()}`, tipTitle: "Tip ng araw", cookMode: "Cook mode", stepOf: (i, n) => `Hakbang ${i} ng ${n}`, startTimer: "Simulan", timerDone: "Tapos na ang oras!", finish: "Tapusin",
    mealPlans: "Mga meal plan", mpTitle: n => `${n}-araw na meal plan`, mpLen: n => n === 365 ? "1 taon" : `${n} araw`, mpDayOf: (d, n) => `Araw ${d} ng ${n}`, mpIntro: p => `Binuo mula sa koleksyon para sa iyong plano: ${p}. Ang almusal, tanghalian, hapunan at meryenda sa bawat araw ay pasok sa iyong pang-araw-araw na limitasyon.`,
    mpSlots: ["Almusal", "Tanghalian", "Hapunan", "Meryenda"], mpDay: d => `Araw ${d}`, mpShuffle: "I-shuffle", mpUseDay: "Idagdag ang araw na ito sa Aking araw", mpUsed: "Naidagdag ang araw sa Aking araw",
    mpNone: "Walang sapat na recipe na pasok sa mga limitasyong ito. Luwagan ang isang limitasyon sa iyong plano.", mpNote: "Mga mungkahi lamang, awtomatikong binuo mula sa datos ng nutrisyon. Pag-usapan ang mga bahagi sa iyong care team.",
    heroEyebrow: "Bato · diabetes · presyon ng dugo · puso", heroTitle: 'Pang-araw-araw na pagkain, <em>para sa iyong kalusugan</em>',
    heroLede: n => `${n} recipe mula sa mapagkakatiwalaang organisasyong pangkalusugan, na may kumpletong nutrisyon bawat serving. Pumili ng plano para sa sakit sa bato, diabetes, altapresyon o kalusugan ng puso at tingnan kung paano pasok ang bawat putahe sa iyong araw.`,
    statRecipes: "recipe", statPhotos: "may larawan", statVideos: "video sa pagluluto", statSources: "pinagmulan", featured: "Tampok",
    legendLo: "Mababa", legendMid: "Katamtaman", legendHi: "Mataas", legendMeal: "bahagi ng isang pagkain", navHome: "Home", themeNames: { system: "Tema: system", dark: "Tema: madilim", light: "Tema: maliwanag" }, source: "Pinagmulan", allDone: "Tapos na ang lahat ng hakbang. Kain na!",
    plan: "Aking health plan", planEdit: "I-edit ang mga dami", profiles: { hd: "Bato: dialysis", ckd: "Bato: CKD, hindi nagda-dialysis", dm: "Bato: CKD na may diabetes", t2: "Diabetes", bp: "Altapresyon", heart: "Kalusugan ng puso", gen: "Pangkalahatang malusog na pagkain" },
    planIntro: "Piliin ang iyong plano at ilagay ang pang-araw-araw na dami na ibinigay ng iyong doktor o dietitian. Ipinapakita ng mga meter ng recipe ang bahagi ng bawat serving sa isang pagkain, na binibilang bilang isang-katlo ng iyong araw. Nagiging amber at pula ang mga limitasyon habang papalapit ka; nagiging berde ang mga layunin.",
    weight: "Timbang ng katawan", perKg: "Protina bawat kg ng timbang ng katawan", daily: "Pang-araw-araw na dami", carbsOff: "iwanang blangko para hindi subaybayan",
    planSource: "Mga panimulang halaga: sinusunod ng mga plano sa bato ang KDOQI 2020 (protina, sodium) at ang gawi ng mga renal dietitian (potassium, phosphorus); sinusunod ng diabetes ang gabay ng ADA na humigit-kumulang 45–60 g carbohydrate bawat pagkain; sinusunod ng presyon ng dugo ang DASH at AHA (1,500 mg sodium, pagkaing mayaman sa potassium); sinusunod ng kalusugan ng puso at pangkalahatang pagkain ang AHA at ang Dietary Guidelines for Americans (sodium na mas mababa sa 2,300 mg, added sugar na mas mababa sa 25–50 g, fiber na 25–30 g). Mas matimbang ang mga numero ng sarili mong care team.",
    reset: "I-reset ang mga limitasyon", resetPlan: "Gamitin ang mga panimulang halaga", done: "Tapos na",
    dv: "Pananaw ng dietitian", dvSub: "bahagi ng isang pagkain · isang-katlo ng iyong araw", mealPct: p => `${p}% ng isang pagkain`, dayPct: p => `${p}% ng araw`,
    goal: "layunin", ratio: "Phosphorus bawat gramo ng protina", ratioNote: "Ang mas mababa sa 12 mg bawat gramo ay itinuturing na mabuti. Gumagamit ng kabuuang phosphorus, dahil hindi hiwalay na inilista ng DaVita ang mga phosphate additive.",
    nK: "Mataas sa potassium. Kung mataas ang potassium mo, itanong sa iyong dietitian ang tungkol sa bahagi.",
    nP: "Mataas sa phosphorus. Itanong sa iyong dietitian kung iinumin ang iyong phosphate binder kasabay ng pagkaing ito.",
    nNa: p => `Ang isang serving ay gumagamit ng ${p}% ng sodium sa isang araw.`, nLow: "Mababa sa sodium, potassium at phosphorus.",
    nProtGood: g => `Magandang pinagmumulan ng protina: ${g} g para sa iyong layunin sa protina sa dialysis.`, nProtOver: "Mas maraming protina kaysa isang-katlo ng iyong pang-araw-araw na limitasyon sa protina.",
    nSugar: g => `${g} g added sugar bawat serving. Isama ito sa bilang ng iyong carbohydrate choices.`, nCarb: c => `${c} carbohydrate choice bawat serving (humigit-kumulang 15 g bawat isa).`,
    nFiber: "Magandang pinagmumulan ng fiber.", limitW: "limitasyon", goalW: "layunin", perDay: "araw", planDesc: { hd: "Mas mataas na protina, limitado ang sodium, potassium, phosphorus", ckd: "Mas mababang protina, limitado ang mga mineral", dm: "Mga limitasyon sa bato dagdag ang carbohydrate at asukal", t2: "Carbohydrate, added sugar at fiber", bp: "DASH: mababa sa sodium, mayaman sa potassium", heart: "Sodium, asukal, cholesterol, fiber", gen: "Balanseng pang-araw-araw na target" }, nKGood: "Mayaman sa potassium, na nakatutulong magpababa ng presyon ng dugo (kumonsulta muna kung may sakit ka sa bato).",
    addDay: "Idagdag sa aking araw", added: "Naidagdag sa aking araw", servingsEaten: "Mga serving", myDay: "Aking araw",
    dayIntro: "Mga recipe na plano mong kainin ngayong araw, kinukwenta laban sa iyong pang-araw-araw na dami.", dayEmpty: "Wala pang nakaplano. Magbukas ng recipe at piliin ang “Idagdag sa aking araw”.",
    dayTotals: "Kabuuan ngayong araw", clearDay: "I-clear ang araw", remove: "Alisin", calories: "Calories", nutr: ["Sodium","Potassium","Phosphorus","Protina","Carbohydrates","Added sugar","Fiber","Cholesterol"], brand: 'Kusinang <span>Malusog</span>', tagline: n => `${n} recipe para sa kalusugan ng bato, diabetes at puso`, search: "Maghanap ng recipe o sangkap, hal. manok, kanela, kanin",
    filters: "Mga Filter", saved: "Naka-save", refine: "Paliitin ang resulta ayon sa", clearAll: "I-clear lahat", all: "Lahat ng recipe",
    diet: "Uri ng diyeta", cat: "Kategorya", dish: "Uri ng putahe", method: "Paraan ng pagluluto", holiday: "Pista opisyal", cuisine: "Lutuin",
    serv: "Bilang ng serving", photo: "May larawan ng recipe", photoYes: "May larawan", photoNo: "Walang larawan", dietNote: "Dapat tumugma ang mga recipe sa bawat diyetang tinitikan mo",
    quick: "Mabilisang pili ayon sa kondisyon", limits: "Mga limitasyon ng nutrisyon bawat serving", reset: "I-reset ang mga limitasyon", leaveOut: "Huwag isama ang isang sangkap", leavePh: "hal. kamatis, keso",
    more: "Higit pa", hasVideo: "May video sa pagluluto", rated4: "May rating na 4 na bituin pataas", any: "Alinman", sort: "Ayusin",
    sorts: { az: "A hanggang Z", fit: "Pinakamababang bahagi ng aking mga limitasyon", na: "Pinakamababa sa sodium", k: "Pinakamababa sa potassium", p: "Pinakamababa sa phosphorus", cal: "Pinakakaunting calories", protein: "Pinakamaraming protina", new: "Kamakailang na-update" },
    count: (n, c) => `<span class="num">${n}</span> ${n === 1 ? "recipe" : "recipe"}`, moreBtn: n => `Magpakita pa ng mga recipe (${n} pa)`,
    emptyH: "Walang recipe na tumutugma sa lahat ng filter na ito", emptyP: "Alisin ang isang filter o luwagan ang limitasyon ng nutrisyon para makakita ng higit pa.",
    presets: ["Mababa sa sodium", "Mababa sa potassium", "Mababa sa phosphorus", "Angkop sa diabetes", "Mabuti sa puso", "Wala pang 300 calories", "Mas mababang protina"],
    sliders: ["Sodium", "Potassium", "Phosphorus", "Protina", "Calories", "Carbohydrates", "Added sugar", "Cholesterol"],
    lvl: { lo: "Mababa", mid: "Katamtaman", hi: "Mataas" }, minerals: ["Sodium", "Potassium", "Phosphorus"],
    reviews: n => `${n} review`, cal: "cal", protein: "g protina", video: "Video", back: "Bumalik", prev: "Nakaraan", next: "Susunod", save: "I-save", savedBtn: "Naka-save", copy: "Kopyahin",
    source: "DaVita", copied: "Nakopya ang recipe", copyFail: "Piliin ang teksto para makopya ito",
    portions: "Mga bahagi", serving: "Laki ng serving", dietTypes: "Mga uri ng diyeta", ing: "Mga sangkap", prep: "Paghahanda", hints: "Mga kapaki-pakinabang na tip",
    nut: "Mga nutrient bawat serving", choices: "Mga food choice para sa bato at sa may diabetes na may sakit sa bato", carb: "Carbohydrate choices", by: "Isinumite ni",
    items: n => `${n} aytem · i-tap para i-tsek`, stepsHint: "i-tap ang hakbang kapag tapos na", watch: "Panoorin ang video sa pagluluto", watchSub: "Magbubukas ang video sa bagong tab",
    translated: src => `Isinalin mula sa orihinal na recipe sa ${src}`, officialEs: "Opisyal na bersyong Spanish ng DaVita",
    occasions: "Mga okasyon", without: "Walang", saveOnly: "Naka-save lang", servUnit: "serving",
    footer: (n, x) => `${n} recipe mula sa DaVita at mga nangungunang organisasyon para sa kalusugan ng bato, diabetes at puso, sa English, Spanish at Arabic. Mga antas ng kulay bawat serving: sodium na mababa ≤140 mg, mataas >400 mg; potassium na mababa ≤200 mg, mataas >400 mg; phosphorus na mababa ≤100 mg, mataas >250 mg. Pang-ayos lamang ang mga ito. Sundin ang payo ng iyong doktor o dietitian.`
};
NLABEL.tl = ["Calories","Protina","Carbohydrates","Taba","Cholesterol","Sodium","Potassium","Phosphorus","Calcium","Fiber","Added Sugar"];
NUNIT.tl = ["","g","g","g","mg","mg","mg","mg","mg","g","g"];
TIPS_X.tl = {
  kidney: [
    ["🥔","Bawasan ang potassium sa patatas at mga ugat na gulay: balatan, hiwain nang maliliit at ibabad, o pakuluan nang dalawang beses sa bagong tubig."],
    ["🏷️","Suriin ang listahan ng sangkap para sa mga phosphate additive (mga salitang may \"phos\"). Halos buong nasisipsip ng katawan ang phosphorus mula sa additive."],
    ["🌿","Timplahan ang pagkain ng mga halamang gamot, kalamansi o lemon, bawang at pampalasa sa halip na asin. Iwasan ang mga pamalit sa asin na gawa sa potassium chloride."],
    ["💧","Kung may limitasyon ka sa likido, bilangin din bilang likido ang sabaw, yelo at mga prutas na maraming katas."],
    ["💊","Inumin ang mga phosphate binder kasabay ng mga pagkain at meryenda ayon sa eksaktong reseta."]
  ],
  diabetes: [
    ["🍽️","Gamitin ang plate method: kalahati ay mga gulay na walang starch, isang-kapat ay lean na protina, isang-kapat ay mga pagkaing may carbohydrate."],
    ["⚖️","Panatilihing magkakatulad ang bahagi ng carbohydrate sa bawat pagkain. Ang isang carbohydrate choice ay humigit-kumulang 15 g."],
    ["🌾","Pumili ng whole grains, beans at lentils; pinapabagal ng kanilang fiber ang pagtaas ng blood sugar."],
    ["🥤","Palitan ang matatamis na inumin ng tubig, tsaa o kape na walang asukal."],
    ["🍎","Kumain ng prutas kasabay ng kaunting protina o healthy fat, at ikalat ito sa buong araw."]
  ],
  bp: [
    ["🧂","Karamihan ng sodium ay galing sa tinapay, processed na karne, de-latang sopas, atsara at pagkain sa restawran, hindi sa lalagyan ng asin."],
    ["🥬","Kumain ng maraming gulay, prutas at beans na mayaman sa potassium, maliban kung nililimitahan ng doktor mo ang potassium."],
    ["🥛","Pumili ng low-fat na gatas at keso at whole grains, tulad ng sa DASH eating plan."],
    ["🥫","Banlawan ang mga de-latang beans at gulay para maalis ang hanggang isang-katlo ng sodium."],
    ["🚶","Kumilos nang mga 30 minuto sa halos araw-araw; nakatutulong kahit maikling lakad pagkatapos kumain."]
  ],
  heart: [
    ["🫒","Magluto gamit ang olive o canola oil sa halip na mantikilya o ghee."],
    ["🐟","Kumain ng isda dalawang beses sa isang linggo, lalo na ng mamantikang isda tulad ng salmon o sardinas."],
    ["🥩","Pumili ng lean na parte ng karne at alisin ang nakikitang taba at balat."],
    ["🥣","Ang oats, barley, beans at lentils ay may soluble fiber na nakatutulong magpababa ng LDL cholesterol."],
    ["🍬","Panatilihing wala pang mga 25 g ang added sugar kada araw para sa kababaihan at 36 g para sa kalalakihan."]
  ],
  gen: [
    ["📅","Planuhin nang maaga ang mga pagkain sa isang linggo; nakatitipid ito at napapanatili ang tamang nutrisyon."],
    ["💧","Uminom ng tubig sa buong araw, maliban kung may limitasyon ka sa likido."],
    ["🍇","Kumain ng mga gulay at prutas na may iba't ibang kulay para sa mas malawak na hanay ng nutrients."],
    ["🏷️","Basahin ang nutrition label bawat serving, at tingnan kung ilang serving ang laman ng pakete."],
    ["🥕","Maghanda ng madaling meryenda: prutas, hiniwang gulay o yogurt."]
  ]
};
TERMS_X.tl = {
"5 or less ingredients":"5 o mas kaunting sangkap",
"African":"Aprikano",
"American":"Amerikano",
"Appetizers & Snacks":"Pampagana at Meryenda",
"Asian":"Asyano",
"Bake":"Inihurno",
"Beef, Lamb & Pork":"Baka, Tupa at Baboy",
"Beverages":"Mga Inumin",
"Bread":"Tinapay",
"Breads":"Mga Tinapay",
"Breakfast & Brunch":"Almusal at Brunch",
"British":"Britanya",
"Budget":"Mura",
"CKD non-dialysis":"CKD na hindi nagda-dialysis",
"Cake":"Keyk",
"Candy":"Kendi",
"Caribbean":"Caribbean",
"Chicken & Turkey":"Manok at Pabo",
"Chinese":"Tsino",
"Christmas":"Pasko",
"Cookies":"Cookies",
"Desserts":"Panghimagas",
"Diabetes":"Diabetes",
"Dialysis":"Dialysis",
"Easter":"Pasko ng Pagkabuhay",
"Easy":"Madali",
"Filipino":"Pilipino",
"Fish & Seafood":"Isda at Lamang-dagat",
"Freezer":"Pang-freezer",
"French":"Pranses",
"Fry":"Prito",
"German":"Aleman",
"Gluten-free":"Walang gluten",
"Greek":"Griyego",
"Grill":"Inihaw",
"Halloween":"Halloween",
"Hanukkah":"Hanukkah",
"Hawaiian":"Hawaiian",
"Heart Healthy":"Mabuti sa Puso",
"Higher Potassium":"Mas Mataas sa Potassium",
"Independence Day":"Araw ng Kalayaan",
"Indian":"Indiyano",
"International":"Internasyonal",
"Irish":"Irlandes",
"Italian":"Italyano",
"Japanese":"Hapones",
"Jewish":"Hudyo",
"Korean":"Koreano",
"Lower Potassium":"Mas Mababa sa Potassium",
"Lower Protein":"Mas Mababang Protina",
"Meatless Entree":"Pangunahing Putaheng Walang Karne",
"Mediterranean":"Mediterranean",
"Mexican":"Mehikano",
"Microwave":"Microwave",
"Middle Eastern":"Gitnang Silangan",
"Mother's Day":"Araw ng mga Ina",
"Muffin":"Muffin",
"Native American":"Katutubong Amerikano",
"New Year":"Bagong Taon",
"No Cooking":"Hindi Niluluto",
"One-Dish Meal":"Pagkaing Isang Putahe",
"Oven":"Oven",
"Pasta, Rice & Grains":"Pasta, Kanin at Butil",
"Picnic":"Piknik",
"Pie":"Pie",
"Pizza & Sandwiches":"Pizza at Sandwich",
"Potluck":"Potluck",
"Quick":"Mabilis",
"Refrigerator":"Pang-ref",
"Roast":"Inihaw sa Hurno",
"Salads & Dressings":"Salad at Dressing",
"Sauces & Seasonings":"Sawsawan at Pampalasa",
"Slow Cooker":"Slow Cooker",
"Soup":"Sabaw",
"Soups & Stews":"Sabaw at Nilaga",
"South American":"Timog Amerikano",
"Southern":"Timog (Southern)",
"Spanish":"Espanyol",
"Special Celebrations":"Mga Espesyal na Pagdiriwang",
"St Patrick's Day":"Araw ni San Patricio",
"Stew":"Nilaga",
"Stir-fry":"Gisa",
"Stove Top":"Sa Kalan",
"Thai":"Thai",
"Thanksgiving":"Thanksgiving",
"Valentine's Day":"Araw ng mga Puso",
"Vegetables":"Mga Gulay",
"Vegetarian":"Vegetarian"
};

Object.assign(UI.tl, {
  accTitle: "Aking account",
  accOpen: "Buksan ang aking account",
  signIn: "Mag-sign in",
  signUp: "Gumawa ng account",
  signOut: "Mag-sign out",
  signedOut: "Naka-sign out na",
  password: "Password",
  authIntro: "Mag-sign in para maitago sa iyong account ang iyong impormasyon, mga plano, timbang, at mga naka-save na recipe.",
  noAccount: "Bago ka rito?",
  haveAccount: "May account ka na?",
  guest: "Magpatuloy nang walang account",
  pwShort: "Gumamit ng hindi bababa sa 8 character para sa iyong password.",
  welcome: n => `Maligayang pagdating, ${n}`,
  synced: "Na-save sa iyong account",
  syncing: "Sine-save…",
  syncErr: "Hindi na-save, tingnan ang koneksyon",
  adminTitle: "Admin",
  adUsers: "Mga user",
  adAdmins: "Mga admin",
  adActive: "Aktibo ngayong linggo",
  adWeighIns: "Mga timbang",
  adPlans: "Mga user ayon sa plano",
  adSaved: "Naka-save",
  adLast: "Huling sign-in",
  adRole: "Papel",
  confirmDel: "I-tap ulit para burahin",
  loading: "Naglo-load…",
  pfTitle: "Aking impormasyon",
  pfName: "Pangalan",
  pfGoal: "Target na timbang",
  goalLose: "Magbawas ng timbang",
  goalKeep: "Panatilihin ang timbang ko",
  goalGain: "Magdagdag ng timbang",
  pfTarget: "Target na timbang",
  pfGoalNote: k => `Ang iyong target na calorie ay humigit-kumulang ${k} kcal na ngayon kada araw.`,
  pfPrefs: "Mga kagustuhan at pagkaing iniiwasan ko",
  pfDislikes: "Mga pagkaing hindi ko kinakain",
  pfAllergies: "Mga allergy",
  pfLikes: "Mga pagkaing gusto ko",
  pfHide: "Itago ang mga recipe na may pagkaing iniiwasan ko",
  pfDoctor: "Mga tagubilin ng doktor at mga gamot",
  pfDoctorNote: "Mga tagubilin ng aking doktor o dietitian",
  pfMeds: "Aking mga gamot (hal. phosphate binder kasabay ng pagkain)",
  pfDoctorShort: "Aking mga tala sa pangangalaga",
  pfProgress: (w, t) => `Ngayon ${w} kg · target ${t} kg (${(w - t > 0 ? "−" : "+") + Math.abs(w - t).toFixed(1)} kg pa)`
});

Object.assign(UI.tl, { roleUser: "User", roleAdmin: "Admin" });

Object.assign(UI.tl, { netErr: "Hindi maabot ang server ng account. Subukang muli maya-maya.", localOnly: "Sa device na ito lang naka-save ang iyong impormasyon. Para itago ito sa account, buksan ang app mula sa Health Kitchen server (tingnan ang README)." });

Object.assign(UI.tl, { fitOf: (sv, total, amt) => `Kakain ka ng ${sv} sa ${total} serving ng resiping ito${amt ? ` (${sv} × ${amt} bawat isa)` : ""}. Nasa column na «aking bahagi» ang nutrients ng iyong bahagi.` });

Object.assign(UI.tl, { signInNeeded: "Mag-sign in para makita ang iyong account: ang iyong impormasyon, istatistika, plano at mga setting.", stTitle: "Aking istatistika", stToday: "Ngayon", stAvg7: "Average (huling 7 araw)", stDays: "Mga araw na naitala", stStreak: "Sunod-sunod na araw", stSaved: "Mga naka-save na recipe", stWeighIns: "Mga pagtimbang", stChange: "Pagbabago ng timbang", stBmi: "BMI", badLogin: "Mali ang email o password.", accDisabled: "Naka-disable ang account na ito. Makipag-ugnayan sa administrator.", emailTaken: "May account na gamit ang email na ito.", badEmail: "Maglagay ng wastong email address.", adOnly: "Administrator lang ang maaaring magbukas ng page na ito. Mag-sign in gamit ang admin account.", adActiveDay: "Aktibo ngayon", adDisabled: "Mga naka-disable na account", adDisabledOne: "Naka-disable", adSignups: "Mga bagong user (huling 30 araw)", adNoPlan: "Wala pang plano", adRecipesLang: "Mga recipe bawat wika", adRecipesSrc: "Mga recipe bawat pinagmulan", adSearch: "Hanapin sa email o pangalan", adExport: "I-export ang CSV", adDetail: "Mga detalye", adJoined: "Sumali", adPrivacy: "Nananatiling pribado sa user ang mga tala sa kalusugan, tagubilin ng doktor at gamot, at hindi ipinapakita rito.", adNewPw: "Bagong password (8+ character)", adResetPw: "Itakda ang password", adEnable: "I-enable ang account", adDisable: "I-disable ang account", adPwDone: "Napalitan ang password. Na-sign out ang user sa lahat ng device." });

UI.tl.profiles = { none: "Walang plano (lahat ng resipe)", ...UI.tl.profiles }; UI.tl.conds = { ...UI.tl.conds, none: "Lahat ng resipe" };

Object.assign(TERMS_X.tl, {"Latin American": "Latin Amerikano", "Saudi": "Saudi", "Emirati": "Emirati", "Bahraini": "Bahraini", "Lebanese": "Lebanese", "Turkish": "Turko", "Moroccan": "Moroccan", "Tunisian": "Tunisian", "Egyptian": "Egyptian", "Persian": "Persian", "Afghan": "Afghan"});

Object.assign(UI.tl, {
  tabOverview: "Pangkalahatang-ideya",
  tabProfile: "Aking impormasyon",
  tabHealth: "Kalusugan at mga layunin",
  tabFood: "Mga gustong pagkain",
  tabWeight: "Timbang",
  stKcal14: "Calories, nakaraang 14 araw",
  stGoal: "Progreso ng layunin sa timbang",
  stGoalDone: "Naabot na ang layunin, magaling!",
  stNoData: "Wala pang kasaysayan. Magdagdag ng mga pagkain sa Aking araw at lalabas ito rito.",
  weightLog: "Talaan ng timbang",
  stGoalLeft: n => `${n} kg na lang`,
  memberSince: d => `Miyembro mula ${d}`
});

Object.assign(UI.tl, { mpCuisines: "Mga lutuin", mpAllCuisines: "Lahat ng lutuin", mpCuisNote: "Ang mga pagkain ay mula sa mga lutuing pinili mo; kung walang mapili, kahit anong lutuin ang gagamitin." });

Object.assign(UI.tl, { noServer: "Walang account sa kopyang ito ng app. Buksan ito mula sa Health Kitchen server para magparehistro at subaybayan ang iyong mga plano at impormasyon." });

Object.assign(UI.tl, {
  "tabMyRecipes": "Mga recipe ko",
  "subNew": "Magbahagi ng recipe",
  "subIntro": "Sinusuri ng aming team ang mga recipe na ibinabahagi ninyo (dami, yunit at sangkap) bago ito makita ng iba.",
  "subTitle": "Pangalan ng recipe",
  "subDesc": "Maikling paglalarawan",
  "subCat": "Kategorya",
  "subCuisine": "Lutuin",
  "subServings": "Dami ng serving",
  "subServing": "Laki ng serving (hal. 1 plato, 250 g)",
  "subIng": "Mga sangkap",
  "subQty": "Dami",
  "subItem": "Sangkap",
  "subAddIng": "+ Magdagdag ng sangkap",
  "subSteps": "Mga hakbang",
  "subAddStep": "+ Magdagdag ng hakbang",
  "subHints": "Mga tip (isa kada linya)",
  "subNut": "Nutrisyon kada serving (opsyonal)",
  "subSend": "Ipadala para suriin",
  "subSent": "Naipadala para suriin. Makikita ninyo ang resulta sa Mga recipe ko.",
  "subMine": "Mga naibahagi kong recipe",
  "subNone": "Wala pa kayong naibabahaging recipe.",
  "stPending": "Naghihintay ng pagsusuri",
  "stApproved": "Nailathala",
  "stRejected": "Hindi naaprubahan",
  "subNote": "Tala ng tagasuri",
  "subDelete": "Burahin",
  "subErr": "Magdagdag ng pangalan, kategorya, kahit isang sangkap na may dami at yunit, at isang hakbang.",
  "adSubs": "Mga isinumiteng recipe",
  "adApprove": "Aprubahan at ilathala",
  "adReject": "Huwag aprubahan",
  "adNotePh": "Tala para sa may-akda (hal. pakilagay ang dami sa gramo)",
  "adNoSubs": "Walang recipe rito.",
  "community": "Komunidad"
});

Object.assign(UI.tl, { meal: "Uri ng pagkain", mealTypes: {"main": "Pangunahing ulam", "breakfast": "Almusal", "starter": "Pampagana", "side": "Side dish", "snack": "Meryenda", "dessert": "Panghimagas", "drink": "Inumin", "condiment": "Sawsawan o pampalasa"}, fitCond: "Ito ay sawsawan o pampalasa, hindi pagkain nang mag-isa: isang serving ang kasama ng pagkain at kasama ang nutrients nito sa pagkaing iyon." });
Object.assign(UI.tl, {"cfgTitle":"Mga setting ng app","cfgDefaults":"Mga default para sa bagong bisita","cfgDefaultsNote":"Gagamitin hanggang makapili ang bisita ng sarili niya.","cfgVisitorChoice":"Device ng bisita","cfgAccounts":"Mga account","cfgSignups":"Payagan ang mga bagong sign-up","cfgSession":"Manatiling naka-sign in nang","cfgDays":"araw","cfgAnnounce":"Anunsyo sa home page","cfgAnnounceOn":"Ipakita ang anunsyo","cfgInfo":"Impormasyon","cfgWarn":"Mahalaga","cfgAnnounceNote":"Iwanang walang laman ang isang wika para ipakita ang tekstong Ingles.","cfgSources":"Mga ipinapakitang pinagmulan ng recipe","cfgSourcesNote":"Itinatago sa lahat ang mga pinagmulang walang tsek.","cfgLangs":"Mga alok na wika","cfgSave":"I-save ang mga setting","dbTitle":"Database","dbStatus":"Katayuan","dbConnected":"Nakakonekta","dbNoTables":"Kulang ang mga table","dbName":"Database","dbHost":"Server","dbUser":"User","dbSize":"Laki","dbStates":"Mga naka-save na profile","dbSupported":"Suportado","dbChange":"Gumamit ng ibang database","dbChangeNote":"Subukan muna ang koneksyon. Para gumamit ng bagong walang laman na database, gumawa ng mga table gamit ang owner account, saka lumipat gamit ang API user (hk_api). Hindi kinokopya ang data sa pagitan ng mga database.","dbApiUrl":"API connection URL","dbOwnerUrl":"Owner connection URL (para sa paggawa ng mga table)","dbTest":"Subukan ang koneksyon","dbSwitch":"Lumipat sa database na ito","dbSetup":"Gumawa ng mga table","dbOk":"Gumagana ang koneksyon","dbSetupDone":"Naka-set up na ang mga table, security rule, at function.","dbSwitched":"Gumagamit na ng bagong database ang app."});

Object.assign(UI.tl, { confirmEmail: "Nagawa na ang account. Buksan ang link ng kumpirmasyon sa iyong email, saka mag-sign in.", adPwEmail: "Magpadala ng email para i-reset ang password", adPwEmailed: "Napadalhan ang user ng email para i-reset ang password." });

Object.assign(UI.tl, Object.fromEntries(Object.entries({"sbProject": "Project", "sbSignups": "Sign-ups open", "sbConfirm": "Email confirmation", "sbUrl": "Project URL", "sbKey": "Publishable key (public)", "sbNote": "Accounts and data are stored in Supabase with row-level security. Keys and passwords are managed in the Supabase dashboard; the secret key is never used in the app.", "sbDash": "Dashboard", "sbUsers": "Users", "sbUrls": "Sign-in URLs", "sbProviders": "Sign-in methods", "sbTables": "Tables"}).filter(([k]) => !(k in UI.tl))));

Object.assign(UI.tl, Object.fromEntries(Object.entries({"dbConnectTitle": "Connect a database (e.g. Supabase)", "dbConnectNote": "Paste the owner connection string (in Supabase: Project Settings \u2192 Database \u2192 Connection string, with your database password). The server sets up the tables and security rules, creates a restricted app user with its own password, copies the current accounts and data, and switches. The details are stored encrypted on this server only.", "dbConnectUrl": "Owner connection string", "dbCopy": "Copy the current accounts and data", "dbConnectBtn": "Set up and connect", "dbEncrypted": "The connection is stored encrypted on this server."}).filter(([k]) => !(k in UI.tl))));

Object.assign(UI.tl, Object.fromEntries(Object.entries({"dbPort": "Port", "dbOrUrl": "Or paste a full connection string", "dbNeedFields": "Enter the host and the database password (or a full connection string)."}).filter(([k]) => !(k in UI.tl))));

Object.assign(UI.tl, Object.fromEntries(Object.entries({"dbTablesReady": "Health Kitchen tables found", "dbTablesNew": "empty: tables will be created", "dbNoRoles": "this user cannot create the app user; use the owner (postgres) account"}).filter(([k]) => !(k in UI.tl))));

Object.assign(TERMS_X.tl, {"Canadian": "Kanadyano", "Eastern European": "Silangang Europa", "Jamaican": "Jamaikano"});
Object.assign(TERMS_X.tl, {"North African": "Hilagang Aprikano"});
Object.assign(UI.tl, {"tabMeals": "Talaan ng pagkain", "mtIntro": "Planuhin kung anong recipe ang kakainin mo sa bawat kainan, saka lagyan ng tsek kapag nakain mo na.", "mtAssign": "Itakda sa isang kainan", "mtAssignShort": "Itakda", "mtTaken": "Nakain na", "mtDay": "Araw", "mtTotal": "Plano · nakain", "mtEmpty": "Wala pang nakatakda. Punan ang linggo mula sa meal plan, o buksan ang anumang recipe at piliin ang “Itakda sa isang kainan”.", "mtFromPlan": "I-save ang plano sa aking talaan", "mtSaved": "Na-save sa iyong talaan ng pagkain", "mtPick": "Pumili ng recipe", "mtSearch": "Maghanap ng recipe", "mtClear": "I-clear ang linggong ito", "mtAssigned": "Naitakda", "mtRemove": "Alisin", "mtFill": "Punan mula sa meal plan", "mtWhen": "Anong araw?", "mtWhich": "Anong kainan?", "mtToday": "Ngayon", "mtThisWeek": "Ngayong linggo"}, { mtDone: (a, b) => `${a} sa ${b} pagkain ang nakain na` });
Object.assign(UI.tl, {"authNotConfirmed": "Hindi pa kumpirmado ang email na ito. Buksan ang link ng kumpirmasyon sa iyong email, saka mag-sign in.", "authEmailLimit": "Masyadong maraming email ang naipadala. Maghintay ng ilang minuto at subukan ulit.", "authNoMail": "Hindi pa makapagpadala ng email ang account server sa address na ito. Hilingin sa administrator na idagdag ang iyong account.", "authClosed": "Sarado ang mga bagong pag-sign up."});
Object.assign(UI.tl, {"sbSignin": "Pag-sign in", "sbEmailLogin": "Pag-sign in gamit ang email at password", "sbOn": "Naka-on", "sbOff": "Naka-off", "sbOpen": "Bukas", "sbClosed": "Sarado", "sbConfirmOff": "Agad na naka-sign in ang mga bagong user pagkagawa ng account.", "sbConfirmOn": "Kailangang buksan ng mga bagong user ang email ng kumpirmasyon bago mag-sign in.", "sbDetails": "Mga detalye ng koneksyon", "sbCopy": "Kopyahin", "sbCopied": "Nakopya"});
Object.assign(UI.tl, {"mtType": "Uri", "mtSlotTypes": "Bagay sa kainang ito", "mtAllTypes": "Lahat ng uri", "mtFitOnly": "Mga recipe lang na pasok sa plano ko para sa kainang ito", "mtFits": "Pasok sa iyong plano para sa kainang ito", "mtHigh": "Lampas sa bahagi ng kainang ito sa iyong plano"}, { mtResults: n => `${n} recipe` });
Object.assign(UI.tl, { shopTitle: "Listahan ng bibilhin", shopTesting: "Sinusubok · admin at supervisor", shopIntro: "Lahat ng bibilhin para sa mga planong pagkain, pinagsama mula sa mga recipe at kinuwenta para sa isang serving bawat tao bawat kainan.", shopFrom: "Batay sa", shopPlan: "Meal plan", shopTable: "Aking talaan ng pagkain", shopDays: "Mga araw", shopPeople: "Mga tao", shopStaplesNote: "Tingnan kung ano na ang mayroon ka.", shopNeeded: "ayon sa kailangan", shopRecipes: "Mga recipe sa listahang ito", shopCopy: "Kopyahin ang listahan", shopPrint: "I-print", shopClear: "Alisin lahat ng tsek", shopEmpty: "Walang planong pagkain para sa mga araw na ito. Magtakda ng pagkain sa iyong talaan o piliin ang Meal plan.", roleSupervisor: "Supervisor", roleVisitor: "Bisita (hindi naka-sign in)", adRole: "Tungkulin", adRoleNote: "Nakikita rin ng mga supervisor ang mga feature na sinusubok (Admin → Mga pribilehiyo).", adRoleFixed: "ang mga admin ay itinatakda ng listahan ng admin email", privTitle: "Mga pribilehiyo", privIntro: "Piliin kung sino ang makakakita ng bawat bahagi ng app. Laging nakikita ng admin ang lahat; ang Bisita ay hindi naka-sign in. Agad na nase-save.", privSaved: "Na-save ang mga pribilehiyo", shopSec: {"produce": "Prutas at gulay", "meat": "Karne at isda", "dairy": "Gatas at itlog", "bakery": "Tinapay", "grains": "Kanin, pasta at butil", "canned": "De-lata at garapon", "frozen": "Frozen", "nuts": "Mani, buto at pinatuyong prutas", "other": "Iba pa", "staples": "Pangunahing sangkap sa kusina"}, feat: {"shop": "Listahan ng bibilhin", "plans": "Mga meal plan", "table": "Talaan ng pagkain", "day": "Aking araw", "saved": "Mga naka-save na recipe", "submit": "Magpadala ng recipe", "cook": "Cook mode", "pdf": "PDF at print"}, shopMeals: (m, r) => `${m} pagkain · ${r} recipe`, shopItems: n => `${n} item`, shopLeft: n => `${n} pa ang bibilhin`, shopUsed: n => `sa ${n} recipe` });
Object.assign(UI.tl, {"pwRule": "Gumamit ng hindi bababa sa 10 karakter na may mga titik at numero, at iwasan ang karaniwang password.", "idleOut": "Na-sign out matapos ang panahong walang aktibidad.", "cfgIdle": "Mag-sign out kapag walang aktibidad", "cfgMinutes": "minuto", "cfgIdleNote": "Ang mga naka-sign in ay ma-sign out matapos ang ganitong bilang ng minutong walang aktibidad (0 = hindi kailanman).", "secTitle": "Seguridad"});

UI.tl.dt = { "title": "Aking diet plan", "madeOn": "Ginawa noong", "print": "I-print / i-save bilang PDF", "newMenu": "Bagong menu", "intro": "Ang iyong personal na plano, ginawa mula sa iyong profile: health plan, sukat ng katawan, aktibidad, layunin at mga gustong pagkain. Suriin ito kasama ng iyong doktor o dietitian.", "needInfo": "Ilagay ang iyong edad, taas at timbang sa Aking impormasyon para umangkop sa iyo ang plano.", "editInfo": "I-edit ang aking impormasyon", "secYou": "Tungkol sa iyo", "healthy": "Malusog na timbang para sa iyong taas", "healthyNote": "BMI 18.5–24.9", "secJourney": "Ang iyong paglalakbay", "now": "Ngayon", "goalFig": "Ang iyong layunin", "cheerKeep": "Ituloy mo lang: ang matatag na timbang, masustansyang pagkain at araw-araw na paggalaw ay nagpoprotekta sa iyong kalusugan.", "cheerDone": "Naabot mo na ang iyong layunin — ipagpatuloy mo!", "benefits": ["Mas mababang presyon ng dugo at mas magaan na pasanin sa puso at bato", "Mas matatag na blood sugar", "Mas maraming lakas, mas madaling paggalaw at mas mahimbing na tulog"], "secDaily": "Ang iyong mga target bawat araw", "kcalLose": "mga 500 na mas kaunti sa iyong nasusunog", "kcalGain": "mga 300 na mas marami sa iyong nasusunog", "kcalKeep": "katumbas ng iyong nasusunog sa isang araw", "protKidney": "itinakda para sa iyong kidney plan", "carbLimit": "limitasyon ng iyong plano", "carbHalf": "mga kalahati ng iyong calories", "fat": "Taba", "fatNote": "mga 30% ng calories, karamihan mula sa olive oil, mani at isda", "fluids": "Likido", "fluidLimit": "ang iyong limitasyon (ihi + 750 ml); sundin ang iyong care team", "fluidGen": "bawat araw, maliban kung nililimitahan ng iyong care team ang likido", "secTimeline": "Ang iyong daan patungo sa layunin", "tlKeep": "Ang layunin mo ay panatilihin ang iyong timbang: kumain nang halos katumbas ng iyong calories bawat araw at manatiling aktibo.", "tlNoTarget": "Maglagay ng target na timbang sa Kalusugan at mga layunin para makita ang iyong timeline.", "tlReached": "Nasa target na timbang ka na.", "tlLow": "Ang iyong target ay mas mababa sa malusog na timbang para sa iyong taas (BMI 18.5). Pakikonsulta ito sa iyong doktor.", "tlHowGain": "Paano: mga 300 kcal na dagdag bawat araw, may protina sa bawat kain, at strength training dalawang beses sa isang linggo.", "week": "Linggo", "expected": "Inaasahang timbang", "secSplit": "Paano hatiin ang iyong araw", "splitNote": "Kumain sa regular na oras; opsyonal ang meryenda. Magdagdag ng gulay sa tanghalian at hapunan.", "secMenu": "Ang iyong 7-araw na menu", "menuNote": "Binuo mula sa mga recipe na angkop sa iyong health plan at mga gusto. Ang bahagi (×) ay iniangkop sa iyong calories at mga limitasyon. I-tap ang isang recipe para buksan ito.", "dayTotal": "Kabuuan sa araw", "secChoose": "Mas madalas piliin", "secLimit": "Limitahan o iwasan", "avoidMine": "Iniiwasan din para sa iyo", "secExercise": "Ang iyong exercise plan", "exWeekly": "Lingguhang aktibidad", "exModerate": "katamtaman: kaya mong magsalita pero hindi kumanta", "exStrengthT": "Strength training", "exStrengthV": "2 araw sa isang linggo", "exSteps": "Hakbang bawat araw", "exStepsNote": "magdagdag ng mga 500 bawat linggo", "exBurn": "Nasusunog sa ehersisyo", "exPerWeek": "bawat linggo", "exActivity": "Aktibidad", "exMinutes": "Minuto", "exIntensity": "Tindi", "moderate": "Katamtaman", "light": "Magaan", "ex": {"walk": "Mabilis na paglalakad", "bike": "Pagbibisikleta o paglangoy", "strength": "Strength training (resistance band, magagaang pabigat o sariling bigat ng katawan)", "stretch": "Pag-stretch at balanse"}, "exProgress": "Magsimula sa 10–15 minuto bawat beses at magdagdag ng 5 minuto bawat linggo hanggang maabot mo ang iyong target. Nadaragdag din ang maiikling session (10 minuto).", "exOlder": "Isama ang mga ehersisyo sa balanse (pagtayo sa isang paa malapit sa pader, paglalakad nang sakong-sa-daliri) para maiwasan ang pagkahulog.", "exSafety": {"kidney": "Mag-ehersisyo sa mga araw na walang dialysis o ayon sa payo ng iyong care team; huwag magbuhat o magdiin gamit ang braso na may fistula; isama sa iyong limitasyon sa likido ang mga iniinom habang nag-eehersisyo.", "diabetes": "Suriin ang iyong blood sugar bago at pagkatapos mag-ehersisyo, magdala ng mabilis na asukal (juice o glucose tablets), at mag-ehersisyo 1–3 oras pagkatapos kumain.", "heart": "Mag-warm up at mag-cool down nang 5–10 minuto, huwag pigilan ang hininga habang nagbubuhat, at huminto kung makaramdam ng pananakit ng dibdib, pagkahilo o kakaibang hirap sa paghinga.", "gen": "Magsimula nang dahan-dahan, uminom ng tubig, at huminto kung makaramdam ng sakit o pagkahilo."}, "secHabits": "Mga lingguhang gawi", "habits": ["Timbangin ang sarili isang beses sa isang linggo, sa parehong araw at oras, at ilagay ito sa Timbang", "Itala ang iyong kinakain sa Aking araw", "Gamitin ang meal plan at shopping list para mamili isang beses sa isang linggo", "Matulog nang 7–9 oras", "Inumin ang iyong mga gamot ayon sa reseta at pumunta sa iyong mga appointment"], "disclaimer": "Ang planong ito ay pangkalahatang gabay batay sa impormasyong inilagay mo. Hindi nito pinapalitan ang payo ng iyong doktor o dietitian, lalo na kung may sakit ka sa bato, diabetes o kondisyon sa puso.", "foods": {"kidney": {"choose": ["Prutas na mababa sa potassium: mansanas, berries, ubas, pinya", "Gulay: repolyo, cauliflower, bell pepper, pipino, sibuyas", "Puting kanin, pasta, tinapay na walang asin", "Sariwang karne, manok, isda at itlog sa mga bahaging nasa iyong plano", "Herbs, kalamansi o lemon at pampalasa sa halip na asin"], "limit": ["Asin, bouillon cube, atsara, processed at de-latang pagkain", "Pagkaing mataas sa potassium: saging, dalandan, patatas, kamatis, pinatuyong prutas", "Pagkaing mataas sa phosphorus: gatas at mga produkto nito, cola, processed cheese, mani, whole grains", "Pagkaing may phosphate additives (“phos” sa label)", "Mga pamalit sa asin (may potassium ang mga ito)"]}, "diabetes": {"choose": ["Gulay sa bawat kain (kalahati ng plato)", "Whole grains: oats, brown rice, whole-wheat na tinapay", "Beans, lentils at garbanzos", "Lean protein: isda, manok, itlog, yogurt", "Tubig at inuming walang asukal"], "limit": ["Asukal, matatamis at matatamis na inumin, kasama ang juice", "Malalaking bahagi ng puting tinapay, puting kanin at pastries", "Pritong pagkain at fast food", "Maraming datiles at pinatuyong prutas"]}, "heart": {"choose": ["Gulay at prutas, 5 bahagi bawat araw", "Whole grains at fiber", "Isda dalawang beses sa isang linggo, beans at lentils", "Olive oil, mani at buto na walang asin", "Low-fat na gatas at mga produkto nito"], "limit": ["Asin at maaalat na pagkain (tinapay, keso, atsara, ready-to-eat na pagkain)", "Matatabang karne at processed meat", "Mantikilya, ghee at pritong pagkain", "Asukal at matatamis na inumin"]}, "gen": {"choose": ["Gulay at prutas, 5 bahagi bawat araw", "Whole grains", "Lean protein: isda, manok, beans, itlog", "Tubig", "Lutong-bahay na pagkain"], "limit": ["Asukal at matatamis na inumin", "Asin at processed na pagkain", "Pritong pagkain at fast food", "Malalaking bahagi sa gabi"]}}, "tlLose": (kg, wk, date, rate) => `Magbawas ng mga ${kg} kg sa loob ng ${wk} linggo (bandang ${date}), mga ${rate} kg bawat linggo.`, "tlGain": (kg, wk, date, rate) => `Magdagdag ng mga ${kg} kg sa loob ng ${wk} linggo (bandang ${date}), mga ${rate} kg bawat linggo.`, "tlHowLose": (food, ex) => `Paano: mga ${food} kcal na bawas bawat araw mula sa pagkain, dagdag ang ehersisyo sa ibaba (mga ${ex} kcal bawat linggo).`, "inWeeks": w => `${w} linggo`, "cheer": (kg, w) => `${kg} kg sa loob ng ${w} linggo — isang kain at isang lakad sa bawat pagkakataon. Kaya mo ito!` };
UI.tl.dt.addMore = "Idagdag para maabot ang iyong calories";
Object.assign(UI.tl.dt, {"goalHealthy": "Malusog na timbang para sa iyo", "suggestedNote": "Iminungkahi batay sa iyong taas (BMI 24.9 pinakamataas). Maaari kang magtakda ng sariling target sa Kalusugan at mga layunin.", "setGoal": "Itakda ang aking target"});

// glycemic index and load
Object.assign(UI.tl, {"gl": "Glycemic load", "glBand": {"lo": "Mababa", "mid": "Katamtaman", "hi": "Mataas"}, "giTitle": "Epekto sa blood sugar", "giIdx": "Glycemic index (GI)", "glServ": "Glycemic load bawat serving", "glMine": "Para sa aking bahagi", "giNone": "Masyadong kaunti ang carbohydrate para masukat", "giRaise": "Pinakanagpapataas ng blood sugar", "giAbbr": "GI", "glAbbr": "GL", "dayGl": "Glycemic load", "giNote": "Tantiya mula sa mga sangkap. Ipinapakita ng GI kung gaano kabilis itinataas ng pagkain ang blood sugar (glucose = 100); binibilang din ng GL kung gaano karaming carbohydrate ang nasa isang serving. GI: mababa kung 55 pababa, mataas kung 70 pataas. GL: mababa kung 10 pababa, mataas kung 20 pataas.", "giTipHi": "Mataas ang load: kumain ng mas maliit na bahagi, o samahan ng gulay, salad o protina para mas mabagal tumaas ang blood sugar.", "giSrc": "GI data © GI News, University of Sydney", giShare: n => `${n}% ng sugar load`, nGl: (v, b) => `Glycemic load bawat serving: ${v} (${b}).`});
UI.tl.giTipKid = "Mataas ang load: kumain ng mas maliit na bahagi, o hatiin ito sa dalawang kainan.";
if (UI.tl.sorts) UI.tl.sorts.gl = "Pinakamababang glycemic load";
Object.assign(UI.tl.feat || (UI.tl.feat = {}), {"dieter": "Aking diet plan", "gi": "Glycemic index"});
Object.assign(UI.tl, {sbShow: "Ipakita", sbHide: "Itago"});
if (UI.tl.dt) Object.assign(UI.tl.dt, {atMost: "Hanggang", atLeast: "Hindi bababa sa"});
if (UI.tl.dt) Object.assign(UI.tl.dt, {secMenuJourney: "Ang iyong menu para sa buong paglalakbay", menuJourneyNote: "Bawat yugto ay may sariling isang linggong pagkain, ayon sa calories para sa iyong timbang sa yugtong iyon. Ulitin ang linggo hanggang magsimula ang susunod na yugto.", phase: n => `Yugto ${n}`, weeks: (a, b) => a === b ? `Linggo ${a}` : `Linggo \u2066${a}–${b}\u2069`, perDay: "bawat araw", glDay: "Glycemic load bawat araw", glDayNote: "Average ng menu sa ibaba", sugarTips: ["Pumili ng low-GI na carbohydrates: whole grains, beans, lentils, karamihan ng prutas at gulay", "Kumain ng kanin, tinapay at patatas sa maliit na bahagi, kasama ang gulay at protina", "Ireserba ang matatamis at matamis na inumin sa espesyal na okasyon", "Hatiin ang carbohydrates sa buong araw sa halip na isang malaking kainan"]});
if (UI.tl.dt) Object.assign(UI.tl.dt, {freeTitle: "Free day", freeMealTitle: "Free meal", freeDay: "Free day", freeMeal: "Free meal", freePick: "Aking free day", freeNone: "Walang free day", freeBest: "pinakaaktibong araw", freeSuggest: d => `Mungkahi: ${d}, ang iyong pinakaaktibong araw, para magamit ng katawan ang dagdag na pagkain sa ehersisyo.`, freeAllow: n => `Malayang pagpili sa araw na iyon, hanggang mga ${n}`, freeWhen: ["Magsimula sa ika-3 linggo, kapag sanay ka na sa mga bagong gawi", "Hindi hihigit sa isang beses sa isang linggo; laktawan kung tumaas ang timbang", "Panatilihin ang normal na bahagi: isang paboritong ulam, hindi buong araw na pagkain", "Bumalik agad sa plano kinabukasan"], freeWhenMeal: ["Isang free meal bawat linggo sa halip na buong araw, mula ika-3 linggo", "Iwasan ang matatamis, juice at matamis na inumin", "Suriin ang blood sugar 2 oras pagkatapos kumain", "Sundin ang limitasyon sa asin, potassium at likido kung may sakit sa bato"]});
if (UI.tl.dt) UI.tl.dt.freeMealAllow = n => `Isang free meal, hanggang mga ${n}`;
