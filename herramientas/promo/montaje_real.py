"""Montaje del vídeo de Loren con material REAL (sin IA).
Uso: python herramientas/promo/montaje_real.py <carpeta_trabajo> <salida.mp4>
Requiere ffmpeg (el de imageio-ffmpeg). Lee vídeos de video/ y audios de audio/ y para-loren/promo/polca-original.wav.
"""
import os, sys, subprocess, shutil

FF = r"C:\Users\sefir\AppData\Local\Programs\Python\Python312\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TMP, SAL = sys.argv[1], sys.argv[2]
FONT = "C\\:/Windows/Fonts/arialbd.ttf"
os.makedirs(TMP, exist_ok=True)

# (archivo, inicio_en_origen, duracion, texto_en_pantalla)
CORTES = [
    ("video/loren-vori.mp4",          2.0, 4.0, "Mba’éichapa"),
    ("video/mbeju.mp4",               4.0, 8.0, "Tembi’u"),
    ("video/griselda-empanadas.mp4", 10.0, 7.0, ""),
    ("video/chipa.mp4",               4.0, 6.0, "Aguyje"),
    ("video/visitanos-local.mp4",     3.0, 5.0, "Un pedacito de Paraguay"),
]
# voz de Loren que suena al empezar cada corte (archivo, segundo dentro del montaje)
VOCES = [("audio/mbaeichapa.mp3", 0.2), ("audio/tembiu.mp3", 4.2),
          ("audio/aguyje.mp3", 19.2)]
MUSICA = os.path.join(RAIZ, "para-loren", "promo", "polca-original.wav")

def texto(t):
    if not t:
        return ""
    tam = 118 if len(t) <= 12 else 84
    return (f",drawtext=fontfile='{FONT}':text='{t}':fontcolor=0xF3EEDC:fontsize={tam}:"
            f"x=(w-text_w)/2:y=h*0.13:borderw=6:bordercolor=0x2B1B0E:"
            f"enable='between(t,0.2,3.2)'")

# 1) segmentos de vídeo 1080x1920, 30 fps, sin audio original
partes = []
for i, (src, ini, dur, t) in enumerate(CORTES):
    out = os.path.join(TMP, f"s{i}.mp4")
    vf = ("scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30,"
          "eq=contrast=1.06:saturation=1.12:brightness=-0.01,"
          f"fade=t=in:st=0:d=0.3,fade=t=out:st={dur-0.3:.2f}:d=0.3" + texto(t))
    subprocess.run([FF, "-y", "-loglevel", "error", "-ss", str(ini), "-t", str(dur),
                    "-i", os.path.join(RAIZ, src), "-vf", vf, "-an",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", out], check=True)
    partes.append(out)

# 1b) cierre: fondo carbón, logo y web (5 s)
LOGO = os.path.join(RAIZ, "img", "marca", "logo-loren.webp")
card = os.path.join(TMP, "card.mp4")
subprocess.run([FF, "-y", "-loglevel", "error",
                "-f", "lavfi", "-i", "color=c=0x1C1A18:s=1080x1920:r=30:d=5",
                "-i", LOGO,
                "-filter_complex",
                "[1:v]scale=700:-1,format=rgba[lg];"
                "[0:v][lg]overlay=(W-w)/2:(H-h)/2-160:format=auto,"
                f"drawtext=fontfile='{FONT}':text='lorenrestobar.com':fontcolor=0xF3EEDC:fontsize=64:"
                "x=(w-text_w)/2:y=h*0.62,"
                "fade=t=in:st=0:d=0.4,fade=t=out:st=4.6:d=0.4[v]",
                "-map", "[v]", "-t", "5", "-c:v", "libx264", "-pix_fmt", "yuv420p", card], check=True)
partes.append(card)
CIERRE = 5.0

lista = os.path.join(TMP, "lista.txt")
with open(lista, "w", encoding="utf-8") as f:
    for p in partes:
        f.write(f"file '{p.replace(chr(92), '/')}'\n")
video = os.path.join(TMP, "video.mp4")
subprocess.run([FF, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lista,
                "-c", "copy", video], check=True)
total = sum(d for _, _, d, _ in CORTES) + CIERRE

# 2) audio: voces de Loren + polca bajita, con retardos
entradas = ["-i", video]
filtros = []
mezcla = []
for j, (a, t0) in enumerate(VOCES, start=1):
    entradas += ["-i", os.path.join(RAIZ, a)]
    filtros.append(f"[{j}:a]adelay={int(t0*1000)}|{int(t0*1000)},volume=1.6[v{j}]")
    mezcla.append(f"[v{j}]")
n = len(VOCES) + 1
entradas += ["-stream_loop", "-1", "-i", MUSICA]
filtros.append(f"[{n}:a]atrim=0:{total:.2f},asetpts=PTS-STARTPTS,volume=0.22[m]")
mezcla.append("[m]")
filtros.append(f"{''.join(mezcla)}amix=inputs={len(mezcla)}:normalize=0:duration=longest[aud]")
subprocess.run([FF, "-y", "-loglevel", "error", *entradas,
                "-filter_complex", ";".join(filtros),
                "-map", "0:v", "-map", "[aud]", "-t", f"{total:.2f}",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", SAL], check=True)
print("hecho:", SAL, f"{total:.1f}s")
