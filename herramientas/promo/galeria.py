"""Galería espectacular (foto ENTERA, sin recortes, con brasas, anillo y brillo).
Uso: python herramientas/promo/galeria.py <milanesas|raices|clips> <salida.mp4> [carpeta_reels_720p, sólo clips]   (servidor local en el 8123). Sin música."""
import os, sys, subprocess
from playwright.sync_api import sync_playwright
FF = os.path.join(os.path.dirname(sys.executable), "Lib", "site-packages", "imageio_ffmpeg", "binaries", "ffmpeg-win-x86_64-v7.1.exe")
V, SAL = sys.argv[1], sys.argv[2]
REELS = sys.argv[3] if len(sys.argv) > 3 else ""      # carpeta con los reels 720p (sólo para el tema «clips»)
FPS = 30
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
VID = lambda f: os.path.join(RAIZ, "video", f)
DESC = r"C:/Users/sefir/Downloads/WhatsApp Video 2026-11-16 at 23.44.37.mp4"
# clips del tema «clips»: id -> (archivo, inicio_s)
CLIPS = {
    "chipa": (VID("chipa.mp4"), 6.0), "mbeju": (VID("mbeju.mp4"), 43.0), "chyryry": (VID("chyryry.mp4"), 21.0),
    "vori": (os.path.join(REELS, "DdCWXbbM0z1.mp4"), 80.5), "mila": (os.path.join(REELS, "DPjAK4zjC51.mp4"), 40.5),
    "sopa": (VID("sopa.mp4"), 3.0), "empanada": (DESC, 66.3), "mbeju2": (VID("mbeju.mp4"), 35.5),
}
CARPETA = os.path.join(AQUI, "_clips")
if V == "clips":
    import shutil
    shutil.rmtree(CARPETA, ignore_errors=True)
    for cid, (ruta, ini) in CLIPS.items():
        d = os.path.join(CARPETA, cid); os.makedirs(d)
        subprocess.run([FF, "-y", "-loglevel", "error", "-ss", str(ini), "-t", "3.5", "-i", ruta, "-vf", f"fps={FPS},scale=720:-2", "-frames:v", "105", "-q:v", "3", os.path.join(d, "%04d.jpg")], check=True)
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
        pg.evaluate("Promise.all(window._pend.map((m) => m.decode().catch(() => 0))).then(() => { window._pend = []; })")
        proc.stdin.write(pg.screenshot(type="jpeg", quality=95))
        if i % 150 == 0:
            print("fotograma", i, "de", NF, flush=True)
    nav.close()
proc.stdin.close()
proc.wait()
if V == 'clips':
    import shutil; shutil.rmtree(CARPETA, ignore_errors=True)
print("hecho:", SAL, round(os.path.getsize(SAL) / 1e6, 1), "MB ·", round(dur, 1), "s")
