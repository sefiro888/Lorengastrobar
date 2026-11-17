"""Intro (ñandutí + logo + «Hay sabores que nos hacen sentir en casa») que se une con un fundido al promo de tiles.
Uso: python herramientas/promo/intro_tiles.py <tiles.mp4> <carpeta_trabajo> <salida.mp4>"""
import os, sys, subprocess, shutil
from playwright.sync_api import sync_playwright
FF = os.path.join(os.path.dirname(sys.executable), "Lib", "site-packages", "imageio_ffmpeg", "binaries", "ffmpeg-win-x86_64-v7.1.exe")
TILES, TMP, SAL = sys.argv[1:4]
FPS, DUR, XF = 30, 5.4, 0.6
N = int(FPS * DUR)
os.makedirs(TMP, exist_ok=True)
if len([f for f in os.listdir(TMP) if f.endswith('.png')]) < N:
  with sync_playwright() as pw:
      nav = pw.chromium.launch(); pg = nav.new_page(viewport={"width": 1080, "height": 1920})
      pg.goto("http://localhost:8123/herramientas/promo/video7.html?p=1&n=7", wait_until="load")
      pg.wait_for_function("window.LISTO === true"); pg.wait_for_timeout(1500)
      for i in range(N):
          pg.evaluate(f"render({i / FPS})")
          pg.screenshot(path=os.path.join(TMP, f"{i:05d}.png"), type="png", omit_background=True)
      nav.close()
fondo = "img/kv/textura-oscura.webp"
intro = os.path.join(TMP, "intro.mp4")
filt = ("[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,eq=brightness=-0.12,setsar=1,fps=30[b];"
        "[b][1:v]overlay=0:0:format=auto,format=yuv420p[v]")
subprocess.run([FF, "-y", "-loglevel", "error", "-loop", "1", "-framerate", "30", "-t", str(DUR), "-i", fondo, "-framerate", str(FPS), "-i", os.path.join(TMP, "%05d.png"),
                "-filter_complex", filt, "-map", "[v]", "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-r", "30", "-t", str(DUR), intro], check=True)
filt2 = f"[0:v]settb=AVTB,fps=30,format=yuv420p[a];[1:v]settb=AVTB,fps=30,format=yuv420p[b];[a][b]xfade=transition=fade:duration={XF}:offset={DUR - XF}[v]"
subprocess.run([FF, "-y", "-loglevel", "error", "-i", intro, "-i", TILES, "-filter_complex", filt2, "-map", "[v]", "-an", "-c:v", "libx264", "-crf", "18",
                "-preset", "medium", "-movflags", "+faststart", SAL], check=True)
print("hecho", SAL, round(os.path.getsize(SAL) / 1e6, 1), "MB")
