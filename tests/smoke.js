// Smoke test for the app in a real browser: pages load in English, Arabic and Spanish without errors, a recipe shows its
// blood sugar panel, the Glycemic index tab renders, and diet plans respect the safety rules (kidney + diabetes menus stay
// within protein, potassium and phosphorus limits; insulin turns off the free day and the calorie cut).
//   python3 -m http.server 8731 -d gallery &   then   PW=<path to playwright> node tests/smoke.js
const { chromium } = require(process.env.PW || "playwright");
const BASE = process.env.HK_URL || "http://localhost:8731/";
const fails = [];
const check = (ok, msg) => { console.log(`${ok ? "ok  " : "FAIL"} ${msg}`); if (!ok) fails.push(msg); };
(async () => {
  const b = await chromium.launch();
  const page = async (lang, plan, profile = {}, w = 1200) => {
    const p = await b.newPage({ viewport: { width: w, height: 900 } }), errs = [];
    p.on("pageerror", e => errs.push(e.message));
    await p.addInitScript(([l, pl, pr]) => { localStorage.setItem("kk:lang", JSON.stringify(l)); localStorage.setItem("kk:plan", JSON.stringify(pl)); localStorage.setItem("kk:profile", JSON.stringify(pr));
      localStorage.setItem("kk:cfgCache", JSON.stringify({ access: { dieter: ["admin", "supervisor", "user", "visitor"] } })); }, [lang, plan, profile]);
    await p.goto(BASE + "#" + lang + "-recipes", { waitUntil: "load", timeout: 90000 });
    await p.waitForFunction(() => { try { return typeof R !== "undefined" && R.length > 0 && typeof dieterHTML === "function"; } catch { return false; } }, null, { timeout: 90000 });
    await p.waitForTimeout(1500);
    return { p, errs };
  };
  for (const lang of ["en", "ar", "es"]) {
    const { p, errs } = await page(lang, { type: "t2", weight: 80, unit: "kg", age: 50, height: 170, sex: "m" }, {}, lang === "ar" ? 390 : 1200);
    const id = await p.evaluate(() => R.find(r => r.gl != null && r.gx && r.gx.length).id);
    await p.evaluate(i => openRecipe(i), id); await p.waitForTimeout(800);
    check(await p.evaluate(() => !!document.querySelector("#sheetIn .gibox .gi-carb")), `${lang}: recipe shows carbohydrate per serving and the blood sugar panel`);
    check(await p.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `${lang}: no sideways scroll`);
    check(await p.evaluate(() => { try { return giHTML(u()).includes("giSearch"); } catch (e) { return false; } }), `${lang}: Glycemic index tab renders`);
    check(!errs.length, `${lang}: no script errors ${errs.join("; ")}`);
  }
  // kidney + diabetes: every menu day within the daily limits, protein included
  for (const type of ["dm", "ckd", "hd"]) {
    const { p, errs } = await page("en", { type, weight: 90, unit: "kg", age: 60, height: 168, sex: "m", activity: 1.375 }, { goal: "lose", target: 75 });
    const r = await p.evaluate(t => {
      plan = { ...blankPlan(t), ...plan };   // the plan's default limits, as a new user gets them
      const rows = planTargets().map(x => x[0]);
      const keep = [mpLen, mpSeed]; mpLen = 7; mpSeed = 3; const menu = buildMealPlan(); [mpLen, mpSeed] = keep;
      const over = []; (menu || []).forEach((day, i) => planTargets().forEach(([k, daily, goal]) => { if (goal || (k === "protein_g" && !protCap())) return;
        const v = day.reduce((a, x) => a + (x.n[IDX[k]] || 0), 0); if (v > daily) over.push(`day ${i + 1} ${k} ${Math.round(v)}>${daily}`); }));
      const html = dieterHTML(u());
      return { days: menu ? menu.length : 0, over, noCut: noCut(), legumeTips: /beans, lentils/i.test(html), timeline: !!dieterPlan().tl,
        limits: ["sodium_mg", "potassium_mg", "phosphorus_mg", "protein_g"].every(k => rows.includes(k)), empty: html.includes(u().mpNone) };
    }, type);
    check(r.limits, `${type}: sodium, potassium, phosphorus and protein limits are active`);
    check(!r.empty, `${type}: the diet plan has menus (no "no recipes fit")`);
    check(r.days === 7 && !r.over.length, `${type}: 7-day menu within limits ${r.over.join(", ")}`);
    check(r.noCut === "kidney" && !r.timeline, `${type}: no weight-loss calorie cut or timeline with kidney disease`);
    check(!r.legumeTips, `${type}: no "beans, lentils" blood sugar tips for kidney plans`);
    check(!errs.length, `${type}: no script errors ${errs.join("; ")}`);
  }
  { // insulin: low blood sugar warning, no free day, no calorie cut until the doctor approves
    const { p } = await page("en", { type: "t2", weight: 95, unit: "kg", age: 55, height: 170, sex: "f" }, { goal: "lose", target: 70, hypoMeds: "insulin", freeDay: 4 });
    const r = await p.evaluate(() => { const html = dieterHTML(u()); return { warn: html.includes(D().medsWarn), free: /class="dt-free"/.test(html), noCut: noCut() }; });
    check(r.warn && !r.free && r.noCut === "meds", "insulin: warning shown, free day off, no calorie cut");
  }
  await b.close();
  console.log(fails.length ? `${fails.length} check(s) failed` : "all checks passed");
  process.exit(fails.length ? 1 : 0);
})();
