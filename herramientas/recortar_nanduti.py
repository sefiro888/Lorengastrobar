"""Recorta las piezas de encaje ñandutí de la ilustración de Loren y les quita el fondo burdeos.
Uso: python herramientas/recortar_nanduti.py <imagen_original>
Genera img/marca/nanduti-aro.webp (aro central) y algunas flores sueltas para adornos.
"""
import os, sys
import numpy as np
from PIL import Image
from scipy import ndimage

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = np.asarray(Image.open(sys.argv[1]).convert("RGB")).astype(np.float32)
H, W, _ = src.shape
BG = np.array([87, 1, 23], np.float32)
dist = np.sqrt(((src - BG) ** 2).sum(-1))
ALFA = np.clip((dist - 22) / 95, 0, 1)

def recorte(x0, y0, x1, y1, centro=None, radio=None, solo_principal=False, ajustar=True):
    a = ALFA[y0:y1, x0:x1].copy()
    c = src[y0:y1, x0:x1]
    if centro is not None:
        yy, xx = np.mgrid[y0:y1, x0:x1]
        a[np.hypot(xx - centro[0], yy - centro[1]) > radio] = 0
    if solo_principal:
        etiq, n = ndimage.label(a > 0.25)
        if n:
            tam = ndimage.sum(np.ones_like(a), etiq, range(1, n + 1))
            p = int(np.argmax(tam)) + 1
            sl = ndimage.find_objects(etiq)[p - 1]
            # conservar las piezas que caen dentro de la pieza principal (puntos, detalles)
            dentro = np.zeros_like(a, bool)
            dentro[sl] = True
            ok = np.zeros(n + 1, bool); ok[p] = True
            for k, s in enumerate(ndimage.find_objects(etiq), 1):
                cy, cx = (s[0].start + s[0].stop) / 2, (s[1].start + s[1].stop) / 2
                if sl[0].start <= cy <= sl[0].stop and sl[1].start <= cx <= sl[1].stop:
                    ok[k] = True
            mascara = ok[etiq] | (ndimage.binary_dilation(ok[etiq], iterations=2) & (a > 0))
            a = a * mascara
    with np.errstate(divide="ignore", invalid="ignore"):
        col = np.where(a[..., None] > 0, (c - BG * (1 - a[..., None])) / np.maximum(a[..., None], 1e-3), 0)
    rgba = np.dstack([np.clip(col, 0, 255), a * 255]).astype(np.uint8)
    im = Image.fromarray(rgba, "RGBA")
    if not ajustar:
        return im
    bb = im.getbbox()
    return im.crop(bb) if bb else im

dest = os.path.join(R, "img", "marca")
# centro real del aro (centro del hueco interior, medido sobre la ilustración)
cx, cy, rr = 766.6, 496.0, 330
x0, y0 = int(round(cx - rr)), int(round(cy - rr))
aro = recorte(x0, y0, x0 + 2 * rr, y0 + 2 * rr, (cx, cy), rr, ajustar=False)
aro.save(os.path.join(dest, "nanduti-aro.webp"), "WEBP", quality=92, method=6)
aro.save(os.path.join(dest, "nanduti-aro.png"), optimize=True)
print("aro", aro.size)

piezas = {
    "nanduti-flor-grande": (140, 90, 495, 440),
    "nanduti-flor-roseta": (1035, 90, 1365, 415),
    "nanduti-flor-margarita": (1205, 412, 1518, 722),
    "nanduti-sol": (22, 414, 330, 728),
    "nanduti-flor-pequena": (492, 22, 694, 198),
}
for nombre, (x0, y0, x1, y1) in piezas.items():
    centro = ((x0 + x1) / 2, (y0 + y1) / 2)
    im = recorte(x0, y0, x1, y1, centro, min(x1 - x0, y1 - y0) / 2 - 4)
    im.save(os.path.join(dest, nombre + ".webp"), "WEBP", quality=90, method=6)
    print(nombre, im.size)
for viejo in ("nanduti-esquina.webp", "nanduti-cenefa.webp"):
    if os.path.exists(os.path.join(dest, viejo)):
        os.remove(os.path.join(dest, viejo))
