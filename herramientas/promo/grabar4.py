"""Graba el reel 4 (35 s): fotogramas → ffmpeg con música y efectos.
Uso: python grabar4.py <carpeta_fotogramas> <musica.m4a> <inicio_musica_s> <salida.mp4>"""
import os, sys, subprocess, glob, shutil
from playwright.sync_api import sync_playwright
FF = os.path.join(os.path.dirname(sys.executable), "Lib", "site-packages", "imageio_ffmpeg", "binaries", "ffmpeg-win-x86_64-v7.1.exe")
TMP, MUS, INI, SAL = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
HTML = sys.argv[5] if len(sys.argv) > 5 else "video4.html"
FPS, DUR = 30, 35; N = FPS * DUR
AQUI = os.path.dirname(os.path.abspath(__file__))
if len(glob.glob(os.path.join(TMP, "*.jpg"))) < N:
    shutil.rmtree(TMP, ignore_errors=True); os.makedirs(TMP)
    with sync_playwright() as pw:
        nav = pw.chromium.launch(); pg = nav.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto(f"http://localhost:8123/herramientas/promo/{HTML}", wait_until="load")
        pg.wait_for_function("window.LISTO === true"); pg.wait_for_timeout(1000)
        for i in range(N):
            pg.evaluate(f"render({i / FPS})"); pg.evaluate("window.esperar()")
            pg.screenshot(path=os.path.join(TMP, f"{i:05d}.jpg"), type="jpeg", quality=93)
            if i % 100 == 0: print("fotograma", i, flush=True)
        nav.close()
sfx = os.path.join(TMP, "sfx.wav"); subprocess.run([sys.executable, os.path.join(AQUI, "sfx4.py"), sfx], check=True)
filt = (f"[1:a]loudnorm=I=-16:TP=-1.5:LRA=9,afade=t=in:st=0:d=0.8,afade=t=out:st=32:d=3,atrim=0:{DUR}[m];"
        f"[2:a]volume=0.8[x];[m][x]amix=inputs=2:normalize=0,atrim=0:{DUR}[a]")
subprocess.run([FF, "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(TMP, "%05d.jpg"),
                "-ss", str(INI), "-t", str(DUR + 1), "-i", MUS, "-i", sfx, "-filter_complex", filt, "-map", "0:v", "-map", "[a]",
                "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-t", str(DUR), SAL], check=True)
print("hecho:", SAL, round(os.path.getsize(SAL) / 1e6, 1), "MB")
