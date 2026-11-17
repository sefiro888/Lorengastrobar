"""Versión «calmada» del promo dividido: mismo ritmo en todas las escenas, disolvencias suaves y textos legibles.
Lee video7.html (generado por generar7.py) y escribe video8p.html (parte 1 «Sabores», 6 escenas de 6,5 s)."""
import os, re
AQUI = os.path.dirname(os.path.abspath(__file__))
t = open(os.path.join(AQUI, "video7.html"), encoding="utf-8").read()


def cambia(viejo, nuevo):
    global t
    assert viejo in t, "no encuentro: " + viejo[:80]
    t = t.replace(viejo, nuevo, 1)


# ---- 1) mismo ritmo: 7 escenas de 6,5 s
L = 6.5
nuevo_plan = '"1": [["s0f", 0, 6.5], ["s1", 6.5, 13], ["s2", 13, 19.5], ["s3", 19.5, 26], ["s4", 26, 32.5], ["s7", 32.5, 39], ["s8f", 39, 45.5]],'
t = re.sub(r'"1": \[\["s0f".*?\]\],', nuevo_plan, t, count=1, flags=re.S)
assert nuevo_plan in t

# ---- 2) animaciones sin rebote, más largas y suaves
cambia("const eo = (x) => 1 - Math.pow(1 - clamp(x), 3);", "const eo = (x) => Math.sin(clamp(x) * Math.PI / 2);")
cambia("const eio = (x) => { x = clamp(x); return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };", "const eio = (x) => 0.5 - 0.5 * Math.cos(Math.PI * clamp(x));")
t = re.sub(r"const eb = \(x\) => \{[^\n]*\};", "const eb = (x) => Math.sin(clamp(x) * Math.PI / 2);", t, count=1)
cambia("k = eb(p / 0.8), o = clamp(p / 0.45), fx = e.dataset.fx;", "k = eb(p / 1.2), o = clamp(p / 0.9), fx = e.dataset.fx;")
cambia("tf = `translateY(${(1 - k) * 80}px)`;", "tf = `translateY(${(1 - k) * 46}px)`;")
cambia("tf = `scale(${0.5 + 0.5 * k})`;", "tf = `scale(${0.88 + 0.12 * k})`;")
cambia("translateX(${(1 - eo(p / 0.9)) * -560}px)", "translateX(${(1 - eo(p / 1.4)) * -560}px)")
cambia("translateX(${(1 - eo(p / 0.9)) * 560}px)", "translateX(${(1 - eo(p / 1.4)) * 560}px)")

# ---- 3) cada escena se disuelve en la siguiente (1,2 s), sin cortes
funcion_fade = '''const XF = 1.2;
const fadeDe = (a, b, t) => { const d = a <= 0.01 ? a : a - XF / 2, h = b >= FIN - 0.01 ? b + 1 : b + XF / 2; if (t < d || t >= h) return 0; return Math.max(0.001, Math.min(a <= 0.01 ? 1 : clamp((t - d) / XF), b >= FIN - 0.01 ? 1 : clamp((h - t) / XF))); };
function render(t) {'''
cambia("function render(t) {", funcion_fade)
cambia("  const gr = GR(t);", "  const gr = Math.max(0, ...PLAN.filter((x) => document.getElementById(x[0]).dataset.gr === \"1\").map((x) => fadeDe(x[1], x[2], t)));")
cambia('    if (t < a || t >= b) { s.style.visibility = "hidden"; return; }\n    s.style.visibility = "visible";',
       '    const fo = fadeDe(a, b, t);\n    if (fo <= 0) { s.style.visibility = "hidden"; return; }\n    s.style.visibility = "visible"; s.style.opacity = fo;')

# ---- 4) transición: aro dorado que se abre despacio (sin tapar la imagen)
t = re.sub(r"  // transición con el ñandutí que se abre y se cierra.*?if \(!hay\) cu\.style\.display = \"none\";",
           '''  // transición suave: un aro dorado que se abre despacio mientras una escena se disuelve en la siguiente
  const cu = $("#cubre")[0]; let hay = false;
  for (const c of CORTES) { const p = (t - (c - 0.8)) / 1.6; if (p >= 0 && p <= 1) { const e = Math.sin(p * Math.PI / 2); cu.style.display = "block"; cu.style.background = "transparent"; cu.style.overflow = "visible"; cu.style.boxShadow = "0 0 0 7px rgba(243,238,220,.9), 0 0 0 16px rgba(232,180,58,.85), 0 0 90px 20px rgba(232,180,58,.35)"; cu.style.transform = `scale(${0.25 + 2.3 * e})`; cu.style.opacity = Math.sin(p * Math.PI) * 0.7; hay = true; } }
  if (!hay) cu.style.display = "none";''', t, count=1, flags=re.S)
assert "aro dorado" in t
cambia('$("#flash")[0].style.opacity = fl > 0 && fl < 0.35 ? 0.55 * (1 - fl / 0.35) : 0;', '$("#flash")[0].style.opacity = 0;')
cambia("  #flash {", "  #cubre img { display: none; }\n  #flash {")

# ---- 5) textos legibles: dorado más claro, contorno oscuro, sombras fuertes y velos más oscuros
cambia('.kau { font-family: "Kaushan Script", cursive; color: var(--maiz); line-height: 1.05; }',
       '.kau { font-family: "Kaushan Script", cursive; color: var(--maiz2); line-height: 1.05; -webkit-text-stroke: 2px rgba(42,0,14,.6); paint-order: stroke fill; text-shadow: 0 0 40px rgba(0,0,0,.95), 0 4px 22px rgba(0,0,0,.9); }')
cambia(".eyebrow { font-weight: 700; font-size: 34px; letter-spacing: .28em; text-transform: uppercase; color: var(--maiz); }",
       ".eyebrow { font-weight: 800; font-size: 38px; letter-spacing: .28em; text-transform: uppercase; color: var(--maiz2); text-shadow: 0 0 30px rgba(0,0,0,.95), 0 3px 14px rgba(0,0,0,.9); }")
cambia(".sombra { text-shadow: 0 4px 28px rgba(0,0,0,.75), 0 2px 6px rgba(0,0,0,.6); }",
       ".sombra { text-shadow: 0 0 44px rgba(0,0,0,.95), 0 4px 22px rgba(0,0,0,.9), 0 2px 5px rgba(0,0,0,.85); }")
cambia(".velo { position: absolute; inset: 0; background: linear-gradient(rgba(14,6,9,.62), transparent 30%, transparent 52%, rgba(14,6,9,.78)); }",
       ".velo { position: absolute; inset: 0; background: linear-gradient(rgba(14,6,9,.86), rgba(14,6,9,.45) 36%, rgba(14,6,9,.12) 58%, rgba(14,6,9,.86)); }")
# apertura: sin el ñandutí claro detrás del texto y con un velo oscuro
cambia('style="opacity:.55;width:1300px;height:1300px;margin:-650px 0 0 -650px" alt="">\n    <img class="logo" data-in="1.2"',
       'style="opacity:.22;width:1300px;height:1300px;margin:-650px 0 0 -650px" alt="">\n    <div style="left:0;right:0;top:640px;height:760px;background:radial-gradient(62% 52% at 50% 50%, rgba(8,3,5,.82), transparent 78%)"></div>\n    <img class="logo" data-in="1.2"')
cambia('<div class="centro kau" data-in="2.9" data-fx="up" style="top:900px;font-size:118px;line-height:1.08;left:40px;right:40px">Hay sabores<br>que nos hacen<br>sentir en casa</div>',
       '<div class="centro kau" data-in="2.9" data-fx="up" style="top:880px;font-size:118px;line-height:1.1;left:40px;right:40px;color:var(--crema)">Hay sabores<br>que nos hacen<br><span style="color:var(--maiz2);font-size:140px">sentir en casa</span></div>')
open(os.path.join(AQUI, "video7.html"), "w", encoding="utf-8").write(t)
print("ok")
