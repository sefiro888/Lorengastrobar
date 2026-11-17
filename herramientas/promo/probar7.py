"""Hoja de fotogramas del promo dividido. Uso: python probar7.py <parte 1|2> <base.mp4 o -> <salida.jpg> t1 t2 ..."""
import os, sys, io, subprocess
from playwright.sync_api import sync_playwright
from PIL import Image
FF = os.path.join(os.path.dirname(sys.executable), "Lib", "site-packages", "imageio_ffmpeg", "binaries", "ffmpeg-win-x86_64-v7.1.exe")
parte, base, salida, ts = sys.argv[1], sys.argv[2], sys.argv[3], [float(x) for x in sys.argv[4:]]
cols = 8; w, h = 216, 384; filas = (len(ts) + cols - 1) // cols
hoja = Image.new("RGB", (cols * w, filas * h))
with sync_playwright() as pw:
    nav = pw.chromium.launch(); pg = nav.new_page(viewport={"width": 1080, "height": 1920})
    pg.on("pageerror", lambda e: print("ERR", e))
    pg.goto(f"http://localhost:8123/herramientas/promo/video7.html?p={parte}", wait_until="load")
    pg.wait_for_function("window.LISTO === true"); pg.wait_for_timeout(1200)
    for i, t in enumerate(ts):
        pg.evaluate(f"render({t})"); pg.wait_for_timeout(180)
        capa = Image.open(io.BytesIO(pg.screenshot(type="png", omit_background=True))).convert("RGBA")
        if base != "-":
            raw = subprocess.run([FF, "-loglevel", "error", "-ss", str(t), "-i", base, "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
            fondo = Image.open(io.BytesIO(raw)).convert("RGBA")
        else:
            fondo = Image.new("RGBA", (1080, 1920), (0, 0, 0, 255))
        fondo.alpha_composite(capa)
        hoja.paste(fondo.convert("RGB").resize((w, h)), ((i % cols) * w, (i // cols) * h))
    nav.close()
hoja.save(salida, quality=86); print("ok")
