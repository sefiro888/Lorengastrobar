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
           '  <link rel="stylesheet" href="css/v2.css?v=3">\n  <meta name="robots" content="noindex">\n</head>')

# --- Todas las páginas (menos la carta para imprimir, que se queda igual) ---
for f in glob.glob(os.path.join(V, "*.html")):
    n = os.path.basename(f)
    if n == "carta-clasica.html":
        continue
    cambios = [("</head>", FUENTES), ("</body>", '<script src="js/v2.js?v=2"></script>\n</body>')]
    s = open(f, encoding="utf-8").read()
    if "img/marca/nanduti-aro.webp" in s:
        cambios.append(("img/marca/nanduti-aro.webp", "img/kv/flor-kv.webp"))
    editar(n, cambios)

# --- Inicio: la cocina de Loren (equipo + vídeos), menú del día y dos locales ---
VIDEOS = [("mbeju", "Mbejú", "de la sartén a la mesa"), ("sopa", "Sopa paraguaya", "la sopa que se corta"),
          ("chyryry", "Mandi'ó chyryry", "yuca salteada"), ("vori", "Vorí vorí de ternera", "bolitas recién hechas"),
          ("chipa", "Chipa guazú", "costra dorada del horno")]
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
      <div class="polaroids polaroids--solo rv rv--der">
        <figure class="polaroid polaroid--solo"><img src="img/kv/loren-sarten.webp" alt="Loren mostrando un plato recién hecho" loading="lazy"><figcaption>Loren</figcaption></figure>
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
        <h3>Cambia cada día</h3>
        <ul>
          <li>Primer plato</li>
          <li>Segundo plato</li>
          <li>Postre</li>
          <li>Bebida</li>
        </ul>
        <div class="precios">
          <div><span class="precio">15,90 €</span><small>miércoles a viernes</small></div>
          <div><span class="precio">19,90 €</span><small>sábado y domingo</small></div>
        </div>
      </div>
      <div class="mdd__local">🍽️ Al mediodía, de <b>miércoles a domingo</b></div>
    </div>
    <div class="mdd__der rv rv--der">
      <span class="eyebrow">Al mediodía</span>
      <h2 class="titulo">Comer como en casa <em>a precio de barrio</em></h2>
      <p>Primero, segundo, postre y bebida, cocinados ese mismo día. Entre semana para la pausa del trabajo y el finde para venir en familia.</p>
      <div class="mdd__foto">
        <img src="img/kv/mila-napolitana-nueva.webp" alt="Milanesa con huevo frito y patatas" loading="lazy">
        <img class="flor" src="img/kv/flor-kv.webp" alt="" aria-hidden="true">
      </div>
      <p class="mdd__nota">Los platos cambian cada día: pregúntanos por WhatsApp qué hay hoy.</p>
      <a href="#" class="btn" data-reserva style="margin-top:10px">Preguntar el menú de hoy</a>
    </div>
  </div>
</section>

<!-- ============ FINDE ============ -->'''

editar("index.html", [
    ('<img class="plato__encaje" src="img/kv/flor-kv.webp"', '<img class="plato__encaje plato__encaje--bandera" src="img/kv/nanduti-bandera.webp"'),
    ("<!-- ============ HISTORIA ============ -->", COCINA),
    ("<!-- ============ FINDE ============ -->", MDD),
])

# --- Carta: fotos propias en lugar de las genéricas ---
editar("js/data.js", [
    ('nombre: "Empanada de ternera", precio: 3.80, img: "img/platos/empanada-carne.webp"', 'nombre: "Empanada de ternera", precio: 3.80, img: "img/kv/empanadas-cesta.webp"'),
    ('nombre: "Picada paraguaya", precio: 32.90, img: "img/platos/parrillada-paraguaya.webp"', 'nombre: "Picada paraguaya", precio: 32.90, img: "img/kv/parrillada-kv.webp"'),
    ('nombre: "Milanesa a la napolitana", precio: 17.90, img: "img/platos/hl-milanesa.webp"', 'nombre: "Milanesa a la napolitana", precio: 17.90, img: "img/kv/mila-napolitana-nueva.webp"'),
    ('nombre: "Entrecot de ternera con chorizo", precio: 17.90, img: null', 'nombre: "Entrecot de ternera con chorizo", precio: 17.90, img: "img/kv/entrecot-kv.webp"'),
    ('nombre: "Hamburguesa de ternera completa", precio: 12.90, img: "img/platos/hl-hamburguesa.webp"', 'nombre: "Hamburguesa de ternera completa", precio: 12.90, img: "img/kv/hamburguesa-kv.webp"'),
])

# --- Eventos: las bandejas de bocaditos reales ---
editar("eventos.html", [
    ('<img src="img/local/bandeja-chipas-empanadas.webp" alt="Bandeja de empanadas, croquetas y chipas" loading="lazy">',
     '<img src="img/kv/bocaditos-empanadas.webp" alt="Bandejas de empanadas y croquetas" loading="lazy" style="object-position:50% 45%">'),
    ('<img src="img/local/catering-bandeja.webp" alt="Bandeja de sándwiches de miga y milanesitas" loading="lazy">',
     '<img src="img/kv/bocaditos-sandwiches.webp" alt="Bandejas de sándwiches de miga" loading="lazy" style="object-position:50% 45%">'),
])


# --- Lote 2 de material: fotos reales del local, reportaje de SNT y receta en vídeo ---
editar("js/data.js", [
    ('img: "img/platos/hl-chorizo.webp"', 'img: "img/nuevo/chorizo.webp"'),
    ('nombre: "Ñoquis de ternera", precio: 15.90, img: "img/platos/hl-noquis.webp",\n    desc: "Ñoquis caseros con carne de ternera guisada en su salsa."',
     'nombre: "Ñoquis de ternera", precio: 15.90, img: "img/nuevo/noquis.webp",\n    desc: "Ñoquis caseros con estofado de carne de ternera."'),
    ('nombre: "Yucas bravas", precio: 8.90, img: "img/platos/yuca-brava-pro.webp"', 'nombre: "Yucas bravas", precio: 8.90, img: "img/nuevo/yuca-brava.webp"'),
])
editar("domicilio.html", [('<div class="phero__arco"><img src="img/platos/box-empanadas.webp" alt="Cesta de empanadas caseras"></div>',
                           '<div class="phero__arco"><img src="img/nuevo/loren-empanada.webp" alt="Loren con una empanada recién frita" style="object-position:50% 40%"></div>')])
editar("visitanos.html", [('      <a class="rv" href="#" data-lb="img/local/barra.webp" data-cap="La barra">',
    '      <a class="rv" href="#" data-lb="img/nuevo/jose-terraza.webp" data-cap="José en la terraza"><img src="img/nuevo/jose-terraza.webp" alt="José, camarero, en la terraza" loading="lazy"></a>\n'
    '      <a class="rv" href="#" data-lb="img/nuevo/fanny-jennifer.webp" data-cap="Fanny y Jennifer en la barra"><img src="img/nuevo/fanny-jennifer.webp" alt="Fanny y Jennifer, camareras, en la barra" loading="lazy" style="object-position:50% 30%"></a>\n'
    '      <a class="rv" href="#" data-lb="img/local/barra.webp" data-cap="La barra">')])
editar("historia.html", [
    ('<span class="ini">Je</span></div><h3>Jennifer y el equipo</h3><div class="rol">En sala</div><p>Jennifer, Romina y todo el equipo de sala: los nombres que más se repiten en vuestras reseñas.</p></div>',
     '<img src="img/nuevo/fanny-jennifer.webp" alt="Fanny y Jennifer" style="object-position:50% 26%"></div><h3>Fanny, Jennifer y José</h3><div class="rol">En sala</div><p>Fanny y Jennifer en la barra y José en la terraza: los nombres que más se repiten en vuestras reseñas.</p></div>'),
    ('''    </div>
  </div>
</section>

<!-- VALORES -->''', '''    </div>
    <div class="sala-fotos">
      <figure class="polaroid rv" data-delay="1"><img src="img/nuevo/loren-empanada.webp" alt="Loren con una empanada recién frita" loading="lazy" style="object-position:50% 45%"><figcaption>Loren y sus empanadas</figcaption></figure>
      <figure class="polaroid rv" data-delay="2"><img src="img/nuevo/fanny-jennifer.webp" alt="Fanny y Jennifer en la barra" loading="lazy" style="object-position:50% 28%"><figcaption>Fanny y Jennifer</figcaption></figure>
      <figure class="polaroid rv" data-delay="3"><img src="img/nuevo/jose-terraza.webp" alt="José en la terraza" loading="lazy" style="object-position:50% 40%"><figcaption>José, en la terraza</figcaption></figure>
    </div>
  </div>
</section>

<!-- VALORES -->'''),
    ('<!-- PRENSA -->', '''<!-- SALIMOS EN LA TELE (v2) -->
<section class="sec sec--oscuro tele">
  <div class="wrap tele__grid">
    <figure class="tele__video rv rv--izq">
      <video controls playsinline preload="none" poster="video/snt-loren.jpg" src="video/snt-loren.mp4" aria-label="Fragmento del reportaje de SNT sobre Loren"></video>
      <figcaption>Fragmento del informativo <b>24 Horas de SNT Cerro Corá</b> (Paraguay). Imágenes: SNT.</figcaption>
    </figure>
    <div class="rv rv--der">
      <span class="eyebrow">Salimos en la tele <span class="gn">marandu</span></span>
      <h2 class="titulo">Vive y trabaja lejos, <em>pero no olvida su país</em></h2>
      <p class="lead">El informativo 24 Horas de SNT, la televisión paraguaya, cruzó el océano para contar la historia de Loren: de San José de los Arroyos a Cataluña, diecisiete años lejos de casa y una cocina que sabe exactamente a Paraguay.</p>
      <span class="sc">Una historia de sacrificio y de esperanza</span>
    </div>
  </div>
</section>

<!-- PRENSA -->'''),
])
editar("sabores.html", [('<section class="sec" id="quiz">', '''<section class="sec sec--oscuro receta">
  <div class="wrap receta__grid">
    <div class="rv rv--izq">
      <span class="letrero">Así la hacemos</span>
      <h2 class="titulo" style="margin-top:34px">La chipa guazú, <em>paso a paso</em></h2>
      <p class="lead">Maíz, queso, cebolla y huevos, a mano y al horno hasta que sale la costra dorada. Dale al play con el sonido activado y te lo contamos desde la cocina.</p>
      <a class="btn" href="carta.html#c-paraguayo">Verla en la carta</a>
    </div>
    <figure class="receta__video rv rv--der">
      <video controls playsinline preload="none" poster="video/receta-chipa.jpg" src="video/receta-chipa.mp4" aria-label="Receta de la chipa guazú en la cocina de Loren"></video>
    </figure>
  </div>
</section>

<section class="sec" id="quiz">''')])

# Las letras Anton y Kaushan dibujan «» como «<<»: en la v2 se usan comillas “”
for f in glob.glob(os.path.join(V, "*.html")) + glob.glob(os.path.join(V, "js", "*.js")):
    if f.endswith("i18n.js"):
        continue
    t = open(f, encoding="utf-8").read()
    t2 = t.replace("«", "“").replace("»", "”")
    if t2 != t:
        open(f, "w", encoding="utf-8").write(t2)
print("v2 lista")
