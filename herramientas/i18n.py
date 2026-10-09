"""
LOREN RESTOBAR · Traducción de la web (ES → CA / EN)

Uso:
  python herramientas/i18n.py extraer    → lista los textos de las páginas en i18n/claves.json
  python herramientas/i18n.py construir  → genera ca/*.html, en/*.html y js/i18n.js

Las traducciones viven en i18n/ca.json e i18n/en.json  ({ "texto en español": "traducción" }).
Si falta una traducción, se deja el texto en español y se avisa por pantalla.
"""
import json, os, re, sys
from bs4 import BeautifulSoup, NavigableString, Tag, Comment, Doctype, Declaration

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGINAS = ["index", "historia", "sabores", "carta", "domicilio", "eventos", "visitanos", "carta-clasica"]
IDIOMAS = {"ca": "ca-ES", "en": "en"}
INLINE = {"a", "strong", "em", "b", "i", "small", "span", "br", "sup", "sub", "abbr", "mark"}
SALTAR = {"script", "style", "svg", "noscript", "template", "canvas", "iframe", "video"}
ATRIBUTOS = ["alt", "placeholder", "aria-label", "title", "data-cap", "data-nombre"]
LETRAS = re.compile(r"[A-Za-zÀ-ÿ]")


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def es_unidad(tag):
    if not LETRAS.search(tag.get_text()):
        return False
    for d in tag.descendants:
        if isinstance(d, Tag) and (d.name not in INLINE or d.name in SALTAR):
            return False
    return True


def recorrer(el, fn):
    """Llama fn(clave, aplicar) por cada unidad traducible."""
    for hijo in list(el.children):
        if isinstance(hijo, (Comment, Doctype, Declaration)):
            continue
        if isinstance(hijo, NavigableString):
            t = str(hijo)
            if LETRAS.search(t) and el.name not in SALTAR:
                k = norm(t)
                pre = t[: len(t) - len(t.lstrip())]
                post = t[len(t.rstrip()):]
                fn(k, lambda v, h=hijo, pre=pre, post=post: h.replace_with(NavigableString(pre + v + post)))
            continue
        if not isinstance(hijo, Tag) or hijo.name in SALTAR or hijo.has_attr("data-no-t"):
            continue
        for a in ATRIBUTOS:
            if hijo.has_attr(a) and LETRAS.search(hijo[a]):
                fn(norm(hijo[a]), lambda v, h=hijo, a=a: h.__setitem__(a, v))
        if hijo.name == "input" and hijo.get("type") == "checkbox" and hijo.has_attr("value"):
            fn(norm(hijo["value"]), lambda v, h=hijo: h.__setitem__("value", v))
        if hijo.name == "meta" and hijo.get("name") == "description" or hijo.get("property") in ("og:title", "og:description"):
            if hijo.has_attr("content"):
                fn(norm(hijo["content"]), lambda v, h=hijo: h.__setitem__("content", v))
        if hijo.name in ("title",):
            fn(norm(hijo.get_text()), lambda v, h=hijo: (h.clear(), h.append(v)))
            continue
        if es_unidad(hijo) and hijo.name not in ("html", "head", "body"):
            k = norm(hijo.decode_contents())
            def aplicar(v, h=hijo):
                h.clear()
                frag = BeautifulSoup(v, "html.parser")
                for n in list(frag.contents):
                    h.append(n)
            fn(k, aplicar)
        else:
            recorrer(hijo, fn)


def leer(p):
    return BeautifulSoup(open(os.path.join(RAIZ, p + ".html"), encoding="utf-8").read(), "html.parser")


def extraer():
    claves, vistos = [], set()
    for p in PAGINAS:
        sopa = leer(p)
        def fn(k, _):
            if k not in vistos:
                vistos.add(k); claves.append({"p": p, "es": k})
        recorrer(sopa, fn)
    os.makedirs(os.path.join(RAIZ, "i18n"), exist_ok=True)
    json.dump(claves, open(os.path.join(RAIZ, "i18n", "claves.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(claves), "textos")


def reescribir_enlaces(sopa, lang):
    pagina_re = re.compile(r"^(" + "|".join(PAGINAS) + r")\.html(#.*)?$")
    for a in sopa.find_all(href=True):
        h = a["href"]
        if pagina_re.match(h):
            a["href"] = lang + "/" + h


def construir():
    dic = {l: json.load(open(os.path.join(RAIZ, "i18n", l + ".json"), encoding="utf-8")) for l in IDIOMAS}
    for lang, locale in IDIOMAS.items():
        faltan = set()
        os.makedirs(os.path.join(RAIZ, lang), exist_ok=True)
        for p in PAGINAS:
            sopa = leer(p)
            def fn(k, aplicar):
                v = dic[lang].get(k)
                if v is None:
                    faltan.add(k)
                elif v != k:
                    aplicar(v)
            recorrer(sopa, fn)
            sopa.html["lang"] = lang
            head = sopa.head
            base = sopa.new_tag("base", href="../")
            head.insert(0, base)
            cfg = sopa.new_tag("script")
            cfg.string = f'window.IDIOMA="{lang}";window.PREF="{lang}/";'
            base.insert_after(cfg)
            for alt, href in (("es", ""), ("ca", "ca/"), ("en", "en/")):
                head.append(sopa.new_tag("link", rel="alternate", hreflang=alt, href=href + p + ".html"))
            reescribir_enlaces(sopa, lang)
            # i18n.js antes que el resto de scripts
            primero = sopa.find("script", src=True)
            if primero:
                primero.insert_before(sopa.new_tag("script", src="js/i18n.js?v=5"))
            html = str(sopa)
            if not html.lower().startswith("<!doctype"):
                html = "<!doctype html>\n" + html
            open(os.path.join(RAIZ, lang, p + ".html"), "w", encoding="utf-8").write(html)
        if faltan:
            print(f"[{lang}] {len(faltan)} textos sin traducir:")
            for k in sorted(faltan)[:40]:
                print("   ·", k[:100])
        else:
            print(f"[{lang}] completo")
    js = "/* Generado por herramientas/i18n.py — no editar a mano */\nwindow.I18N = " + json.dumps(dic, ensure_ascii=False) + ";\n"
    open(os.path.join(RAIZ, "js", "i18n.js"), "w", encoding="utf-8").write(js)
    print("js/i18n.js escrito")


if __name__ == "__main__":
    {"extraer": extraer, "construir": construir}[sys.argv[1]]()
