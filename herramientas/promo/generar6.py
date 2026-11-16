"""Genera video6.html (versión B, carrusel de círculos) a partir de video4.html (versión C)."""
import os
AQUI = os.path.dirname(os.path.abspath(__file__))
t = open(os.path.join(AQUI, "video4.html"), encoding="utf-8").read()

# 1) los 6 pasos sueltos se sustituyen por UNA escena con un carrusel
a = t.index("  <!-- 2..7 · Pasos -->"); b = t.index("  <!-- 8 · El queso -->")
carrusel = '''  <!-- 2 · CARRUSEL de los 6 pasos -->
  <section class="sc" id="s2">
    <img class="flor" data-rot="18" src="../../img/kv/flor-kv.webp" alt="">
    <div class="pasos" id="cpasos" style="top:200px"></div>
    <div class="centro eyebrow sombra" id="ceyebrow" style="top:262px"></div>
    <div class="centro anton sombra" id="cpal" style="top:330px;font-size:230px"></div>
    <img class="encaje" id="canillo" data-rot="55" src="../../img/kv/flor-kv.webp" style="top:560px;width:1360px;height:1360px;margin-left:-680px" alt="">
    <div id="orbita"></div>
    <div id="items"></div>
    <div class="chip" id="cchip" style="top:1470px;z-index:30"></div>
  </section>

'''
t = t[:a] + carrusel + t[b:]

# 2) fuera la construcción de pasos del JS
a = t.index("// --- construir las 6 escenas de pasos"); b = t.index("// brasas y chispas fijas")
t = t[:a] + t[b:]

# 3) tiempos y transiciones propios
t = t.replace("const T = [0, 2.4, 2.4 + P, 2.4 + 2 * P, 2.4 + 3 * P, 2.4 + 4 * P, 2.4 + 5 * P, 2.4 + 6 * P, 2.4 + 7 * P, 2.4 + 7 * P + 5.57, 35.0];",
              "const T2 = 2.4 + P, T8 = 2.4 + 7 * P, T9 = T8 + 5.57;\nconst T = [0, 2.4, T2, T8, T9, 35.0];")
t = t.replace('const TIPO = ["circulo", "whip", "zoom", "arriba", "diagonal", "giro", "whip", "circulo", "zoom"];  // 9 cortes',
              'const TIPO = ["circulo", "giro", "zoom", "circulo"];')

# 4) el carrusel
carr_js = '''
const STEPS = [
  { pal: "JAMÓN", det: "Jamón dulce en cubitos", clip: "jamon", cx: .50, cy: .36 },
  { pal: "BECHAMEL", det: "Mantequilla, harina y leche", clip: "bechamel", cx: .50, cy: .34 },
  { pal: "MASA", det: "Casera, hecha en el día", clip: "masa", cx: .50, cy: .36 },
  { pal: "RELLENO", det: "Bien cargadito de jamón y queso", clip: "relleno", cx: .55, cy: .38 },
  { pal: "CERRAR", det: "Con el rodillo, a mano", clip: "cerrar", cx: .52, cy: .36 },
  { pal: "FRITA", det: "Dorada en aceite bien caliente", clip: "frita", cx: .50, cy: .40 }];
const ITEMS = $("#items");
STEPS.forEach((s, k) => { const d = document.createElement("div"); d.className = "aro"; d.style.cssText = "position:absolute;width:900px;height:900px;margin-left:-450px;top:680px;left:50%"; d.innerHTML = `<img class="vf"><div class="num" style="position:absolute;left:30px;top:30px;width:150px;height:150px;font-size:110px">${k + 1}</div>`; ITEMS.appendChild(d); s.el = d; });
const OR = $("#orbita"); for (let i = 0; i < 10; i++) { const e = document.createElement("div"); e.className = "chispa"; e.style.cssText = "position:absolute;left:540px;top:1130px;opacity:.9"; e.dataset.a = (i / 10) * Math.PI * 2; OR.appendChild(e); }
$("#cpasos").innerHTML = [1, 2, 3, 4, 5, 6].map(() => "<b></b>").join("");
function carrusel(s, t) {
  const t0 = T2, u = (t - t0) / P, i = Math.max(0, Math.min(5, Math.floor(u))), fr = u - i;
  const pos = Math.min(5, i + eio((fr - 0.78) / 0.22) * (i < 5 ? 1 : 0));
  const idx = Math.max(0, Math.min(5, Math.floor(u + 0.11)));
  $$("#cpasos b", s).forEach((b, k) => (b.className = k <= idx ? "on" : ""));
  $("#ceyebrow", s).textContent = "Paso " + (idx + 1);
  const wt = (t - t0) - idx * P + 0.11 * P, pal = $("#cpal", s); pal.textContent = STEPS[idx].pal;
  pal.style.transform = `scale(${1 + (1 - clamp(wt / 0.3)) * 1.7})`; pal.style.opacity = clamp(wt / 0.25);
  const ch = $("#cchip", s); ch.innerHTML = STEPS[idx].det; ch.style.opacity = clamp((wt - .2) / .3); ch.style.transform = `translateX(-50%) translateY(${(1 - eo((wt - .2) / .5)) * 60}px)`;
  STEPS.forEach((st, k) => {
    const d = k - pos, ad = Math.abs(d), el = st.el;
    if (ad > 1.7) { el.style.display = "none"; return; }
    el.style.display = "block";
    const sc = 1 - 0.43 * Math.min(ad, 1.3), x = d * 600, y = 20 + ad * 70;
    el.style.transform = `translate(${x}px, ${y}px) scale(${sc}) rotate(${d * 7}deg)`; el.style.opacity = Math.max(0, 1 - 0.3 * ad);
    el.style.zIndex = 10 - Math.round(ad * 3);
    const local = clamp(t - (t0 + k * P) + (k > 0 ? 0 : 0.3), 0, 3.3), im = $("img.vf", el);
    im.src = cargar(st.clip, Math.max(1, Math.min(Math.floor(local * FR) + 1, 102))).src;
    const D = 900, z = 1.9 * (1 + 0.07 * clamp(local / 3)), w = D * z, scl = w / 576;
    im.style.width = w + "px"; im.style.height = (1024 * scl) + "px"; im.style.left = (D / 2 - st.cx * w) + "px"; im.style.top = (D / 2 - st.cy * 1024 * scl) + "px";
  });
  $("#canillo", s).style.opacity = .55 + .15 * Math.sin(t * 3);
  $$(".chispa", $("#orbita")).forEach((e) => { const a = +e.dataset.a + t * 1.2, r = 590; e.style.transform = `translate(${Math.cos(a) * r}px, ${Math.sin(a) * r * .72}px)`; });
}
'''
t = t.replace("function render(t) {", carr_js + "function render(t) {", 1)
t = t.replace("    // vídeo dentro del círculo", "    if (s.id === \"s2\") carrusel(s, t);\n    // vídeo dentro del círculo")
t = t.replace("</style>", "  #items, #orbita { inset: 0; }\n</style>", 1)
open(os.path.join(AQUI, "video6.html"), "w", encoding="utf-8").write(t)
print("ok")
