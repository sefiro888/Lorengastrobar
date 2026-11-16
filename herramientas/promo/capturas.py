"""Capturas de la web (móvil) y fotogramas de vídeos para el vídeo promocional de Instagram."""
import os, subprocess, sys, json
from playwright.sync_api import sync_playwright
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SALIDA = os.path.join(RAIZ, "herramientas", "promo", "assets")
BASE = "http://localhost:8123"
PAGINAS = {"carta": ("carta.html", 3400), "sabores": ("sabores.html", 3000), "eventos": ("eventos.html", 4200), "vori": ("vori-vori.html", 3000), "historia": ("historia.html", 3000)}
with sync_playwright() as pw:
    nav = pw.chromium.launch()
    ctx = nav.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, reduced_motion="reduce", is_mobile=True, has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('loren-cookies', JSON.stringify({v:1,fecha:Date.now(),mapas:false}))}catch(e){}")
    pg = ctx.new_page()
    for k, (url, alto) in PAGINAS.items():
        pg.goto(f"{BASE}/{url}", wait_until="load")
        pg.wait_for_timeout(2500)
        pg.add_style_tag(content=".cookies,.loader{display:none!important} *{animation:none!important}")
        pg.evaluate("document.querySelectorAll('.rv').forEach(e=>e.classList.add('is-in'))")
        pg.evaluate("window.scrollTo(0, document.body.scrollHeight)"); pg.wait_for_timeout(800); pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(500)
        pg.screenshot(path=os.path.join(SALIDA, f"pantalla_{k}.jpg"), full_page=True, type="jpeg", quality=88, clip={"x": 0, "y": 0, "width": 390, "height": alto})
        print(k, "ok")
    nav.close()
