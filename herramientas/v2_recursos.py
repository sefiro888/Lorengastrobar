"""Prepara los recursos de la versión 2 a partir de materialnuevo/ (Key Visual, carteles, fotos y vídeos).
Uso: python herramientas/v2_recursos.py
"""
import os, subprocess
import numpy as np
import fitz
from PIL import Image
import imageio_ffmpeg

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = os.path.join(R, "materialnuevo")
O = os.path.join(R, "v2", "img", "kv")
os.makedirs(O, exist_ok=True)
KV = fitz.open(os.path.join(M, "Key Visual - Loren Resto Bar.pdf_20261109_145226_0000.pdf"))


def guardar(im, nombre, q=84, maxlado=None):
    if maxlado:
        im.thumbnail((maxlado, maxlado), Image.LANCZOS)
    im.save(os.path.join(O, nombre), "WEBP", quality=q, method=6)
    print(nombre, im.size)


def kv_img(xref):
    pix = fitz.Pixmap(KV, xref)
    if pix.n - pix.alpha > 3:
        pix = fitz.Pixmap(fitz.csRGB, pix)
    return Image.frombytes("RGBA" if pix.alpha else "RGB", (pix.width, pix.height), pix.samples).convert("RGB")


def sin_marca(im, f=0.86):
    """Quita la esquina inferior derecha (logo de agua) recortando a un cuadrado algo menor."""
    w, h = im.size
    return im.crop((0, 0, int(w * f), int(h * f)))


# --- Fotos del Key Visual ---
guardar(sin_marca(kv_img(436)), "equipo.webp")             # Loren y el equipo de cocina
guardar(sin_marca(kv_img(437)), "loren-sarten.webp")       # Loren con la sartén
guardar(sin_marca(kv_img(441)), "brasero-mesa.webp")       # Brasero en la mesa
guardar(sin_marca(kv_img(423)), "sopa-paraguaya-kv.webp")  # Sopa paraguaya
guardar(sin_marca(kv_img(427)), "parrillada-kv.webp")      # Parrillada
guardar(sin_marca(kv_img(420)), "entrecot-kv.webp")        # Carne

# Hamburguesa (página 13 del Key Visual): se renderiza la zona de la foto
p = KV[12]
r = p.rect
clip = fitz.Rect(r.width * 0.19, r.height * 0.27, r.width * 0.81, r.height * 0.795)
pm = p.get_pixmap(matrix=fitz.Matrix(2.2, 2.2), clip=clip)
guardar(Image.frombytes("RGB", (pm.width, pm.height), pm.samples), "hamburguesa-kv.webp", maxlado=1400)

# Flor de ñandutí grande (crema sobre negro) -> PNG con transparencia
flor = np.asarray(kv_img(33)).astype(np.float32)
lum = flor.max(-1)
alfa = np.clip((lum - 42) / 110, 0, 1)
rgb = np.clip(flor / np.maximum(alfa[..., None], 1e-3), 0, 255)
Image.fromarray(np.dstack([rgb, alfa * 255]).astype(np.uint8), "RGBA").save(os.path.join(O, "flor-kv.webp"), "WEBP", quality=90, method=6)
print("flor-kv.webp")

# --- Motivos vectoriales de los carteles: máscaras blancas con transparencia ---
cartel = fitz.open(os.path.join(M, "cartel290x290.pdf"))[0]
esc = cartel.rect.width / 5000  # las coordenadas se midieron sobre un render de 5000 px
motivos = {"pavo": (1084, 2972, 1544, 3424), "roseta": (1676, 976, 2092, 1384)}
for nombre, (x0, y0, x1, y1) in motivos.items():
    pad = 6
    clip = fitz.Rect((x0 - pad) * esc, (y0 - pad) * esc, (x1 + pad) * esc, (y1 + pad) * esc)
    z = 1400 / clip.width
    pm = cartel.get_pixmap(matrix=fitz.Matrix(z, z), clip=clip, alpha=False)
    a = np.frombuffer(pm.samples, np.uint8).reshape(pm.height, pm.width, 3).astype(np.float32)
    tinta = np.clip((255 - a.mean(-1)) / 140, 0, 1)
    im = Image.fromarray(np.dstack([np.full_like(tinta, 255)] * 3 + [tinta * 255]).astype(np.uint8), "RGBA")
    im.save(os.path.join(O, f"motivo-{nombre}.png"), optimize=True)
    print("motivo", nombre, im.size)

# --- Fotos nuevas de WhatsApp ---
W = lambda n: Image.open(os.path.join(M, f"WhatsApp Image 2026-11-09 at {n}.jpeg")).convert("RGB")
guardar(W("14.33.53"), "mila-napolitana-nueva.webp", maxlado=1400)
emp = W("14.48.53")
w, h = emp.size
guardar(emp.crop((int(w * .08), 0, int(w * .80), int(h * .86))), "empanadas-cesta.webp", maxlado=1400)  # sin el logo
guardar(W("14.40.34"), "bocaditos-sandwiches.webp", maxlado=1300)
guardar(W("14.41.18"), "bocaditos-empanadas.webp", maxlado=1300)
guardar(W("14.27.16"), "banner-nanduti.webp", maxlado=1600)
fondo = W("14.12.29")  # plantilla vacía del menú del día: textura de encaje sobre negro
guardar(fondo.crop((0, 520, 1080, 1290)), "textura-oscura.webp", q=70)

import sys
if "--sin-videos" in sys.argv:
    sys.exit()

# --- Vídeos: H.264 ligero, sin audio, con póster ---
FF = imageio_ffmpeg.get_ffmpeg_exe()
videos = {
    "14.27.02": "mbeju", "14.27.39": "sopa", "14.28.39": "chyryry",
    "14.33.00": "vori", "14.46.48": "chipa",
}
VO = os.path.join(R, "v2", "video")
POSTER = {"mbeju": "40", "sopa": "14", "chyryry": "26", "vori": "16", "chipa": "4"}  # segundo del fotograma de portada
os.makedirs(VO, exist_ok=True)
for t, n in videos.items():
    src = os.path.join(M, f"WhatsApp Video 2026-11-09 at {t}.mp4")
    dst = os.path.join(VO, f"{n}.mp4")
    extra = ["-t", "16"] if n == "chipa" else []  # la chipa acaba con el rótulo final: se corta antes
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", src, *extra, "-an", "-vf", "scale=480:-2", "-c:v", "libx264",
                    "-preset", "slow", "-crf", "27", "-pix_fmt", "yuv420p", "-movflags", "+faststart", dst], check=True)
    subprocess.run([FF, "-y", "-loglevel", "error", "-ss", POSTER.get(n, "3"), "-i", dst, "-frames:v", "1", "-q:v", "4",
                    os.path.join(VO, f"{n}.jpg")], check=True)
    print("video", n, os.path.getsize(dst) // 1024, "KB")
