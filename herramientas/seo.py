"""
LOREN RESTOBAR · SEO

Uso (siempre después de traducir):
  python herramientas/i18n.py construir
  python herramientas/seo.py

Qué hace:
  1. Abre cada página (ES, CA y EN) en un navegador sin pantalla y guarda dentro del
     HTML lo que pinta el JavaScript (cabecera, pie, carta completa, enciclopedia de
     sabores). Así Google lee todo el contenido sin tener que ejecutar nada. Al cargar
     la página, el JavaScript lo vuelve a pintar igual, así que no cambia nada a la vista.
  2. Escribe en cada <head>, entre <!--seo--> y <!--/seo-->: canonical, hreflang,
     og:url, og:locale y los datos estructurados (JSON-LD) del restaurante, la página,
     las migas, la carta (Menu), las preguntas frecuentes (FAQPage) y la receta.
  3. Genera sitemap.xml (con idiomas e imágenes) y robots.txt.

Requiere:  pip install playwright  y  python -m playwright install chromium
"""
import datetime, json, os, re, subprocess, sys, time
from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://lorenrestobar.com"
PUERTO = 8791
PAGINAS = ["index", "historia", "sabores", "carta", "domicilio", "eventos", "visitanos", "aviso-legal", "chipa-guazu", "sopa-paraguaya", "mbeju", "vori-vori", "empanadas"]
SIN_INDEXAR = {"aviso-legal"}
IDIOMAS = {"es": "", "ca": "ca/", "en": "en/"}
LOCALES = {"es": "es_ES", "ca": "ca_ES", "en": "en_GB"}
COCINA = {"es": ["Paraguaya", "Latinoamericana"], "ca": ["Paraguaiana", "Llatinoamericana"], "en": ["Paraguayan", "Latin American"]}
HOY = datetime.date.today().isoformat()
DIAS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
TIPO_PAGINA = {"historia": "AboutPage", "visitanos": "ContactPage", "carta": "WebPage", "sabores": "WebPage"}


def url(lang, p):
    pre = IDIOMAS[lang]
    return f"{BASE}/{pre}" if p == "index" else f"{BASE}/{pre}{p}.html"


def absoluta(src):
    return src if not src or src.startswith("http") else f"{BASE}/{src.lstrip('/')}"


def hora(h):
    if h >= 24:
        return "23:59"
    return f"{int(h):02d}:{round((h % 1) * 60):02d}"


CAPTURA = """() => {
  const limpiar = (el) => {
    const c = el.cloneNode(true);
    c.querySelectorAll('[data-nanduti], .enc').forEach((n) => (n.innerHTML = ''));
    c.querySelectorAll('.is-in').forEach((n) => n.classList.remove('is-in'));
    return c.innerHTML.trim();
  };
  const pre = {};
  document.querySelectorAll('[data-pre]').forEach((el) => { if (el.id) pre[el.id] = limpiar(el); });
  if (window.__SHELL) { pre['shell-top'] = window.__SHELL.top.trim(); pre['shell-bottom'] = window.__SHELL.bottom.trim(); }
  const txt = (el) => (el ? el.textContent.replace(/\\s+/g, ' ').trim() : '');
  const faq = [...document.querySelectorAll('.faq details')].map((d) => ({ q: txt(d.querySelector('summary')), a: txt(d.querySelector('p')) }));
  const r = document.getElementById('receta-chipa');
  const receta = r ? {
    nombre: txt(r.querySelector('h3')), intro: txt(r.querySelector('p')),
    ing: [...r.querySelectorAll('ul li')].map(txt), pasos: [...r.querySelectorAll('ol li')].map(txt),
    video: (document.querySelector('.receta__video video') || {}).getAttribute?.('src') || '',
    poster: (document.querySelector('.receta__video video') || {}).getAttribute?.('poster') || '',
    videoNombre: (document.querySelector('.receta__video video') || {}).getAttribute?.('aria-label') || ''
  } : null;
  const miga = txt(document.querySelector('.miga span'));
  const imgs = [...new Set([...document.querySelectorAll('main img[alt]')].filter((i) => i.alt.trim() && !i.src.includes('/kv/') && !i.src.includes('/marca/')).map((i) => i.getAttribute('src')))];
  const L = window.LOREN;
  const carta = (window.CARTA && document.body.dataset.page === 'carta') ? window.CATEGORIAS.map((c) => ({
    n: c.n, items: window.CARTA.filter((p) => p.cat === c.id).map((p) => ({ n: p.n, d: p.d, precio: p.precio, img: p.img }))
  })) : null;
  return {
    pre, faq, receta, miga, imgs, carta,
    titulo: document.title,
    desc: (document.querySelector('meta[name=description]') || {}).content || '',
    noindex: !!document.querySelector('meta[name=robots][content*=noindex]'),
    loren: { tel: L.telefonoIntl, email: L.email, dir: L.direccion, cp: L.cp, coords: L.coords, links: L.links, horario: L.horario, inicio: T('Inicio') }
  };
}"""


def grafo(lang, p, d):
    L = d["loren"]
    u = url(lang, p)
    rest_id = f"{BASE}/#restaurante"
    grupos = {}
    for k, h in enumerate(L["horario"]):
        if not h.get("cerrado"):
            grupos.setdefault((hora(h["abre"]), hora(h["cierra"])), []).append(DIAS[k])
    horario = [{"@type": "OpeningHoursSpecification", "dayOfWeek": dias, "opens": a, "closes": c} for (a, c), dias in grupos.items()]
    restaurante = {
        "@type": "Restaurant", "@id": rest_id, "name": "Loren Restobar",
        "alternateName": "Loren Gastrobar",
        "url": url(lang, "index"),
        "image": [f"{BASE}/img/redes/og-index-es.jpg", f"{BASE}/img/platos/chipa-guazu.webp", f"{BASE}/img/platos/sopa-paraguaya.webp"],
        "logo": f"{BASE}/img/marca/logo-loren.webp",
        "telephone": "+" + L["tel"], "email": L["email"],
        "address": {"@type": "PostalAddress", "streetAddress": L["dir"] + ", local 1", "postalCode": L["cp"].split()[0],
                    "addressLocality": "Barcelona", "addressRegion": "Cataluña", "addressCountry": "ES"},
        "geo": {"@type": "GeoCoordinates", "latitude": L["coords"]["lat"], "longitude": L["coords"]["lng"]},
        "hasMap": L["links"]["maps"],
        "servesCuisine": COCINA[lang], "priceRange": "€", "currenciesAccepted": "EUR",
        "acceptsReservations": True, "hasMenu": url(lang, "carta"),
        "openingHoursSpecification": horario,
        "foundingDate": "2020",
        "founder": {"@type": "Person", "@id": f"{BASE}/#loren-vera", "name": "Loren Vera"},
        "areaServed": "Barcelona",
        "sameAs": [L["links"]["instagram"], L["links"]["tiktok"], L["links"]["facebook"]],
    }
    web = {"@type": "WebSite", "@id": f"{BASE}/#web", "url": f"{BASE}/", "name": "Loren Restobar",
           "inLanguage": ["es", "ca", "en"], "publisher": {"@id": rest_id}}
    pagina = {"@type": TIPO_PAGINA.get(p, "WebPage"), "@id": u + "#pagina", "url": u, "name": d["titulo"],
              "description": d["desc"], "inLanguage": lang, "isPartOf": {"@id": f"{BASE}/#web"}, "about": {"@id": rest_id}}
    g = [restaurante, web, pagina]
    if p != "index":
        pagina["breadcrumb"] = {"@id": u + "#migas"}
        g.append({"@type": "BreadcrumbList", "@id": u + "#migas", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": L["inicio"], "item": url(lang, "index")},
            {"@type": "ListItem", "position": 2, "name": d["miga"] or d["titulo"], "item": u}]})
    if p == "historia":
        pagina["mainEntity"] = {"@id": f"{BASE}/#loren-vera"}
        g.append({"@type": "Person", "@id": f"{BASE}/#loren-vera", "name": "Loren Vera", "jobTitle": "Chef",
                  "birthPlace": "San José de los Arroyos, Paraguay", "worksFor": {"@id": rest_id}})
    if p == "carta" and d["carta"]:
        secciones = []
        for c in d["carta"]:
            items = []
            for it in c["items"]:
                m = {"@type": "MenuItem", "name": it["n"]}
                if it["d"]:
                    m["description"] = it["d"]
                if it["img"]:
                    m["image"] = absoluta(it["img"])
                if it["precio"] is not None:
                    m["offers"] = {"@type": "Offer", "price": f'{it["precio"]:.2f}', "priceCurrency": "EUR"}
                items.append(m)
            if items:
                secciones.append({"@type": "MenuSection", "name": c["n"], "hasMenuItem": items})
        g.append({"@type": "Menu", "@id": u + "#menu", "name": d["titulo"].split(" · ")[0], "url": u, "inLanguage": lang, "hasMenuSection": secciones})
        restaurante["hasMenu"] = {"@id": u + "#menu"}
    if d["faq"]:
        g.append({"@type": "FAQPage", "@id": u + "#preguntas", "mainEntity": [
            {"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in d["faq"] if f["q"] and f["a"]]})
    r = d["receta"]
    if r:
        receta = {"@type": "Recipe", "@id": u + "#receta-chipa", "name": r["nombre"], "description": r["intro"],
                  "image": [f"{BASE}/img/platos/chipa-guazu.webp"], "author": {"@id": rest_id},
                  "recipeCuisine": COCINA[lang][0], "recipeYield": "6", "prepTime": "PT20M", "cookTime": "PT45M", "totalTime": "PT65M",
                  "keywords": "chipa guazú, comida paraguaya, maíz, sin trigo", "inLanguage": lang,
                  "recipeIngredient": r["ing"],
                  "recipeInstructions": [{"@type": "HowToStep", "position": i + 1, "text": t} for i, t in enumerate(r["pasos"])]}
        if r["video"]:
            receta["video"] = {"@type": "VideoObject", "name": r["videoNombre"] or r["nombre"], "description": r["intro"],
                               "thumbnailUrl": absoluta(r["poster"]), "contentUrl": absoluta(r["video"]), "uploadDate": "2026-11-10"}
        g.append(receta)
    return {"@context": "https://schema.org", "@graph": g}


def bloque_seo(lang, p, d):
    u = url(lang, p)
    lineas = [f'<link rel="canonical" href="{u}">']
    for l in IDIOMAS:
        lineas.append(f'<link rel="alternate" hreflang="{l}" href="{url(l, p)}">')
    lineas.append(f'<link rel="alternate" hreflang="x-default" href="{url("es", p)}">')
    lineas.append(f'<meta property="og:url" content="{u}">')
    img = f"img/redes/og-{p}-{lang}.jpg"
    if not os.path.exists(os.path.join(RAIZ, img)):
        img = f"img/redes/og-index-{lang}.jpg"
    lineas.append(f'<meta property="og:image" content="{BASE}/{img}">')
    lineas.append('<meta property="og:image:width" content="1200">')
    lineas.append('<meta property="og:image:height" content="630">')
    lineas.append(f'<meta property="og:image:alt" content="{d["titulo"].replace(chr(34), "")}">')
    lineas.append(f'<meta name="twitter:image" content="{BASE}/{img}">')
    lineas.append(f'<meta property="og:locale" content="{LOCALES[lang]}">')
    for l in IDIOMAS:
        if l != lang:
            lineas.append(f'<meta property="og:locale:alternate" content="{LOCALES[l]}">')
    ld = json.dumps(grafo(lang, p, d), ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    lineas.append(f'<script type="application/ld+json">{ld}</script>')
    return "<!--seo-->\n  " + "\n  ".join(lineas) + "\n  <!--/seo-->"


def aplicar(ruta, lang, p, d):
    s = open(ruta, encoding="utf-8").read()
    s, n = re.subn(r"<!--seo-->.*?<!--/seo-->", lambda m: bloque_seo(lang, p, d), s, count=1, flags=re.S)
    assert n == 1, f"{ruta}: falta <!--seo--><!--/seo--> en el <head>"
    # restos de versiones anteriores (generados antes por i18n.py)
    s = re.sub(r'\s*<link href="[^"]*" hreflang="[^"]*" rel="alternate"/>', "", s)
    for idn, html in d["pre"].items():
        if "<!--/pre-->" in html or not html:
            continue
        patron = re.compile(r'(<[a-z]+\b[^<>]*\bid="' + re.escape(idn) + r'"[^<>]*>)(.*?)(<!--/pre-->)', re.S)
        s, n = patron.subn(lambda m: m.group(1) + html + m.group(3), s, count=1)
        if n != 1:
            print(f"   ! {ruta}: no encuentro el bloque #{idn}")
    open(ruta, "w", encoding="utf-8").write(s)


def mapa_y_robots(datos):
    x = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for p in PAGINAS:
        if p in SIN_INDEXAR:
            continue
        for lang in IDIOMAS:
            x.append("  <url>")
            x.append(f"    <loc>{url(lang, p)}</loc>")
            x.append(f"    <lastmod>{HOY}</lastmod>")
            for l in IDIOMAS:
                x.append(f'    <xhtml:link rel="alternate" hreflang="{l}" href="{url(l, p)}"/>')
            x.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{url("es", p)}"/>')
            for src in datos[(lang, p)]["imgs"][:60]:
                x.append(f"    <image:image><image:loc>{absoluta(src)}</image:loc></image:image>")
            x.append("  </url>")
    x.append("</urlset>")
    open(os.path.join(RAIZ, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(x) + "\n")
    open(os.path.join(RAIZ, "robots.txt"), "w", encoding="utf-8").write(
        "User-agent: *\nAllow: /\nDisallow: /herramientas/\nDisallow: /i18n/\nDisallow: /tarjeta/\n\n"
        f"Sitemap: {BASE}/sitemap.xml\n")


def main():
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(PUERTO), "--bind", "127.0.0.1", "--directory", RAIZ],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
    datos = {}
    try:
        with sync_playwright() as pw:
            nav = pw.chromium.launch()
            ctx = nav.new_context(viewport={"width": 1280, "height": 900}, reduced_motion="reduce")
            ctx.route("**/*", lambda r: r.continue_() if r.request.url.startswith(f"http://127.0.0.1:{PUERTO}") else r.abort())
            pg = ctx.new_page()
            errores = []
            pg.on("pageerror", lambda e: errores.append(str(e)))
            for lang, pre in IDIOMAS.items():
                for p in PAGINAS:
                    pg.goto(f"http://127.0.0.1:{PUERTO}/{pre}{p}.html", wait_until="load")
                    pg.wait_for_timeout(250)
                    d = pg.evaluate(CAPTURA)
                    datos[(lang, p)] = d
                    aplicar(os.path.join(RAIZ, pre, p + ".html"), lang, p, d)
                    print(f"[{lang}] {p:12} {len(d['pre'])} bloques · {len(d['imgs'])} fotos · {len(d['faq'])} preguntas" + (" · carta" if d["carta"] else "") + (" · receta" if d["receta"] else ""))
            nav.close()
            if errores:
                print("Errores de JavaScript:", *errores[:10], sep="\n   ")
    finally:
        srv.terminate()
    mapa_y_robots(datos)
    print("sitemap.xml y robots.txt escritos")


if __name__ == "__main__":
    main()
