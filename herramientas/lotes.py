"""Une los textos del HTML y del JS en i18n/todas.json y los divide en lotes numerados para traducir.
Uso: python herramientas/lotes.py <carpeta_salida>
"""
import json, os, sys
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
h = json.load(open(os.path.join(RAIZ, "i18n", "claves.json"), encoding="utf-8"))
j = json.load(open(os.path.join(RAIZ, "i18n", "claves_js.json"), encoding="utf-8"))
es, vistos = [], set()
for k in [x["es"] for x in h] + j:
    if k not in vistos:
        vistos.add(k); es.append(k)
json.dump(es, open(os.path.join(RAIZ, "i18n", "todas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(RAIZ, "i18n")
T = 220
for a in range(0, len(es), T):
    with open(os.path.join(out, f"lote_{a // T}.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(f"{i}|{es[i]}" for i in range(a, min(a + T, len(es)))))
print(len(es), "textos ·", sum(len(x) for x in es), "caracteres ·", (len(es) + T - 1) // T, "lotes")
