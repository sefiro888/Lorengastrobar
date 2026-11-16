"""Graba el vídeo promocional de Instagram (1080x1920, 30 fps) y lo monta con ffmpeg y la voz de Loren.
Uso:  python herramientas/promo/grabar.py        (necesita el servidor local en el puerto 8123)
Salida: para-loren/promo/loren-web-nueva-instagram.mp4"""
import os, subprocess, sys, shutil, glob
from playwright.sync_api import sync_playwright
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FF = os.path.join(os.path.dirname(sys.executable), "Lib", "site-packages", "imageio_ffmpeg", "binaries", "ffmpeg-win-x86_64-v7.1.exe")
FPS, DUR = 30, 45
TMP = os.environ.get("PROMO_TMP") or os.path.join(RAIZ, "para-loren", "promo", "frames")
SAL = os.path.join(RAIZ, "para-loren", "promo", "loren-web-nueva-instagram.mp4")
if not os.path.isdir(TMP) or len(glob.glob(os.path.join(TMP, "*.jpg"))) < FPS * DUR:
    shutil.rmtree(TMP, ignore_errors=True); os.makedirs(TMP)
    with sync_playwright() as pw:
        nav = pw.chromium.launch()
        pg = nav.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto("http://localhost:8123/herramientas/promo/video.html", wait_until="load")
        pg.wait_for_function("window.LISTO === true"); pg.wait_for_timeout(1000)
        for i in range(FPS * DUR):
            pg.evaluate(f"render({i / FPS})")
            pg.screenshot(path=os.path.join(TMP, f"{i:05d}.jpg"), type="jpeg", quality=92)
            if i % 150 == 0: print("fotograma", i, flush=True)
        nav.close()
A = os.path.join(RAIZ, "audio")
voces = [("mbaeichapa.mp3", 0.9), ("tuicha.mp3", 18.4), ("aguyje.mp3", 40.6)]
entradas = ["-framerate", str(FPS), "-i", os.path.join(TMP, "%05d.jpg")]
filtro = []
for k, (f, t) in enumerate(voces):
    entradas += ["-i", os.path.join(A, f)]
    filtro.append(f"[{k + 1}:a]adelay={int(t * 1000)}|{int(t * 1000)},volume=1.6[v{k}]")
filtro.append("".join(f"[v{k}]" for k in range(len(voces))) + f"amix=inputs={len(voces)}:normalize=0,apad,atrim=0:{DUR}[a]")
cmd = [FF, "-y", "-loglevel", "error"] + entradas + ["-filter_complex", ";".join(filtro), "-map", "0:v", "-map", "[a]",
       "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "-t", str(DUR), SAL]
subprocess.run(cmd, check=True)
print("hecho:", SAL, round(os.path.getsize(SAL) / 1e6, 1), "MB")
