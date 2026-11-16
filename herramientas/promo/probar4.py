"""Hoja de fotogramas del reel 4. Uso: python probar4.py salida.jpg t1 t2 ..."""
import os, sys
from playwright.sync_api import sync_playwright
from PIL import Image
import io
HTML = sys.argv[-1] if sys.argv[-1].endswith(".html") else "video4.html"
salida, ts = sys.argv[1], [float(x) for x in sys.argv[2:] if not x.endswith(".html")]
cols = 8; w, h = 216, 384; filas = (len(ts) + cols - 1) // cols
hoja = Image.new("RGB", (cols * w, filas * h))
with sync_playwright() as pw:
    nav = pw.chromium.launch(); pg = nav.new_page(viewport={"width": 1080, "height": 1920})
    pg.on("pageerror", lambda e: print("ERR", e))
    pg.goto("http://localhost:8123/herramientas/promo/" + (sys.argv[-1] if sys.argv[-1].endswith(".html") else "video4.html"), wait_until="load")
    pg.wait_for_function("window.LISTO === true"); pg.wait_for_timeout(800)
    for i, t in enumerate(ts):
        pg.evaluate(f"render({t})"); pg.evaluate("window.esperar()"); pg.wait_for_timeout(120)
        im = Image.open(io.BytesIO(pg.screenshot(type="jpeg", quality=85))).convert("RGB").resize((w, h))
        hoja.paste(im, ((i % cols) * w, (i // cols) * h))
    nav.close()
hoja.save(salida, quality=86); print("ok")
