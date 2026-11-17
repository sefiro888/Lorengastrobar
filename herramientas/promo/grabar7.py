"""Graba una parte del promo dividido y le pone la canción. Uso: python grabar7.py <parte 1|2> <base.mp4> <frames> <musica.m4a> <inicio_s> <salida.mp4>"""
import os, sys, subprocess, shutil, glob
from playwright.sync_api import sync_playwright
FF = os.path.join(os.path.dirname(sys.executable), "Lib", "site-packages", "imageio_ffmpeg", "binaries", "ffmpeg-win-x86_64-v7.1.exe")
PARTE, BASE, TMP, MUS, INI, SAL = sys.argv[1:7]
FPS = 24
DUR = {"1": 48, "2": 42}[PARTE]; N = FPS * DUR
if len(glob.glob(os.path.join(TMP, "*.png"))) < N:
    shutil.rmtree(TMP, ignore_errors=True); os.makedirs(TMP)
    with sync_playwright() as pw:
        nav = pw.chromium.launch(); pg = nav.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto(f"http://localhost:8123/herramientas/promo/video7.html?p={PARTE}", wait_until="load")
        pg.wait_for_function("window.LISTO === true"); pg.wait_for_timeout(1500)
        for i in range(N):
            pg.evaluate(f"render({i / FPS})")
            pg.screenshot(path=os.path.join(TMP, f"{i:05d}.png"), type="png", omit_background=True)
            if i % 120 == 0: print("fotograma", i, flush=True)
        nav.close()
if PARTE == "1":     # base de vídeo real (parte 1)
    entrada_base = ["-i", BASE]
else:                # parte 2: fondo negro
    entrada_base = ["-f", "lavfi", "-i", f"color=c=black:s=1080x1920:r={FPS}:d={DUR}"]
musica = ["-ss", str(INI), "-t", str(DUR + 1), "-i", MUS]
filt = f"[0:v][1:v]overlay=0:0:format=auto,format=yuv420p[v];[2:a]loudnorm=I=-16:TP=-1.5:LRA=9,afade=t=in:st=0:d=1.0,afade=t=out:st={DUR - 3.5}:d=3.5,atrim=0:{DUR}[a]"
subprocess.run([FF, "-y", "-loglevel", "error"] + entrada_base + ["-framerate", str(FPS), "-i", os.path.join(TMP, "%05d.png")] + musica +
               ["-filter_complex", filt, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-t", str(DUR), SAL], check=True)
print("hecho:", SAL, round(os.path.getsize(SAL) / 1e6, 1), "MB")
