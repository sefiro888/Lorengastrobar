"""
LOREN RESTOBAR · Campaña de Navidad y Fin de Año (combos de bocaditos)

Uso:  python herramientas/navidad.py
Lee los datos de herramientas/navidad_datos.py y las fotos de para-loren/navidad/fotos-loren/.
Genera en para-loren/navidad/:
  1-instagram-carrusel/  6 imágenes 1080×1350 (portada, 4 combos, cómo encargar)
  2-instagram-historias/ 6 imágenes 1080×1920 (texto dentro de la zona segura)
  3-whatsapp/            resumen 1080×1350 y estado 1080×1920
  4-imprenta/            cartel A4 y flyer A5 (PDF con 3 mm de sangrado + PNG 300 ppp)
y copia las fotos optimizadas para la web en img/navidad/.
"""
import pathlib, shutil, sys
import segno
from PIL import Image
from playwright.sync_api import sync_playwright

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "herramientas"))
from navidad_datos import COMBOS, WHATSAPP, WEB

FOTOS = RAIZ / "para-loren" / "navidad" / "fotos-loren"
SAL = RAIZ / "para-loren" / "navidad"
TMP = SAL / "_tmp"
R = RAIZ.as_uri()

# ---------- fotos para la web (900 px, WebP) ----------
(RAIZ / "img" / "navidad").mkdir(parents=True, exist_ok=True)
for c in COMBOS:
    if c["foto"]:
        dst = RAIZ / "img" / "navidad" / f"{c['foto']}.webp"
        if not dst.exists():
            im = Image.open(FOTOS / f"{c['foto']}.webp").convert("RGB")
            im.thumbnail((900, 1200), Image.LANCZOS); im.save(dst, "WEBP", quality=82, method=6)
qr = SAL / "qr-navidad.svg"
segno.make("https://" + WEB, error="h").save(str(qr), scale=10, border=0, dark="#2a000e", light=None)


def foto(c):
    return f"{FOTOS.as_uri()}/{c['foto']}.webp" if c["foto"] else None


CSS = """
:root { --maiz:#e8b43a; --maiz2:#f4d27a; --crema:#f3eedc; --vino:#59011d; --vino9:#2a000e; }
* { margin:0; padding:0; box-sizing:border-box; }
html, body { background:#151012; -webkit-print-color-adjust:exact; print-color-adjust:exact; }
.lz { position:relative; overflow:hidden; font-family:Montserrat, sans-serif; color:var(--crema);
      background:#151012 url("img/kv/textura-oscura.webp") center/cover; display:flex; flex-direction:column; align-items:center; }
.lz::before { content:""; position:absolute; inset:0; background:radial-gradient(70% 45% at 50% 50%, rgba(125,11,46,.55), transparent 75%), linear-gradient(rgba(21,16,18,.35), rgba(21,16,18,.6)); }
.lz > * { position:relative; z-index:2; }
.deco { position:absolute !important; z-index:1 !important; pointer-events:none; }
.copo { opacity:.45; filter:drop-shadow(0 0 6px rgba(255,248,225,.9)) drop-shadow(0 0 14px rgba(244,210,122,.5)); }
.bokeh { border-radius:50%; filter:blur(6px); }
.estrella { color:var(--maiz2); text-shadow:0 0 18px rgba(244,210,122,.95), 0 0 4px #fff; line-height:1; }
.guirnalda { left:0; top:0; }
.bombilla { border-radius:50%; }
.colg { display:flex; flex-direction:column; align-items:center; }
.colg .hilo { width:2px; flex:1; background:linear-gradient(rgba(244,210,122,.5), var(--maiz2)); }
.colg .tapa { flex:none; width:24%; height:9px; border-radius:3px 3px 1px 1px; background:linear-gradient(90deg, #8a5a10, #f4d27a 45%, #8a5a10); margin-bottom:-2px; position:relative; z-index:2; }
.colg .bola { border-radius:50%; position:relative; overflow:hidden; flex:none;
  background:radial-gradient(circle at 34% 30%, #fff7dc 0, #f4d27a 22%, #c98e1e 62%, #6e4308 100%);
  box-shadow:0 0 34px rgba(244,210,122,.55), 0 10px 24px rgba(0,0,0,.5); }
.colg .bola img { position:absolute; inset:9%; width:82%; height:82%; opacity:.6; mix-blend-mode:multiply; }
.colg .bola.vino { background:radial-gradient(circle at 34% 30%, #ffd0d8 0, #b0405f 20%, #59011d 60%, #1c0009 100%); box-shadow:0 0 30px rgba(176,64,95,.55), 0 10px 24px rgba(0,0,0,.5); }
.colg .bola.vino img { mix-blend-mode:screen; opacity:.55; filter:sepia(1) saturate(2.5) hue-rotate(5deg) brightness(1.1); }
.colg .bola::after { content:""; position:absolute; left:18%; top:12%; width:30%; height:20%; border-radius:50%; background:rgba(255,255,255,.55); filter:blur(3px); }
.cinta { display:inline-block; position:relative; font-family:"Kaushan Script", cursive; color:var(--vino9); background:linear-gradient(90deg, #c98e1e, #f4d27a 30%, #fff1c2 50%, #f4d27a 70%, #c98e1e);
  padding:.18em 1.1em .26em; box-shadow:0 10px 26px -8px rgba(0,0,0,.7), 0 0 26px rgba(244,210,122,.35); transform:rotate(-2deg); }
.cinta::before, .cinta::after { content:""; position:absolute; top:22%; width:.9em; height:76%; background:#a9761c; z-index:-1; }
.cinta::before { left:-.55em; clip-path:polygon(0 0, 100% 0, 100% 100%, 0 100%, 40% 50%); }
.cinta::after { right:-.55em; clip-path:polygon(0 0, 100% 0, 60% 50%, 100% 100%, 0 100%); }
.logo { filter:drop-shadow(0 6px 16px rgba(0,0,0,.6)); }
.eyebrow { font-weight:800; letter-spacing:.28em; text-transform:uppercase; color:var(--maiz2); text-shadow:0 2px 14px rgba(0,0,0,.9); text-align:center; }
.anton { font-family:Anton, Impact, sans-serif; font-weight:400; text-transform:uppercase; line-height:.98; text-align:center; text-shadow:0 8px 34px rgba(0,0,0,.85); }
.kau { font-family:"Kaushan Script", cursive; color:var(--maiz2); text-align:center; line-height:1.1; -webkit-text-stroke:1.5px rgba(42,0,14,.5); paint-order:stroke fill; text-shadow:0 4px 24px rgba(0,0,0,.9); transform:rotate(-3deg); }
.marco { position:relative; border-radius:28px; overflow:hidden; background:#000;
  box-shadow:0 0 0 7px var(--crema), 0 0 0 15px var(--maiz), 0 30px 70px rgba(0,0,0,.7), 0 0 90px 10px rgba(232,180,58,.25); }
.marco img { width:100%; height:100%; object-fit:cover; display:block; }
.marco--sin { background:radial-gradient(circle at 50% 45%, #3d0014, #1c0009); display:grid; place-items:center; }
.marco--sin img { width:78%; height:auto; opacity:.85; object-fit:contain; filter:drop-shadow(0 0 30px rgba(244,210,122,.35)); }
.marco--sin .kau { position:absolute; bottom:12%; }
.lista { list-style:none; }
.lista li { position:relative; padding-left:1.25em; line-height:1.28; font-weight:600; text-shadow:0 2px 10px rgba(0,0,0,.8); }
.lista li::before { content:"✦"; position:absolute; left:0; color:var(--maiz2); text-shadow:0 0 10px rgba(244,210,122,.9); }
.precio { display:inline-flex; align-items:baseline; gap:.5em; background:var(--vino); border:3px solid var(--maiz); border-radius:18px 46px 18px 46px;
  padding:.35em .9em; box-shadow:0 14px 34px -8px rgba(0,0,0,.7), 0 0 30px rgba(232,180,58,.25); }
.precio small { font-weight:700; letter-spacing:.06em; text-transform:uppercase; color:var(--maiz2); }
.precio b { font-family:Anton, sans-serif; font-weight:400; color:#fff; white-space:nowrap; }
.precio small { white-space:nowrap; }
.pill { display:inline-block; background:var(--maiz); color:var(--vino9); font-weight:800; border-radius:999px; box-shadow:0 14px 34px -8px rgba(232,180,58,.6); }
.cta { font-weight:700; text-align:center; text-shadow:0 2px 12px rgba(0,0,0,.9); }
.cta b { color:var(--maiz2); }
"""


def decoracion(W, H, colgantes, estrellas, copos, semilla=1):
    """Navidad: luces desenfocadas, guirnalda de bombillas, bolas doradas y burdeos de ñandutí colgando de ella,
    copos de ñandutí y destellos. Posiciones deterministas (misma semilla = mismo dibujo)."""
    import math
    def r(n):
        x = math.sin(semilla * 97.3 + n * 31.7) * 43758.5453
        return x - math.floor(x)
    sag = max(46, H * .045)
    gy = lambda x: 14 + sag * abs(math.sin(math.pi * x / (W / 2)))       # dos guirnaldas colgando
    h = []
    for i in range(18):                                                    # luces desenfocadas (bokeh)
        x, y, d = r(i + 600) * W, r(i + 700) * H, 50 + r(i + 800) * 170
        col = ("244,210,122", "255,170,80", "255,236,190", "176,64,95")[i % 4]
        h.append(f'<div class="deco bokeh" style="left:{x - d / 2:.0f}px;top:{y - d / 2:.0f}px;width:{d:.0f}px;height:{d:.0f}px;'
                 f'background:radial-gradient(circle, rgba({col},.5) 0, rgba({col},.18) 45%, rgba({col},0) 70%);opacity:{.35 + r(i + 900) * .5:.2f}"></div>')
    for i in range(copos * 3):                                             # copos de ñandutí nítidos y pequeños
        x, y, d = r(i + 200) * W, 120 + r(i + 300) * (H - 160), 26 + r(i + 400) * 48
        h.append(f'<img class="deco copo" src="img/kv/flor-kv.webp" style="left:{x - d / 2:.0f}px;top:{y - d / 2:.0f}px;width:{d:.0f}px;'
                 f'opacity:{.22 + r(i + 450) * .38:.2f};transform:rotate({r(i + 500) * 360:.0f}deg)">')
    for i in range(estrellas):                                             # destellos
        x, y, d = r(i) * W, 120 + r(i + 50) * (H - 160), 16 + r(i + 90) * 30
        h.append(f'<div class="deco estrella" style="left:{x:.0f}px;top:{y:.0f}px;font-size:{d:.0f}px;opacity:{.35 + r(i + 7) * .6:.2f}">{"✦✧"[i % 5 == 0]}</div>')
    pts = " ".join(f"{x:.0f},{gy(x):.1f}" for x in range(-10, W + 11, 6))   # guirnalda
    h.append(f'<svg class="deco guirnalda" width="{W}" height="{sag + 60:.0f}"><polyline points="{pts}" fill="none" stroke="#f4d27a" stroke-width="2.5" '
             f'style="filter:drop-shadow(0 0 4px rgba(244,210,122,.9))"/></svg>')
    cols = ("#fff3c4", "#f4d27a", "#ffb347", "#fff3c4", "#ffd27a")
    for k, x in enumerate(range(18, W, 54)):
        y, d, c = gy(x) + 4, 11 + (k % 3) * 2, cols[k % len(cols)]
        h.append(f'<div class="deco bombilla" style="left:{x - d / 2}px;top:{y - 2:.0f}px;width:{d}px;height:{d * 1.25:.0f}px;background:{c};'
                 f'box-shadow:0 0 10px 3px {c}, 0 0 26px 8px rgba(255,190,90,.45)"></div>')
    for i, (x, largo, d) in enumerate(colgantes):                          # bolas que cuelgan de la guirnalda
        top = gy(x)
        h.append(f'<div class="deco colg" style="left:{x - d / 2}px;top:{top:.0f}px;width:{d}px;height:{largo + d + 8}px"><span class="hilo"></span><span class="tapa"></span>'
                 f'<span class="bola{" vino" if i % 2 else ""}" style="width:{d}px;height:{d}px"><img src="img/kv/flor-kv.webp"></span></div>')
    return "".join(h)


def pagina(cuerpo, W, H, extra_css="", zoom=None):
    z = f"zoom:{zoom};" if zoom else ""
    return f"""<!doctype html><html><head><meta charset="utf-8"><base href="{R}/">
<link rel="stylesheet" href="css/fuentes.css"><style>{CSS}
.lz {{ width:{W}px; height:{H}px; {z} }} {extra_css}</style></head><body><div class="lz">{cuerpo}</div></body></html>"""


def lista(items, fs, cols=1):
    estilo = f"font-size:{fs}px;" + (f"columns:{cols};column-gap:34px;" if cols > 1 else "")
    return f'<ul class="lista" style="{estilo}">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def marco(c, w, h, pos="50% 62%"):
    if c["foto"]:
        return f'<div class="marco" style="width:{w}px;height:{h}px"><img src="{foto(c)}" style="object-position:{pos}"></div>'
    return (f'<div class="marco marco--sin" style="width:{w}px;height:{h}px"><img src="img/kv/flor-kv.webp">'
            f'<div class="kau" style="font-size:{int(w * .13)}px">quesos y frutas</div></div>')


# ---------- 1. Carrusel 1080×1350 ----------
def portada(W, H, alto):
    fotos = [c for c in COMBOS if c["foto"]]
    f = lambda c: foto(c)
    sy = 1 if alto else 0
    return decoracion(W, H, [(90, 90 + 150 * sy, 84 + 6 * sy), (260, 20 + 110 * sy, 60), (W - 260, 20 + 130 * sy, 64), (W - 90, 110 + 110 * sy, 90 + 6 * sy)], 22, 5, 3) + f"""
<img class="logo" src="img/marca/logo-loren.webp" style="width:{210 if not alto else 260}px;margin-top:{70 if not alto else 290}px">
<div class="eyebrow" style="font-size:30px;margin-top:30px">Nochebuena 24 · Fin de Año 31</div>
<div class="anton" style="font-size:{150 if not alto else 170}px;margin-top:18px">Bocaditos<br>de Navidad</div>
<div class="kau" style="font-size:{92 if not alto else 104}px;margin-top:6px">a la paraguaya</div>
<div style="margin-top:{10 if not alto else 26}px"><span class="cinta" style="font-size:{38 if not alto else 44}px">¡Vy'apavẽ Navidad!</span></div>
<div style="position:relative;width:1000px;height:{430 if not alto else 540}px;margin-top:{26 if not alto else 44}px">
  <div style="position:absolute;left:40px;top:40px;transform:rotate(-8deg)">{marco(COMBOS[2], 330, 400, "50% 50%")}</div>
  <div style="position:absolute;right:40px;top:40px;transform:rotate(8deg)">{marco(COMBOS[0], 330, 400)}</div>
  <div style="position:absolute;left:290px;top:0;z-index:3">{marco(COMBOS[1], 420, {410 if not alto else 500}, "50% 55%")}</div>
</div>
<div style="margin-top:{34 if not alto else 64}px"><span class="pill" style="font-size:38px;padding:20px 50px">Desde 42,90 € · Encarga por WhatsApp</span></div>
"""


def slide_combo(c, W, H, alto, n):
    largo = len(c["items"]) > 5
    if not alto:
        cuerpo = f"""
<img class="logo" src="img/marca/logo-loren.webp" style="width:170px;margin-top:56px">
<div class="eyebrow" style="font-size:26px;margin-top:22px">Navidad y Año Nuevo</div>
<div class="anton" style="font-size:118px;margin-top:10px">{c['titulo']}</div>
<div class="kau" style="font-size:62px">{c['sub']}</div>
<div style="display:flex;gap:44px;align-items:center;margin-top:44px;padding:0 60px;width:100%">
  {marco(c, 470, 620)}
  <div style="flex:1">
    {lista(c['items'], 33 if not largo else 31)}
    <div class="precio" style="margin-top:36px;font-size:30px"><small>{c['cantidad']}</small><b style="font-size:66px">{c['precio']}</b></div>
  </div>
</div>
<div class="cta" style="font-size:31px;margin-top:auto;margin-bottom:58px">Encarga por WhatsApp <b>{WHATSAPP}</b><br><span style="font-size:25px;opacity:.85">{WEB}</span></div>"""
        return decoracion(W, H, [(90, 120, 70), (W - 90, 170, 80)], 18, 4, n + 10) + cuerpo
    cuerpo = f"""
<img class="logo" src="img/marca/logo-loren.webp" style="width:210px;margin-top:270px">
<div class="eyebrow" style="font-size:30px;margin-top:22px">Navidad y Año Nuevo</div>
<div class="anton" style="font-size:136px;margin-top:8px">{c['titulo']}</div>
<div class="kau" style="font-size:70px">{c['sub']}</div>
<div style="margin-top:36px">{marco(c, 600, 560)}</div>
<div style="margin-top:46px;padding:0 90px;width:100%">{lista(c['items'], 34 if not largo else 31, 2 if largo else 1)}</div>
<div class="precio" style="margin-top:34px;font-size:32px"><small>{c['cantidad']}</small><b style="font-size:72px">{c['precio']}</b></div>
<div class="cta" style="font-size:34px;margin-top:40px">Encarga por WhatsApp <b>{WHATSAPP}</b></div>"""
    return decoracion(W, H, [(100, 190, 80), (W - 100, 230, 92)], 24, 5, n + 20) + cuerpo


def slide_encargar(W, H, alto):
    top = 290 if alto else 70
    pasos = [("1", "Elige tu combo", "Combo 1, Combo 2, embutidos o quesos"),
             ("2", "Escríbenos por WhatsApp", f"{WHATSAPP} · dinos el día: 24 o 31 de diciembre"),
             ("3", "Recógelo en el local", "Carrer de la Muntanya 115 · Camp de l'Arpa")]
    p = "".join(f"""<div style="display:flex;gap:30px;align-items:center;margin-top:{38 if alto else 30}px">
      <div style="flex:none;width:96px;height:96px;border-radius:50%;background:var(--maiz);color:var(--vino9);display:grid;place-items:center;font-family:Anton;font-size:58px;box-shadow:0 0 30px rgba(232,180,58,.5)">{n}</div>
      <div><div style="font-family:Anton;text-transform:uppercase;font-size:50px;line-height:1">{t}</div><div style="font-size:28px;font-weight:600;margin-top:8px;opacity:.9">{s}</div></div></div>""" for n, t, s in pasos)
    return decoracion(W, H, [(120, 140 + (200 if alto else 0), 84), (W - 120, 200 + (200 if alto else 0), 96)], 22, 5, 77) + f"""
<img class="logo" src="img/marca/logo-loren.webp" style="width:{180 if not alto else 220}px;margin-top:{top}px">
<div class="anton" style="font-size:{120 if not alto else 136}px;margin-top:26px">¿Cómo lo<br>encargo?</div>
<div class="kau" style="font-size:64px">fácil y sin complicaciones</div>
<div style="margin-top:20px;padding:0 90px;width:100%">{p}</div>
<div style="margin-top:{56 if alto else 46}px"><span class="pill" style="font-size:40px;padding:22px 54px">Encarga con antelación</span></div>
<div class="cta" style="font-size:30px;margin-top:28px">{WEB}</div>"""


# ---------- 3/4. Resumen (WhatsApp, cartel A4, flyer A5) ----------
def fila(c, fs, fw, fh):
    img = (f'<div class="marco" style="width:{fw}px;height:{fh}px;border-radius:18px;flex:none"><img src="{foto(c)}" style="object-position:50% 60%"></div>' if c["foto"]
           else f'<div class="marco marco--sin" style="width:{fw}px;height:{fh}px;border-radius:18px;flex:none"><img src="img/kv/flor-kv.webp" style="width:62%"><div class="kau" style="font-size:{fs * 1.5:.0f}px;bottom:6%">quesos y frutas</div></div>')
    return f"""<div style="display:flex;gap:{fs * 1.4:.0f}px;align-items:center">
  {img}
  <div style="flex:1;min-width:0">
    <div style="display:flex;align-items:baseline;gap:14px;flex-wrap:wrap"><span class="anton" style="font-size:{fs * 2.2:.0f}px;text-align:left">{c['titulo']}</span><span class="kau" style="font-size:{fs * 1.45:.0f}px;display:inline-block">{c['sub']}</span></div>
    <div style="margin-top:{fs * .5:.0f}px">{lista(c['items'], fs, 2)}</div>
    <div style="margin-top:{fs * .6:.0f}px"><span class="precio" style="font-size:{fs * .8:.0f}px;padding:.3em .8em"><small>{c['cantidad']}</small><b style="font-size:{fs * 1.75:.0f}px">{c['precio']}</b></span></div>
  </div>
</div>"""


def resumen(W, H, con_qr, alto_extra=0, fs=21, fw=250, fh=205, fila_gap=26, fila_top=28, pad=60, titulo=92):
    qr_html = (f'<div style="background:#fffdf6;padding:16px;border-radius:18px;box-shadow:0 0 0 5px var(--maiz)"><img src="{qr.as_uri()}" style="width:150px;height:150px;display:block"></div>'
               if con_qr else "")
    return decoracion(W, H, [(80, 80 + alto_extra, 70), (190, 20 + alto_extra * .6, 50), (W - 190, 26 + alto_extra * .6, 54), (W - 80, 100 + alto_extra, 76)], 26, 6, 5) + f"""
<img class="logo" src="img/marca/logo-loren.webp" style="width:{150 if H < 1500 else 190}px;margin-top:{40 + alto_extra}px">
<div class="eyebrow" style="font-size:24px;margin-top:16px">Nochebuena 24 · Fin de Año 31</div>
<div class="anton" style="font-size:{titulo}px;margin-top:8px">Bocaditos de Navidad</div>
<div class="kau" style="font-size:{titulo * .58:.0f}px">a la paraguaya</div>
<div style="display:flex;flex-direction:column;gap:{fila_gap}px;padding:0 {pad}px;margin-top:{fila_top}px;width:100%">
  {''.join(fila(c, fs, fw, fh) for c in COMBOS)}
</div>
<div style="display:flex;align-items:center;gap:34px;margin-top:auto;margin-bottom:{44 + alto_extra}px">
  {qr_html}
  <div class="cta" style="font-size:30px;text-align:{'left' if con_qr else 'center'}">Encarga por WhatsApp{'<br>' if con_qr else ' '}<b style="font-size:{52 if con_qr else 44}px;font-family:Anton;font-weight:400">{WHATSAPP}</b><br>
  <span style="font-size:22px;opacity:.9">Encarga con antelación · Recogida en Carrer de la Muntanya 115</span></div>
</div>"""


def main():
    TMP.mkdir(parents=True, exist_ok=True)
    trabajos = []  # (carpeta, nombre, html, W, H, pdf_mm)
    trabajos.append(("1-instagram-carrusel", "01-portada", pagina(portada(1080, 1350, False), 1080, 1350), 1080, 1350, None))
    trabajos.append(("2-instagram-historias", "01-portada", pagina(portada(1080, 1920, True), 1080, 1920), 1080, 1920, None))
    for n, c in enumerate(COMBOS):
        trabajos.append(("1-instagram-carrusel", f"0{n + 2}-{c['id']}", pagina(slide_combo(c, 1080, 1350, False, n), 1080, 1350), 1080, 1350, None))
        trabajos.append(("2-instagram-historias", f"0{n + 2}-{c['id']}", pagina(slide_combo(c, 1080, 1920, True, n), 1080, 1920), 1080, 1920, None))
    trabajos.append(("1-instagram-carrusel", "06-como-encargar", pagina(slide_encargar(1080, 1350, False), 1080, 1350), 1080, 1350, None))
    trabajos.append(("2-instagram-historias", "06-como-encargar", pagina(slide_encargar(1080, 1920, True), 1080, 1920), 1080, 1920, None))
    trabajos.append(("3-whatsapp", "resumen-1080x1350", pagina(resumen(1080, 1350, False, 0, 19, 215, 165, 12, 16, 50, 78), 1080, 1350), 1080, 1350, None))
    trabajos.append(("3-whatsapp", "estado-1080x1920", pagina(resumen(1080, 1920, False, 200, 21, 240, 200, 22, 26, 56, 92), 1080, 1920), 1080, 1920, None))
    # imprenta: diseño a 1111×1559 px = A4/A5 con 3 mm de sangrado (misma proporción)
    trabajos.append(("4-imprenta", "cartel-A4", pagina(resumen(1111, 1559, True, 10, 20, 240, 185, 16, 20, 70, 88), 1111, 1559), 1111, 1559, (216, 303)))
    trabajos.append(("4-imprenta", "flyer-A5", pagina(resumen(1111, 1559, True, 10, 20, 240, 185, 16, 20, 70, 88), 1111, 1559), 1111, 1559, (154, 216)))
    with sync_playwright() as pw:
        nav = pw.chromium.launch()
        for carpeta, nombre, html, W, H, mm in trabajos:
            d = SAL / carpeta; d.mkdir(parents=True, exist_ok=True)
            f = TMP / f"{carpeta}-{nombre}.html"; f.write_text(html, encoding="utf-8")
            if mm:
                ppp_px = mm[0] / 25.4 * 300 / W       # PNG a 300 ppp
                pg = nav.new_page(viewport={"width": W, "height": H}, device_scale_factor=ppp_px)
            else:
                pg = nav.new_page(viewport={"width": W, "height": H})
            pg.goto(f.as_uri()); pg.wait_for_load_state("networkidle"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
            desborde = pg.evaluate("(() => { const l = document.querySelector('.lz'); const m = Math.max(...[...l.children].filter(e => !e.classList.contains('deco')).map(e => e.getBoundingClientRect().bottom + parseFloat(getComputedStyle(e).marginBottom))); return Math.round(m - l.clientHeight); })()")
            if mm:
                zoom = mm[0] / 25.4 * 96 / W
                pg.evaluate(f"document.querySelector('.lz').style.zoom = {zoom}")
                pg.pdf(path=str(d / f"{nombre}-imprenta.pdf"), width=f"{mm[0]}mm", height=f"{mm[1]}mm", print_background=True)
                pg.evaluate("document.querySelector('.lz').style.zoom = ''")
            tmp_png = TMP / f"{carpeta}-{nombre}.png"
            pg.locator(".lz").screenshot(path=str(tmp_png))
            try:
                shutil.copyfile(tmp_png, d / f"{nombre}.png")
            except OSError:
                print(f"   ⚠ {nombre}.png está abierto en otro programa: ciérralo y vuelve a ejecutar")
            if not mm:  # versión JPG ligera para mandar por WhatsApp / subir
                Image.open(d / f"{nombre}.png").convert("RGB").save(d / f"{nombre}.jpg", quality=92)
                (d / f"{nombre}.png").unlink()
            print(f"{carpeta}/{nombre}" + (f"   ⚠ se sale {desborde} px" if desborde > 0 else ""))
            pg.close()
        nav.close()
    shutil.rmtree(TMP, ignore_errors=True)


if __name__ == "__main__":
    main()
