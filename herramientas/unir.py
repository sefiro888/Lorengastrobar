"""Une las traducciones por número (i18n/tr/ca_*.txt, en_*.txt) con i18n/todas.json
y actualiza los diccionarios i18n/ca.json e i18n/en.json (clave = texto en español).
Comprueba que no falte ninguna y que las etiquetas HTML coincidan.
"""
import glob, json, os, re
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
es = json.load(open(os.path.join(RAIZ, "i18n", "todas.json"), encoding="utf-8"))
etiquetas = lambda s: sorted(re.findall(r"</?([a-z0-9]+)", s))
for lang in ("ca", "en"):
    ruta = os.path.join(RAIZ, "i18n", lang + ".json")
    dic = json.load(open(ruta, encoding="utf-8")) if os.path.exists(ruta) else {}
    vistos = set()
    for f in sorted(glob.glob(os.path.join(RAIZ, "i18n", "tr", lang + "_*.txt"))):
        for linea in open(f, encoding="utf-8").read().splitlines():
            if not linea.strip():
                continue
            n, t = linea.split("|", 1)
            n = int(n); k = es[n]; vistos.add(n)
            v = k if t.strip() == "=" else t.strip()
            if etiquetas(v) != etiquetas(k):
                print(f"[{lang}] {n}: etiquetas distintas\n   es: {k[:120]}\n   {lang}: {v[:120]}")
            dic[k] = v
    faltan = [i for i in range(len(es)) if i not in vistos and es[i] not in dic]
    if faltan:
        print(f"[{lang}] faltan {len(faltan)}: {faltan[:20]}")
    json.dump(dic, open(ruta, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"[{lang}] {len(dic)} traducciones")
