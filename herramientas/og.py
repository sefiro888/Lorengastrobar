"""
LOREN RESTOBAR · Imágenes para compartir (Open Graph, 1200 × 630)

Uso:  python herramientas/og.py
Genera img/redes/og-<página>-<idioma>.jpg con la línea gráfica de la web
(carbón, encaje de ñandutí, Anton + Kaushan Script, dorado maíz).
herramientas/seo.py las enlaza en cada página (og:image y twitter:image).
"""
import os, pathlib
from playwright.sync_api import sync_playwright

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "img" / "redes"

# página: (foto, encuadre, {idioma: (antetítulo, titular, acento a pincel)})
PAGINAS = {
    "index": ("img/platos/plato-vori.webp", "50% 50%", {
        "es": ("Cocina casera desde 2020", "Restaurante paraguayo", "en Barcelona"),
        "ca": ("Cuina casolana des del 2020", "Restaurant paraguaià", "a Barcelona"),
        "en": ("Homemade cooking since 2020", "Paraguayan restaurant", "in Barcelona")}),
    "carta": ("img/platos/plato-mila-caballo.webp", "50% 50%", {
        "es": ("Precios y pedidos", "La carta", "107 platos y bebidas"),
        "ca": ("Preus i comandes", "La carta", "107 plats i begudes"),
        "en": ("Prices and orders", "The menu", "107 dishes and drinks")}),
    "sabores": ("img/platos/hl-chipa-guazu.webp", "50% 50%", {
        "es": ("Platos típicos y receta", "Comida paraguaya", "explicada"),
        "ca": ("Plats típics i recepta", "Cuina paraguaiana", "explicada"),
        "en": ("Classic dishes and a recipe", "Paraguayan food", "explained")}),
    "historia": ("img/local/loren-chef-vori.webp", "50% 22%", {
        "es": ("De Paraguay a Barcelona", "Nuestra historia", "Loren Vera"),
        "ca": ("Del Paraguai a Barcelona", "La nostra història", "Loren Vera"),
        "en": ("From Paraguay to Barcelona", "Our story", "Loren Vera")}),
    "domicilio": ("img/platos/box-empanadas.webp", "50% 50%", {
        "es": ("Paraguay en tu mesa", "A domicilio", "Glovo · Uber Eats · WhatsApp"),
        "ca": ("El Paraguai a la teva taula", "A domicili", "Glovo · Uber Eats · WhatsApp"),
        "en": ("Paraguay at your table", "Delivery", "Glovo · Uber Eats · WhatsApp")}),
    "eventos": ("img/local/catering-bandeja.webp", "50% 50%", {
        "es": ("Bandejas para compartir", "Eventos y catering", "a la paraguaya"),
        "ca": ("Safates per compartir", "Esdeveniments i càtering", "a la paraguaiana"),
        "en": ("Party platters", "Events and catering", "Paraguayan style")}),
    "visitanos": ("img/platos/hl-fachada.webp", "50% 40%", {
        "es": ("Horario y reservas", "Visítanos", "en Camp de l'Arpa"),
        "ca": ("Horari i reserves", "Visita'ns", "a Camp de l'Arpa"),
        "en": ("Opening hours and bookings", "Visit us", "in Camp de l'Arpa")}),
    "chipa-guazu": ("img/platos/hl-chipa-guazu.webp", "50% 50%", {
        "es": ("Sabores de Paraguay", "Chipa guazú", "qué es y cómo la hacemos"),
        "ca": ("Sabors del Paraguai", "Chipa guazú", "què és i com la fem"),
        "en": ("Flavours of Paraguay", "Chipa guazú", "what it is, how we make it")}),
    "sopa-paraguaya": ("img/platos/sopa-paraguaya.webp", "50% 50%", {
        "es": ("Sabores de Paraguay", "Sopa paraguaya", "la que se come con tenedor"),
        "ca": ("Sabors del Paraguai", "Sopa paraguaiana", "la que es menja amb forquilla"),
        "en": ("Flavours of Paraguay", "Sopa paraguaya", "the one you eat with a fork")}),
    "mbeju": ("img/platos/mbeju-queso.webp", "50% 50%", {
        "es": ("Sabores de Paraguay", "Mbejú", "el queso estira por dentro"),
        "ca": ("Sabors del Paraguai", "Mbejú", "el formatge s'estira per dins"),
        "en": ("Flavours of Paraguay", "Mbejú", "stretchy cheese inside")}),
    "vori-vori": ("img/platos/hl-vori-vori.webp", "50% 50%", {
        "es": ("Sabores de Paraguay", "Vorí vorí", "el caldo de bolitas de maíz"),
        "ca": ("Sabors del Paraguai", "Vorí vorí", "el brou de boletes de blat de moro"),
        "en": ("Flavours of Paraguay", "Vorí vorí", "the corn-dumpling broth")}),
    "empanadas": ("img/platos/empanada-ternera.webp", "50% 50%", {
        "es": ("Cocina casera", "Empanadas paraguayas", "ternera, pollo, jamón y queso, choclo"),
        "ca": ("Cuina casolana", "Empanades paraguaianes", "vedella, pollastre, pernil i formatge, choclo"),
        "en": ("Homemade cooking", "Paraguayan empanadas", "beef, chicken, ham and cheese, corn")}),
}

PLANTILLA = """<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="{raiz}/css/fuentes.css">
<style>
  * {{ box-sizing: border-box; margin: 0; }}
  html, body {{ width: 1200px; height: 630px; overflow: hidden; }}
  body {{ background: #151012 url("{raiz}/img/kv/textura-oscura.webp") center / cover; position: relative; font-family: Montserrat, sans-serif; color: #f3eedc; }}
  .luz {{ position: absolute; inset: 0; background: radial-gradient(60% 80% at 78% 50%, rgba(255,138,42,.22), transparent 60%), linear-gradient(90deg, rgba(21,16,18,.92) 0%, rgba(21,16,18,.55) 55%, rgba(21,16,18,.2) 100%); }}
  .disco {{ position: absolute; right: 70px; top: 50%; width: 430px; height: 430px; translate: 0 -50%; }}
  .disco .enc {{ position: absolute; inset: -70px; width: calc(100% + 140px); height: calc(100% + 140px); object-fit: contain; rotate: 12deg;
                 filter: drop-shadow(0 0 40px rgba(255,130,40,.25)) drop-shadow(0 30px 50px rgba(0,0,0,.6)); }}
  .disco .foto {{ position: absolute; inset: 34px; border-radius: 50%; overflow: hidden; box-shadow: 0 0 0 6px rgba(232,180,58,.9), 0 30px 60px rgba(0,0,0,.6); }}
  .disco .foto img {{ width: 100%; height: 100%; object-fit: cover; object-position: {encuadre}; }}
  .txt {{ position: absolute; left: 72px; top: 70px; width: 610px; }}
  .logo {{ height: 92px; filter: drop-shadow(0 6px 16px rgba(0,0,0,.5)); }}
  .eyebrow {{ margin-top: 40px; display: flex; align-items: center; gap: 14px; font-weight: 700; font-size: 19px; letter-spacing: .22em; text-transform: uppercase; color: #e8b43a; }}
  .eyebrow::before {{ content: ""; width: 42px; height: 2px; background: currentColor; }}
  h1 {{ margin-top: 16px; font-family: Anton, Impact, sans-serif; font-weight: 400; text-transform: uppercase; font-size: {tam}px; line-height: 1; letter-spacing: .01em; text-shadow: 0 6px 24px rgba(0,0,0,.5); }}
  .sc {{ display: inline-block; margin-top: 10px; font-family: "Kaushan Script", cursive; color: #e8b43a; font-size: {tam_sc}px; transform: rotate(-3deg); transform-origin: left; text-shadow: 0 6px 24px rgba(0,0,0,.5); white-space: nowrap; }}
  .pie {{ position: absolute; left: 72px; bottom: 44px; font-size: 19px; font-weight: 600; letter-spacing: .04em; color: rgba(243,238,220,.82); }}
  .pie b {{ color: #e8b43a; font-weight: 700; }}
  .bandera {{ position: absolute; left: 0; right: 0; bottom: 0; height: 12px; background: linear-gradient(#d52b1e 0 33.3%, #f3eedc 33.3% 66.6%, #0038a8 66.6%); }}
</style></head><body>
  <div class="luz"></div>
  <div class="disco"><img class="enc" src="{raiz}/img/kv/flor-kv.webp"><div class="foto"><img src="{raiz}/{foto}"></div></div>
  <div class="txt">
    <img class="logo" src="{raiz}/img/marca/logo-loren.webp">
    <div class="eyebrow">{eyebrow}</div>
    <h1>{titular}</h1>
    <div class="sc">{acento}</div>
  </div>
  <div class="pie"><b>lorenrestobar.com</b> · Carrer de la Muntanya 115 · Barcelona</div>
  <div class="bandera"></div>
</body></html>"""


def main():
    raiz = RAIZ.as_uri()
    tmp = RAIZ / "herramientas" / "_og_tmp.html"
    with sync_playwright() as pw:
        nav = pw.chromium.launch()
        pg = nav.new_page(viewport={"width": 1200, "height": 630})
        try:
            for p, (foto, encuadre, textos) in PAGINAS.items():
                for lang, (eyebrow, titular, acento) in textos.items():
                    n = len(titular)
                    tam = 104 if n <= 12 else 92 if n <= 18 else 80 if n <= 22 else 70
                    tam_sc = 64 if len(acento) <= 16 else 50 if len(acento) <= 22 else 42
                    tmp.write_text(PLANTILLA.format(raiz=raiz, foto=foto, encuadre=encuadre, eyebrow=eyebrow, titular=titular,
                                                    acento=acento, tam=tam, tam_sc=tam_sc), encoding="utf-8")
                    pg.goto(tmp.as_uri()); pg.wait_for_load_state("networkidle"); pg.evaluate("document.fonts.ready")
                    ancho = pg.evaluate("document.querySelector('h1').scrollWidth")
                    if ancho > 620:  # titular demasiado largo: se reduce hasta que quepa
                        pg.evaluate(f"document.querySelector('h1').style.fontSize = '{int(tam * 610 / ancho)}px'")
                    destino = SALIDA / f"og-{p}-{lang}.jpg"
                    pg.screenshot(path=str(destino), type="jpeg", quality=86)
                    print(destino.relative_to(RAIZ), round(destino.stat().st_size / 1024), "KB")
        finally:
            nav.close()
            tmp.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
