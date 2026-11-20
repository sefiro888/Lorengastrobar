"""
LOREN RESTOBAR · Navidad 2026 · VERSIÓN ALTERNATIVA «Navidad como un regalo»
Fondo crema de papel, cinta burdeos con lazo, fotos tipo polaroid y el precio en una etiqueta de regalo.

Uso:  python herramientas/navidad_b.py
Datos: herramientas/navidad_datos.py (los mismos que la versión 1).
Salida: para-loren/navidad/version-alternativa/ (carrusel, historias, WhatsApp, imprenta).
"""
import math, pathlib, shutil, sys
from PIL import Image
from playwright.sync_api import sync_playwright

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "herramientas"))
from navidad_datos import COMBOS, WHATSAPP, WEB

FOTOS = RAIZ / "para-loren" / "navidad" / "fotos-loren"
SAL = RAIZ / "para-loren" / "navidad" / "version-alternativa"
TMP = SAL / "_tmp"
QR = RAIZ / "para-loren" / "navidad" / "qr-navidad.svg"
R = RAIZ.as_uri()
foto = lambda c: f"{FOTOS.as_uri()}/{c['foto']}.webp"

LAZO = """<svg class="lazo" viewBox="0 0 200 160" style="{st}"><defs>
<linearGradient id="lz{n}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b3194a"/><stop offset=".55" stop-color="#6d0624"/><stop offset="1" stop-color="#3d0014"/></linearGradient></defs>
<path d="M93 72 L58 150 L71 141 L79 156 L104 80Z" fill="url(#lz{n})" stroke="#e8b43a" stroke-width="1.5"/>
<path d="M107 72 L142 150 L129 141 L121 156 L96 80Z" fill="url(#lz{n})" stroke="#e8b43a" stroke-width="1.5"/>
<path d="M100 70 C 62 18, 4 22, 16 64 C 26 96, 72 92, 100 76Z" fill="url(#lz{n})" stroke="#e8b43a" stroke-width="2"/>
<path d="M100 70 C 138 18, 196 22, 184 64 C 174 96, 128 92, 100 76Z" fill="url(#lz{n})" stroke="#e8b43a" stroke-width="2"/>
<path d="M96 70 C 72 46, 42 46, 40 62 C 44 76, 76 78, 96 73Z" fill="#2a000e" opacity=".45"/>
<path d="M104 70 C 128 46, 158 46, 160 62 C 156 76, 124 78, 104 73Z" fill="#2a000e" opacity=".45"/>
<path d="M28 44 C 46 28, 74 34, 92 58" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="4" stroke-linecap="round"/>
<path d="M172 44 C 154 28, 126 34, 108 58" fill="none" stroke="#fff" stroke-opacity=".25" stroke-width="4" stroke-linecap="round"/>
<rect x="85" y="56" width="30" height="30" rx="10" fill="url(#lz{n})" stroke="#e8b43a" stroke-width="2"/>
<path d="M90 62 Q100 58 110 62" fill="none" stroke="#fff" stroke-opacity=".4" stroke-width="3" stroke-linecap="round"/></svg>"""

CSS = """
:root { --vino:#59011d; --vino2:#7d0b2e; --oro:#c98e1e; --oro2:#e8b43a; --tinta:#2a1a1e; --crema:#f6eedd; }
* { margin:0; padding:0; box-sizing:border-box; }
html, body { background:var(--crema); -webkit-print-color-adjust:exact; print-color-adjust:exact; }
.lz { position:relative; overflow:hidden; font-family:Montserrat, sans-serif; color:var(--tinta); display:flex; flex-direction:column; align-items:center;
  background:radial-gradient(rgba(89,1,29,.035) 1px, transparent 1.4px) 0 0/7px 7px, radial-gradient(120% 80% at 50% 40%, #fbf6ea, #efe2c6); }
.lz > * { position:relative; z-index:3; }
.deco { position:absolute !important; pointer-events:none; }
.encaje { z-index:1 !important; mix-blend-mode:multiply; opacity:.16; }
.confeti { z-index:2 !important; color:var(--oro); line-height:1; }
.cinta-v { z-index:2 !important; top:0; bottom:0; background:linear-gradient(90deg, #3d0014, #7d0b2e 28%, #b3194a 50%, #7d0b2e 72%, #3d0014);
  border-left:3px solid var(--oro2); border-right:3px solid var(--oro2); box-shadow:0 0 24px rgba(61,0,20,.35); }
.cinta-h { z-index:2 !important; left:0; right:0; background:linear-gradient(#3d0014, #7d0b2e 28%, #b3194a 50%, #7d0b2e 72%, #3d0014);
  border-top:3px solid var(--oro2); border-bottom:3px solid var(--oro2); box-shadow:0 0 24px rgba(61,0,20,.35); }
.lazo { position:absolute; z-index:6; filter:drop-shadow(0 10px 14px rgba(42,0,14,.45)); }
.eyebrow { font-weight:800; letter-spacing:.26em; text-transform:uppercase; color:var(--oro); text-align:center; }
.titulo { font-family:"Kaushan Script", cursive; color:var(--vino); line-height:1.02; text-align:center; text-shadow:0 2px 0 rgba(255,255,255,.6); }
.anton { font-family:Anton, sans-serif; font-weight:400; text-transform:uppercase; letter-spacing:.18em; color:var(--oro); text-align:center; }
.pola { position:relative; background:#fffdf8; padding:18px 18px 74px; box-shadow:0 22px 44px -14px rgba(60,10,20,.5), 0 2px 6px rgba(0,0,0,.12); }
.pola img { display:block; object-fit:cover; }
.pola .pie { position:absolute; left:0; right:0; bottom:14px; text-align:center; font-family:"Kaushan Script"; color:var(--vino); }
.pola .adh { position:absolute; top:-20px; left:50%; width:44%; height:42px; margin-left:-22%; background:rgba(232,180,58,.55);
  box-shadow:0 2px 6px rgba(0,0,0,.12); transform:rotate(-4deg); clip-path:polygon(2% 0, 98% 6%, 100% 100%, 0 94%); }
.tagw { position:relative; filter:drop-shadow(0 12px 16px rgba(60,10,20,.35)); }
.tag { position:relative; display:inline-flex; flex-direction:column; align-items:flex-start; background:linear-gradient(135deg, #f7ead0, #e6cf9c);
  color:var(--vino); padding:.45em 1.1em .5em 2.3em; clip-path:polygon(1.3em 0, 100% 0, 100% 100%, 1.3em 100%, 0 50%); }
.tag::before { content:""; position:absolute; left:1.05em; top:50%; width:.55em; height:.55em; margin-top:-.275em; border-radius:50%; background:#efe2c6; box-shadow:inset 0 0 0 2px var(--oro); }
.tag small { font-weight:800; letter-spacing:.08em; text-transform:uppercase; color:var(--oro); font-size:.42em; white-space:nowrap; }
.tag b { font-family:Anton, sans-serif; font-weight:400; font-size:1em; line-height:1; white-space:nowrap; }
.cordel { position:absolute; left:-.2em; top:50%; width:2.2em; height:2px; background:var(--oro); transform-origin:right center; transform:rotate(-28deg) translateX(-1.6em); }
.lista { list-style:none; }
.lista li { position:relative; padding-left:1.3em; line-height:1.3; font-weight:600; }
.lista li::before { content:"✦"; position:absolute; left:0; color:var(--oro2); }
.pill { display:inline-block; background:var(--vino); color:#fff6e0; font-weight:800; border-radius:999px; box-shadow:0 14px 30px -10px rgba(89,1,29,.6), inset 0 0 0 3px var(--oro2); }
.cta { font-weight:700; text-align:center; color:var(--tinta); }
.cta b { color:var(--vino); }
"""


def rnd(seed, n):
    x = math.sin(seed * 97.3 + n * 31.7) * 43758.5453
    return x - math.floor(x)


def fondo(W, H, seed, n_conf=26):
    h = []
    for (x, y, d) in ((-d0 * .3, -d0 * .3, d0) for d0 in [W * .55]):
        h.append(f'<img class="deco encaje" src="img/kv/flor-kv.webp" style="left:{x:.0f}px;top:{y:.0f}px;width:{d:.0f}px">')
    d = W * .62
    h.append(f'<img class="deco encaje" src="img/kv/flor-kv.webp" style="left:{W - d * .65:.0f}px;top:{H - d * .62:.0f}px;width:{d:.0f}px">')
    for i in range(n_conf):
        x, y, s = rnd(seed, i) * W, rnd(seed, i + 40) * H, 12 + rnd(seed, i + 80) * 22
        ch = "✦" if i % 3 else "●"
        if ch == "●": s *= .35
        h.append(f'<div class="deco confeti" style="left:{x:.0f}px;top:{y:.0f}px;font-size:{s:.0f}px;opacity:{.35 + rnd(seed, i + 9) * .5:.2f}">{ch}</div>')
    return "".join(h)


def lazo(x, y, w, n, rot=0):
    return LAZO.format(st=f"left:{x - w / 2:.0f}px;top:{y - w * .35:.0f}px;width:{w}px;transform:rotate({rot}deg)", n=n)


def pola(c, w, h, rot, pie, fs=40, pos="50% 58%"):
    return (f'<div class="pola" style="transform:rotate({rot}deg)"><span class="adh"></span>'
            f'<img src="{foto(c)}" style="width:{w}px;height:{h}px;object-position:{pos}"><div class="pie" style="font-size:{fs}px">{pie}</div></div>')


def tag(c, fs, rot=-5, cordel=True):
    return (f'<div class="tagw" style="transform:rotate({rot}deg);font-size:{fs}px">{'<span class="cordel"></span>' if cordel else ''}'
            f'<div class="tag"><small>{c["cantidad"]}</small><b>{c["precio"]}</b></div></div>')


def lista(items, fs, cols=1):
    est = f"font-size:{fs}px;" + (f"columns:{cols};column-gap:30px;" if cols > 1 else "")
    return f'<ul class="lista" style="{est}">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def pagina(cuerpo, W, H):
    return f"""<!doctype html><html><head><meta charset="utf-8"><base href="{R}/">
<link rel="stylesheet" href="css/fuentes.css"><style>{CSS} .lz {{ width:{W}px; height:{H}px; }}</style></head>
<body><div class="lz">{cuerpo}</div></body></html>"""


# ---------- piezas ----------
def portada(W, H, alto):
    k = 1.0 if not alto else 1.12
    cy = 905 if not alto else 1200                                  # centro de la fila de polaroids
    return fondo(W, H, 3) + f"""
<div class="deco cinta-h" style="top:{cy - 34}px;height:68px"></div>
<img src="img/marca/logo-loren.webp" style="width:{int(190 * k)}px;margin-top:{60 if not alto else 270}px;filter:drop-shadow(0 6px 10px rgba(60,10,20,.25))">
<div class="eyebrow" style="font-size:{int(28 * k)}px;margin-top:22px">Nochebuena 24 · Fin de Año 31</div>
<div class="titulo" style="font-size:{int(124 * k)}px;margin-top:10px">Bocaditos<br>de Navidad</div>
<div class="anton" style="font-size:{int(40 * k)}px;margin-top:14px">· a la paraguaya ·</div>
<div style="position:absolute;left:0;right:0;top:{cy - 250 * k:.0f}px;height:{500 * k:.0f}px;z-index:4">
  <div style="position:absolute;left:{70 * k:.0f}px;top:{40 * k:.0f}px">{pola(COMBOS[2], int(270 * k), int(300 * k), -9, "embutidos", int(34 * k), "50% 50%")}</div>
  <div style="position:absolute;right:{70 * k:.0f}px;top:{40 * k:.0f}px">{pola(COMBOS[3], int(270 * k), int(300 * k), 8, "quesos", int(34 * k), "45% 50%")}</div>
  <div style="position:absolute;left:50%;top:0;margin-left:{-170 * k:.0f}px;z-index:2">{pola(COMBOS[1], int(304 * k), int(340 * k), -1.5, "bocaditos", int(36 * k), "50% 55%")}</div>
</div>
{lazo(W / 2, cy - 250 * k - 14, int(200 * k), 1)}
<div style="margin-top:auto;margin-bottom:{44 if not alto else 286}px"><span class="pill" style="font-size:{int(36 * k)}px;padding:20px 46px">Desde 42,90 € · Encarga por WhatsApp</span></div>
<div class="deco" style="left:0;right:0;top:{cy + 250 * k - (34 if not alto else 75):.0f}px;text-align:center;font-family:'Kaushan Script';color:var(--vino);font-size:{int(46 * k)}px;z-index:5">¡Vy'apavẽ Navidad!</div>"""


def slide_combo(c, W, H, alto, n):
    largo = len(c["items"]) > 5
    cx = W - 120
    deco = fondo(W, H, 10 + n) + f'<div class="deco cinta-v" style="left:{cx - 30}px;width:60px"></div>' + lazo(cx, 150 if not alto else 330, 200, 10 + n, 8)
    if not alto:
        return deco + f"""
<div style="align-self:flex-start;margin:66px 0 0 70px;width:{W - 330}px;text-align:left">
  <img src="img/marca/logo-loren.webp" style="width:150px;filter:drop-shadow(0 6px 10px rgba(60,10,20,.25))">
  <div class="eyebrow" style="font-size:24px;margin-top:18px;text-align:left">Navidad y Año Nuevo</div>
  <div class="titulo" style="font-size:118px;margin-top:6px;text-align:left">{c['titulo']}</div>
  <div class="anton" style="font-size:30px;text-align:left;letter-spacing:.16em">{c['sub']}</div>
</div>
<div style="display:flex;gap:36px;align-items:flex-start;align-self:flex-start;margin:40px 0 0 64px">
  <div style="flex:none;margin-top:14px">{pola(c, 390, 460, -4, c['titulo'], 38)}</div>
  <div style="flex:none;width:{W - 64 - 426 - 36 - 190}px;padding-top:24px">
    {lista(c['items'], 28 if not largo else 26)}
    <div style="margin-top:38px">{tag(c, 60)}</div>
  </div>
</div>
<div class="cta" style="font-size:28px;margin-top:auto;margin-bottom:56px;align-self:flex-start;margin-left:70px;text-align:left">Encarga por WhatsApp <b>{WHATSAPP}</b><br><span style="font-size:23px;opacity:.75">{WEB}</span></div>"""
    return deco + f"""
<div style="align-self:flex-start;margin:270px 0 0 80px;width:{W - 330}px">
  <img src="img/marca/logo-loren.webp" style="width:180px;filter:drop-shadow(0 6px 10px rgba(60,10,20,.25))">
  <div class="eyebrow" style="font-size:28px;margin-top:18px;text-align:left">Navidad y Año Nuevo</div>
  <div class="titulo" style="font-size:140px;margin-top:4px;text-align:left">{c['titulo']}</div>
  <div class="anton" style="font-size:34px;text-align:left;letter-spacing:.16em">{c['sub']}</div>
</div>
<div style="align-self:flex-start;margin:44px 0 0 90px">{pola(c, 560, 520, -3, c['titulo'], 44)}</div>
<div style="align-self:flex-start;margin:44px 0 0 90px;width:{W - 330}px">{lista(c['items'], 31 if not largo else 29, 2 if largo else 1)}</div>
<div style="align-self:flex-start;margin:34px 0 0 110px">{tag(c, 70)}</div>"""


def slide_encargar(W, H, alto):
    top = 270 if alto else 70
    pasos = [("Elige tu combo", "Combo 1, Combo 2, embutidos o quesos"),
             ("Escríbenos por WhatsApp", f"{WHATSAPP} · dinos el día: 24 o 31"),
             ("Recógelo en el local", "Carrer de la Muntanya 115 · Camp de l'Arpa")]
    p = "".join(f"""<div style="display:flex;gap:28px;align-items:center;margin-top:{36 if alto else 26}px">
  <div style="flex:none;position:relative;width:104px;height:104px">
    <img src="img/kv/flor-kv.webp" style="position:absolute;inset:-14px;width:132px;opacity:.5;mix-blend-mode:multiply">
    <div style="position:absolute;inset:10px;border-radius:50%;background:var(--vino);color:#fff6e0;display:grid;place-items:center;font-family:'Kaushan Script';font-size:50px;box-shadow:inset 0 0 0 3px var(--oro2)">{i + 1}</div></div>
  <div><div style="font-family:'Kaushan Script';color:var(--vino);font-size:50px;line-height:1">{t}</div><div style="font-size:27px;font-weight:600;margin-top:8px;opacity:.85">{s}</div></div></div>""" for i, (t, s) in enumerate(pasos))
    return fondo(W, H, 77) + f'<div class="deco cinta-h" style="top:{top + 150}px;height:56px;opacity:.95"></div>' + lazo(W / 2, top + 178, 210, 77) + f"""
<img src="img/marca/logo-loren.webp" style="width:{170 if not alto else 200}px;margin-top:{top}px;filter:drop-shadow(0 6px 10px rgba(60,10,20,.25))">
<div class="titulo" style="font-size:{112 if not alto else 130}px;margin-top:{120 if not alto else 130}px">¿Cómo lo encargo?</div>
<div class="anton" style="font-size:32px;margin-top:8px">· fácil y sin complicaciones ·</div>
<div style="margin-top:22px;padding:0 90px;width:100%">{p}</div>
<div style="margin-top:{50 if alto else 40}px"><span class="pill" style="font-size:38px;padding:22px 52px">Encarga con antelación</span></div>
<div class="cta" style="font-size:30px;margin-top:24px">{WEB}</div>"""


def fila(c, fs, fw, fh, rot):
    """Cada combo en su propia tarjeta: foto, nombre con su precio al lado y la lista debajo (sin cordel, para que no haya dudas)."""
    pol = pola(c, fw, fh, rot, "", 10).replace('class="pola"', 'class="pola" style="padding:10px 10px 26px"', 1).replace(f'style="transform:rotate({rot}deg)"', f'style="padding:10px 10px 26px;transform:rotate({rot}deg)"', 1)
    return f"""<div style="display:flex;gap:{fs * 1.3:.0f}px;align-items:center;background:rgba(255,253,246,.72);border:2px solid rgba(201,142,30,.35);border-radius:20px;padding:{fs * .55:.0f}px {fs * .9:.0f}px;box-shadow:0 8px 20px -14px rgba(60,10,20,.45)">
  <div style="flex:none">{pol}</div>
  <div style="flex:1;min-width:0">
    <div style="display:flex;align-items:center;justify-content:space-between;gap:12px">
      <div style="display:flex;align-items:baseline;gap:14px;flex-wrap:wrap;min-width:0"><span class="titulo" style="font-size:{fs * 2.3:.0f}px;text-align:left">{c['titulo']}</span><span class="anton" style="font-size:{fs * .9:.0f}px;letter-spacing:.14em">{c['sub']}</span></div>
      <div style="flex:none">{tag(c, fs * 1.6, -3, False)}</div>
    </div>
    <div style="margin-top:{fs * .45:.0f}px">{lista(c['items'], fs, 2)}</div>
  </div>
</div>"""


def resumen(W, H, con_qr, alto_extra=0, fs=20, fw=220, fh=170, gap=18, top=22, pad=60, tit=96):
    qr_html = (f'<div style="background:#fffdf8;padding:14px;border-radius:14px;box-shadow:0 0 0 4px var(--oro2), 0 10px 24px -8px rgba(60,10,20,.4)"><img src="{QR.as_uri()}" style="width:140px;height:140px;display:block"></div>'
               if con_qr else "")
    rots = [-3, 2.5, -2, 3]
    filas = "".join(fila(c, fs, fw, fh, rots[i]) for i, c in enumerate(COMBOS))
    return fondo(W, H, 5, 30) + f'<div class="deco cinta-h" style="top:{18 + alto_extra}px;height:46px"></div>' + lazo(W - 170, 41 + alto_extra, 150, 5, 6) + f"""
<img src="img/marca/logo-loren.webp" style="width:{140 if H < 1500 else 170}px;margin-top:{86 + alto_extra}px;filter:drop-shadow(0 6px 10px rgba(60,10,20,.25))">
<div class="eyebrow" style="font-size:22px;margin-top:12px">Nochebuena 24 · Fin de Año 31</div>
<div class="titulo" style="font-size:{tit}px;margin-top:2px">Bocaditos de Navidad</div>
<div class="anton" style="font-size:{tit * .3:.0f}px">· a la paraguaya ·</div>
<div style="display:flex;flex-direction:column;gap:{gap}px;padding:0 {pad}px;margin-top:{top}px;width:100%">{filas}</div>
<div style="display:flex;align-items:center;gap:30px;margin-top:auto;margin-bottom:{34 + alto_extra}px">
  {qr_html}
  <div class="cta" style="font-size:28px;text-align:{'left' if con_qr else 'center'}">Encarga por WhatsApp{'<br>' if con_qr else ' '}<b style="font-size:{48 if con_qr else 40}px;font-family:Anton;font-weight:400">{WHATSAPP}</b><br>
  <span style="font-size:21px;opacity:.8">Encarga con antelación · Recogida en Carrer de la Muntanya 115</span></div>
</div>"""


def main():
    TMP.mkdir(parents=True, exist_ok=True)
    T = []
    T.append(("1-instagram-carrusel", "01-portada", pagina(portada(1080, 1350, False), 1080, 1350), 1080, 1350, None))
    T.append(("2-instagram-historias", "01-portada", pagina(portada(1080, 1920, True), 1080, 1920), 1080, 1920, None))
    for n, c in enumerate(COMBOS):
        T.append(("1-instagram-carrusel", f"0{n + 2}-{c['id']}", pagina(slide_combo(c, 1080, 1350, False, n), 1080, 1350), 1080, 1350, None))
        T.append(("2-instagram-historias", f"0{n + 2}-{c['id']}", pagina(slide_combo(c, 1080, 1920, True, n), 1080, 1920), 1080, 1920, None))
    T.append(("1-instagram-carrusel", "06-como-encargar", pagina(slide_encargar(1080, 1350, False), 1080, 1350), 1080, 1350, None))
    T.append(("2-instagram-historias", "06-como-encargar", pagina(slide_encargar(1080, 1920, True), 1080, 1920), 1080, 1920, None))
    T.append(("3-whatsapp", "resumen-1080x1350", pagina(resumen(1080, 1350, False, 0, 19, 200, 150, 14, 14, 46, 78), 1080, 1350), 1080, 1350, None))
    T.append(("3-whatsapp", "estado-1080x1920", pagina(resumen(1080, 1920, False, 170, 22, 235, 182, 18, 20, 50, 94), 1080, 1920), 1080, 1920, None))
    T.append(("4-imprenta", "cartel-A4", pagina(resumen(1111, 1559, True, 0, 20, 225, 170, 14, 14, 60, 86), 1111, 1559), 1111, 1559, (216, 303)))
    T.append(("4-imprenta", "flyer-A5", pagina(resumen(1111, 1559, True, 0, 20, 225, 170, 14, 14, 60, 86), 1111, 1559), 1111, 1559, (154, 216)))
    with sync_playwright() as pw:
        nav = pw.chromium.launch()
        for carpeta, nombre, html, W, H, mm in T:
            d = SAL / carpeta; d.mkdir(parents=True, exist_ok=True)
            f = TMP / f"{carpeta}-{nombre}.html"; f.write_text(html, encoding="utf-8")
            esc = (mm[0] / 25.4 * 300 / W) if mm else 1
            pg = nav.new_page(viewport={"width": W, "height": H}, device_scale_factor=esc)
            pg.goto(f.as_uri()); pg.wait_for_load_state("networkidle"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
            sale = pg.evaluate("(() => { const l = document.querySelector('.lz'); const m = Math.max(...[...l.children].filter(e => !e.classList.contains('deco') && !e.classList.contains('lazo')).map(e => e.getBoundingClientRect().bottom + parseFloat(getComputedStyle(e).marginBottom))); return Math.round(m - l.clientHeight); })()")
            if mm:
                pg.evaluate(f"document.querySelector('.lz').style.zoom = {mm[0] / 25.4 * 96 / W}")
                pg.pdf(path=str(d / f"{nombre}-imprenta.pdf"), width=f"{mm[0]}mm", height=f"{mm[1]}mm", print_background=True)
                pg.evaluate("document.querySelector('.lz').style.zoom = ''")
            tmp_png = TMP / f"{carpeta}-{nombre}.png"
            pg.locator(".lz").screenshot(path=str(tmp_png))
            if mm:
                try: shutil.copyfile(tmp_png, d / f"{nombre}.png")
                except OSError: print(f"   ⚠ {nombre}.png está abierto en otro programa")
            else:
                Image.open(tmp_png).convert("RGB").save(d / f"{nombre}.jpg", quality=92)
            print(f"{carpeta}/{nombre}" + (f"   ⚠ se sale {sale} px" if sale > 0 else ""))
            pg.close()
        nav.close()
    shutil.rmtree(TMP, ignore_errors=True)


if __name__ == "__main__":
    main()
