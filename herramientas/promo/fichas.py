"""Fichas de grabación para Loren (imágenes 1080x1920 para WhatsApp, estilo de la web).
Uso: python herramientas/promo/fichas.py        (servidor local en el puerto 8123)  → para-loren/fichas/*.png"""
import os, html
from playwright.sync_api import sync_playwright
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
SAL = os.path.join(RAIZ, "para-loren", "fichas"); os.makedirs(SAL, exist_ok=True)
e = html.escape

CSS = '''
:root{--vino:#59011d;--vino9:#2a000e;--vino5:#7d0b2e;--crema:#f3eedc;--maiz:#e8b43a;--maiz2:#f4d27a;--carbon:#151012}
*{box-sizing:border-box;margin:0;padding:0}html,body{width:1080px;background:#000}
#f{position:relative;width:1080px;min-height:1920px;padding-bottom:120px;overflow:hidden;font-family:Montserrat,sans-serif;color:var(--crema);background:var(--carbon) url("../../img/kv/textura-oscura.webp") center/cover}
#f::before{content:"";position:absolute;inset:0;background:linear-gradient(rgba(21,16,18,.7),rgba(21,16,18,.7)),radial-gradient(80% 45% at 50% 12%,rgba(125,11,46,.8),transparent 70%)}
.flor{position:absolute;right:-380px;top:-330px;width:980px;height:980px;object-fit:contain;opacity:.16}
.c{position:relative;padding:0 64px}
.top{position:relative;padding:70px 64px 0;display:flex;align-items:center;gap:26px}
.num{width:150px;height:150px;border-radius:50%;background:var(--maiz);color:var(--vino9);display:grid;place-items:center;font-family:Anton;font-size:100px;line-height:1;flex:none;box-shadow:0 16px 40px -8px rgba(232,180,58,.55)}
.top .ey{font-weight:800;font-size:30px;letter-spacing:.26em;text-transform:uppercase;color:var(--maiz2)}
h1{font-family:Anton;font-weight:400;text-transform:uppercase;font-size:86px;line-height:1;margin-top:8px}
h1 span{color:var(--maiz)}
.para{position:relative;padding:26px 64px 0;font-size:38px;line-height:1.3;font-weight:500}
.chips{position:relative;padding:26px 64px 0;display:flex;gap:16px}
.chip{background:rgba(243,238,220,.12);border:2px solid rgba(232,180,58,.7);border-radius:60px;padding:14px 30px;font-weight:800;font-size:32px}
.chip b{color:var(--maiz2)}
.caja{position:relative;margin:30px 64px 0;background:rgba(243,238,220,.08);border-left:10px solid var(--maiz);border-radius:0 28px 28px 0;padding:24px 34px;font-size:33px;line-height:1.32}
.caja h3{font-family:Anton;font-weight:400;font-size:40px;text-transform:uppercase;color:var(--maiz2);margin-bottom:8px;letter-spacing:.04em}
.caja li{margin-left:34px;margin-bottom:4px}
.pasos{position:relative;margin:30px 64px 0;display:flex;flex-direction:column;gap:14px}
.row{display:flex;gap:22px;align-items:stretch;background:var(--crema);color:var(--vino9);border-radius:28px;padding:20px 26px;box-shadow:0 18px 40px -22px rgba(0,0,0,.9)}
.row.g{background:var(--maiz);}
.row .n{width:70px;height:70px;border-radius:50%;background:var(--vino);color:var(--crema);display:grid;place-items:center;font-family:Anton;font-size:44px;flex:none;align-self:center}
.row.g .n{background:var(--vino9)}
.row .t{flex:1;font-size:32px;line-height:1.25}
.row .t b{font-weight:800;letter-spacing:.04em}
.row .t i{font-style:normal;font-weight:700;color:var(--vino5)}
.row.g .t i{color:var(--vino9)}
.row .s{width:120px;text-align:center;align-self:center;font-family:Anton;font-size:46px;line-height:1;color:var(--vino)}
.row .s small{display:block;font-family:Montserrat;font-weight:800;font-size:20px;letter-spacing:.1em;color:#6b5458;margin-top:2px}
.pie{position:relative;margin:26px 64px 0;display:flex;gap:18px}
.pie div{flex:1;background:var(--vino);border:3px solid var(--maiz);border-radius:26px;padding:20px 26px;font-size:30px;line-height:1.28}
.pie b{display:block;font-family:Anton;font-weight:400;font-size:34px;color:var(--maiz2);text-transform:uppercase;letter-spacing:.04em;margin-bottom:4px}
.marca{position:absolute;left:0;right:0;bottom:36px;text-align:center;font-weight:800;font-size:28px;letter-spacing:.2em;text-transform:uppercase;color:rgba(243,238,220,.7)}
.regla{display:flex;gap:26px;align-items:center;margin:0 0 20px;font-size:38px;line-height:1.25;font-weight:600}
.regla .n{width:84px;height:84px;border-radius:50%;background:var(--maiz);color:var(--vino9);display:grid;place-items:center;font-family:Anton;font-size:54px;flex:none}
.regla b{color:var(--maiz2)}
'''

def pagina(cuerpo):
    return f'<!doctype html><html lang="es"><head><meta charset="utf-8"><link rel="stylesheet" href="../../css/fuentes.css"><style>{CSS}</style></head><body><div id="f"><img class="flor" src="../../img/kv/flor-kv.webp" alt="">{cuerpo}<div class="marca">Loren Restobar · fichas de grabación</div></div></body></html>'

def ficha(num, ey, titulo, resalte, para, dur, graba, necesitas, pasos, gancho, cierre, evita):
    filas = ""
    for k, (tipo, ensena, di, seg) in enumerate(pasos, 1):
        di_html = f'<br><i>DI:</i> «{e(di)}»' if di else '<br><i>SIN VOZ:</i> deja el sonido real'
        etiqueta = {"g": "GANCHO · ", "k": "PLANO CLAVE · ", "c": "CIERRE · "}.get(tipo, "")
        filas += (f'<div class="row{" g" if tipo in "gkc" else ""}"><div class="n">{k}</div>'
                  f'<div class="t"><b>{etiqueta}ENSEÑA:</b> {e(ensena)}{di_html}</div>'
                  f'<div class="s">{seg}<small>SEG.</small></div></div>')
    nec = "".join(f"<li>{e(n)}</li>" for n in necesitas)
    return pagina(f'''<div class="top"><div class="num">{num}</div><div><div class="ey">{e(ey)}</div><h1>{e(titulo)} <span>{e(resalte)}</span></h1></div></div>
<div class="para">{e(para)}</div>
<div class="chips"><div class="chip">Vídeo final <b>{e(dur)}</b></div><div class="chip">Grabar: <b>{e(graba)}</b></div></div>
<div class="caja"><h3>Necesitas</h3><ul>{nec}</ul></div>
<div class="pasos">{filas}</div>
<div class="pie"><div><b>Cierre</b>{e(cierre)}</div><div><b>Evita</b>{e(evita)}</div></div>''')

reglas = pagina('''<div class="top"><div class="num" style="font-size:80px">★</div><div><div class="ey">Para todos los vídeos</div><h1>8 reglas <span>de oro</span></h1></div></div>
<div class="para">Léelas una vez y ya sirven para siempre. Con esto, el 90 % del vídeo sale bien.</div>
<div class="c" style="margin-top:40px">
<div class="regla"><div class="n">1</div><div><b>Móvil en vertical</b>, a la altura de los ojos, y limpia la lente con un paño.</div></div>
<div class="regla"><div class="n">2</div><div><b>Luz de frente</b> o de ventana. Nunca con la ventana a tu espalda.</div></div>
<div class="regla"><div class="n">3</div><div><b>Apaga el extractor</b> y la música cuando hables.</div></div>
<div class="regla"><div class="n">4</div><div><b>Graba cada plano 3 veces.</b> Siempre sale una buena.</div></div>
<div class="regla"><div class="n">5</div><div>Quédate <b>quieta 3 segundos</b> antes y después de cada plano.</div></div>
<div class="regla"><div class="n">6</div><div>Usa los <b>3 planos</b>: general (el sitio), detalle (manos y comida) y cara.</div></div>
<div class="regla"><div class="n">7</div><div><b>Sin zoom con los dedos:</b> acerca el móvil tú, a 20 cm de la comida.</div></div>
<div class="regla"><div class="n">8</div><div>Mándame todo <b>sin editar y como «documento»</b> en WhatsApp, para que no se comprima. Yo pongo textos, música y cierre.</div></div>
</div>
<div class="pie" style="margin-top:20px"><div><b>Recuerda</b>Si dudas, graba de más. Siempre es mejor tener material que no tenerlo.</div></div>''')

f1 = ficha("1", "Receta · la más importante", "La empanada de", "jamón y queso",
           "Enseñar cómo se hace y que a todo el mundo le dé hambre con el queso que se estira. La graba Griselda.",
           "30–35 s", "15 minutos",
           ["Guantes y delantal limpios", "Todos los ingredientes ya preparados sobre la mesa", "Móvil en vertical, lente limpia, luz de frente", "Alguien que sostenga el móvil (o un apoyo fijo)"],
           [("g", "tu cara, sonriendo, con una empanada recién hecha en la mano", "Mira cómo hacemos la empanada de jamón y queso", 3),
            ("n", "los ingredientes sobre la mesa, vistos desde arriba", "Jamón en cubitos y queso", 4),
            ("n", "la masa: las manos amasando o estirando con el rodillo", "", 4),
            ("n", "poner el relleno en el centro de la masa, bien cerca", "Bien cargadita", 4),
            ("n", "cerrar la empanada con las manos o con el rodillo", "La cerramos a mano", 4),
            ("n", "la empanada entrando en el aceite caliente, muy cerca", "", 4),
            ("k", "PARTIR la empanada y estirar el queso, lento, cerca del móvil", "¡Mira ese queso!", 6)],
           "", "Te esperamos en Loren Restobar", "Tapar la lente con la mano; hablar con el extractor encendido")

f2 = ficha("2", "Sin hablar · sólo imágenes y sonido", "Del fuego", "a la mesa",
           "Planos muy cerca de la comida, con su sonido real. Es lo que más engancha y no hay que decir nada.",
           "20–25 s", "15 minutos",
           ["Los platos recién hechos (aprovecha cuando salgan del servicio)", "Móvil a 15–20 cm de la comida, fijo o moviéndose muy despacio", "Cocina en silencio: sin música ni extractor"],
           [("g", "el chisporroteo de la sartén del mandi'ó chyryry", "", 3),
            ("n", "la parrilla con humo, o la carne dándose la vuelta", "", 3),
            ("n", "la cuchara entrando en el vorí vorí humeante", "", 3),
            ("n", "la chipa guazú recién sacada del horno, dorada", "", 3),
            ("n", "el mbejú abriéndose, con el queso que estira", "", 3),
            ("n", "yuca frita saliendo de la freidora", "", 3),
            ("k", "el plato terminado sobre el mármol, desde arriba, y una mano que lo coge", "", 4)],
           "", "Lo pongo yo: música y el cartel final", "Cambiar de plato sin esperar: si hoy no hay vorí vorí, graba otro")

f3 = ficha("3", "Las personas · una ficha por persona", "Conoce", "al equipo",
           "Cada persona del equipo se presenta en 20 segundos. Da confianza y gusta mucho. Antes, pídele permiso.",
           "20 s", "5 minutos cada una",
           ["Un fondo bonito: la barra, la pared verde o la terraza", "Alguien que haga las preguntas desde fuera de cámara", "Que la persona mire al móvil y sonría", "El permiso de la persona para publicarlo"],
           [("g", "la persona a cámara, de pie", "Hola, soy ___ y trabajo en Loren Restobar", 3),
            ("n", "su cara, relajada", "Mi plato favorito de la carta es…", 5),
            ("n", "su cara, relajada", "La palabra en guaraní que más me gusta es…", 5),
            ("n", "su cara, relajada", "Lo que más me gusta de trabajar aquí es…", 5),
            ("c", "sonriendo a cámara y despidiéndose", "Y a ti te espero en Loren Restobar", 3)],
           "", "Pongo su nombre y su cargo en pantalla", "Leer de un papel: mejor hablar con tus palabras, aunque te equivoques")

paginas = [("ficha-0-reglas-de-oro", reglas), ("ficha-1-empanada-jamon-queso", f1), ("ficha-2-del-fuego-a-la-mesa", f2), ("ficha-3-conoce-al-equipo", f3)]
with sync_playwright() as pw:
    nav = pw.chromium.launch(); pg = nav.new_page(viewport={"width": 1080, "height": 1920})
    for nombre, h in paginas:
        ruta = os.path.join(AQUI, nombre + ".html"); open(ruta, "w", encoding="utf-8").write(h)
        pg.goto(f"http://localhost:8123/herramientas/promo/{nombre}.html", wait_until="load")
        pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(700)
        sobra = pg.evaluate("(() => { const f = document.querySelector('.marca').getBoundingClientRect().top; const u = [...document.querySelectorAll('#f > *')].filter(x => !x.classList.contains('marca') && !x.classList.contains('flor')).map(x => x.getBoundingClientRect().bottom); return Math.round(Math.max(...u) - f); })()")
        pg.locator('#f').screenshot(path=os.path.join(SAL, nombre + ".png"))
        print(nombre, "· alto de la imagen:", pg.evaluate("document.querySelector('#f').offsetHeight"), "px")
    nav.close()
for nombre, _ in paginas:
    os.remove(os.path.join(AQUI, nombre + ".html"))
