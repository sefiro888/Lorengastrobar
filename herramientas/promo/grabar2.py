"""Graba el promo 2 de Instagram (1080x1920, 24 fps, 78 s): capa gráfica con transparencia sobre la pista base de vídeo.
Uso: python herramientas/promo/grabar2.py <base.mp4> <carpeta_frames> <salida.mp4>   (servidor local en el puerto 8123)"""
import os, sys, subprocess, shutil, glob
from playwright.sync_api import sync_playwright
FF = os.path.join(os.path.dirname(sys.executable), "Lorengastrobarbarcelona" if False else "Lib", "site-packages", "imageio_ffmpeg", "binaries", "ffmpeg-win-x86_64-v7.1.exe")
BASE, TMP, SAL = sys.argv[1], sys.argv[2], sys.argv[3]
FPS, DUR = 24, 78
N = FPS * DUR
if len(glob.glob(os.path.join(TMP, "*.png"))) < N:
    shutil.rmtree(TMP, ignore_errors=True); os.makedirs(TMP)
    with sync_playwright() as pw:
        nav = pw.chromium.launch(); pg = nav.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto("http://localhost:8123/herramientas/promo/video2.html", wait_until="load")
        pg.wait_for_function("window.LISTO === true"); pg.wait_for_timeout(1500)
        for i in range(N):
            pg.evaluate(f"render({i / FPS})")
            pg.screenshot(path=os.path.join(TMP, f"{i:05d}.png"), type="png", omit_background=True)
            if i % 120 == 0: print("fotograma", i, flush=True)
        nav.close()
subprocess.run([FF, "-y", "-loglevel", "error", "-i", BASE, "-framerate", str(FPS), "-i", os.path.join(TMP, "%05d.png"),
                "-filter_complex", "[0:v][1:v]overlay=0:0:format=auto,format=yuv420p[v]", "-map", "[v]", "-c:v", "libx264", "-preset", "slow", "-crf", "17",
                "-r", str(FPS), "-movflags", "+faststart", "-t", str(DUR), SAL], check=True)
print("hecho:", SAL, round(os.path.getsize(SAL) / 1e6, 1), "MB")
