"""Genera navidad.html (página de los combos de Navidad, sólo en español) a partir de herramientas/navidad_datos.py.
Uso: python herramientas/navidad_web.py   (después: git push)
La página se enlaza desde un aviso en Inicio y Eventos que se oculta solo a partir del 1-ene-2027 (data-hasta)."""
import json, pathlib, re, sys, urllib.parse
RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "herramientas"))
from navidad_datos import COMBOS, WHATSAPP, WA_LINK, mensaje_wa

V = re.search(r"\?v=(\d+)", (RAIZ / "index.html").read_text(encoding="utf-8")).group(1)   # misma versión de caché que el resto
URL = "https://lorenrestobar.com/navidad"
wa = lambda texto: WA_LINK + "?text=" + urllib.parse.quote(texto)
TIT = "Bocaditos de Navidad y Fin de Año · Loren Restobar"
DESC = ("Combos de bocaditos paraguayos para Nochebuena y Fin de Año en Barcelona: 50 unidades desde 65 €, tablas de embutidos "
        "y quesos para 8–10 personas. Encarga por WhatsApp y recoge en Carrer de la Muntanya 115.")


def tarjeta(c, i):
    img = (f'<img src="img/navidad/{c["foto"]}.webp" alt="{c["titulo"]} de Navidad: {", ".join(c["items"][:3]).lower()}" loading="lazy" style="object-position:50% 62%">'
           if c["foto"] else '<img src="img/kv/flor-kv.webp" alt="" aria-hidden="true" class="nav-sinfoto">')
    items = "".join(f"<li>{x}</li>" for x in c["items"])
    return f"""      <article class="bandeja-card rv" data-delay="{i % 3 + 1}">
        <div class="bandeja-card__img{' bandeja-card__img--sin' if not c['foto'] else ''}">{img}<span class="pers">{c['cantidad']}</span></div>
        <div class="bandeja-card__body"><h3>{c['titulo']} <small class="nav-sub">{c['sub']}</small></h3>
          <ul>{items}</ul>
          <p class="nav-precio">{c['precio']}</p>
          <a class="btn btn--sm btn--vino" href="{wa(mensaje_wa(c))}" target="_blank" rel="noopener">Encargar este combo</a></div>
      </article>"""


ld = {"@context": "https://schema.org", "@type": "WebPage", "url": URL, "name": TIT, "description": DESC, "inLanguage": "es",
      "about": {"@id": "https://lorenrestobar.com/#restaurante"},
      "mainEntity": {"@type": "OfferCatalog", "name": "Bocaditos de Navidad y Fin de Año", "itemListElement": [
          {"@type": "Offer", "price": c["precio"].replace(" €", "").replace(",", "."), "priceCurrency": "EUR",
           "itemOffered": {"@type": "Product", "name": f"{c['titulo']} · {c['sub']}", "description": ", ".join(c["items"])}} for c in COMBOS]}}

pasos = [("Elige tu combo", "Combo 1, Combo 2, la tabla de embutidos o la de quesos."),
         ("Escríbenos por WhatsApp", f"Al {WHATSAPP}: dinos el combo, la cantidad y el día (24 o 31 de diciembre)."),
         ("Recógelo en el local", "Carrer de la Muntanya 115, Camp de l'Arpa. Encarga con antelación.")]

html = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{TIT}</title>
  <meta name="description" content="{DESC}">
  <link rel="canonical" href="{URL}">
  <meta property="og:title" content="Bocaditos de Navidad a la paraguaya · Loren Restobar">
  <meta property="og:description" content="Nochebuena 24 y Fin de Año 31: combos caseros de bocaditos y tablas para compartir. Encarga por WhatsApp.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{URL}">
  <meta property="og:image" content="https://lorenrestobar.com/img/redes/og-navidad-es.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:locale" content="es_ES">
  <meta property="og:site_name" content="Loren Restobar">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#59011d">
  <link rel="icon" href="img/marca/favicon.webp" type="image/webp">
  <link rel="stylesheet" href="css/styles.css?v={V}">
  <link rel="stylesheet" href="css/paginas.css?v={V}">
  <link rel="preload" href="fuentes/montserrat-latin-e56e84.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="fuentes/anton-latin-a6f395.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="css/fuentes.css?v={V}">
  <link rel="stylesheet" href="css/v2.css?v={V}">
  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body data-page="navidad">
<!-- Generado por herramientas/navidad_web.py: los cambios se hacen en herramientas/navidad_datos.py -->
<div id="shell-top"></div>
<main>

<section class="phero">
  <canvas id="brasas" aria-hidden="true"></canvas><div class="hero__grano"></div>
  <div class="phero__encaje" data-nanduti></div>
  <div class="wrap phero__grid">
    <div>
      <nav class="miga" aria-label="Migas"><a href="index.html">Inicio</a> / <span>Navidad</span></nav>
      <span class="eyebrow">Nochebuena 24 · Fin de Año 31 <span class="gn">vy'a</span></span>
      <h1>Bocaditos de Navidad <em>a la paraguaya</em></h1>
      <p class="phero__txt">Este año, la Nochebuena sabe a Paraguay. En Paraguay no hay fiesta sin bocaditos, y en las mesas de Navidad nunca faltan la chipa y la sopa paraguaya. Te preparamos bandejas caseras para el 24 y el 31 de diciembre, listas para recoger.</p>
      <div class="hero__ctas"><a href="{wa(mensaje_wa())}" target="_blank" rel="noopener" class="btn">Encargar por WhatsApp</a><a href="#combos" class="btn btn--ghost">Ver los combos</a></div>
      <div class="phero__datos">
        <div><b>50</b><span>bocaditos por combo</span></div>
        <div><b>42,90 €</b><span>tablas desde</span></div>
        <div><b>24 · 31</b><span>de diciembre</span></div>
      </div>
    </div>
    <div class="phero__media">
      <div class="phero__arco"><img src="img/navidad/bandeja-variada-combo2.webp" alt="Bandeja de bocaditos paraguayos: sándwiches de miga, empanaditas, chipa guazú, croquetas y milanesitas" style="object-position:50% 55%"></div>
      <div class="phero__chapa"><b>Hecho en casa</b><small>Encarga con antelación · Recogida en Carrer de la Muntanya 115</small></div>
    </div>
  </div>
</section>

<section class="sec" id="combos">
  <div class="wrap">
    <div class="cabecera cabecera--centro">
      <span class="eyebrow rv">Navidad y Año Nuevo</span>
      <h2 class="titulo rv" data-delay="1">Elige tu <em>combo</em></h2>
      <p class="lead rv" data-delay="2">Dos combos de 50 bocaditos y dos tablas para compartir entre 8 y 10 personas. Toca “Encargar” y te abrimos WhatsApp con el pedido ya escrito.</p>
    </div>
    <div class="tres bandejas-grid">
{chr(10).join(tarjeta(c, i) for i, c in enumerate(COMBOS))}
    </div>
    <p class="carta__nota" style="margin-top:22px;text-align:center">⏰ Encarga con antelación · Recogida en el local, Carrer de la Muntanya 115 · WhatsApp {WHATSAPP}</p>
  </div>
</section>

<section class="sec sec--oscuro">
  <div class="wrap">
    <div class="cabecera cabecera--centro">
      <span class="eyebrow rv">Cómo funciona</span>
      <h2 class="titulo rv" data-delay="1">Encargarlo es <em>muy fácil</em></h2>
    </div>
    <div class="pasos nav-pasos">
{chr(10).join(f'      <div class="paso rv" data-delay="{i + 1}"><h3>{t}</h3><p>{p}</p></div>' for i, (t, p) in enumerate(pasos))}
    </div>
  </div>
</section>

<section class="sec sec--vino cta-final">
  <div class="wrap">
    <h2 class="titulo rv">Este año, la Nochebuena <em>sabe a Paraguay</em></h2>
    <p class="lead rv" style="margin:18px auto 0">Escríbenos y te lo dejamos listo para recoger.</p>
    <div class="hero__ctas rv"><a href="{wa(mensaje_wa())}" target="_blank" rel="noopener" class="btn">Encargar por WhatsApp</a><a href="carta.html" class="btn btn--ghost">Ver la carta</a></div>
  </div>
</section>

</main>
<div id="shell-bottom"></div>
<script src="js/data.js?v={V}"></script>
<script src="js/layout.js?v={V}"></script>
<script src="js/cookies.js?v={V}"></script>
<script src="js/nanduti.js?v={V}"></script>
<script src="js/paginas.js?v={V}"></script>
<script src="js/main.js?v={V}"></script>
<script src="js/v2.js?v={V}"></script>
</body>
</html>
"""
(RAIZ / "navidad.html").write_text(html, encoding="utf-8")
print("navidad.html escrito (v=" + V + ")")
