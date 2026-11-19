"""Reel de Navidad (combos de bocaditos) · 1080×1920, 30 fps, H.264 yuv420p, SIN música.
Uso: python herramientas/promo/navidad_video.py [salida.mp4]
Arranca su propio servidor local. Datos: herramientas/navidad_datos.py · plantilla: navidad_video.html."""
import json, os, subprocess, sys, time
from playwright.sync_api import sync_playwright

AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "herramientas"))
from navidad_datos import COMBOS, WHATSAPP, WEB

FF = os.path.join(os.path.dirname(sys.executable), "Lib", "site-packages", "imageio_ffmpeg", "binaries", "ffmpeg-win-x86_64-v7.1.exe")
SAL = sys.argv[1] if len(sys.argv) > 1 else os.path.join(RAIZ, "para-loren", "navidad", "5-video", "reel-navidad-combos.mp4")
os.makedirs(os.path.dirname(SAL), exist_ok=True)
FPS, PUERTO = 30, 8124
DATOS = {"combos": COMBOS, "whatsapp": WHATSAPP, "web": WEB}

srv = subprocess.Popen([sys.executable, "-m", "http.server", str(PUERTO), "--bind", "127.0.0.1", "--directory", RAIZ],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.2)
try:
    with sync_playwright() as pw:
        nav = pw.chromium.launch()
        pg = nav.new_page(viewport={"width": 1080, "height": 1920})
        pg.add_init_script("window.DATOS = " + json.dumps(DATOS, ensure_ascii=False) + ";")
        pg.goto(f"http://127.0.0.1:{PUERTO}/herramientas/promo/navidad_video.html", wait_until="load")
        pg.wait_for_function("window.LISTO === true"); pg.wait_for_timeout(600)
        dur = pg.evaluate("window.DUR"); NF = int(dur * FPS)
        proc = subprocess.Popen([FF, "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-",
                                 "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p", "-an", "-movflags", "+faststart", SAL],
                                stdin=subprocess.PIPE)
        for i in range(NF):
            pg.evaluate(f"render({i / FPS})")
            proc.stdin.write(pg.screenshot(type="jpeg", quality=95))
            if i % 150 == 0:
                print("fotograma", i, "de", NF, flush=True)
        nav.close()
    proc.stdin.close(); proc.wait()
finally:
    srv.terminate()
print("hecho:", SAL, round(os.path.getsize(SAL) / 1e6, 1), "MB ·", round(dur, 1), "s")
