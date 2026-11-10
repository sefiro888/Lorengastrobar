"""Convierte la versión 2 (carpeta v2/) en la web principal. Se ejecuta una sola vez.
La versión 1 queda en el historial de git con la etiqueta «version-1-antigua».
"""
import glob, json, os, re, shutil

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = os.path.join(R, "v2")
os.chdir(R)

# 1. Páginas, estilos, scripts, imágenes nuevas y vídeos de la v2 -> raíz
paginas = sorted(os.path.basename(f) for f in glob.glob(os.path.join(V, "*.html")))
for p in paginas:
    shutil.copy(os.path.join(V, p), p)
for sub in ("css", "js", "video"):
    for f in glob.glob(os.path.join(V, sub, "*.*")):
        shutil.copy(f, os.path.join(sub, os.path.basename(f)))
for sub in ("kv", "nuevo"):
    shutil.copytree(os.path.join(V, "img", sub), os.path.join("img", sub), dirs_exist_ok=True)

# 2. Quitar lo que era sólo de la propuesta
V1_FUENTES = re.compile(r'  <link href="https://fonts\.googleapis\.com/css2\?family=DM\+Sans[^"]*" rel="stylesheet">\n')
for p in paginas:
    s = open(p, encoding="utf-8").read()
    s = s.replace('  <meta name="robots" content="noindex">\n', "")
    if p != "carta-clasica.html":  # la carta para imprimir sí usa las fuentes clásicas
        s = V1_FUENTES.sub("", s)
    open(p, "w", encoding="utf-8").write(s)

js = open("js/v2.js", encoding="utf-8").read()
i = js.index("  // Distintivo para comparar con la versión 1")
j = js.index("})();", i)
js = js[:i] + js[j:]
open("js/v2.js", "w", encoding="utf-8").write(js)

css = open("css/v2.css", encoding="utf-8").read()
css = css.replace(".idiomas { display: none !important; }\n", "")
open("css/v2.css", "w", encoding="utf-8").write(css)

# 3. Traducciones: la v2 usa comillas “” (Anton y Kaushan pintan «» como <<)
for idioma in ("ca", "en"):
    f = os.path.join("i18n", idioma + ".json")
    d = json.load(open(f, encoding="utf-8"))
    q = lambda t: t.replace("«", "“").replace("»", "”")
    d = {q(k): q(v) for k, v in d.items()}
    json.dump(d, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# 4. La carpeta v2/ pasa a redirigir a la web principal (para no romper enlaces compartidos)
shutil.rmtree(V)
os.makedirs(V)
for p in paginas:
    open(os.path.join(V, p), "w", encoding="utf-8").write(f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><title>Loren Restobar</title>
<meta name="robots" content="noindex"><link rel="canonical" href="https://sefiro888.github.io/Lorengastrobar/{p}">
<meta http-equiv="refresh" content="0; url=../{p}">
<script>location.replace("../{p}" + location.hash);</script></head>
<body><a href="../{p}">Ir a Loren Restobar</a></body></html>
''')

# 5. Las herramientas que generaban la v2 ya no hacen falta
os.makedirs(os.path.join("herramientas", "archivo"), exist_ok=True)
for h in ("v2_construir.py", "v2_recursos.py", "v2_material2.py"):
    if os.path.exists(os.path.join("herramientas", h)):
        shutil.move(os.path.join("herramientas", h), os.path.join("herramientas", "archivo", h))
print("versión 2 = web principal ·", len(paginas), "páginas")
