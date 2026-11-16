"""Saca fotogramas sueltos del vídeo promocional para revisarlos. Uso: python probar.py 2 7 12 ..."""
import os, sys
from playwright.sync_api import sync_playwright
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(RAIZ, "para-loren", "promo", "prueba"); os.makedirs(OUT, exist_ok=True)
ts = [float(x) for x in sys.argv[1:]] or [2, 6, 9]
with sync_playwright() as pw:
    nav = pw.chromium.launch()
    pg = nav.new_page(viewport={"width": 1080, "height": 1920})
    pg.goto("http://localhost:8123/herramientas/promo/video.html", wait_until="load")
    pg.wait_for_function("window.LISTO === true"); pg.wait_for_timeout(800)
    for t in ts:
        pg.evaluate(f"render({t})"); pg.wait_for_timeout(250)
        pg.screenshot(path=os.path.join(OUT, f"f_{t:05.1f}.jpg"), type="jpeg", quality=82)
    nav.close()
print("ok")
