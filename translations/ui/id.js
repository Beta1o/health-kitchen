UI.id = {
    navAbout: "Tentang", footNote: "Untuk informasi umum; ikuti saran tim perawatan Anda.", srcFacet: "Sumber", fitTitle: "Sesuaikan dengan target saya", fitLine: (sv, kcal, p) => `Porsi Anda: ${sv} sajian, sekitar ${kcal} kkal, dalam bagian satu kali makan dari batas ${p} Anda.`, fitOver: x => `Setengah sajian pun sudah melebihi bagian satu kali makan untuk: ${x}. Padukan dengan hidangan yang lebih ringan hari ini.`, fitScale: sv => `Masak sesuai porsi saya saja (${sv} sajian)`, fitScaled: sv => `disesuaikan menjadi ${sv} sajian`, perServing: "per sajian", myPortionW: "porsi saya", recTitle: "Menu makan yang disarankan untuk Anda", recAddAll: "Tambahkan semua ke Hari saya", recNote: (k, p) => `Menu makan satu hari yang disesuaikan dengan target ${k.toLocaleString()} kkal Anda, dalam batas ${p} Anda. Porsi disesuaikan untuk setiap waktu makan.`, servX: x => `${x} sajian`, fitOnly: "Sesuai target harian saya", settings: "Pengaturan", setLang: "Bahasa", setTheme: "Tema", setAddr: "Sapa saya sebagai", addrM: "Pria", addrF: "Wanita", setAddrNote: "Mengubah cara petunjuk berbahasa Arab menyapa Anda.", setData: "Data saya", clearSaved: "Hapus resep tersimpan", kidneySub: { hd: "Dialisis", ckd: "PGK, tanpa dialisis", dm: "PGK + diabetes" }, aboutLatest: "Pembaruan terbaru", updates: [["2026-10-02", ["Dasbor baru dengan pengalih kondisi, target harian, saran, dan kalkulator", "Pencatat berat badan, mode memasak dengan pengatur waktu, dan satuan metrik", "Resep dari AAKP, Kidney Care UK, My Renal Nutrition, dan DaVita Arab Saudi", "Rencana makan dari 7 hari hingga satu tahun penuh", "Tema terang dan gelap, berbagi, dan ekspor PDF"]], ["2026-10-01", ["Resep dalam bahasa Inggris, Spanyol, dan Arab", "Rencana kesehatan untuk penyakit ginjal, diabetes, tekanan darah, dan kesehatan jantung"]]], conds: { kidney: "Ginjal", t2: "Diabetes", bp: "Tekanan darah", heart: "Jantung", gen: "Umum" },
    aboutWhat: "Apa itu Dapur Sehat?", aboutWhatP: "Dapur Sehat menghimpun resep dari organisasi tepercaya untuk kesehatan ginjal, diabetes, dan jantung di satu tempat, dalam bahasa Inggris, Spanyol, dan Arab. Setiap resep menampilkan nutrisi per sajian dan tautan ke sumber aslinya, sehingga Anda dapat memasak dengan percaya diri dan membagikan apa yang Anda temukan.",
    aboutHow: "Cara kerjanya", aboutSteps: [["🎯", "Pilih kondisi Anda", "Ginjal, diabetes, tekanan darah, jantung, atau umum. Dasbor menyesuaikan diri dengan pilihan Anda."], ["🍽️", "Temukan resep yang cocok", "Saring berdasarkan diet, nutrisi, dan bahan, lalu lihat bagian setiap hidangan dari jumlah harian Anda."], ["📅", "Rencanakan dan masak", "Susun rencana makan, catat hari dan berat badan Anda, serta masak langkah demi langkah dengan pengatur waktu."]],
    aboutSources: "Sumber resep", aboutSourcesP: "Setiap resep mencantumkan dan menautkan organisasi yang menerbitkannya.", aboutShare: "Bagikan Dapur Sehat", shareBtn: "Bagikan", shareMsg: "Dapur Sehat: resep untuk kesehatan ginjal, diabetes, dan jantung dalam bahasa Inggris, Spanyol, dan Arab.",
    email: "Email", copyLink: "Salin tautan", linkCopied: "Tautan disalin",
    disclaimer: "Dapur Sehat hanya untuk informasi umum. Aplikasi ini tidak menggantikan saran dari dokter, ahli gizi, atau tim dialisis Anda; ikuti batasan yang mereka berikan.",
    unitsLabel: "Satuan", unitsMetric: "Satuan metrik (g, ml, °C)", unitsUS: "Satuan AS (oz, cangkir, °F)",
    dRecTitle: "Target harian Anda", dTipsTitle: "Saran untuk rencana Anda", dToolsTitle: "Alat & kalkulator",
    tCalories: "Kalori", tPerDay: "per hari", tPerMeal: x => `sekitar ${x} per kali makan`, tChoices: n => `sekitar ${n} pilihan per kali makan`, tSalt: g => `= ${g} g garam`,
    tFluid: "Cairan", tFluidNote: "volume urine + 750 ml", tBmi: "IMT", tNote: "Perkiraan berdasarkan rencana dan data tubuh Anda (Mifflin-St Jeor untuk kalori, berat badan ideal Devine). Target dari tim perawatan Anda adalah yang utama.",
    bmiCat: b => b < 18.5 ? "Berat badan kurang" : b < 25 ? "Berat badan sehat" : b < 30 ? "Berat badan berlebih" : "Obesitas",
    toolNames: { bmi: "IMT & berat badan sehat", needs: "Kalori & protein harian", fluid: "Batas asupan cairan (dialisis)", convert: "Konverter garam, mmol & karbohidrat", weight: "Pencatat berat badan" },
    bmiSub: "Indeks massa tubuh, rentang sehat, berat badan ideal", needsSub: "Energi dan protein untuk rencana Anda", fluidSub: "Berdasarkan volume urine harian Anda", convSub: "Garam ↔ natrium, mmol ↔ mg, pilihan karbohidrat", weightSub: "Catat berat badan Anda dan lihat tren",
    height: "Tinggi badan", age: "Usia", years: "tahun", sex: "Jenis kelamin", female: "Wanita", male: "Pria", activity: "Aktivitas", act: ["Sedikit atau tanpa olahraga", "Ringan (1–3 hari/minggu)", "Sedang (3–5 hari/minggu)", "Sangat aktif (6–7 hari/minggu)"],
    healthyRange: "Rentang berat badan sehat", ibw: "Berat badan ideal", adjw: "Berat badan yang disesuaikan (dipakai untuk protein)", bmr: "Energi istirahat (BMR)", meal: "kali makan", choicesW: "pilihan karbohidrat",
    fluidIntro: "Untuk dialisis, titik awal yang umum adalah volume urine harian Anda ditambah 500–1.000 ml. Unit dialisis Anda menetapkan batas yang sebenarnya.", urine: "Urine per hari", cups250: "Cangkir 250 ml",
    salt: "Garam", convHint: "Masukkan nilai di salah satu kolom.", date: "Tanggal", addWeight: "Simpan berat badan", weightSaved: "Berat badan disimpan", weightEmpty: "Tambahkan dua berat badan atau lebih untuk melihat tren Anda.",
    calcNote: "Hanya sebagai panduan. Tanyakan kepada dokter atau ahli gizi Anda untuk target pribadi Anda.",
    navRecipes: "Resep", dCats: "Telusuri menurut kategori", dAll: "Semua resep", dMore: "Lihat semua", dPicks: p => `Pilihan terbaik untuk ${p}`, dPlanTitle: "Hari ini dalam rencana makan Anda", dOpenPlans: "Buka rencana makan", dBrowse: "Telusuri semua resep", greetMorning: "Selamat pagi", greetAfternoon: "Selamat siang", greetEvening: "Selamat malam", streak: n => `Beruntun ${n} hari`, pickPlan: "Anda memasak untuk apa?",
    nextIdea: slot => `Ide untuk ${slot.toLowerCase()}`, tipTitle: "Tips hari ini", cookMode: "Mode memasak", stepOf: (i, n) => `Langkah ${i} dari ${n}`, startTimer: "Mulai", timerDone: "Waktu habis!", finish: "Selesai",
    mealPlans: "Rencana makan", mpTitle: n => `Rencana makan ${n} hari`, mpLen: n => n === 365 ? "1 tahun" : `${n} hari`, mpDayOf: (d, n) => `Hari ${d} dari ${n}`, mpIntro: p => `Disusun dari koleksi untuk rencana Anda: ${p}. Sarapan, makan siang, makan malam, dan camilan setiap hari tetap dalam batas harian Anda.`,
    mpSlots: ["Sarapan", "Makan siang", "Makan malam", "Camilan"], mpDay: d => `Hari ${d}`, mpShuffle: "Acak", mpUseDay: "Tambahkan hari ini ke Hari saya", mpUsed: "Hari ditambahkan ke Hari saya",
    mpNone: "Resep yang sesuai dengan batas ini tidak cukup. Longgarkan salah satu batas dalam rencana Anda.", mpNote: "Hanya saran, disusun otomatis dari data nutrisi. Periksakan porsi dengan tim perawatan Anda.",
    heroEyebrow: "Ginjal · diabetes · tekanan darah · jantung", heroTitle: 'Makanan sehari-hari, <em>dibuat untuk kesehatan Anda</em>',
    heroLede: n => `${n} resep dari organisasi kesehatan tepercaya, dengan nutrisi lengkap per sajian. Pilih rencana untuk penyakit ginjal, diabetes, tekanan darah, atau kesehatan jantung dan lihat bagaimana setiap hidangan cocok dengan hari Anda.`,
    statRecipes: "resep", statPhotos: "dengan foto", statVideos: "video memasak", statSources: "sumber", featured: "Unggulan",
    legendLo: "Rendah", legendMid: "Sedang", legendHi: "Lebih tinggi", legendMeal: "bagian dari satu kali makan", navHome: "Beranda", themeNames: { system: "Tema: sistem", dark: "Tema: gelap", light: "Tema: terang" }, source: "DaVita", allDone: "Semua langkah selesai. Selamat menikmati hidangan Anda!",
    plan: "Rencana kesehatan saya", planEdit: "Ubah jumlah", profiles: { hd: "Ginjal: dialisis", ckd: "Ginjal: PGK, tidak menjalani dialisis", dm: "Ginjal: PGK dengan diabetes", t2: "Diabetes", bp: "Tekanan darah tinggi", heart: "Kesehatan jantung", gen: "Pola makan sehat umum" },
    planIntro: "Pilih rencana Anda dan masukkan jumlah harian yang diberikan dokter atau ahli gizi Anda. Pengukur resep menunjukkan bagian setiap sajian dari satu kali makan, dihitung sebagai sepertiga dari hari Anda. Batas berubah menjadi kuning dan merah saat Anda mendekatinya; target terisi hijau.",
    weight: "Berat badan", perKg: "Protein per kg berat badan", daily: "Jumlah harian", carbsOff: "kosongkan jika tidak ingin dipantau",
    planSource: "Nilai awal: rencana ginjal mengikuti KDOQI 2020 (protein, natrium) dan praktik ahli gizi ginjal (kalium, fosfor); diabetes mengikuti panduan ADA sekitar 45–60 g karbohidrat per kali makan; tekanan darah mengikuti DASH dan AHA (natrium 1.500 mg, makanan kaya kalium); kesehatan jantung dan pola makan umum mengikuti AHA dan Pedoman Diet untuk Warga Amerika (natrium di bawah 2.300 mg, gula tambahan di bawah 25–50 g, serat 25–30 g). Angka dari tim perawatan Anda sendiri adalah yang utama.",
    reset: "Atur ulang batas", resetPlan: "Gunakan nilai awal", done: "Selesai",
    dv: "Sudut pandang ahli gizi", dvSub: "bagian dari satu kali makan · sepertiga dari hari Anda", mealPct: p => `${p}% dari satu kali makan`, dayPct: p => `${p}% dari sehari`,
    goal: "target", ratio: "Fosfor per gram protein", ratioNote: "Di bawah 12 mg per gram dianggap menguntungkan. Menggunakan total fosfor, karena DaVita tidak mencantumkan aditif fosfat secara terpisah.",
    nK: "Tinggi kalium. Jika kadar kalium Anda cenderung tinggi, tanyakan porsinya kepada ahli gizi Anda.",
    nP: "Tinggi fosfor. Tanyakan kepada ahli gizi Anda apakah pengikat fosfat perlu diminum bersama hidangan ini.",
    nNa: p => `Satu sajian memakai ${p}% natrium sehari.`, nLow: "Rendah natrium, kalium, dan fosfor.",
    nProtGood: g => `Sumber protein yang baik: ${g} g menuju target protein dialisis Anda.`, nProtOver: "Protein lebih banyak dari sepertiga batas protein harian Anda.",
    nSugar: g => `${g} g gula tambahan per sajian. Hitung dalam pilihan karbohidrat Anda.`, nCarb: c => `${c} pilihan karbohidrat per sajian (sekitar 15 g masing-masing).`,
    nFiber: "Sumber serat yang baik.", limitW: "batas", goalW: "target", perDay: "hari", planDesc: { hd: "Protein lebih tinggi, natrium, kalium, dan fosfor dibatasi", ckd: "Protein lebih rendah, mineral dibatasi", dm: "Batas ginjal ditambah karbohidrat dan gula", t2: "Karbohidrat, gula tambahan, dan serat", bp: "DASH: rendah natrium, kaya kalium", heart: "Natrium, gula, kolesterol, serat", gen: "Target sehari-hari yang seimbang" }, nKGood: "Kaya kalium, yang membantu menurunkan tekanan darah (periksakan dulu jika Anda menderita penyakit ginjal).",
    addDay: "Tambahkan ke hari saya", added: "Ditambahkan ke hari saya", servingsEaten: "Sajian", myDay: "Hari saya",
    dayIntro: "Resep yang Anda rencanakan untuk dimakan hari ini, dijumlahkan terhadap jumlah harian Anda.", dayEmpty: "Belum ada yang direncanakan. Buka resep dan pilih “Tambahkan ke hari saya”.",
    dayTotals: "Total hari ini", clearDay: "Kosongkan hari", remove: "Hapus", calories: "Kalori", nutr: ["Natrium","Kalium","Fosfor","Protein","Karbohidrat","Gula tambahan","Serat","Kolesterol"], brand: 'Dapur <span>Sehat</span>', tagline: n => `${n} resep untuk kesehatan ginjal, diabetes, dan jantung`, search: "Cari resep atau bahan, mis. ayam, kayu manis, nasi",
    filters: "Filter", saved: "Tersimpan", refine: "Persempit hasil menurut", clearAll: "Hapus semua", all: "Semua resep",
    diet: "Jenis diet", cat: "Kategori", dish: "Jenis hidangan", method: "Cara memasak", holiday: "Hari raya", cuisine: "Masakan",
    serv: "Jumlah sajian", photo: "Dilengkapi foto resep", photoYes: "Dengan foto", photoNo: "Tanpa foto", dietNote: "Resep harus sesuai dengan setiap diet yang Anda centang",
    quick: "Pilihan cepat menurut kondisi", limits: "Batas nutrisi per sajian", leaveOut: "Kecualikan bahan", leavePh: "mis. tomat, keju",
    more: "Lainnya", hasVideo: "Ada video memasak", rated4: "Berperingkat 4 bintang atau lebih", any: "Apa saja", sort: "Urutkan",
    sorts: { az: "A sampai Z", fit: "Bagian terendah dari batas saya", na: "Natrium terendah", k: "Kalium terendah", p: "Fosfor terendah", cal: "Kalori paling sedikit", protein: "Protein terbanyak", new: "Baru diperbarui" },
    count: (n, c) => `<span class="num">${n}</span> resep`, moreBtn: n => `Tampilkan resep lainnya (${n} lagi)`,
    emptyH: "Tidak ada resep yang cocok dengan semua filter ini", emptyP: "Hapus satu filter atau longgarkan batas nutrisi untuk melihat lebih banyak.",
    presets: ["Rendah natrium", "Rendah kalium", "Rendah fosfor", "Ramah diabetes", "Sehat untuk jantung", "Di bawah 300 kalori", "Protein lebih rendah"],
    sliders: ["Natrium", "Kalium", "Fosfor", "Protein", "Kalori", "Karbohidrat", "Gula tambahan", "Kolesterol"],
    lvl: { lo: "Rendah", mid: "Sedang", hi: "Lebih tinggi" }, minerals: ["Natrium", "Kalium", "Fosfor"],
    reviews: n => `${n} ulasan`, cal: "kal", protein: "g protein", video: "Video", back: "Kembali", prev: "Sebelumnya", next: "Berikutnya", save: "Simpan", savedBtn: "Tersimpan", copy: "Salin",
    copied: "Resep disalin", copyFail: "Pilih teks untuk menyalinnya",
    portions: "Porsi", serving: "Ukuran sajian", dietTypes: "Jenis diet", ing: "Bahan", prep: "Persiapan", hints: "Petunjuk berguna",
    nut: "Nutrisi per sajian", choices: "Pilihan makanan untuk ginjal dan ginjal dengan diabetes", carb: "Pilihan karbohidrat", by: "Dikirim oleh",
    items: n => `${n} item · ketuk untuk mencentang`, stepsHint: "ketuk langkah saat sudah selesai", watch: "Tonton video memasak", watchSub: "Membuka video di tab baru",
    translated: src => `Diterjemahkan dari resep ${src} asli`, officialEs: "Versi bahasa Spanyol resmi DaVita",
    occasions: "Acara", without: "Tanpa", saveOnly: "Hanya yang tersimpan", servUnit: "sajian",
    footer: (n, x) => `${n} resep dari DaVita dan organisasi kesehatan ginjal, diabetes, dan jantung terkemuka, dalam bahasa Inggris, Spanyol, dan Arab. Tingkat warna per sajian: natrium rendah ≤140 mg, lebih tinggi >400 mg; kalium rendah ≤200 mg, lebih tinggi >400 mg; fosfor rendah ≤100 mg, lebih tinggi >250 mg. Tingkat ini hanya membantu pengurutan. Ikuti saran dokter atau ahli gizi Anda.`
};
NLABEL.id = ["Kalori","Protein","Karbohidrat","Lemak","Kolesterol","Natrium","Kalium","Fosfor","Kalsium","Serat","Gula tambahan"];
NUNIT.id = ["","g","g","g","mg","mg","mg","mg","mg","g","g"];
TIPS_X.id = {
  kidney: [
    ["🥔", "Kurangi kalium pada kentang dan sayuran umbi: kupas, potong dadu, lalu rendam, atau rebus dua kali dengan air baru."],
    ["🏷️", "Periksa daftar bahan untuk aditif fosfat (kata yang mengandung \"fos\"). Tubuh menyerap fosfor dari aditif hampir sepenuhnya."],
    ["🌿", "Beri cita rasa dengan rempah, lemon, bawang putih, dan bumbu sebagai pengganti garam. Hindari pengganti garam yang dibuat dari kalium klorida."],
    ["💧", "Jika Anda memiliki batas cairan, hitung juga sup, es, dan buah berair sebagai cairan."],
    ["💊", "Minum pengikat fosfat bersama makanan utama dan camilan persis sesuai resep."] ],
  diabetes: [
    ["🍽️", "Gunakan metode piring: setengah sayuran non-bertepung, seperempat protein tanpa lemak, seperempat makanan berkarbohidrat."],
    ["⚖️", "Jaga porsi karbohidrat tetap serupa pada setiap kali makan. Satu pilihan karbohidrat sekitar 15 g."],
    ["🌾", "Pilih biji-bijian utuh, kacang-kacangan, dan lentil; seratnya memperlambat kenaikan gula darah."],
    ["🥤", "Ganti minuman manis dengan air putih, teh, atau kopi tanpa gula."],
    ["🍎", "Makan buah bersama sedikit protein atau lemak sehat, dan sebarkan sepanjang hari."] ],
  bp: [
    ["🧂", "Sebagian besar natrium berasal dari roti, daging olahan, sup kaleng, acar, dan makanan restoran, bukan dari botol garam."],
    ["🥬", "Makan banyak sayuran, buah, dan kacang-kacangan yang kaya kalium, kecuali dokter Anda membatasi kalium."],
    ["🥛", "Pilih produk susu rendah lemak dan biji-bijian utuh, seperti dalam pola makan DASH."],
    ["🥫", "Bilas kacang dan sayuran kaleng untuk membuang hingga sepertiga natriumnya."],
    ["🚶", "Bergeraklah sekitar 30 menit hampir setiap hari; berjalan kaki singkat setelah makan pun bermanfaat."] ],
  heart: [
    ["🫒", "Masak dengan minyak zaitun atau minyak kanola sebagai pengganti mentega atau ghee."],
    ["🐟", "Makan ikan dua kali seminggu, terutama ikan berminyak seperti salmon atau sarden."],
    ["🥩", "Pilih potongan daging tanpa lemak dan buang lemak serta kulit yang terlihat."],
    ["🥣", "Oat, jelai, kacang-kacangan, dan lentil mengandung serat larut yang membantu menurunkan kolesterol LDL."],
    ["🍬", "Batasi gula tambahan di bawah sekitar 25 g sehari untuk wanita dan 36 g untuk pria."] ],
  gen: [
    ["📅", "Rencanakan menu makan seminggu di muka; hemat uang dan menjaga nutrisi tetap terpenuhi."],
    ["💧", "Minum air sepanjang hari, kecuali Anda memiliki batas cairan."],
    ["🍇", "Makan sayuran dan buah berbagai warna untuk beragam nutrisi yang lebih luas."],
    ["🏷️", "Baca label nutrisi per sajian, dan periksa berapa banyak sajian dalam satu kemasan."],
    ["🥕", "Siapkan camilan praktis: buah, potongan sayuran, atau yogurt."] ]
};
TERMS_X.id = {
"5 or less ingredients": "5 bahan atau kurang",
"African": "Afrika",
"American": "Amerika",
"Appetizers & Snacks": "Hidangan Pembuka & Camilan",
"Asian": "Asia",
"Bake": "Panggang (oven)",
"Beef, Lamb & Pork": "Daging Sapi, Domba & Babi",
"Beverages": "Minuman",
"Bread": "Roti",
"Breads": "Roti-rotian",
"Breakfast & Brunch": "Sarapan & Brunch",
"British": "Inggris",
"Budget": "Hemat",
"CKD non-dialysis": "PGK tanpa dialisis",
"Cake": "Kue",
"Candy": "Permen",
"Caribbean": "Karibia",
"Chicken & Turkey": "Ayam & Kalkun",
"Chinese": "Tionghoa",
"Christmas": "Natal",
"Cookies": "Kue Kering",
"Desserts": "Hidangan Penutup",
"Diabetes": "Diabetes",
"Dialysis": "Dialisis",
"Easter": "Paskah",
"Easy": "Mudah",
"Filipino": "Filipina",
"Fish & Seafood": "Ikan & Makanan Laut",
"Freezer": "Freezer",
"French": "Prancis",
"Fry": "Goreng",
"German": "Jerman",
"Gluten-free": "Bebas Gluten",
"Greek": "Yunani",
"Grill": "Bakar",
"Halloween": "Halloween",
"Hanukkah": "Hanukkah",
"Hawaiian": "Hawaii",
"Heart Healthy": "Sehat untuk Jantung",
"Higher Potassium": "Kalium Lebih Tinggi",
"Independence Day": "Hari Kemerdekaan",
"Indian": "India",
"International": "Internasional",
"Irish": "Irlandia",
"Italian": "Italia",
"Japanese": "Jepang",
"Jewish": "Yahudi",
"Korean": "Korea",
"Lower Potassium": "Kalium Lebih Rendah",
"Lower Protein": "Protein Lebih Rendah",
"Meatless Entree": "Hidangan Utama Tanpa Daging",
"Mediterranean": "Mediterania",
"Mexican": "Meksiko",
"Microwave": "Microwave",
"Middle Eastern": "Timur Tengah",
"Mother's Day": "Hari Ibu",
"Muffin": "Muffin",
"Native American": "Penduduk Asli Amerika",
"New Year": "Tahun Baru",
"No Cooking": "Tanpa Memasak",
"One-Dish Meal": "Hidangan Satu Piring",
"Oven": "Oven",
"Pasta, Rice & Grains": "Pasta, Nasi & Biji-bijian",
"Picnic": "Piknik",
"Pie": "Pai",
"Pizza & Sandwiches": "Pizza & Sandwich",
"Potluck": "Potluck",
"Quick": "Cepat",
"Refrigerator": "Kulkas",
"Roast": "Panggang",
"Salads & Dressings": "Salad & Saus Salad",
"Sauces & Seasonings": "Saus & Bumbu",
"Slow Cooker": "Slow Cooker",
"Soup": "Sup",
"Soups & Stews": "Sup & Semur",
"South American": "Amerika Selatan",
"Southern": "Amerika Selatan (Gaya Selatan)",
"Spanish": "Spanyol",
"Special Celebrations": "Perayaan Istimewa",
"St Patrick's Day": "Hari Santo Patrick",
"Stew": "Semur",
"Stir-fry": "Tumis",
"Stove Top": "Kompor",
"Thai": "Thailand",
"Thanksgiving": "Thanksgiving",
"Valentine's Day": "Hari Valentine",
"Vegetables": "Sayuran",
"Vegetarian": "Vegetarian"
};

Object.assign(UI.id, {
  accTitle: "Akun saya",
  accOpen: "Buka akun saya",
  signIn: "Masuk",
  signUp: "Buat akun",
  signOut: "Keluar",
  signedOut: "Sudah keluar",
  password: "Kata sandi",
  authIntro: "Masuk untuk menyimpan informasi, rencana, berat badan, dan resep tersimpan Anda di akun.",
  noAccount: "Baru di sini?",
  haveAccount: "Sudah punya akun?",
  guest: "Lanjut tanpa akun",
  pwShort: "Gunakan minimal 8 karakter untuk kata sandi.",
  welcome: n => `Selamat datang, ${n}`,
  synced: "Tersimpan di akun Anda",
  syncing: "Menyimpan…",
  syncErr: "Belum tersimpan, periksa koneksi",
  adminTitle: "Admin",
  adUsers: "Pengguna",
  adAdmins: "Admin",
  adActive: "Aktif minggu ini",
  adWeighIns: "Penimbangan",
  adPlans: "Pengguna per rencana",
  adSaved: "Tersimpan",
  adLast: "Masuk terakhir",
  adRole: "Peran",
  confirmDel: "Ketuk lagi untuk menghapus",
  loading: "Memuat…",
  pfTitle: "Data saya",
  pfName: "Nama",
  pfGoal: "Target berat badan",
  goalLose: "Menurunkan berat badan",
  goalKeep: "Menjaga berat badan",
  goalGain: "Menaikkan berat badan",
  pfTarget: "Berat target",
  pfGoalNote: k => `Target kalori Anda sekarang sekitar ${k} kkal per hari.`,
  pfPrefs: "Preferensi dan makanan yang saya hindari",
  pfDislikes: "Makanan yang tidak saya makan",
  pfAllergies: "Alergi",
  pfLikes: "Makanan yang saya suka",
  pfHide: "Sembunyikan resep dengan makanan yang saya hindari",
  pfDoctor: "Anjuran dokter dan obat",
  pfDoctorNote: "Anjuran dari dokter atau ahli gizi saya",
  pfMeds: "Obat saya (mis. pengikat fosfat saat makan)",
  pfDoctorShort: "Catatan kesehatan saya",
  pfProgress: (w, t) => `Saat ini ${w} kg · target ${t} kg (${(w - t > 0 ? "−" : "+") + Math.abs(w - t).toFixed(1)} kg lagi)`
});

Object.assign(UI.id, { roleUser: "Pengguna", roleAdmin: "Admin" });

Object.assign(UI.id, { netErr: "Tidak dapat terhubung ke server akun. Coba lagi sebentar lagi.", localOnly: "Informasi Anda hanya tersimpan di perangkat ini. Untuk menyimpannya di akun, buka aplikasi dari server Health Kitchen (lihat README)." });

Object.assign(UI.id, { fitOf: (sv, total, amt) => `Anda makan ${sv} dari ${total} porsi resep ini${amt ? ` (${sv} × ${amt} per porsi)` : ""}. Nutrisi porsi Anda ada di kolom «porsi saya».` });

Object.assign(UI.id, { signInNeeded: "Masuk untuk melihat akun Anda: informasi, statistik, rencana, dan pengaturan.", stTitle: "Statistik saya", stToday: "Hari ini", stAvg7: "Rata-rata (7 hari terakhir)", stDays: "Hari tercatat", stStreak: "Rentetan hari", stSaved: "Resep tersimpan", stWeighIns: "Penimbangan", stChange: "Perubahan berat badan", stBmi: "BMI", badLogin: "Email atau kata sandi salah.", accDisabled: "Akun ini dinonaktifkan. Hubungi administrator.", emailTaken: "Akun dengan email ini sudah ada.", badEmail: "Masukkan alamat email yang valid.", adOnly: "Hanya administrator yang dapat membuka halaman ini. Masuk dengan akun admin.", adActiveDay: "Aktif hari ini", adDisabled: "Akun nonaktif", adDisabledOne: "Nonaktif", adSignups: "Pengguna baru (30 hari terakhir)", adNoPlan: "Belum ada rencana", adRecipesLang: "Resep per bahasa", adRecipesSrc: "Resep per sumber", adSearch: "Cari berdasarkan email atau nama", adExport: "Ekspor CSV", adDetail: "Detail", adJoined: "Bergabung", adPrivacy: "Catatan kesehatan, instruksi dokter, dan obat-obatan bersifat pribadi bagi pengguna dan tidak ditampilkan di sini.", adNewPw: "Kata sandi baru (minimal 8 karakter)", adResetPw: "Atur kata sandi", adEnable: "Aktifkan akun", adDisable: "Nonaktifkan akun", adPwDone: "Kata sandi diubah. Pengguna telah dikeluarkan dari semua perangkat." });

UI.id.profiles = { none: "Tanpa rencana (semua resep)", ...UI.id.profiles }; UI.id.conds = { ...UI.id.conds, none: "Semua resep" };

Object.assign(TERMS_X.id, {"Latin American": "Amerika Latin", "Saudi": "Saudi", "Emirati": "Emirat", "Bahraini": "Bahrain", "Lebanese": "Lebanon", "Turkish": "Turki", "Moroccan": "Maroko", "Tunisian": "Tunisia", "Egyptian": "Mesir", "Persian": "Persia", "Afghan": "Afganistan"});

Object.assign(UI.id, {
  tabOverview: "Ringkasan",
  tabProfile: "Informasi saya",
  tabHealth: "Kesehatan & tujuan",
  tabFood: "Preferensi makanan",
  tabWeight: "Berat badan",
  stKcal14: "Kalori, 14 hari terakhir",
  stGoal: "Kemajuan target berat badan",
  stGoalDone: "Target tercapai, kerja bagus!",
  stNoData: "Belum ada riwayat. Tambahkan makanan ke Hari saya dan akan tampil di sini.",
  weightLog: "Catatan berat badan",
  stGoalLeft: n => `${n} kg lagi`,
  memberSince: d => `Anggota sejak ${d}`
});

Object.assign(UI.id, { mpCuisines: "Masakan", mpAllCuisines: "Semua masakan", mpCuisNote: "Menu diambil dari masakan pilihan Anda; menu yang tidak tersedia memakai masakan apa pun." });

Object.assign(UI.id, { noServer: "Akun tidak tersedia di salinan aplikasi ini. Buka dari server Health Kitchen untuk mendaftar dan memantau rencana serta informasi Anda." });

Object.assign(UI.id, {
  "tabMyRecipes": "Resep saya",
  "subNew": "Bagikan resep",
  "subIntro": "Resep yang Anda bagikan diperiksa oleh tim kami (takaran, satuan, dan bahan) sebelum dapat dilihat orang lain.",
  "subTitle": "Nama resep",
  "subDesc": "Deskripsi singkat",
  "subCat": "Kategori",
  "subCuisine": "Masakan",
  "subServings": "Porsi",
  "subServing": "Ukuran porsi (mis. 1 piring, 250 g)",
  "subIng": "Bahan",
  "subQty": "Jumlah",
  "subItem": "Bahan",
  "subAddIng": "+ Tambah bahan",
  "subSteps": "Langkah",
  "subAddStep": "+ Tambah langkah",
  "subHints": "Tips (satu per baris)",
  "subNut": "Gizi per porsi (opsional)",
  "subSend": "Kirim untuk ditinjau",
  "subSent": "Terkirim untuk ditinjau. Hasilnya akan tampil di Resep saya.",
  "subMine": "Resep yang saya bagikan",
  "subNone": "Anda belum membagikan resep apa pun.",
  "stPending": "Menunggu tinjauan",
  "stApproved": "Dipublikasikan",
  "stRejected": "Tidak disetujui",
  "subNote": "Catatan peninjau",
  "subDelete": "Hapus",
  "subErr": "Harap tambahkan nama, kategori, minimal satu bahan beserta jumlah dan satuannya, dan satu langkah.",
  "adSubs": "Kiriman resep",
  "adApprove": "Setujui dan publikasikan",
  "adReject": "Jangan setujui",
  "adNotePh": "Catatan untuk penulis (mis. harap tulis jumlah dalam gram)",
  "adNoSubs": "Tidak ada resep di sini.",
  "community": "Komunitas"
});

Object.assign(UI.id, { meal: "Jenis hidangan", mealTypes: {"main": "Hidangan utama", "breakfast": "Sarapan", "starter": "Hidangan pembuka", "side": "Lauk pendamping", "snack": "Camilan", "dessert": "Hidangan penutup", "drink": "Minuman", "condiment": "Saus atau bumbu"}, fitCond: "Ini saus atau bumbu, bukan makanan tersendiri: satu porsi menemani makanan, dan nutrisinya dihitung dalam makanan itu." });
Object.assign(UI.id, {"cfgTitle":"Pengaturan aplikasi","cfgDefaults":"Default untuk pengunjung baru","cfgDefaultsNote":"Dipakai sampai pengunjung memilih sendiri.","cfgVisitorChoice":"Perangkat pengunjung","cfgAccounts":"Akun","cfgSignups":"Izinkan pendaftaran baru","cfgSession":"Tetap masuk selama","cfgDays":"hari","cfgAnnounce":"Pengumuman di beranda","cfgAnnounceOn":"Tampilkan pengumuman","cfgInfo":"Informasi","cfgWarn":"Penting","cfgAnnounceNote":"Kosongkan suatu bahasa untuk menampilkan teks bahasa Inggris.","cfgSources":"Sumber resep yang ditampilkan","cfgSourcesNote":"Sumber yang tidak dicentang disembunyikan dari semua orang.","cfgLangs":"Bahasa yang tersedia","cfgSave":"Simpan pengaturan","dbTitle":"Database","dbStatus":"Status","dbConnected":"Terhubung","dbNoTables":"Tabel belum ada","dbName":"Database","dbHost":"Server","dbUser":"Pengguna","dbSize":"Ukuran","dbStates":"Profil tersimpan","dbSupported":"Didukung","dbChange":"Gunakan database lain","dbChangeNote":"Uji koneksi dulu. Untuk memakai database kosong yang baru, buat tabel dengan akun pemilik, lalu beralih menggunakan pengguna API (hk_api). Data tidak disalin antar database.","dbApiUrl":"URL koneksi API","dbOwnerUrl":"URL koneksi pemilik (untuk membuat tabel)","dbTest":"Uji koneksi","dbSwitch":"Beralih ke database ini","dbSetup":"Buat tabel","dbOk":"Koneksi berfungsi","dbSetupDone":"Tabel, aturan keamanan, dan fungsi sudah disiapkan.","dbSwitched":"Aplikasi sekarang memakai database baru."});

Object.assign(UI.id, { confirmEmail: "Akun dibuat. Buka tautan konfirmasi di email Anda, lalu masuk.", adPwEmail: "Kirim email atur ulang kata sandi", adPwEmailed: "Email atur ulang kata sandi telah dikirim ke pengguna." });

Object.assign(UI.id, Object.fromEntries(Object.entries({"sbProject": "Project", "sbSignups": "Sign-ups open", "sbConfirm": "Email confirmation", "sbUrl": "Project URL", "sbKey": "Publishable key (public)", "sbNote": "Accounts and data are stored in Supabase with row-level security. Keys and passwords are managed in the Supabase dashboard; the secret key is never used in the app.", "sbDash": "Dashboard", "sbUsers": "Users", "sbUrls": "Sign-in URLs", "sbProviders": "Sign-in methods", "sbTables": "Tables"}).filter(([k]) => !(k in UI.id))));

Object.assign(UI.id, Object.fromEntries(Object.entries({"dbConnectTitle": "Connect a database (e.g. Supabase)", "dbConnectNote": "Paste the owner connection string (in Supabase: Project Settings \u2192 Database \u2192 Connection string, with your database password). The server sets up the tables and security rules, creates a restricted app user with its own password, copies the current accounts and data, and switches. The details are stored encrypted on this server only.", "dbConnectUrl": "Owner connection string", "dbCopy": "Copy the current accounts and data", "dbConnectBtn": "Set up and connect", "dbEncrypted": "The connection is stored encrypted on this server."}).filter(([k]) => !(k in UI.id))));

Object.assign(UI.id, Object.fromEntries(Object.entries({"dbPort": "Port", "dbOrUrl": "Or paste a full connection string", "dbNeedFields": "Enter the host and the database password (or a full connection string)."}).filter(([k]) => !(k in UI.id))));

Object.assign(UI.id, Object.fromEntries(Object.entries({"dbTablesReady": "Health Kitchen tables found", "dbTablesNew": "empty: tables will be created", "dbNoRoles": "this user cannot create the app user; use the owner (postgres) account"}).filter(([k]) => !(k in UI.id))));

Object.assign(TERMS_X.id, {"Canadian": "Kanada", "Eastern European": "Eropa Timur", "Jamaican": "Jamaika"});
Object.assign(TERMS_X.id, {"North African": "Afrika Utara"});
Object.assign(UI.id, {"tabMeals": "Tabel makan", "mtIntro": "Rencanakan resep untuk setiap waktu makan, lalu centang setelah Anda memakannya.", "mtAssign": "Tetapkan ke waktu makan", "mtAssignShort": "Tetapkan", "mtTaken": "Sudah dimakan", "mtDay": "Hari", "mtTotal": "Rencana · dimakan", "mtEmpty": "Belum ada yang ditetapkan. Isi minggu ini dari rencana makan, atau buka resep dan pilih “Tetapkan ke waktu makan”.", "mtFromPlan": "Simpan rencana ke tabel makan saya", "mtSaved": "Disimpan ke tabel makan Anda", "mtPick": "Pilih resep", "mtSearch": "Cari resep", "mtClear": "Kosongkan minggu ini", "mtAssigned": "Ditetapkan", "mtRemove": "Hapus", "mtFill": "Isi dari rencana makan", "mtWhen": "Hari apa?", "mtWhich": "Waktu makan apa?", "mtToday": "Hari ini", "mtThisWeek": "Minggu ini"}, { mtDone: (a, b) => `${a} dari ${b} makanan sudah dimakan` });
Object.assign(UI.id, {"authNotConfirmed": "Email ini belum dikonfirmasi. Buka tautan konfirmasi di email Anda, lalu masuk.", "authEmailLimit": "Terlalu banyak email terkirim barusan. Tunggu beberapa menit lalu coba lagi.", "authNoMail": "Server akun belum dapat mengirim email ke alamat ini. Minta administrator menambahkan akun Anda.", "authClosed": "Pendaftaran baru ditutup."});
Object.assign(UI.id, {"sbSignin": "Masuk", "sbEmailLogin": "Masuk dengan email dan kata sandi", "sbOn": "Aktif", "sbOff": "Nonaktif", "sbOpen": "Dibuka", "sbClosed": "Ditutup", "sbConfirmOff": "Pengguna baru langsung masuk setelah membuat akun.", "sbConfirmOn": "Pengguna baru harus membuka email konfirmasi sebelum masuk.", "sbDetails": "Detail koneksi", "sbCopy": "Salin", "sbCopied": "Disalin"});
Object.assign(UI.id, {"mtType": "Jenis", "mtSlotTypes": "Cocok untuk waktu makan ini", "mtAllTypes": "Semua jenis", "mtFitOnly": "Hanya resep yang sesuai rencana saya untuk waktu makan ini", "mtFits": "Sesuai rencana Anda untuk waktu makan ini", "mtHigh": "Melebihi jatah waktu makan ini dalam rencana Anda"}, { mtResults: n => `${n} resep` });
Object.assign(UI.id, { shopTitle: "Daftar belanja", shopTesting: "Uji coba · admin dan supervisor", shopIntro: "Semua yang perlu dibeli untuk makanan yang direncanakan, dijumlahkan dari semua resep dan dihitung satu porsi per orang per waktu makan.", shopFrom: "Berdasarkan", shopPlan: "Rencana makan", shopTable: "Tabel makan saya", shopDays: "Hari", shopPeople: "Orang", shopStaplesNote: "Periksa apa yang sudah ada di rumah.", shopNeeded: "secukupnya", shopRecipes: "Resep dalam daftar ini", shopCopy: "Salin daftar", shopPrint: "Cetak", shopClear: "Hapus semua centang", shopEmpty: "Tidak ada makanan yang direncanakan untuk hari-hari ini. Tetapkan makanan di tabel makan Anda atau pilih Rencana makan.", roleSupervisor: "Supervisor", roleVisitor: "Pengunjung (belum masuk)", adRole: "Peran", adRoleNote: "Supervisor juga melihat fitur yang sedang diuji (Admin → Hak akses).", adRoleFixed: "admin ditentukan oleh daftar email admin", privTitle: "Hak akses", privIntro: "Pilih siapa yang dapat melihat setiap bagian aplikasi. Admin selalu melihat semuanya; Pengunjung berarti belum masuk. Perubahan langsung disimpan.", privSaved: "Hak akses disimpan", shopSec: {"produce": "Buah & sayur", "meat": "Daging & ikan", "dairy": "Susu & telur", "bakery": "Roti & kue", "grains": "Nasi, pasta & biji-bijian", "canned": "Kaleng & stoples", "frozen": "Beku", "nuts": "Kacang, biji & buah kering", "other": "Lainnya", "staples": "Bahan dapur dasar"}, feat: {"shop": "Daftar belanja", "plans": "Rencana makan", "table": "Tabel makan", "day": "Hari saya", "saved": "Resep tersimpan", "submit": "Kirim resep", "cook": "Mode memasak", "pdf": "PDF & cetak"}, shopMeals: (m, r) => `${m} makanan · ${r} resep`, shopItems: n => `${n} barang`, shopLeft: n => `${n} belum dibeli`, shopUsed: n => `di ${n} resep` });
Object.assign(UI.id, {"pwRule": "Gunakan minimal 10 karakter dengan huruf dan angka, dan hindari kata sandi umum.", "idleOut": "Keluar setelah tidak ada aktivitas.", "cfgIdle": "Keluar saat tidak aktif", "cfgMinutes": "menit", "cfgIdleNote": "Pengguna yang masuk akan dikeluarkan setelah sekian menit tanpa aktivitas (0 = tidak pernah).", "secTitle": "Keamanan"});
