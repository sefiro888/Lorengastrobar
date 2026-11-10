"""Prepara la carta impresa del local (tríptico) para el inicio de la web.
- Borra la contraseña del wifi del panel exterior (relleno con el degradado del fondo).
- Guarda las dos caras en img/carta/.
Los originales quedan en materialnuevo/lote2/.
Uso: python herramientas/carta_local.py <imagen exterior> <imagen interior>
"""
import os, shutil, sys
import numpy as np
from PIL import Image

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
O = os.path.join(R, "img", "carta"); os.makedirs(O, exist_ok=True)
ORIG = os.path.join(R, "materialnuevo", "lote2"); os.makedirs(ORIG, exist_ok=True)
ext, intr = sys.argv[1], sys.argv[2]
shutil.copy(ext, os.path.join(ORIG, "carta-exterior" + os.path.splitext(ext)[1]))
shutil.copy(intr, os.path.join(ORIG, "carta-interior" + os.path.splitext(intr)[1]))

im = Image.open(ext).convert("RGB")
a = np.asarray(im).astype(np.float32).copy()
x0, y0, x1, y1 = 604, 552, 828, 624  # caja del texto «LorenRestobar · CLAVE · contraseña»
arriba, abajo = a[y0 - 3:y0, x0:x1].mean(0), a[y1:y1 + 3, x0:x1].mean(0)
for k, y in enumerate(range(y0, y1)):
    t = (k + .5) / (y1 - y0)
    a[y, x0:x1] = arriba * (1 - t) + abajo * t
Image.fromarray(a.clip(0, 255).astype(np.uint8)).save(os.path.join(O, "carta-exterior.webp"), "WEBP", quality=86, method=6)
Image.open(intr).convert("RGB").save(os.path.join(O, "carta-interior.webp"), "WEBP", quality=86, method=6)
for n in ("carta-exterior", "carta-interior"):
    print(n, os.path.getsize(os.path.join(O, n + ".webp")) // 1024, "KB")
