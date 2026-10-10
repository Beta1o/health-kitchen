UI.fr = {
    navAbout: "À propos", footNote: "À titre d'information générale ; suivez les conseils de votre équipe soignante.", srcFacet: "Source", fitTitle: "Adapté à mes objectifs", fitLine: (sv, kcal, p) => `Votre portion : ${sv} portion(s), environ ${kcal} kcal, dans la part d'un repas de vos limites de ${p}.`, fitOver: x => `Même une demi-portion dépasse la part d'un repas pour : ${x}. Associez-la aujourd'hui à des plats plus légers.`, fitScale: sv => `Cuisiner uniquement ma portion (${sv} portion)`, fitScaled: sv => `ajusté à ${sv} portion`, perServing: "par portion", myPortionW: "ma portion", recTitle: "Repas recommandés pour vous", recAddAll: "Tout ajouter à Ma journée", recNote: (k, p) => `Une journée de repas adaptée à votre objectif de ${k.toLocaleString()} kcal, dans le respect de vos limites de ${p}. Les portions sont ajustées pour chaque repas.`, servX: x => `${x} portion${x === "1" ? "" : "s"}`, fitOnly: "Convient à mes objectifs quotidiens", settings: "Paramètres", setLang: "Langue", setTheme: "Thème", setAddr: "M'adresser à vous en tant que", addrM: "Homme", addrF: "Femme", setAddrNote: "Modifie la façon dont les instructions en arabe s'adressent à vous.", setData: "Mes données", clearSaved: "Effacer les recettes enregistrées", kidneySub: { hd: "Dialyse", ckd: "MRC, sans dialyse", dm: "MRC + diabète" }, aboutLatest: "Dernières nouveautés", updates: [["2026-10-02", ["Nouveau tableau de bord avec sélecteur d'affection, objectifs quotidiens, conseils et calculateurs", "Suivi du poids, mode cuisine avec minuteurs et unités métriques", "Recettes d'AAKP, Kidney Care UK, My Renal Nutrition et DaVita Saudi Arabia", "Plans de repas de 7 jours à une année complète", "Thèmes clair et sombre, partage et export PDF"]], ["2026-10-01", ["Recettes en anglais, espagnol et arabe", "Plans de santé pour les maladies rénales, le diabète, la tension artérielle et la santé cardiaque"]]], conds: { kidney: "Reins", t2: "Diabète", bp: "Tension artérielle", heart: "Cœur", gen: "Général" },
    aboutWhat: "Qu'est-ce que Cuisine Santé ?", aboutWhatP: "Cuisine Santé rassemble en un seul endroit des recettes d'organisations reconnues dans les domaines de la santé rénale, du diabète et de la santé cardiaque, en anglais, espagnol et arabe. Chaque recette indique ses valeurs nutritionnelles par portion et renvoie à sa source d'origine, pour que vous cuisiniez en toute confiance et partagiez vos trouvailles.",
    aboutHow: "Comment ça marche", aboutSteps: [["🎯", "Choisissez votre affection", "Reins, diabète, tension artérielle, cœur ou général. Le tableau de bord s'y adapte."], ["🍽️", "Trouvez des recettes adaptées", "Filtrez par régime, nutriments et ingrédients, et voyez la part de vos apports quotidiens que représente chaque plat."], ["📅", "Planifiez et cuisinez", "Créez des plans de repas, suivez votre journée et votre poids, et cuisinez pas à pas avec des minuteurs."]],
    aboutSources: "Sources des recettes", aboutSourcesP: "Chaque recette mentionne l'organisation qui l'a publiée et renvoie vers elle.", aboutShare: "Partager Cuisine Santé", shareBtn: "Partager", shareMsg: "Cuisine Santé : des recettes pour la santé rénale, le diabète et la santé cardiaque en anglais, espagnol et arabe.",
    email: "E-mail", copyLink: "Copier le lien", linkCopied: "Lien copié",
    disclaimer: "Cuisine Santé fournit des informations générales. Elle ne remplace pas les conseils de votre médecin, de votre diététicien ou de votre équipe de dialyse ; respectez les limites qu'ils vous indiquent.",
    unitsLabel: "Unités", unitsMetric: "Unités métriques (g, ml, °C)", unitsUS: "Unités américaines (oz, tasses, °F)",
    dRecTitle: "Vos objectifs quotidiens", dTipsTitle: "Conseils pour votre plan", dToolsTitle: "Outils et calculateurs",
    tCalories: "Calories", tPerDay: "par jour", tPerMeal: x => `environ ${x} par repas`, tChoices: n => `environ ${n} choix par repas`, tSalt: g => `= ${g} g de sel`,
    tFluid: "Liquides", tFluidNote: "diurèse + 750 ml", tBmi: "IMC", tNote: "Estimations basées sur votre plan et vos données corporelles (Mifflin-St Jeor pour les calories, poids idéal de Devine). Les objectifs de votre équipe soignante restent prioritaires.",
    bmiCat: b => b < 18.5 ? "Insuffisance pondérale" : b < 25 ? "Poids normal" : b < 30 ? "Surpoids" : "Obésité",
    toolNames: { bmi: "IMC et poids santé", needs: "Calories et protéines quotidiennes", fluid: "Apport en liquides (dialyse)", convert: "Convertisseur sel, mmol et glucides", weight: "Suivi du poids" },
    bmiSub: "Indice de masse corporelle, plage saine, poids idéal", needsSub: "Énergie et protéines pour votre plan", fluidSub: "Selon votre diurèse quotidienne", convSub: "Sel ↔ sodium, mmol ↔ mg, choix de glucides", weightSub: "Notez votre poids et suivez l'évolution",
    height: "Taille", age: "Âge", years: "ans", sex: "Sexe", female: "Femme", male: "Homme", activity: "Activité", act: ["Peu ou pas d'exercice", "Légère (1 à 3 jours/semaine)", "Modérée (3 à 5 jours/semaine)", "Très active (6 à 7 jours/semaine)"],
    healthyRange: "Plage de poids santé", ibw: "Poids idéal", adjw: "Poids ajusté (utilisé pour les protéines)", bmr: "Dépense énergétique de repos (métabolisme de base)", meal: "repas", choicesW: "choix de glucides",
    fluidIntro: "En dialyse, un point de départ courant est votre diurèse quotidienne plus 500 à 1 000 ml. Votre centre de dialyse fixe votre limite réelle.", urine: "Urine par jour", cups250: "Tasses de 250 ml",
    salt: "Sel", convHint: "Saisissez une valeur dans l'une des cases.", date: "Date", addWeight: "Enregistrer le poids", weightSaved: "Poids enregistré", weightEmpty: "Ajoutez au moins deux poids pour voir votre évolution.",
    calcNote: "À titre indicatif uniquement. Demandez vos objectifs personnels à votre médecin ou à votre diététicien.",
    navRecipes: "Recettes", dCats: "Parcourir par catégorie", dAll: "Toutes les recettes", dMore: "Tout voir", dPicks: p => `Nos meilleures idées pour ${p}`, dPlanTitle: "Aujourd'hui dans votre plan de repas", dOpenPlans: "Ouvrir les plans de repas", dBrowse: "Parcourir toutes les recettes", greetMorning: "Bonjour", greetAfternoon: "Bon après-midi", greetEvening: "Bonsoir", streak: n => `Série de ${n} jours`, pickPlan: "Pour quelle raison cuisinez-vous ?",
    nextIdea: slot => `Idée : ${slot.toLowerCase()}`, tipTitle: "Conseil du jour", cookMode: "Mode cuisine", stepOf: (i, n) => `Étape ${i} sur ${n}`, startTimer: "Démarrer", timerDone: "Le temps est écoulé !", finish: "Terminer",
    mealPlans: "Plans de repas", mpTitle: n => `Plan de repas sur ${n} jours`, mpLen: n => n === 365 ? "1 an" : `${n} jours`, mpDayOf: (d, n) => `Jour ${d} sur ${n}`, mpIntro: p => `Créé à partir de la collection correspondant à votre plan : ${p}. Le petit-déjeuner, le déjeuner, le dîner et la collation de chaque jour respectent vos limites quotidiennes.`,
    mpSlots: ["Petit-déjeuner", "Déjeuner", "Dîner", "Collation"], mpDay: d => `Jour ${d}`, mpShuffle: "Mélanger", mpUseDay: "Ajouter ce jour à Ma journée", mpUsed: "Jour ajouté à Ma journée",
    mpNone: "Pas assez de recettes respectent ces limites. Assouplissez une limite dans votre plan.", mpNote: "Simples suggestions, générées automatiquement à partir des données nutritionnelles. Vérifiez les portions avec votre équipe soignante.",
    heroEyebrow: "Reins · diabète · tension artérielle · cœur", heroTitle: 'Une cuisine de tous les jours, <em>pensée pour votre santé</em>',
    heroLede: n => `${n} recettes d'organisations de santé reconnues, avec les valeurs nutritionnelles complètes par portion. Choisissez un plan pour les maladies rénales, le diabète, la tension artérielle ou la santé cardiaque et voyez comment chaque plat s'intègre à votre journée.`,
    statRecipes: "recettes", statPhotos: "avec photos", statVideos: "vidéos de cuisine", statSources: "sources", featured: "À la une",
    legendLo: "Faible", legendMid: "Modéré", legendHi: "Élevé", legendMeal: "part d'un repas", navHome: "Accueil", themeNames: { system: "Thème : système", dark: "Thème : sombre", light: "Thème : clair" }, source: "Source", allDone: "Toutes les étapes sont terminées. Bon appétit !",
    plan: "Mon plan de santé", planEdit: "Modifier les quantités", profiles: { hd: "Reins : dialyse", ckd: "Reins : MRC, sans dialyse", dm: "Reins : MRC avec diabète", t2: "Diabète", bp: "Hypertension artérielle", heart: "Santé cardiaque", gen: "Alimentation saine générale" },
    planIntro: "Choisissez votre plan et saisissez les quantités quotidiennes indiquées par votre médecin ou votre diététicien. Les jauges des recettes montrent la part de chaque portion pour un repas, comptée comme un tiers de votre journée. Les limites passent à l'orange puis au rouge à mesure que vous vous en approchez ; les objectifs se remplissent en vert.",
    weight: "Poids corporel", perKg: "Protéines par kg de poids corporel", daily: "Quantités quotidiennes", carbsOff: "laissez vide pour ne pas suivre",
    planSource: "Valeurs de départ : les plans rénaux suivent les KDOQI 2020 (protéines, sodium) et la pratique des diététiciens en néphrologie (potassium, phosphore) ; le diabète suit les recommandations de l'ADA, soit environ 45 à 60 g de glucides par repas ; la tension artérielle suit DASH et l'AHA (1 500 mg de sodium, aliments riches en potassium) ; la santé cardiaque et l'alimentation générale suivent l'AHA et les Dietary Guidelines for Americans (sodium sous 2 300 mg, sucres ajoutés sous 25 à 50 g, fibres 25 à 30 g). Les chiffres de votre propre équipe soignante restent prioritaires.",
    reset: "Réinitialiser les limites", resetPlan: "Utiliser les valeurs de départ", done: "Terminé",
    dv: "L'avis du diététicien", dvSub: "part d'un repas · un tiers de votre journée", mealPct: p => `${p} % d'un repas`, dayPct: p => `${p} % de la journée`,
    goal: "objectif", ratio: "Phosphore par gramme de protéines", ratioNote: "Moins de 12 mg par gramme est considéré comme favorable. Basé sur le phosphore total, car DaVita ne détaille pas séparément les additifs phosphatés.",
    nK: "Riche en potassium. Si votre taux de potassium est élevé, interrogez votre diététicien sur la portion.",
    nP: "Riche en phosphore. Demandez à votre diététicien si vous devez prendre votre chélateur de phosphate avec ce repas.",
    nNa: p => `Une portion représente ${p} % du sodium d'une journée.`, nLow: "Pauvre en sodium, en potassium et en phosphore.",
    nProtGood: g => `Bonne source de protéines : ${g} g vers votre objectif de protéines en dialyse.`, nProtOver: "Plus de protéines que le tiers de votre limite quotidienne de protéines.",
    nSugar: g => `${g} g de sucres ajoutés par portion. Comptez-les dans vos choix de glucides.`, nCarb: c => `${c} choix de glucides par portion (environ 15 g chacun).`,
    nFiber: "Bonne source de fibres.", limitW: "limite", goalW: "objectif", perDay: "jour", planDesc: { hd: "Plus de protéines, sodium, potassium et phosphore limités", ckd: "Moins de protéines, minéraux limités", dm: "Limites rénales plus glucides et sucres", t2: "Glucides, sucres ajoutés et fibres", bp: "DASH : pauvre en sodium, riche en potassium", heart: "Sodium, sucres, cholestérol, fibres", gen: "Objectifs équilibrés pour le quotidien" }, nKGood: "Riche en potassium, ce qui aide à faire baisser la tension artérielle (demandez d'abord conseil si vous avez une maladie rénale).",
    addDay: "Ajouter à ma journée", added: "Ajouté à ma journée", servingsEaten: "Portions", myDay: "Ma journée",
    dayIntro: "Les recettes que vous prévoyez de manger aujourd'hui, totalisées par rapport à vos apports quotidiens.", dayEmpty: "Rien de prévu pour l'instant. Ouvrez une recette et choisissez « Ajouter à ma journée ».",
    dayTotals: "Totaux du jour", clearDay: "Vider la journée", remove: "Retirer", calories: "Calories", nutr: ["Sodium","Potassium","Phosphore","Protéines","Glucides","Sucres ajoutés","Fibres","Cholestérol"], brand: 'Cuisine <span>Santé</span>', tagline: n => `${n} recettes pour la santé rénale, le diabète et la santé cardiaque`, search: "Rechercher des recettes ou des ingrédients, p. ex. poulet, cannelle, riz",
    filters: "Filtres", saved: "Enregistrées", refine: "Affiner les résultats par", clearAll: "Tout effacer", all: "Toutes les recettes",
    diet: "Type de régime", cat: "Catégorie", dish: "Type de plat", method: "Mode de cuisson", holiday: "Fête", cuisine: "Cuisine",
    serv: "Nombre de portions", photo: "Avec photo de la recette", photoYes: "Avec photo", photoNo: "Sans photo", dietNote: "Les recettes doivent correspondre à tous les régimes cochés",
    quick: "Sélections rapides par affection", limits: "Limites de nutriments par portion", reset: "Réinitialiser les limites", leaveOut: "Exclure un ingrédient", leavePh: "p. ex. tomate, fromage",
    more: "Plus", hasVideo: "Avec vidéo de cuisine", rated4: "Notées 4 étoiles ou plus", any: "Indifférent", sort: "Trier",
    sorts: { az: "De A à Z", fit: "Plus faible part de mes limites", na: "Moins de sodium", k: "Moins de potassium", p: "Moins de phosphore", cal: "Moins de calories", protein: "Plus de protéines", new: "Mises à jour récemment" },
    count: (n, c) => `<span class="num">${n}</span> ${n === 1 ? "recette" : "recettes"}`, moreBtn: n => `Afficher plus de recettes (${n} restantes)`,
    emptyH: "Aucune recette ne correspond à tous ces filtres", emptyP: "Retirez un filtre ou assouplissez une limite de nutriments pour voir plus de résultats.",
    presets: ["Pauvre en sodium", "Pauvre en potassium", "Pauvre en phosphore", "Adapté au diabète", "Bon pour le cœur", "Moins de 300 calories", "Moins de protéines"],
    sliders: ["Sodium", "Potassium", "Phosphore", "Protéines", "Calories", "Glucides", "Sucres ajoutés", "Cholestérol"],
    lvl: { lo: "Faible", mid: "Modéré", hi: "Élevé" }, minerals: ["Sodium", "Potassium", "Phosphore"],
    reviews: n => `${n} avis`, cal: "cal", protein: "g de protéines", video: "Vidéo", back: "Retour", prev: "Précédent", next: "Suivant", save: "Enregistrer", savedBtn: "Enregistrée", copy: "Copier",
    source: "DaVita", copied: "Recette copiée", copyFail: "Sélectionnez le texte pour le copier",
    portions: "Portions", serving: "Taille de la portion", dietTypes: "Types de régime", ing: "Ingrédients", prep: "Préparation", hints: "Astuces utiles",
    nut: "Nutriments par portion", choices: "Choix d'aliments pour les reins et le diabète rénal", carb: "Choix de glucides", by: "Proposée par",
    items: n => `${n} éléments · touchez pour cocher`, stepsHint: "touchez une étape lorsqu'elle est terminée", watch: "Regarder la vidéo de cuisine", watchSub: "Ouvre la vidéo dans un nouvel onglet",
    translated: src => `Traduit de la recette originale ${src}`, officialEs: "Version espagnole officielle de DaVita",
    occasions: "Occasions", without: "Sans", saveOnly: "Enregistrées uniquement", servUnit: "portions",
    footer: (n, x) => `${n} recettes de DaVita et d'organisations de premier plan en santé rénale, diabète et santé cardiaque, en anglais, espagnol et arabe. Niveaux de couleur par portion : sodium faible ≤140 mg, élevé >400 mg ; potassium faible ≤200 mg, élevé >400 mg ; phosphore faible ≤100 mg, élevé >250 mg. Ils servent uniquement au tri. Suivez les conseils de votre médecin ou de votre diététicien.` };
NLABEL.fr = ["Calories","Protéines","Glucides","Lipides","Cholestérol","Sodium","Potassium","Phosphore","Calcium","Fibres","Sucres ajoutés"];
NUNIT.fr = ["","g","g","g","mg","mg","mg","mg","mg","g","g"];
TIPS_X.fr = {
  kidney: [
    ["🥔", "Réduisez le potassium des pommes de terre et des légumes racines : épluchez-les, coupez-les en dés et faites-les tremper, ou faites-les bouillir deux fois dans de l'eau fraîche."],
    ["🏷️", "Vérifiez dans la liste des ingrédients la présence d'additifs phosphatés (mots contenant « phos »). L'organisme absorbe presque entièrement le phosphore des additifs."],
    ["🌿", "Parfumez vos plats avec des herbes, du citron, de l'ail et des épices plutôt qu'avec du sel. Évitez les substituts de sel à base de chlorure de potassium."],
    ["💧", "Si vous avez une limite de liquides, comptez aussi les soupes, les glaçons et les fruits juteux comme des liquides."],
    ["💊", "Prenez vos chélateurs de phosphate avec les repas et les collations, exactement comme prescrit."]],
  diabetes: [
    ["🍽️", "Utilisez la méthode de l'assiette : la moitié de légumes non féculents, un quart de protéines maigres, un quart d'aliments riches en glucides."],
    ["⚖️", "Gardez des portions de glucides similaires à chaque repas. Un choix de glucides correspond à environ 15 g."],
    ["🌾", "Choisissez des céréales complètes, des haricots et des lentilles ; leurs fibres ralentissent l'élévation de la glycémie."],
    ["🥤", "Remplacez les boissons sucrées par de l'eau, du thé ou du café non sucrés."],
    ["🍎", "Mangez les fruits avec un peu de protéines ou de bonnes graisses, et répartissez-les au fil de la journée."]],
  bp: [
    ["🧂", "La plupart du sodium provient du pain, de la charcuterie, des soupes en conserve, des cornichons et de la restauration, et non de la salière."],
    ["🥬", "Mangez beaucoup de légumes, de fruits et de légumineuses riches en potassium, sauf si votre médecin limite le potassium."],
    ["🥛", "Choisissez des produits laitiers allégés et des céréales complètes, comme dans le régime DASH."],
    ["🥫", "Rincez les haricots et les légumes en conserve pour éliminer jusqu'à un tiers du sodium."],
    ["🚶", "Bougez environ 30 minutes presque tous les jours ; même une courte marche après les repas est bénéfique."]],
  heart: [
    ["🫒", "Cuisinez avec de l'huile d'olive ou de colza plutôt qu'avec du beurre ou du ghee."],
    ["🐟", "Mangez du poisson deux fois par semaine, en particulier du poisson gras comme le saumon ou les sardines."],
    ["🥩", "Choisissez des morceaux de viande maigres et retirez le gras visible et la peau."],
    ["🥣", "L'avoine, l'orge, les haricots et les lentilles contiennent des fibres solubles qui aident à faire baisser le cholestérol LDL."],
    ["🍬", "Limitez les sucres ajoutés à environ 25 g par jour pour les femmes et 36 g pour les hommes."]],
  gen: [
    ["📅", "Planifiez les repas de la semaine à l'avance : cela fait économiser de l'argent et préserve l'équilibre nutritionnel."],
    ["💧", "Buvez de l'eau tout au long de la journée, sauf si vous avez une limite de liquides."],
    ["🍇", "Mangez des légumes et des fruits de toutes les couleurs pour varier les nutriments."],
    ["🏷️", "Lisez les étiquettes nutritionnelles par portion et vérifiez combien de portions contient l'emballage."],
    ["🥕", "Gardez des collations faciles à portée de main : fruits, bâtonnets de légumes ou yaourt."]]
};
TERMS_X.fr = {
"5 or less ingredients": "5 ingrédients ou moins",
"African": "Africaine",
"American": "Américaine",
"Appetizers & Snacks": "Entrées et en-cas",
"Asian": "Asiatique",
"Bake": "Cuisson au four",
"Beef, Lamb & Pork": "Bœuf, agneau et porc",
"Beverages": "Boissons",
"Bread": "Pain",
"Breads": "Pains",
"Breakfast & Brunch": "Petit-déjeuner et brunch",
"British": "Britannique",
"Budget": "Économique",
"CKD non-dialysis": "MRC sans dialyse",
"Cake": "Gâteau",
"Candy": "Confiseries",
"Caribbean": "Caribéenne",
"Chicken & Turkey": "Poulet et dinde",
"Chinese": "Chinoise",
"Christmas": "Noël",
"Cookies": "Biscuits",
"Desserts": "Desserts",
"Diabetes": "Diabète",
"Dialysis": "Dialyse",
"Easter": "Pâques",
"Easy": "Facile",
"Filipino": "Philippine",
"Fish & Seafood": "Poissons et fruits de mer",
"Freezer": "Congélateur",
"French": "Française",
"Fry": "Friture",
"German": "Allemande",
"Gluten-free": "Sans gluten",
"Greek": "Grecque",
"Grill": "Grillade",
"Halloween": "Halloween",
"Hanukkah": "Hanoucca",
"Hawaiian": "Hawaïenne",
"Heart Healthy": "Bon pour le cœur",
"Higher Potassium": "Plus riche en potassium",
"Independence Day": "Fête de l'Indépendance",
"Indian": "Indienne",
"International": "Internationale",
"Irish": "Irlandaise",
"Italian": "Italienne",
"Japanese": "Japonaise",
"Jewish": "Juive",
"Korean": "Coréenne",
"Lower Potassium": "Plus pauvre en potassium",
"Lower Protein": "Moins de protéines",
"Meatless Entree": "Plat principal sans viande",
"Mediterranean": "Méditerranéenne",
"Mexican": "Mexicaine",
"Microwave": "Micro-ondes",
"Middle Eastern": "Moyen-orientale",
"Mother's Day": "Fête des mères",
"Muffin": "Muffin",
"Native American": "Amérindienne",
"New Year": "Nouvel An",
"No Cooking": "Sans cuisson",
"One-Dish Meal": "Plat unique",
"Oven": "Four",
"Pasta, Rice & Grains": "Pâtes, riz et céréales",
"Picnic": "Pique-nique",
"Pie": "Tarte",
"Pizza & Sandwiches": "Pizzas et sandwichs",
"Potluck": "Repas partagé",
"Quick": "Rapide",
"Refrigerator": "Réfrigérateur",
"Roast": "Rôti",
"Salads & Dressings": "Salades et vinaigrettes",
"Sauces & Seasonings": "Sauces et assaisonnements",
"Slow Cooker": "Mijoteuse",
"Soup": "Soupe",
"Soups & Stews": "Soupes et ragoûts",
"South American": "Sud-américaine",
"Southern": "Cuisine du Sud des États-Unis",
"Spanish": "Espagnole",
"Special Celebrations": "Fêtes et célébrations",
"St Patrick's Day": "Saint-Patrick",
"Stew": "Ragoût",
"Stir-fry": "Sauté à la poêle",
"Stove Top": "Sur la cuisinière",
"Thai": "Thaïlandaise",
"Thanksgiving": "Thanksgiving",
"Valentine's Day": "Saint-Valentin",
"Vegetables": "Légumes",
"Vegetarian": "Végétarien"
};

Object.assign(UI.fr, {
  accTitle: "Mon compte",
  accOpen: "Ouvrir mon compte",
  signIn: "Se connecter",
  signUp: "Créer un compte",
  signOut: "Se déconnecter",
  signedOut: "Déconnecté",
  password: "Mot de passe",
  authIntro: "Connectez-vous pour conserver vos informations, plans, poids et recettes enregistrées dans votre compte.",
  noAccount: "Nouveau ici ?",
  haveAccount: "Vous avez déjà un compte ?",
  guest: "Continuer sans compte",
  pwShort: "Utilisez au moins 8 caractères pour votre mot de passe.",
  welcome: n => `Bienvenue, ${n}`,
  synced: "Enregistré dans votre compte",
  syncing: "Enregistrement…",
  syncErr: "Non enregistré, vérifiez la connexion",
  adminTitle: "Administration",
  adUsers: "Utilisateurs",
  adAdmins: "Administrateurs",
  adActive: "Actifs cette semaine",
  adWeighIns: "Pesées",
  adPlans: "Utilisateurs par plan",
  adSaved: "Enregistrées",
  adLast: "Dernière connexion",
  adRole: "Rôle",
  confirmDel: "Appuyez encore pour supprimer",
  loading: "Chargement…",
  pfTitle: "Mes informations",
  pfName: "Nom",
  pfGoal: "Objectif de poids",
  goalLose: "Perdre du poids",
  goalKeep: "Garder mon poids",
  goalGain: "Prendre du poids",
  pfTarget: "Poids cible",
  pfGoalNote: k => `Votre objectif calorique est maintenant d'environ ${k} kcal par jour.`,
  pfPrefs: "Préférences et aliments que j'évite",
  pfDislikes: "Aliments que je ne mange pas",
  pfAllergies: "Allergies",
  pfLikes: "Aliments que j'aime",
  pfHide: "Masquer les recettes contenant des aliments que j'évite",
  pfDoctor: "Consignes du médecin et médicaments",
  pfDoctorNote: "Consignes de mon médecin ou de mon diététicien",
  pfMeds: "Mes médicaments (p. ex. chélateur de phosphate pendant les repas)",
  pfDoctorShort: "Mes notes de santé",
  pfProgress: (w, t) => `Actuel ${w} kg · cible ${t} kg (${(w - t > 0 ? "−" : "+") + Math.abs(w - t).toFixed(1)} kg restants)`
});

Object.assign(UI.fr, { roleUser: "Utilisateur", roleAdmin: "Administrateur" });

Object.assign(UI.fr, { netErr: "Impossible de joindre le serveur des comptes. Réessayez dans un instant.", localOnly: "Vos informations sont enregistrées sur cet appareil uniquement. Pour les garder dans un compte, ouvrez l'app depuis le serveur Health Kitchen (voir le README)." });

Object.assign(UI.fr, { fitOf: (sv, total, amt) => `Vous mangez ${sv} des ${total} portions de la recette${amt ? ` (${sv} × ${amt} chacune)` : ""}. Les nutriments de votre part sont dans la colonne « ma part ».` });

Object.assign(UI.fr, { signInNeeded: "Connectez-vous pour voir votre compte : vos informations, statistiques, plan et paramètres.", stTitle: "Mes statistiques", stToday: "Aujourd’hui", stAvg7: "Moyenne (7 derniers jours)", stDays: "Jours enregistrés", stStreak: "Jours consécutifs", stSaved: "Recettes enregistrées", stWeighIns: "Pesées", stChange: "Variation de poids", stBmi: "IMC", badLogin: "E-mail ou mot de passe incorrect.", accDisabled: "Ce compte est désactivé. Contactez l’administrateur.", emailTaken: "Un compte avec cet e-mail existe déjà.", badEmail: "Saisissez une adresse e-mail valide.", adOnly: "Seuls les administrateurs peuvent ouvrir cette page. Connectez-vous avec un compte administrateur.", adActiveDay: "Actifs aujourd’hui", adDisabled: "Comptes désactivés", adDisabledOne: "Désactivé", adSignups: "Nouveaux utilisateurs (30 derniers jours)", adNoPlan: "Aucun plan pour l’instant", adRecipesLang: "Recettes par langue", adRecipesSrc: "Recettes par source", adSearch: "Rechercher par e-mail ou nom", adExport: "Exporter en CSV", adDetail: "Détails", adJoined: "Inscription", adPrivacy: "Les notes de santé, les consignes du médecin et les médicaments restent privés pour l’utilisateur et ne sont pas affichés ici.", adNewPw: "Nouveau mot de passe (8 caractères min.)", adResetPw: "Définir le mot de passe", adEnable: "Activer le compte", adDisable: "Désactiver le compte", adPwDone: "Mot de passe modifié. L’utilisateur a été déconnecté de tous ses appareils." });

UI.fr.profiles = { none: "Sans plan (toutes les recettes)", ...UI.fr.profiles }; UI.fr.conds = { ...UI.fr.conds, none: "Toutes les recettes" };

Object.assign(TERMS_X.fr, {"Latin American": "Latino-américaine", "Saudi": "Saoudienne", "Emirati": "Émiratie", "Bahraini": "Bahreïnienne", "Lebanese": "Libanaise", "Turkish": "Turque", "Moroccan": "Marocaine", "Tunisian": "Tunisienne", "Egyptian": "Égyptienne", "Persian": "Persane", "Afghan": "Afghane"});

Object.assign(UI.fr, {
  tabOverview: "Aperçu",
  tabProfile: "Mes informations",
  tabHealth: "Santé et objectifs",
  tabFood: "Préférences alimentaires",
  tabWeight: "Poids",
  stKcal14: "Calories, 14 derniers jours",
  stGoal: "Progression de l'objectif de poids",
  stGoalDone: "Objectif atteint, bravo !",
  stNoData: "Aucun historique pour l'instant. Ajoutez des repas dans Ma journée et ils apparaîtront ici.",
  weightLog: "Journal de poids",
  stGoalLeft: n => `${n} kg restants`,
  memberSince: d => `Membre depuis ${d}`
});

Object.assign(UI.fr, { mpCuisines: "Cuisines", mpAllCuisines: "Toutes les cuisines", mpCuisNote: "Les repas viennent des cuisines choisies ; un repas qu'elles ne couvrent pas utilise n'importe quelle cuisine." });

Object.assign(UI.fr, { noServer: "Les comptes ne sont pas disponibles sur cette copie de l'app. Ouvrez-la depuis le serveur Health Kitchen pour vous inscrire et suivre vos plans et informations." });

Object.assign(UI.fr, {
  "tabMyRecipes": "Mes recettes",
  "subNew": "Partager une recette",
  "subIntro": "Les recettes que vous partagez sont vérifiées par notre équipe (quantités, unités et ingrédients) avant que quiconque puisse les voir.",
  "subTitle": "Nom de la recette",
  "subDesc": "Brève description",
  "subCat": "Catégorie",
  "subCuisine": "Cuisine",
  "subServings": "Portions",
  "subServing": "Taille de la portion (p. ex. 1 assiette, 250 g)",
  "subIng": "Ingrédients",
  "subQty": "Quantité",
  "subItem": "Ingrédient",
  "subAddIng": "+ Ajouter un ingrédient",
  "subSteps": "Étapes",
  "subAddStep": "+ Ajouter une étape",
  "subHints": "Astuces (une par ligne)",
  "subNut": "Valeurs nutritionnelles par portion (facultatif)",
  "subSend": "Envoyer pour relecture",
  "subSent": "Envoyée pour relecture. Vous verrez le résultat dans Mes recettes.",
  "subMine": "Mes recettes partagées",
  "subNone": "Vous n'avez encore partagé aucune recette.",
  "stPending": "En attente de relecture",
  "stApproved": "Publiée",
  "stRejected": "Non approuvée",
  "subNote": "Note du relecteur",
  "subDelete": "Supprimer",
  "subErr": "Veuillez ajouter un nom, une catégorie, au moins un ingrédient avec sa quantité et son unité, et une étape.",
  "adSubs": "Recettes soumises",
  "adApprove": "Approuver et publier",
  "adReject": "Ne pas approuver",
  "adNotePh": "Note pour l'auteur (p. ex. merci d'indiquer la quantité en grammes)",
  "adNoSubs": "Aucune recette ici.",
  "community": "Communauté"
});

Object.assign(UI.fr, { meal: "Type de plat", mealTypes: {"main": "Plat principal", "breakfast": "Petit-déjeuner", "starter": "Entrée", "side": "Accompagnement", "snack": "En-cas", "dessert": "Dessert", "drink": "Boisson", "condiment": "Sauce ou assaisonnement"}, fitCond: "C'est une sauce ou un assaisonnement, pas un repas à part entière : une portion accompagne un repas et ses nutriments comptent dans ce repas." });
Object.assign(UI.fr, {"cfgTitle":"Paramètres de l’appli","cfgDefaults":"Valeurs par défaut pour les nouveaux visiteurs","cfgDefaultsNote":"Utilisées tant que le visiteur n’a pas fait son propre choix.","cfgVisitorChoice":"Appareil du visiteur","cfgAccounts":"Comptes","cfgSignups":"Autoriser les nouvelles inscriptions","cfgSession":"Rester connecté pendant","cfgDays":"jours","cfgAnnounce":"Annonce sur la page d’accueil","cfgAnnounceOn":"Afficher l’annonce","cfgInfo":"Information","cfgWarn":"Important","cfgAnnounceNote":"Laissez une langue vide pour afficher le texte anglais.","cfgSources":"Sources de recettes affichées","cfgSourcesNote":"Les sources décochées sont masquées pour tout le monde.","cfgLangs":"Langues proposées","cfgSave":"Enregistrer les paramètres","dbTitle":"Base de données","dbStatus":"État","dbConnected":"Connecté","dbNoTables":"Tables manquantes","dbName":"Base de données","dbHost":"Serveur","dbUser":"Utilisateur","dbSize":"Taille","dbStates":"Profils enregistrés","dbSupported":"Pris en charge","dbChange":"Utiliser une autre base de données","dbChangeNote":"Testez d’abord la connexion. Pour utiliser une nouvelle base vide, créez les tables avec un compte propriétaire, puis basculez avec l’utilisateur API (hk_api). Les données ne sont pas copiées d’une base à l’autre.","dbApiUrl":"URL de connexion API","dbOwnerUrl":"URL de connexion propriétaire (pour créer les tables)","dbTest":"Tester la connexion","dbSwitch":"Basculer vers cette base","dbSetup":"Créer les tables","dbOk":"La connexion fonctionne","dbSetupDone":"Les tables, règles de sécurité et fonctions sont en place.","dbSwitched":"L’appli utilise maintenant la nouvelle base de données."});

Object.assign(UI.fr, { confirmEmail: "Compte créé. Ouvrez le lien de confirmation reçu par e-mail, puis connectez-vous.", adPwEmail: "Envoyer un e-mail de réinitialisation", adPwEmailed: "Un e-mail de réinitialisation a été envoyé à l'utilisateur." });

Object.assign(UI.fr, Object.fromEntries(Object.entries({"sbProject": "Project", "sbSignups": "Sign-ups open", "sbConfirm": "Email confirmation", "sbUrl": "Project URL", "sbKey": "Publishable key (public)", "sbNote": "Accounts and data are stored in Supabase with row-level security. Keys and passwords are managed in the Supabase dashboard; the secret key is never used in the app.", "sbDash": "Dashboard", "sbUsers": "Users", "sbUrls": "Sign-in URLs", "sbProviders": "Sign-in methods", "sbTables": "Tables"}).filter(([k]) => !(k in UI.fr))));

Object.assign(UI.fr, Object.fromEntries(Object.entries({"dbConnectTitle": "Connect a database (e.g. Supabase)", "dbConnectNote": "Paste the owner connection string (in Supabase: Project Settings \u2192 Database \u2192 Connection string, with your database password). The server sets up the tables and security rules, creates a restricted app user with its own password, copies the current accounts and data, and switches. The details are stored encrypted on this server only.", "dbConnectUrl": "Owner connection string", "dbCopy": "Copy the current accounts and data", "dbConnectBtn": "Set up and connect", "dbEncrypted": "The connection is stored encrypted on this server."}).filter(([k]) => !(k in UI.fr))));

Object.assign(UI.fr, Object.fromEntries(Object.entries({"dbPort": "Port", "dbOrUrl": "Or paste a full connection string", "dbNeedFields": "Enter the host and the database password (or a full connection string)."}).filter(([k]) => !(k in UI.fr))));

Object.assign(UI.fr, Object.fromEntries(Object.entries({"dbTablesReady": "Health Kitchen tables found", "dbTablesNew": "empty: tables will be created", "dbNoRoles": "this user cannot create the app user; use the owner (postgres) account"}).filter(([k]) => !(k in UI.fr))));

Object.assign(TERMS_X.fr, {"Canadian": "Canadienne", "Eastern European": "Europe de l'Est", "Jamaican": "Jamaïcaine"});
Object.assign(TERMS_X.fr, {"North African": "Nord-africaine"});
Object.assign(UI.fr, {"tabMeals": "Tableau des repas", "mtIntro": "Prévoyez la recette de chaque repas, puis cochez-la une fois mangée.", "mtAssign": "Attribuer à un repas", "mtAssignShort": "Attribuer", "mtTaken": "Pris", "mtDay": "Jour", "mtTotal": "Prévu · pris", "mtEmpty": "Rien d'attribué pour l'instant. Remplissez la semaine depuis un plan de repas, ou ouvrez une recette et choisissez « Attribuer à un repas ».", "mtFromPlan": "Enregistrer le plan dans mon tableau", "mtSaved": "Enregistré dans votre tableau des repas", "mtPick": "Choisissez une recette", "mtSearch": "Rechercher des recettes", "mtClear": "Vider cette semaine", "mtAssigned": "Attribuée", "mtRemove": "Retirer", "mtFill": "Remplir depuis un plan de repas", "mtWhen": "Quel jour ?", "mtWhich": "Quel repas ?", "mtToday": "Aujourd'hui", "mtThisWeek": "Cette semaine"}, { mtDone: (a, b) => `${a} repas pris sur ${b}` });
Object.assign(UI.fr, {"authNotConfirmed": "Cet e-mail n'est pas encore confirmé. Ouvrez le lien de confirmation reçu, puis connectez-vous.", "authEmailLimit": "Trop d'e-mails envoyés à l'instant. Attendez quelques minutes et réessayez.", "authNoMail": "Le serveur de comptes ne peut pas encore envoyer d'e-mail à cette adresse. Demandez à l'administrateur d'ajouter votre compte.", "authClosed": "Les nouvelles inscriptions sont fermées."});
Object.assign(UI.fr, {"sbSignin": "Connexion", "sbEmailLogin": "Connexion par e-mail et mot de passe", "sbOn": "Activé", "sbOff": "Désactivé", "sbOpen": "Ouvertes", "sbClosed": "Fermées", "sbConfirmOff": "Les nouveaux utilisateurs sont connectés dès la création du compte.", "sbConfirmOn": "Les nouveaux utilisateurs doivent ouvrir un e-mail de confirmation avant de se connecter.", "sbDetails": "Détails de connexion", "sbCopy": "Copier", "sbCopied": "Copié"});
Object.assign(UI.fr, {"mtType": "Type", "mtSlotTypes": "Adapté à ce repas", "mtAllTypes": "Tous les types", "mtFitOnly": "Seulement les recettes adaptées à mon plan pour ce repas", "mtFits": "Adaptée à votre plan pour ce repas", "mtHigh": "Au-dessus de la part de ce repas dans votre plan"}, { mtResults: n => `${n} recettes` });
Object.assign(UI.fr, { shopTitle: "Liste de courses", shopTesting: "En test · administrateurs et superviseurs", shopIntro: "Tout ce qu'il faut acheter pour vos repas prévus, additionné sur les recettes et calculé pour une portion par personne et par repas.", shopFrom: "D'après", shopPlan: "Plan de repas", shopTable: "Mon tableau des repas", shopDays: "Jours", shopPeople: "Personnes", shopStaplesNote: "Vérifiez ce que vous avez déjà.", shopNeeded: "selon besoin", shopRecipes: "Recettes de cette liste", shopCopy: "Copier la liste", shopPrint: "Imprimer", shopClear: "Tout décocher", shopEmpty: "Aucun repas prévu pour ces jours. Attribuez des repas dans votre tableau ou choisissez Plan de repas.", roleSupervisor: "Superviseur", roleVisitor: "Visiteur (non connecté)", adRole: "Rôle", adRoleNote: "Les superviseurs voient aussi les fonctions en test (Admin → Privilèges).", adRoleFixed: "les administrateurs sont définis par la liste d'e-mails administrateur", privTitle: "Privilèges", privIntro: "Choisissez qui voit chaque partie de l'app. Les administrateurs voient tout ; Visiteur signifie non connecté. Enregistrement immédiat.", privSaved: "Privilèges enregistrés", shopSec: {"produce": "Fruits et légumes", "meat": "Viande et poisson", "dairy": "Produits laitiers et œufs", "bakery": "Pain et boulangerie", "grains": "Riz, pâtes et céréales", "canned": "Conserves et bocaux", "frozen": "Surgelés", "nuts": "Noix, graines et fruits secs", "other": "Autres", "staples": "Placard"}, feat: {"shop": "Liste de courses", "plans": "Plans de repas", "table": "Tableau des repas", "day": "Ma journée", "saved": "Recettes enregistrées", "submit": "Proposer des recettes", "cook": "Mode cuisine", "pdf": "PDF et impression"}, shopMeals: (m, r) => `${m} repas · ${r} recettes`, shopItems: n => `${n} articles`, shopLeft: n => `${n} à acheter`, shopUsed: n => n === 1 ? "dans 1 recette" : `dans ${n} recettes` });
Object.assign(UI.fr, {"pwRule": "Utilisez au moins 10 caractères avec des lettres et des chiffres, et évitez les mots de passe courants.", "idleOut": "Déconnecté après une période d'inactivité.", "cfgIdle": "Déconnexion après inactivité", "cfgMinutes": "minutes", "cfgIdleNote": "Les personnes connectées sont déconnectées après ce nombre de minutes sans activité (0 = jamais).", "secTitle": "Sécurité"});

UI.fr.dt = { "title": "Mon plan alimentaire", "madeOn": "Créé le", "print": "Imprimer / enregistrer en PDF", "newMenu": "Nouveau menu", "intro": "Votre plan personnel, établi à partir de votre profil : plan de santé, mesures corporelles, activité, objectif et préférences alimentaires. Revoyez-le avec votre médecin ou votre diététicien.", "needInfo": "Ajoutez votre âge, votre taille et votre poids dans Mes informations pour que le plan vous corresponde.", "editInfo": "Modifier mes informations", "secYou": "Vous en bref", "healthy": "Poids santé pour votre taille", "healthyNote": "BMI 18,5–24,9", "secJourney": "Votre parcours", "now": "Maintenant", "goalFig": "Votre objectif", "cheerKeep": "Continuez : un poids stable, une bonne alimentation et du mouvement chaque jour protègent votre santé.", "cheerDone": "Vous avez atteint votre objectif — continuez comme ça !", "benefits": ["Une tension artérielle plus basse et moins d'effort pour le cœur et les reins", "Une glycémie plus stable", "Plus d'énergie, des mouvements plus faciles et un meilleur sommeil"], "secDaily": "Vos objectifs quotidiens", "kcalLose": "environ 500 de moins que ce que vous dépensez", "kcalGain": "environ 300 de plus que ce que vous dépensez", "kcalKeep": "ce que vous dépensez en une journée", "protKidney": "adaptées à votre plan rénal", "carbLimit": "la limite de votre plan", "carbHalf": "environ la moitié de vos calories", "fat": "Lipides", "fatNote": "environ 30 % des calories, surtout de l'huile d'olive, des oléagineux et du poisson", "fluids": "Liquides", "fluidLimit": "votre limite (urine + 750 ml) ; suivez les consignes de votre équipe soignante", "fluidGen": "par jour, sauf si votre équipe soignante limite les liquides", "secTimeline": "Votre chemin vers l'objectif", "tlKeep": "Votre objectif est de garder votre poids : mangez à peu près vos calories du jour et restez actif.", "tlNoTarget": "Indiquez un poids cible dans Santé et objectifs pour voir votre calendrier.", "tlReached": "Vous avez atteint votre poids cible.", "tlLow": "Votre objectif est en dessous d'un poids santé pour votre taille (BMI 18,5). Parlez-en à votre médecin.", "tlHowGain": "Comment : environ 300 kcal de plus par jour, avec des protéines à chaque repas et du renforcement musculaire deux fois par semaine.", "week": "Semaine", "expected": "Poids prévu", "secSplit": "Comment répartir votre journée", "splitNote": "Prenez vos repas à heures régulières ; la collation est facultative. Ajoutez des légumes au déjeuner et au dîner.", "secMenu": "Votre menu sur 7 jours", "menuNote": "Composé de recettes adaptées à votre plan de santé et à vos préférences. La portion (×) est ajustée à vos calories et à vos limites. Touchez une recette pour l'ouvrir.", "dayTotal": "Total du jour", "secChoose": "À privilégier", "secLimit": "À limiter ou éviter", "avoidMine": "Également évités pour vous", "secExercise": "Votre programme d'activité physique", "exWeekly": "Activité hebdomadaire", "exModerate": "modérée : vous pouvez parler mais pas chanter", "exStrengthT": "Renforcement", "exStrengthV": "2 jours par semaine", "exSteps": "Pas par jour", "exStepsNote": "ajoutez environ 500 chaque semaine", "exBurn": "L'exercice brûle", "exPerWeek": "par semaine", "exActivity": "Activité", "exMinutes": "Minutes", "exIntensity": "Intensité", "moderate": "Modérée", "light": "Légère", "ex": {"walk": "Marche rapide", "bike": "Vélo ou natation", "strength": "Renforcement (élastiques, poids légers ou poids du corps)", "stretch": "Étirements et équilibre"}, "exProgress": "Commencez par 10 à 15 minutes à la fois et ajoutez 5 minutes chaque semaine jusqu'à atteindre votre objectif. Les séances courtes (10 minutes) comptent aussi.", "exOlder": "Ajoutez des exercices d'équilibre (tenir sur un pied près d'un mur, marcher en plaçant le talon devant la pointe de l'autre pied) pour prévenir les chutes.", "exSafety": {"kidney": "Faites de l'exercice les jours sans dialyse ou selon les conseils de votre équipe soignante ; ne portez pas de poids et n'appuyez pas avec le bras de la fistule ; comptez les boissons prises pendant l'effort dans votre limite de liquides.", "diabetes": "Contrôlez votre glycémie avant et après l'exercice, ayez toujours du sucre rapide sur vous (jus ou comprimés de glucose) et faites de l'exercice 1 à 3 heures après un repas.", "heart": "Échauffez-vous et récupérez pendant 5 à 10 minutes, ne bloquez pas votre respiration en soulevant des poids, et arrêtez-vous en cas de douleur dans la poitrine, de vertiges ou d'essoufflement inhabituel.", "gen": "Commencez doucement, buvez de l'eau et arrêtez-vous en cas de douleur ou de vertiges."}, "secHabits": "Habitudes de la semaine", "habits": ["Pesez-vous une fois par semaine, le même jour et à la même heure, et notez-le dans Poids", "Notez ce que vous mangez dans Ma journée", "Utilisez le plan de repas et la liste de courses pour faire vos courses une fois par semaine", "Dormez 7 à 9 heures", "Prenez vos médicaments comme prescrit et allez à vos rendez-vous"], "disclaimer": "Ce plan donne des conseils généraux à partir des informations que vous avez saisies. Il ne remplace pas l'avis de votre médecin ou de votre diététicien, surtout en cas de maladie rénale, de diabète ou de problèmes cardiaques.", "foods": {"kidney": {"choose": ["Fruits pauvres en potassium : pommes, fruits rouges, raisin, ananas", "Légumes : chou, chou-fleur, poivrons, concombre, oignon", "Riz blanc, pâtes, pain sans sel", "Viande fraîche, poulet, poisson et œufs selon les portions de votre plan", "Herbes, citron et épices à la place du sel"], "limit": ["Sel, bouillons cubes, pickles, aliments transformés et en conserve", "Aliments riches en potassium : bananes, oranges, pommes de terre, tomates, fruits secs", "Aliments riches en phosphore : produits laitiers, cola, fromage fondu, oléagineux, céréales complètes", "Aliments avec additifs phosphatés (« phos » sur l'étiquette)", "Substituts de sel (ils contiennent du potassium)"]}, "diabetes": {"choose": ["Des légumes à chaque repas (la moitié de l'assiette)", "Céréales complètes : avoine, riz complet, pain complet", "Haricots, lentilles et pois chiches", "Protéines maigres : poisson, poulet, œufs, yaourt", "Eau et boissons non sucrées"], "limit": ["Sucre, sucreries et boissons sucrées, y compris les jus", "Pain blanc, riz blanc et pâtisseries en grandes portions", "Fritures et restauration rapide", "Dattes et fruits secs en grande quantité"]}, "heart": {"choose": ["Légumes et fruits, 5 portions par jour", "Céréales complètes et fibres", "Poisson deux fois par semaine, haricots et lentilles", "Huile d'olive, oléagineux et graines non salés", "Produits laitiers allégés"], "limit": ["Sel et aliments salés (pain, fromage, pickles, plats préparés)", "Viandes grasses et transformées", "Beurre, ghee et fritures", "Sucre et boissons sucrées"]}, "gen": {"choose": ["Légumes et fruits, 5 portions par jour", "Céréales complètes", "Protéines maigres : poisson, poulet, légumineuses, œufs", "Eau", "Repas faits maison"], "limit": ["Sucre et boissons sucrées", "Sel et aliments transformés", "Fritures et restauration rapide", "Grandes portions tard le soir"]}}, "tlLose": (kg, wk, date, rate) => `Perdre environ ${kg} kg en ${wk} semaines (vers ${date}), à raison d'environ ${rate} kg par semaine.`, "tlGain": (kg, wk, date, rate) => `Prendre environ ${kg} kg en ${wk} semaines (vers ${date}), à raison d'environ ${rate} kg par semaine.`, "tlHowLose": (food, ex) => `Comment : environ ${food} kcal de moins par jour dans l'alimentation, plus l'exercice ci-dessous (environ ${ex} kcal par semaine).`, "inWeeks": w => `${w} semaines`, "cheer": (kg, w) => `${kg} kg en ${w} semaines — un repas et une marche à la fois. Vous pouvez y arriver !` };
UI.fr.dt.addMore = "Ajoutez pour atteindre vos calories";
Object.assign(UI.fr.dt, {"goalHealthy": "Poids santé pour vous", "suggestedNote": "Suggéré d'après votre taille (IMC 24,9 au plus). Vous pouvez fixer votre objectif dans Santé et objectifs.", "setGoal": "Fixer mon objectif"});

// glycemic index and load
Object.assign(UI.fr, {"gl": "Charge glycémique", "glBand": {"lo": "Faible", "mid": "Moyenne", "hi": "Élevée"}, "giBand": {"lo": "Faible", "mid": "Moyen", "hi": "Élevé"}, "giTitle": "Effet sur la glycémie", "giIdx": "Index glycémique (IG)", "glServ": "Charge glycémique par portion", "glMine": "Pour ma portion", "giNone": "Trop peu de glucides pour l'évaluer", "giRaise": "Ce qui fait le plus monter la glycémie", "giAbbr": "IG", "glAbbr": "CG", "dayGl": "Charge glycémique", "giNote": "Estimation à partir des ingrédients. L'IG indique la vitesse à laquelle un aliment fait monter la glycémie (glucose = 100) ; la CG tient aussi compte de la quantité de glucides dans la portion. IG : faible 55 ou moins, élevé 70 ou plus. CG : faible 10 ou moins, élevée 20 ou plus.", "giTipHi": "Charge élevée : prenez une plus petite portion, ou accompagnez-la de légumes, de salade ou de protéines pour ralentir la montée de la glycémie.", "giSrc": "Données IG © GI News, Université de Sydney", giShare: n => `${n} % de la charge en sucre`, nGl: (v, b) => `Charge glycémique par portion : ${v} (${b}).`});
UI.fr.giTipKid = "Charge élevée : prenez une plus petite portion, ou répartissez-la sur deux repas.";
if (UI.fr.sorts) UI.fr.sorts.gl = "Charge glycémique la plus faible";
Object.assign(UI.fr.feat || (UI.fr.feat = {}), {"dieter": "Mon plan alimentaire", "gi": "Index glycémique"});
Object.assign(UI.fr, {sbShow: "Afficher", sbHide: "Masquer"});
if (UI.fr.dt) Object.assign(UI.fr.dt, {atMost: "Jusqu'à", atLeast: "Au moins"});
if (UI.fr.dt) Object.assign(UI.fr.dt, {secMenuJourney: "Votre menu pour tout le parcours", menuJourneyNote: "Chaque étape a sa propre semaine de repas, calculée sur les calories adaptées à votre poids à cette étape. Répétez la semaine jusqu'au début de l'étape suivante.", phase: n => `Étape ${n}`, weeks: (a, b) => a === b ? `Semaine ${a}` : `Semaines \u2066${a}–${b}\u2069`, perDay: "par jour", glDay: "Charge glycémique par jour", glDayNote: "Moyenne du menu ci-dessous", sugarTips: ["Choisissez des glucides à IG bas : céréales complètes, haricots, lentilles, la plupart des fruits et légumes", "Mangez le riz, le pain et les pommes de terre en petites portions, avec des légumes et des protéines", "Gardez les sucreries et les boissons sucrées pour les occasions", "Répartissez les glucides sur la journée plutôt qu'en un gros repas"]});
if (UI.fr.dt) Object.assign(UI.fr.dt, {freeTitle: "Jour libre", freeMealTitle: "Repas libre", freeDay: "Jour libre", freeMeal: "Repas libre", freePick: "Mon jour libre", freeNone: "Pas de jour libre", freeBest: "jour le plus actif", freeSuggest: d => `Suggéré : ${d}, votre jour le plus actif, pour que le supplément nourrisse votre exercice.`, freeAllow: n => `Choix libre ce jour-là, jusqu'à environ ${n}`, freeWhen: ["Commencez à partir de la semaine 3, quand les nouvelles habitudes sont installées", "Au plus une fois par semaine ; sautez-le si votre poids a augmenté cette semaine", "Gardez des portions normales : un plat préféré, pas une journée entière à manger", "Reprenez le plan dès le lendemain"], freeWhenMeal: ["Un repas libre par semaine au lieu d'une journée, à partir de la semaine 3", "Sans sucreries, jus ni boissons sucrées", "Mesurez votre glycémie 2 heures après le repas", "Respectez vos limites de sel, potassium et liquides en cas de maladie rénale"]});
if (UI.fr.dt) UI.fr.dt.freeMealAllow = n => `Un repas libre, jusqu'à environ ${n}`;
Object.assign(UI.fr, {giTab: "Index glycémique", giWhat: "Que signifient IG et CG", giTodayT: "Charge glycémique du jour", gi14: "Charge glycémique, 14 derniers jours", giFoods: "Aliments selon leur index glycémique", giFoodsNote: "IG médian des aliments testés dans la base de l'Université de Sydney (glucose = 100). La portion compte aussi : une petite portion d'un aliment à IG élevé peut avoir une charge faible.", giRecs: "Recettes à faible charge glycémique pour vous", giDayEmpty: "Rien dans Ma journée pour l'instant. Ajoutez des recettes pour voir leur charge glycémique.", giNoHist: "Les jours enregistrés dans Ma journée apparaîtront ici.", giTotal: "Total"});
UI.fr.giUsedIn = n => `dans ${n} recettes`;
if (UI.fr.dt) UI.fr.dt.exAerobic = "Marche et vélo";
Object.assign(UI.fr, {gsT: "Rechercher dans la base d'IG", gsName: "Aliment", gsCat: "Catégorie", gsCountry: "Pays", gsAny: "Tous", gsServ: "Portion (g)", gsCarbs: "Glucides par portion (g)", gsSort: "Trier", gsSorts: ["IG le plus bas", "IG le plus élevé", "CG la plus basse", "Nom"], gsMore: "Voir plus", gsN: n => `${n} aliments`, gsNote: n => `Base d'IG de l'Université de Sydney : ${n} aliments avec leur IG mesuré, tels que publiés (noms en anglais). Les aliments contenant du porc, de la gélatine ou de l'alcool sont exclus.`, gsMin: "min", gsMax: "max", gsLoading: "Chargement…"});
Object.assign(UI.fr, {dayGi: "IG combiné", giWhole: "L'IG du plat entier : tous ses ingrédients glucidiques ensemble, chacun pondéré par les glucides qu'il apporte."});
Object.assign(UI.fr, {giWithout: "Sans", giHalf: "Avec la moitié"});
UI.fr.gsLinked = "Seulement les aliments de nos recettes";
Object.assign(UI.fr, {carbServ: "Glucides par portion", giBasis: n => `Il repose sur ${n} % des glucides du plat ; le reste vient d'aliments sans IG mesuré, comme les légumes.`});
if (UI.fr.dt) Object.assign(UI.fr.dt, {showDoctor: "Ceci est un guide. Montrez ce plan à votre médecin ou diététicien.", medsQ: "Prenez-vous des médicaments contre le diabète ?", meds: {"none": "Pas de médicament contre le diabète", "insulin": "Insuline", "sulfonylurea": "Sulfamides (ex. gliclazide, glimépiride)", "other": "Autres médicaments du diabète (ex. metformine)", "unsure": "Je ne sais pas"}, medsWarn: "L'insuline et les sulfamides peuvent faire trop baisser la glycémie. Ne sautez pas de repas, gardez un sucre rapide sur vous (jus ou comprimés de glucose) et voyez toute baisse de calories avec votre médecin. Ce plan garde vos calories d'entretien sauf si vous cochez la case ci-dessous.", medsUnsure: "Demandez à votre médecin ou pharmacien si vos médicaments peuvent faire baisser la glycémie avant de réduire les calories.", cutOk: "Mon médecin a approuvé une baisse de calories", freeOffMeds: "Avec l'insuline ou les sulfamides, ce plan n'a ni jour ni repas libre : les grands changements d'alimentation compliquent le contrôle de la glycémie.", noCutKidney: "En cas de maladie rénale, ce plan ne réduit pas les calories : la perte de poids doit être planifiée avec votre néphrologue ou diététicien rénal pour ne pas perdre de muscle.", noCutMeds: "Ce plan ne réduit pas les calories car vous prenez de l'insuline ou des sulfamides. Cochez « Mon médecin a approuvé une baisse de calories » quand il est d'accord.", sugarTipsKid: ["Répartissez les glucides de façon égale sur vos repas", "Mangez riz, pain et pâtes dans les portions données par votre diététicien rénal", "Gardez sucreries, jus et boissons sucrées pour les occasions", "Vérifiez que tout remplacement respecte vos limites de potassium, phosphore et protéines"]});
UI.fr.giNoEst = "Pas d'estimation d'IG pour ce plat : trop peu de ses ingrédients glucidiques ont un IG mesuré. Comptez plutôt les glucides ci-dessus.";
