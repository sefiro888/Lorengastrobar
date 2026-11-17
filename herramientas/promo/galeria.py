"""Galería espectacular (foto ENTERA, sin recortes, con brasas, anillo y brillo).
Uso: python herramientas/promo/galeria.py <milanesas|raices> <salida.mp4>   (servidor local en el 8123). Sin música."""
import os, sys, subprocess
from playwright.sync_api import sync_playwright
FF = os.path.join(os.path.dirname(sys.executable), "Lib", "site-packages", "imageio_ffmpeg", "binaries", "ffmpeg-win-x86_64-v7.1.exe")
V, SAL = sys.argv[1], sys.argv[2]
FPS = 30
with sync_playwright() as pw:
    nav = pw.chromium.launch()
    pg = nav.new_page(viewport={"width": 1080, "height": 1920})
    pg.goto(f"http://localhost:8123/herramientas/promo/galeria.html?v={V}&n=3", wait_until="load")
    pg.wait_for_function("window.LISTO === true")
    pg.wait_for_timeout(800)
    dur = pg.evaluate("window.DUR")
    NF = int(dur * FPS)
    proc = subprocess.Popen([FF, "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-",
                             "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p", "-an", "-movflags", "+faststart", SAL], stdin=subprocess.PIPE)
    for i in range(NF):
        pg.evaluate(f"render({i / FPS})")
        proc.stdin.write(pg.screenshot(type="jpeg", quality=95))
        if i % 150 == 0:
            print("fotograma", i, "de", NF, flush=True)
    nav.close()
proc.stdin.close()
proc.wait()
print("hecho:", SAL, round(os.path.getsize(SAL) / 1e6, 1), "MB ·", round(dur, 1), "s")
