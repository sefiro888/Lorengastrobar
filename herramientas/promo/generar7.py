"""Genera video7.html (promo largo dividido en 2 partes) a partir de video2.html.
?p=1  → Parte 1 «Sabores»  (apertura de comida, local, chipa guazú, vorí vorí, ambiente, receta, cierre)
?p=2  → Parte 2 «La web»   (mosaico de platos, web en móviles, familia, cierre)"""
import os
AQUI = os.path.dirname(os.path.abspath(__file__))
t = open(os.path.join(AQUI, "video2.html"), encoding="utf-8").read()


def cambia(viejo, nuevo, veces=1):
    global t
    assert viejo in t, "no encuentro: " + viejo[:70]
    t = t.replace(viejo, nuevo, veces)


# ---- 1) escenas nuevas (aperturas y cierre de comida)
nuevas = '''
  <!-- Parte 1 · apertura de comida -->
  <section class="sc" id="s0f" data-gr="1">
    <div class="luz" data-in="0.2" data-fx="fade" style="left:-110px;top:310px"></div>
    <img class="enc introflor" src="../../img/kv/flor-kv.webp" style="opacity:.55;width:1300px;height:1300px;margin:-650px 0 0 -650px" alt="">
    <img class="logo" data-in="1.2" data-fx="zoom" style="left:260px;top:360px;width:560px" src="../../img/marca/logo-loren.webp" alt="">
    <div class="centro eyebrow" data-in="2.2" data-fx="spread" style="top:760px;font-size:38px">Cocina paraguaya · Barcelona</div>
    <div class="centro kau" data-in="2.9" data-fx="up" style="top:900px;font-size:118px;line-height:1.08;left:40px;right:40px">Hay sabores<br>que nos hacen<br>sentir en casa</div>
  </section>

  <!-- Parte 2 · mosaico de platos -->
  <section class="sc" id="s0d" data-gr="1">
    <img class="enc introflor" src="../../img/kv/flor-kv.webp" style="opacity:.4;width:1500px;height:1500px;margin:-750px 0 0 -750px" alt="">
    <div class="centro eyebrow" data-in="0.2" data-fx="up" style="top:250px">Loren Restobar</div>
    <div class="centro anton" data-in="0.35" data-fx="slam" style="top:310px;font-size:112px;line-height:1">Todo lo que sale<br><span style="color:var(--maiz);font-size:96px">de la cocina de Loren</span></div>
    <div class="disco" data-in="0.7" data-fx="left" style="left:70px;top:760px;width:400px;height:400px"><img src="../../img/platos/mila-caballo-pro.webp"></div>
    <div class="disco" data-in="0.95" data-fx="right" style="left:610px;top:760px;width:400px;height:400px"><img src="../../img/platos/tallarin-ternera.webp"></div>
    <div class="disco" data-in="1.2" data-fx="zoom" style="left:340px;top:1000px;width:400px;height:400px"><img src="../../img/platos/hl-chipa-guazu.webp"></div>
    <div class="disco" data-in="1.45" data-fx="left" style="left:20px;top:1240px;width:330px;height:330px"><img src="../../img/platos/empanada-ternera.webp"></div>
    <div class="disco" data-in="1.7" data-fx="right" style="left:730px;top:1240px;width:330px;height:330px"><img src="../../img/platos/postre-tarta-queso.webp"></div>
    <div class="centro kau" data-in="2.6" data-fx="up" style="top:1620px;font-size:84px">y ahora, en tu móvil</div>
  </section>

  <!-- Parte 1 · cierre de comida -->
  <section class="sc" id="s8f" data-gr="1">
    <div class="luz" data-in="0.2" data-fx="fade" style="left:-110px;top:230px"></div>
    <img class="logo" data-in="0.3" data-fx="zoom" style="left:290px;top:300px;width:500px" src="../../img/marca/logo-loren.webp" alt="">
    <div class="centro kau" data-in="0.9" data-fx="up" style="top:650px;font-size:128px">Pruébalo en</div>
    <div class="centro anton" data-in="1.2" data-fx="slam" style="top:820px;font-size:190px;line-height:.92">Loren<br>Restobar</div>
    <div class="centro txt" data-in="2.0" data-fx="up" style="top:1240px;font-size:44px;line-height:1.35;left:40px;right:40px">Carrer de la Muntanya 115<br>Camp de l'Arpa · Barcelona</div>
    <div class="centro" data-in="2.6" data-fx="zoom" style="top:1420px"><span class="pill">lorenrestobar.com</span></div>
    <div class="centro txt" data-in="3.3" data-fx="up" style="top:1560px;font-size:36px;opacity:.9">También a domicilio y para eventos</div>
  </section>
'''
cambia('  <div id="cubre">', nuevas + '\n  <div id="cubre">')
cambia('<div class="centro eyebrow sombra" data-in="0.5" data-fx="up" style="top:300px">En la web</div>',
       '<div class="centro eyebrow sombra" data-in="0.5" data-fx="up" style="top:300px">Cocina de Loren</div>')

# ---- 2) plan de tiempos por parte
plan = '''
const PARTE = new URLSearchParams(location.search).get("p") || "1";
const PLAN = {
  "1": [["s0f", 0, 6], ["s1", 6, 13.5], ["s2", 13.5, 21], ["s3", 21, 29], ["s4", 29, 35.5], ["s7", 35.5, 42], ["s8f", 42, 48]],
  "2": [["s0d", 0, 6], ["s5", 6, 25.5], ["s6", 25.5, 33.5], ["s8", 33.5, 42]]
}[PARTE];
$(".sc").forEach((s) => { const e = PLAN.find((x) => x[0] === s.id); s.dataset.a = e ? e[1] : -1; s.dataset.b = e ? e[2] : -1; });
const CORTES = PLAN.slice(1).map((x) => x[1]);
const FIN = PLAN[PLAN.length - 1][2];
const WA = (PLAN.find((x) => x[0] === "s5") || [0, 0, 0])[1], WB = (PLAN.find((x) => x[0] === "s5") || [0, 0, 0])[2];
const GR = (t) => PLAN.some((x) => document.getElementById(x[0]).dataset.gr === "1" && t >= x[1] && t < x[2]) ? 1 : 0;
'''
cambia('const CORTES = [6, 13.5, 21, 29, 35.5, 55, 63, 69.5];', plan.replace("$(", "$("))
# $ en este script es $$ (querySelectorAll); la función de la página se llama $
t = t.replace('$(".sc").forEach((s) => { const e = PLAN', '[...document.querySelectorAll(".sc")].forEach((s) => { const e = PLAN')
cambia('  const gr = t < 6 || (t >= 35.5 && t < 63) || t >= 69.5 ? 1 : 0;', '  const gr = GR(t);')

# ---- 3) la flor de las aperturas: relativa a cada escena
cambia('''  $("#floreIntro")[0].style.transform = `rotate(${-t * 14}deg) scale(${0.3 + 0.7 * eo(t / 2.2)})`;
  $("#floreIntro")[0].style.opacity = t < 6 ? Math.min(.6, t / 1.2) * (t > 4.6 ? 1 - (t - 4.6) / 1.4 * .55 : 1) : 0;''',
       '''  $(".introflor").forEach((f) => { const s = f.closest(".sc"), l = t - (+s.dataset.a), vis = l >= 0 && t < +s.dataset.b; f.style.transform = `rotate(${-l * 14}deg) scale(${0.3 + 0.7 * eo(l / 2.2)})`; f.style.opacity = vis ? Math.min(.6, l / 1.2) * (l > 4.6 ? 1 - (l - 4.6) / 1.4 * .55 : 1) : 0; });''')
cambia('<img class="enc" id="floreIntro"', '<img class="enc introflor" id="floreIntro"')

# ---- 4) la web: tiempos relativos al inicio de su escena
cambia('const imgs = {}; PANT.forEach', 'PANT.forEach((p) => { p.a += WA - 35.5; p.b += WA - 35.5; });\nconst imgs = {}; PANT.forEach')
cambia('  if (t >= 35.5 && t < 55) {\n    const l = t - 35.5,', '  if (WB > WA && t >= WA && t < WB) {\n    const l = t - WA,')
cambia('const fl = t - 72.9;', 'const fl = t - (FIN - 5.1);')
cambia('window.DUR = 78;', 'window.DUR = FIN;')
open(os.path.join(AQUI, "video7.html"), "w", encoding="utf-8").write(t)
print("ok")
