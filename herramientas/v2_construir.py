"""Genera la VERSIÓN 2 (carpeta v2/) a partir de la web actual + el material nuevo.
Copia las páginas, CSS y JS de la versión 1 (sin tocar v2/css/v2.css ni v2/js/v2.js) y les aplica los cambios.
Uso: python herramientas/v2_construir.py   (antes: herramientas/v2_recursos.py para las imágenes y vídeos)
"""
import glob, os, shutil

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = os.path.join(R, "v2")
for f in glob.glob(os.path.join(R, "*.html")):
    shutil.copy(f, V)
for sub in ("css", "js"):
    for f in glob.glob(os.path.join(R, sub, "*.*")):
        shutil.copy(f, os.path.join(V, sub))
for sub in ("clientes", "local", "marca", "platos", "redes"):
    shutil.copytree(os.path.join(R, "img", sub), os.path.join(V, "img", sub), dirs_exist_ok=True)


def editar(f, cambios):
    p = os.path.join(V, f)
    s = open(p, encoding="utf-8").read()
    for a, b in cambios:
        assert a in s, (f, a[:80])
        s = s.replace(a, b)
    open(p, "w", encoding="utf-8").write(s)


FUENTES = ('<link href="https://fonts.googleapis.com/css2?family=Anton&family=Kaushan+Script&family=Montserrat:wght@400;500;600;700;800&display=swap" rel="stylesheet">\n'
           '  <link rel="stylesheet" href="css/v2.css?v=1">\n  <meta name="robots" content="noindex">\n</head>')

# --- Todas las páginas (menos la carta para imprimir, que se queda igual) ---
for f in glob.glob(os.path.join(V, "*.html")):
    n = os.path.basename(f)
    if n == "carta-clasica.html":
        continue
    cambios = [("</head>", FUENTES), ("</body>", '<script src="js/v2.js?v=1"></script>\n</body>')]
    s = open(f, encoding="utf-8").read()
    if "img/marca/nanduti-aro.webp" in s:
        cambios.append(("img/marca/nanduti-aro.webp", "img/kv/flor-kv.webp"))
    editar(n, cambios)

# --- Inicio: la cocina de Loren (equipo + vídeos), menú del día y dos locales ---
VIDEOS = [("mbeju", "Mbejú", "de la sartén a la mesa"), ("sopa", "Sopa paraguaya", "la que se come con tenedor"),
          ("chyryry", "Mandi'ó chyryry", "recién salteado"), ("vori", "Vorí vorí", "bolitas recién hechas"),
          ("chipa", "Chipa guazú", "esponjosa por dentro")]
videos = "\n".join(
    f'      <figure class="video rv" data-delay="{i % 4 + 1}"><video muted loop playsinline preload="none" poster="video/{v}.jpg" src="video/{v}.mp4" aria-label="{t} en la cocina de Loren"></video>'
    f'<span class="vivo">En cocina</span><figcaption><b>{t}</b><span>{s}</span></figcaption></figure>'
    for i, (v, t, s) in enumerate(VIDEOS))

COCINA = f'''<!-- ============ LA COCINA DE LOREN (v2) ============ -->
<section class="cocina" id="cocina">
  <div class="wrap">
    <div class="cocina__cab">
      <div class="rv rv--izq">
        <span class="letrero">La cocina de Loren</span>
        <h2 class="titulo" style="margin-top:34px">Así se hace <em>en casa</em></h2>
        <p>Aquí nada llega precocinado. El mbejú se tuesta en la sartén con mantequilla, la sopa paraguaya sale del horno con su costra dorada y el vorí vorí se sirve con las bolitas recién hechas. Loren y su equipo lo cocinan cada día, como en Paraguay.</p>
        <span class="sc">Hecho cada día, con las manos</span>
      </div>
      <div class="polaroids rv rv--der">
        <figure class="polaroid polaroid--1"><img src="img/kv/equipo.webp" alt="Loren con su equipo de cocina" loading="lazy"><figcaption>El equipo</figcaption></figure>
        <figure class="polaroid polaroid--2"><img src="img/kv/loren-sarten.webp" alt="Loren mostrando un plato recién hecho" loading="lazy"><figcaption>Loren</figcaption></figure>
        <figure class="polaroid polaroid--3"><img src="img/kv/brasero-mesa.webp" alt="Parrillada al brasero en la mesa" loading="lazy"><figcaption>Al brasero</figcaption></figure>
      </div>
    </div>
    <div class="videos">
{videos}
    </div>
  </div>
</section>

<!-- ============ HISTORIA ============ -->'''

MDD = '''<!-- ============ MENÚ DEL DÍA (v2) ============ -->
<section class="mdd" id="menu-del-dia">
  <div class="wrap mdd__grid">
    <div class="mdd__izq rv rv--izq">
      <span class="letrero">Menú del día</span>
      <div class="pergamino">
        <h3>Platos únicos</h3>
        <ul>
          <li>Asado a la olla con arroz quesú</li>
          <li>Milanesa de ternera o de pollo con arroz o ensalada</li>
          <li>Ñoquis con estofado de carne</li>
          <li>Tallarín con estofado de carne</li>
        </ul>
        <span class="precio">11,90 €</span>
        <small>Incluye una bebida</small>
      </div>
      <div class="mdd__local">📍 Exclusivo en el local de <b>Muntanya 115</b></div>
    </div>
    <div class="mdd__der rv rv--der">
      <span class="eyebrow">Entre semana</span>
      <h2 class="titulo">Comer como en casa <em>a precio de barrio</em></h2>
      <p>Un plato único bien servido y una bebida. Perfecto para el mediodía si trabajas o vives por el Camp de l'Arpa.</p>
      <div class="mdd__foto">
        <img src="img/kv/mila-napolitana-nueva.webp" alt="Milanesa con huevo frito y patatas" loading="lazy">
        <img class="flor" src="img/kv/flor-kv.webp" alt="" aria-hidden="true">
      </div>
      <p class="mdd__nota">Los platos pueden cambiar según el día: pregúntanos por WhatsApp qué hay hoy.</p>
      <a href="#" class="btn" data-reserva style="margin-top:10px">Preguntar el menú de hoy</a>
    </div>
  </div>
</section>

<!-- ============ FINDE ============ -->'''

editar("index.html", [
    ("<!-- ============ HISTORIA ============ -->", COCINA),
    ("<!-- ============ FINDE ============ -->", MDD),
    ('<h2 class="titulo">Te esperamos <em>en Muntanya 115</em></h2>',
     '<h2 class="titulo">Te esperamos en <em>nuestros dos locales</em></h2>\n'
     '      <div class="locales">\n'
     '        <div class="local"><span class="n">1</span><div><b>Carrer de la Muntanya, 115</b><small>Camp de l\'Arpa · menú del día · terraza · este es su horario ↓</small></div></div>\n'
     '        <div class="local"><span class="n">2</span><div><b>Carrer de Villarroel, 247</b><small>Eixample · horario por confirmar</small></div></div>\n'
     '      </div>'),
])

# --- Carta: fotos propias en lugar de las genéricas ---
editar("js/data.js", [
    ('nombre: "Sopa paraguaya", precio: 4.40, img: "img/platos/sopa-paraguaya-pro.webp"', 'nombre: "Sopa paraguaya", precio: 4.40, img: "img/kv/sopa-paraguaya-kv.webp"'),
    ('nombre: "Empanada de carne", precio: 4.30, img: "img/platos/empanada-carne.webp"', 'nombre: "Empanada de carne", precio: 4.30, img: "img/kv/empanadas-cesta.webp"'),
    ('nombre: "Parrillada mixta", precio: null, img: "img/platos/parrillada-mixta.webp"', 'nombre: "Parrillada mixta", precio: null, img: "img/kv/parrillada-kv.webp"'),
    ('nombre: "Milanesa de pollo a la napolitana", precio: 18.90, img: "img/platos/mila-pollo-napo.webp"', 'nombre: "Milanesa de pollo a la napolitana", precio: 18.90, img: "img/kv/mila-napolitana-nueva.webp"'),
    ('nombre: "Hamburguesa de ternera completa", precio: 12.90, img: "img/platos/hl-hamburguesa.webp"', 'nombre: "Hamburguesa de ternera completa", precio: 12.90, img: "img/kv/hamburguesa-kv.webp"'),
])

# --- Eventos: las bandejas de bocaditos reales ---
editar("eventos.html", [
    ('<img src="img/local/bandeja-chipas-empanadas.webp" alt="Bandeja de empanadas, croquetas y chipas" loading="lazy">',
     '<img src="img/kv/bocaditos-empanadas.webp" alt="Bandejas de empanadas y croquetas" loading="lazy" style="object-position:50% 45%">'),
    ('<img src="img/local/catering-bandeja.webp" alt="Bandeja de sándwiches de miga y milanesitas" loading="lazy">',
     '<img src="img/kv/bocaditos-sandwiches.webp" alt="Bandejas de sándwiches de miga" loading="lazy" style="object-position:50% 45%">'),
])

# --- Historia: foto del equipo ---
editar("historia.html", [
    ('    <div class="equipo">',
     '    <figure class="polaroid rv" style="position:relative;width:min(520px,92%);margin:0 auto 60px;transform:rotate(-2deg)"><img src="img/kv/equipo.webp" alt="Loren con su equipo de cocina"><figcaption>La familia Loren en la cocina</figcaption></figure>\n    <div class="equipo">'),
])

# --- Pie: los dos locales ---
editar("js/layout.js", [
    ('<li><a href="${P}visitanos.html">Carrer de la Muntanya, 115</a></li><li>08026 Barcelona</li>\n        <li><a href="tel:+34602076828">602 07 68 28</a></li>',
     '<li><a href="${P}visitanos.html">Carrer de la Muntanya, 115</a></li><li><a href="${P}visitanos.html">Carrer de Villarroel, 247</a></li>\n'
     '        <li><a href="tel:+34602076828">602 07 68 28</a></li><li><a href="tel:+34930068665">930 06 86 65</a></li>'),
])
print("v2 lista")
