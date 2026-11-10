"""Aligera las imágenes de la web (las dos versiones) sin cambiar sus nombres.
- Fotos: lado mayor 1000 px, WebP calidad 74 (sólo si así pesan menos).
- Encajes y motivos decorativos: tamaño de uso real.
Antes guarda una copia de cada archivo en materialnuevo/copia_imagenes/ (no se sube al repositorio).
Uso: python herramientas/optimizar_imagenes.py
"""
import glob, os, shutil
from PIL import Image

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COPIA = os.path.join(R, "materialnuevo", "copia_imagenes")
FOTOS = ["img/platos", "img/clientes", "img/local", "img/redes", "v2/img/kv", "v2/img/nuevo"]
DECORACION = {  # archivo: lado máximo
    "img/marca/nanduti-aro.webp": 560, "v2/img/marca/nanduti-aro.webp": 560,
    "v2/img/kv/flor-kv.webp": 640, "v2/img/kv/nanduti-bandera.webp": 760,
    "v2/img/kv/motivo-pavo.png": 620, "v2/img/kv/motivo-roseta.png": 620,
}
antes = despues = 0


def copia(f):
    d = os.path.join(COPIA, os.path.relpath(f, R))
    if not os.path.exists(d):
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copy2(f, d)


def guardar(im, f, q):
    tmp = f + ".tmp"
    if f.endswith(".png"):
        im.save(tmp, "PNG", optimize=True)
    else:
        im.save(tmp, "WEBP", quality=q, method=6)
    return tmp


def procesar(f, lado, q):
    global antes, despues
    t0 = os.path.getsize(f)
    im = Image.open(f)
    im.load()
    modo = "RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB"
    im = im.convert(modo)
    if max(im.size) > lado:
        im.thumbnail((lado, lado), Image.LANCZOS)
    tmp = guardar(im, f, q)
    t1 = os.path.getsize(tmp)
    antes += t0
    if t1 < t0 * 0.95:
        copia(f)
        os.replace(tmp, f)
        despues += t1
    else:
        os.remove(tmp)
        despues += t0


for carpeta in FOTOS:
    for f in glob.glob(os.path.join(R, carpeta, "*.webp")):
        if os.path.relpath(f, R).replace("\\", "/") in DECORACION:
            continue
        procesar(f, 1000, 74)
for rel, lado in DECORACION.items():
    f = os.path.join(R, rel)
    if os.path.exists(f):
        procesar(f, lado, 80)
print(f"imágenes: {antes / 1e6:.1f} MB -> {despues / 1e6:.1f} MB")
