"""Previsualiza fotogramas del promo 2 (capa gráfica sobre la pista base). Uso: python probar2.py base.mp4 salida.jpg t1 t2 ..."""
import os, sys, subprocess, io
from playwright.sync_api import sync_playwright
from PIL import Image
FF = os.path.join(os.path.dirname(sys.executable), "Lib", "site-packages", "imageio_ffmpeg", "binaries", "ffmpeg-win-x86_64-v7.1.exe")
base, salida, ts = sys.argv[1], sys.argv[2], [float(x) for x in sys.argv[3:]]
cols = 6; w, h = 270, 480
filas = (len(ts) + cols - 1) // cols
hoja = Image.new("RGB", (cols * w, filas * h))
with sync_playwright() as pw:
    nav = pw.chromium.launch(); pg = nav.new_page(viewport={"width": 1080, "height": 1920})
    pg.goto("http://localhost:8123/herramientas/promo/video2.html", wait_until="load")
    pg.wait_for_function("window.LISTO === true"); pg.wait_for_timeout(1500)
    for i, t in enumerate(ts):
        pg.evaluate(f"render({t})"); pg.wait_for_timeout(200)
        capa = Image.open(io.BytesIO(pg.screenshot(type="png", omit_background=True))).convert("RGBA")
        raw = subprocess.run([FF, "-loglevel", "error", "-ss", str(t), "-i", base, "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
        fondo = Image.open(io.BytesIO(raw)).convert("RGBA")
        fondo.alpha_composite(capa)
        hoja.paste(fondo.convert("RGB").resize((w, h)), ((i % cols) * w, (i // cols) * h))
    nav.close()
hoja.save(salida, quality=86); print("ok")
