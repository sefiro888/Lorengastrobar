"""Re-edita el reel de la empanada de jamón y queso: gancho, cortes en silencios, marca y cierre.
Uso: python herramientas/promo/reel_empanada.py <video_original.mp4> <carpeta_trabajo> <salida.mp4>   (servidor local en el 8123)"""
import os, sys, subprocess, shutil
from playwright.sync_api import sync_playwright
FF = os.path.join(os.path.dirname(sys.executable), "Lib", "site-packages", "imageio_ffmpeg", "binaries", "ffmpeg-win-x86_64-v7.1.exe")
ORIG, TMP, SAL = sys.argv[1], sys.argv[2], sys.argv[3]
FPS = 30
HOOK = (65.45, 68.45)                     # el queso que se estira (3 s)
CUERPO = [(0.40, 12.85), (18.30, 27.45), (37.55, 48.95), (50.10, 57.85), (59.95, 74.20)]   # cortes en silencios
D_HOOK, D_CUERPO, D_FIN = 3.0, sum(b - a for a, b in CUERPO), 4.4
TOTAL = D_HOOK + D_CUERPO + D_FIN
print("duración total", round(TOTAL, 1))
os.makedirs(TMP, exist_ok=True)
# 1) capas gráficas con transparencia (sólo los instantes que se usan)
def capa(nombre, dur):
    d = os.path.join(TMP, nombre)
    if os.path.isdir(d) and len(os.listdir(d)) >= int(dur * FPS): return d
    shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    with sync_playwright() as pw:
        nav = pw.chromium.launch(); pg = nav.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto(f"http://localhost:8123/herramientas/promo/capas3.html?capa={nombre}", wait_until="load")
        pg.wait_for_function("window.LISTO === true"); pg.wait_for_timeout(1200)
        for i in range(int(dur * FPS)):
            pg.evaluate(f"render({i / FPS})"); pg.screenshot(path=os.path.join(d, f"{i:04d}.png"), type="png", omit_background=True)
        nav.close()
    return d
dh, dl, df = capa("hook", D_HOOK), capa("lt", 4.0), capa("fin", D_FIN)
# 2) vídeo base: gancho + cuerpo + congelado para el cierre
vf = (f"scale=1080:1920:flags=lanczos,eq=contrast=1.07:saturation=1.18:brightness=-0.02,unsharp=5:5:0.8,"
      f"curves=r='0/0 0.5/0.53 1/1':b='0/0 0.5/0.47 1/1',setsar=1,fps={FPS},format=yuv420p")
entradas_seg = [HOOK] + CUERPO          # cada tramo es una entrada distinta (-ss/-t): evita bloqueos de ffmpeg
filt = []
for i, (a, b) in enumerate(entradas_seg):
    filt.append(f"[{i}:v]setpts=PTS-STARTPTS,{vf}[s{i}]")
filt.append("".join(f"[s{i}]" for i in range(len(entradas_seg))) + f"concat=n={len(entradas_seg)}:v=1:a=0,tpad=stop_mode=clone:stop_duration={D_FIN}[base]")
for i, (a, b) in enumerate(CUERPO):
    k = i + 1; fa = 0.04
    filt.append(f"[{k}:a]asetpts=PTS-STARTPTS,afade=t=in:st=0:d={fa},afade=t=out:st={b - a - fa}:d={fa}[a{i}]")
filt.append("".join(f"[a{i}]" for i in range(len(CUERPO))) + f"concat=n={len(CUERPO)}:v=0:a=1,highpass=f=90,afftdn=nr=14,acompressor=threshold=-20dB:ratio=3:attack=15:release=250,loudnorm=I=-14:TP=-1.5:LRA=9,adelay={int(D_HOOK * 1000)}|{int(D_HOOK * 1000)},apad=whole_dur={TOTAL}[voz]")
filt.append(f"anoisesrc=d=1.0:c=pink:r=44100,highpass=f=600,lowpass=f=6500,afade=t=in:st=0:d=0.9,afade=t=out:st=0.9:d=0.1,volume=0.35,adelay=2000|2000,apad=whole_dur={TOTAL}[whoosh]")
filt.append("[voz][whoosh]amix=inputs=2:normalize=0,atrim=0:" + str(TOTAL) + "[audio]")
# 3) paso A: vídeo base + audio (sin capas)
BASEF = os.path.join(TMP, "base.mp4")
filt.append("[base]null[vb]")
cmdA = [FF, "-y", "-loglevel", "error"]
for a_, b_ in entradas_seg:
    cmdA += ["-ss", str(a_), "-t", str(round(b_ - a_, 3)), "-i", ORIG]
cmdA += ["-filter_complex", ";".join(filt), "-map", "[vb]", "-map", "[audio]", "-c:v", "libx264", "-preset", "fast", "-crf", "14", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-t", str(TOTAL), BASEF]
print("paso A: base…", flush=True); subprocess.run(cmdA, check=True)
# 4) paso B: una sola secuencia de capas a lo largo de todo el vídeo (los huecos son PNG transparentes)
TL = os.path.join(TMP, "linea"); N = int(TOTAL * FPS)
if not os.path.isdir(TL) or len(os.listdir(TL)) < N:
    shutil.rmtree(TL, ignore_errors=True); os.makedirs(TL)
    from PIL import Image
    vacio = os.path.join(TMP, "vacio.png"); Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)).save(vacio)
    asign = {}
    for nombre, d, ini in (("hook", dh, 0.0), ("lt", dl, D_HOOK + 0.4), ("fin", df, D_HOOK + D_CUERPO - 0.45)):
        for k, f in enumerate(sorted(os.listdir(d))):
            asign[int(round(ini * FPS)) + k] = os.path.join(d, f)
    for i in range(N):
        shutil.copyfile(asign.get(i, vacio), os.path.join(TL, f"{i:05d}.png"))
# 5) paso C: capas + logo
cmdC = [FF, "-y", "-loglevel", "error", "-i", BASEF, "-framerate", str(FPS), "-i", os.path.join(TL, "%05d.png"),
        "-loop", "1", "-framerate", str(FPS), "-t", str(TOTAL), "-i", os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "img", "marca", "logo-loren.webp"),
        "-filter_complex", f"[0:v][1:v]overlay=0:0:eof_action=pass[b];[2:v]format=rgba,scale=150:-1,colorchannelmixer=aa=0.92[lg];[b][lg]overlay=x=W-w-70:y=120:enable='between(t,{D_HOOK},{D_HOOK + D_CUERPO})':shortest=1,format=yuv420p[v]",
        "-map", "[v]", "-map", "0:a", "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-c:a", "copy", "-movflags", "+faststart", "-t", str(TOTAL), SAL]
print("paso C: capas…", flush=True); subprocess.run(cmdC, check=True)
print("hecho:", SAL, round(os.path.getsize(SAL) / 1e6, 1), "MB")
