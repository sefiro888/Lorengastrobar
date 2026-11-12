"""
LOREN RESTOBAR · Material para pedir reseñas en Google

Uso:  python herramientas/resenas.py
Genera en para-loren/resenas/:
  - cartel-mesa-A6      (105 × 148 mm)  → PDF de imprenta con 3 mm de sangrado + PNG 300 ppp
  - pegatina-redonda-8cm (Ø 80 mm)      → PDF con sangrado + PNG
  - tarjetita-85x55     (85 × 55 mm)    → PDF con sangrado + PNG
  - presentacion.jpg    (los tres juntos, para enseñar)
El QR apunta a https://lorenrestobar.com/resena/ (página de la web que redirige a Google),
así los impresos siguen sirviendo aunque cambie el enlace de Google.
"""
import pathlib
import segno
from playwright.sync_api import sync_playwright
from PIL import Image, ImageFilter, ImageDraw

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SAL = RAIZ / "para-loren" / "resenas"
URL_QR = "https://lorenrestobar.com/resena/"
SANGRE = 3  # mm
PPP = 300

SAL.mkdir(parents=True, exist_ok=True)
segno.make(URL_QR, error="h").save(str(SAL / "qr-resena.svg"), scale=10, border=0, dark="#2a000e", light=None)

R = RAIZ.as_uri()
ESTRELLAS = "★★★★★"

BASE_CSS = f"""
@import url("{R}/css/fuentes.css");
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
:root {{ --carbon: #151012; --vino: #59011d; --vino-9: #2a000e; --crema: #f3eedc; --maiz: #e8b43a; --rojo: #d52b1e; --azul: #0038a8; }}
html, body {{ background: transparent; }}
body {{ font-family: Montserrat, sans-serif; color: var(--crema); -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.pieza {{ position: relative; overflow: hidden; background: var(--carbon) url("{R}/img/kv/textura-oscura.webp") center / cover; }}
.pieza::before {{ content: ""; position: absolute; inset: 0; background: radial-gradient(70% 55% at 50% 52%, rgba(255,138,42,.25), transparent 70%); }}
.anton {{ font-family: Anton, Impact, sans-serif; font-weight: 400; text-transform: uppercase; letter-spacing: .01em; line-height: 1; }}
.script {{ font-family: "Kaushan Script", cursive; color: var(--maiz); }}
.flor {{ position: absolute; object-fit: contain; filter: drop-shadow(0 0 6mm rgba(255,130,40,.25)) drop-shadow(0 3mm 5mm rgba(0,0,0,.55)); }}
.placa {{ position: absolute; background: #fffdf6; border-radius: 4mm; box-shadow: 0 0 0 .9mm var(--maiz), 0 3mm 8mm rgba(0,0,0,.55); }}
.placa img {{ position: absolute; inset: 0; margin: auto; display: block; }}
.estrellas {{ color: var(--maiz); letter-spacing: .6mm; }}
.bandera {{ position: absolute; left: 0; right: 0; bottom: 0; --f: 1mm; background: linear-gradient(var(--rojo) 0 var(--f), #f3eedc var(--f) calc(var(--f) * 2), var(--azul) calc(var(--f) * 2)); }}
.centro {{ position: absolute; left: 0; right: 0; text-align: center; }}
"""

# ---------- 1. Cartel de mesa A6 ----------
W, H = 105 + 2 * SANGRE, 148 + 2 * SANGRE
cartel = f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE_CSS}
@page {{ size: {W}mm {H}mm; margin: 0; }}
.pieza {{ width: {W}mm; height: {H}mm; }}
.logo {{ position: absolute; left: 50%; top: {SANGRE + 7}mm; width: 38mm; translate: -50% 0; filter: drop-shadow(0 1mm 2mm rgba(0,0,0,.5)); }}
.eyebrow {{ top: {SANGRE + 29.5}mm; font-weight: 700; font-size: 2.6mm; letter-spacing: .9mm; color: var(--maiz); }}
.tit {{ top: {SANGRE + 35}mm; font-size: 11mm; }}
.sub {{ top: {SANGRE + 46.5}mm; font-size: 7.4mm; transform: rotate(-3deg); }}
.flor {{ width: 74mm; height: 74mm; left: 50%; top: {SANGRE + 53}mm; translate: -50% 0; }}
.placa {{ width: 50mm; height: 50mm; left: 50%; top: {SANGRE + 65}mm; translate: -50% 0; }}
.placa img {{ width: 41mm; height: 41mm; }}
.estrellas {{ top: {SANGRE + 118}mm; font-size: 5.4mm; }}
.esc {{ top: {SANGRE + 125.5}mm; font-size: 2.9mm; font-weight: 700; }}
.idiomas {{ top: {SANGRE + 130}mm; font-size: 2.35mm; font-weight: 600; opacity: .75; }}
.gracias {{ top: {SANGRE + 134}mm; font-size: 4.6mm; }}
.web {{ top: {SANGRE + 140.3}mm; font-size: 2.4mm; font-weight: 700; letter-spacing: .5mm; opacity: .85; }}
.bandera {{ height: {SANGRE + 3.3}mm; --f: 1.1mm; }}
</style></head><body>
<div class="pieza">
  <img class="logo" src="{R}/tarjeta/logo-hd.png">
  <div class="centro eyebrow">TU OPINIÓN NOS AYUDA MUCHO</div>
  <div class="centro anton tit">¿Te ha gustado?</div>
  <div class="centro script sub">¡Cuéntalo en Google!</div>
  <img class="flor" src="{R}/img/kv/flor-kv.webp">
  <div class="placa"><img src="{SAL.as_uri()}/qr-resena.svg"></div>
  <div class="centro estrellas">{ESTRELLAS}</div>
  <div class="centro esc">Escanea con la cámara del móvil · 1 minuto</div>
  <div class="centro idiomas">Deixa'ns la teva ressenya · Leave us a review</div>
  <div class="centro script gracias">Aguyje! <span style="font-family:Montserrat;font-size:2.5mm;color:var(--crema);opacity:.8">gracias, en guaraní</span></div>
  <div class="centro web">LORENRESTOBAR.COM · CARRER DE LA MUNTANYA 115</div>
  <div class="bandera"></div>
</div></body></html>"""

# ---------- 2. Pegatina redonda Ø 80 mm ----------
D = 80 + 2 * SANGRE
pegatina = f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE_CSS}
@page {{ size: {D}mm {D}mm; margin: 0; }}
.pieza {{ width: {D}mm; height: {D}mm; border-radius: 50%; }}
.aro {{ position: absolute; inset: {SANGRE + 2.2}mm; border-radius: 50%; border: .5mm solid rgba(232,180,58,.7); }}
.flor {{ width: 62mm; height: 62mm; left: 50%; top: 50%; translate: -50% -50%; opacity: .9; }}
.placa {{ width: 36mm; height: 36mm; left: 50%; top: 50%; translate: -50% -47%; border-radius: 3mm; box-shadow: 0 0 0 .7mm var(--maiz), 0 2mm 5mm rgba(0,0,0,.55); }}
.placa img {{ width: 30mm; height: 30mm; }}
svg.arcos {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
svg text {{ fill: var(--crema); }}
</style></head><body>
<div class="pieza">
  <div class="aro"></div>
  <img class="flor" src="{R}/img/kv/flor-kv.webp">
  <div class="placa"><img src="{SAL.as_uri()}/qr-resena.svg"></div>
  <svg class="arcos" viewBox="0 0 {D} {D}">
    <defs>
      <path id="arriba" d="M {D/2 - 31.5},{D/2} a 31.5,31.5 0 0 1 63,0"/>
      <path id="abajo" d="M {D/2 - 34.6},{D/2} a 34.6,34.6 0 0 0 69.2,0"/>
    </defs>
    <text font-family="Anton" font-size="6.4" letter-spacing=".35" text-anchor="middle"><textPath href="#arriba" startOffset="50%">DÉJANOS TU RESEÑA</textPath></text>
    <text font-family="Montserrat" font-weight="700" font-size="3" letter-spacing=".5" text-anchor="middle" style="fill:#e8b43a"><textPath href="#abajo" startOffset="50%">★★★★★  EN GOOGLE  ·  AGUYJE!</textPath></text>
  </svg>
</div></body></html>"""

# ---------- 3. Tarjetita 85 × 55 mm ----------
TW, TH = 85 + 2 * SANGRE, 55 + 2 * SANGRE
tarjetita = f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE_CSS}
@page {{ size: {TW}mm {TH}mm; margin: 0; }}
.pieza {{ width: {TW}mm; height: {TH}mm; }}
.pieza::before {{ background: radial-gradient(60% 90% at 76% 50%, rgba(255,138,42,.28), transparent 70%); }}
.izq {{ position: absolute; left: {SANGRE + 6}mm; top: {SANGRE + 5}mm; width: 42mm; }}
.logo {{ width: 23mm; filter: drop-shadow(0 .6mm 1.2mm rgba(0,0,0,.5)); }}
.tit {{ margin-top: 3mm; font-size: 5.2mm; white-space: nowrap; }}
.sub {{ display: inline-block; margin-top: 1.2mm; font-size: 4.6mm; transform: rotate(-3deg); }}
.txt {{ margin-top: 2.6mm; font-size: 2.35mm; font-weight: 600; line-height: 1.35; opacity: .9; }}
.estrellas {{ margin-top: 1.6mm; font-size: 3.2mm; }}
.flor {{ width: 40mm; height: 40mm; right: {SANGRE + 0.5}mm; top: 50%; translate: 0 -50%; }}
.placa {{ width: 27mm; height: 27mm; right: {SANGRE + 7}mm; top: 50%; translate: 0 -50%; border-radius: 2.5mm; box-shadow: 0 0 0 .6mm var(--maiz), 0 1.6mm 4mm rgba(0,0,0,.55); }}
.placa img {{ width: 22.5mm; height: 22.5mm; }}
.bandera {{ height: {SANGRE + 2.4}mm; --f: .8mm; }}
</style></head><body>
<div class="pieza">
  <div class="izq">
    <img class="logo" src="{R}/tarjeta/logo-hd.png">
    <div class="anton tit">¿Te ha gustado?</div>
    <div class="script sub">Aguyje!</div>
    <div class="txt">Escanea y déjanos tu reseña<br>en Google. ¡Nos ayuda muchísimo!</div>
    <div class="estrellas">{ESTRELLAS}</div>
  </div>
  <img class="flor" src="{R}/img/kv/flor-kv.webp">
  <div class="placa"><img src="{SAL.as_uri()}/qr-resena.svg"></div>
  <div class="bandera"></div>
</div></body></html>"""

PIEZAS = [("cartel-mesa-A6", cartel, W, H), ("pegatina-redonda-8cm", pegatina, D, D), ("tarjetita-85x55", tarjetita, TW, TH)]
MM = 96 / 25.4


def main():
    with sync_playwright() as pw:
        nav = pw.chromium.launch()
        for nombre, html, w, h in PIEZAS:
            f = SAL / f"{nombre}.html"
            f.write_text(html, encoding="utf-8")
            pg = nav.new_page(viewport={"width": round(w * MM), "height": round(h * MM)}, device_scale_factor=PPP / 96)
            pg.goto(f.as_uri()); pg.wait_for_load_state("networkidle"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(400)
            pg.pdf(path=str(SAL / f"{nombre}-imprenta.pdf"), width=f"{w}mm", height=f"{h}mm", print_background=True)
            pg.locator(".pieza").screenshot(path=str(SAL / f"{nombre}.png"), omit_background=True)
            pg.close()
            print(nombre, f"{w}×{h} mm con sangrado")
        nav.close()
    presentacion()


def presentacion():
    """Los tres diseños sobre fondo oscuro, con sombra, para enseñar."""
    fondo = Image.open(RAIZ / "img/kv/textura-oscura.webp").convert("RGB").resize((2400, 1500))
    fondo = Image.blend(fondo, Image.new("RGB", fondo.size, (21, 16, 18)), 0.35)
    def recorte(nombre, ancho_mm, alto_mm, w_px, redondo=False):
        im = Image.open(SAL / f"{nombre}.png").convert("RGBA")
        s = SANGRE * PPP / 25.4  # quitar el sangrado para la vista previa
        im = im.crop((round(s), round(s), round(im.width - s), round(im.height - s)))
        if redondo:
            m = Image.new("L", im.size, 0); ImageDraw.Draw(m).ellipse((0, 0, im.width, im.height), fill=255); im.putalpha(m)
        else:
            m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width, im.height), radius=round(im.width * .015), fill=255); im.putalpha(m)
        return im.resize((w_px, round(w_px * im.height / im.width)), Image.LANCZOS)
    piezas = [(recorte("cartel-mesa-A6", 105, 148, 760), (170, 150)),
              (recorte("pegatina-redonda-8cm", 80, 80, 620, True), (1080, 130)),
              (recorte("tarjetita-85x55", 85, 55, 820), (1000, 860))]
    for im, (x, y) in piezas:
        sombra = Image.new("RGBA", (im.width + 120, im.height + 120), (0, 0, 0, 0))
        sombra.paste((0, 0, 0, 170), (60, 80, 60 + im.width, 80 + im.height), im.split()[3])
        sombra = sombra.filter(ImageFilter.GaussianBlur(28))
        fondo.paste(sombra, (x - 60, y - 60), sombra)
        fondo.paste(im, (x, y), im)
    d = ImageDraw.Draw(fondo)
    fondo.save(SAL / "presentacion.jpg", quality=90)
    print("presentacion.jpg")


if __name__ == "__main__":
    main()
