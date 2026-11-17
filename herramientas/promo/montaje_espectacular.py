"""Montaje espectacular con material REAL de Loren (sin IA): transiciones xfade, zoom lento,
textos animados, voces de Loren, polca y cierre con logo.
Uso: python herramientas/promo/montaje_espectacular.py <carpeta_trabajo> <salida.mp4>
"""
import os, sys, subprocess

FF = r"C:\Users\sefir\AppData\Local\Programs\Python\Python312\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TMP, SAL = sys.argv[1], sys.argv[2]
FONT = "C\\:/Windows/Fonts/arialbd.ttf"
FPS = 30
XF = 0.35                     # duración de cada transición (s)
os.makedirs(TMP, exist_ok=True)

# (archivo, inicio en origen, duración, texto)
PLANOS = [
    ("video/loren-vori.mp4",         2.0, 5.0, "Mba’éichapa"),
    ("video/mbeju.mp4",              3.0, 5.5, "Tembi’u"),
    ("video/sopa.mp4",               0.0, 5.0, "Sopa paraguaya"),
    ("video/chipa.mp4",              4.0, 5.5, "Chipa guazú"),
    ("video/chyryry.mp4",            0.0, 4.5, "Chyryry"),
    ("video/loren-sabores.mp4",      0.0, 4.5, ""),  # trae su propio subtítulo
]
TRANSICIONES = ["circleopen", "wipeleft", "slideup", "radial", "pixelize", "fadewhite", "circlecrop"]
VOZ_INICIO = ("audio/mbaeichapa.mp3", "audio/tembiu.mp3")
VOZ_CIERRE = "audio/aguyje.mp3"
CIERRE = 5.0
MUSICA = os.path.join(RAIZ, "para-loren", "promo", "polca-original.wav")
LOGO = os.path.join(RAIZ, "img", "marca", "logo-loren.webp")


def fuente_texto(t):
    """Texto con entrada animada (sube y aparece) y salida suave."""
    if not t:
        return ""
    tam = 118 if len(t) <= 12 else 84
    return (f",drawtext=fontfile='{FONT}':text='{t}':fontcolor=0xF3EEDC:fontsize={tam}:"
            f"x=(w-text_w)/2:y=h*0.12+60*(1-min(t/0.45\\,1))*(1-min(t/0.45\\,1)):"
            f"alpha='min(t/0.35\\,1)*(1-max((t-{{OUT}})/0.4\\,0))':"
            f"borderw=6:bordercolor=0x2B1B0E:enable='between(t\\,0\\,{{FIN}})'")


# 1) planos: zoom lento + color cálido + textos
segs = []
for i, (src, ini, dur, txt) in enumerate(PLANOS):
    out = os.path.join(TMP, f"p{i}.mp4")
    z = f"(1+0.07*t/{dur})"
    t_txt = fuente_texto(txt).replace("{OUT}", f"{dur-0.7:.2f}").replace("{FIN}", f"{dur:.2f}")
    vf = (f"fps={FPS},scale=w='1080*{z}':h='1920*{z}':eval=frame,crop=1080:1920,setsar=1,"
          f"eq=contrast=1.08:saturation=1.18:brightness=-0.02,"
          f"colorbalance=rs=0.05:gs=0.01:bs=-0.04,vignette=PI/5,format=yuv420p" + t_txt)
    subprocess.run([FF, "-y", "-loglevel", "error", "-ss", str(ini), "-t", str(dur),
                    "-i", os.path.join(RAIZ, src), "-vf", vf, "-an",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "17", out], check=True)
    segs.append((out, dur))

# 2) cierre: fondo carbón, logo y web
card = os.path.join(TMP, "cierre.mp4")
subprocess.run([FF, "-y", "-loglevel", "error",
                "-f", "lavfi", "-i", f"color=c=0x1C1A18:s=1080x1920:r={FPS}:d={CIERRE}",
                "-i", LOGO, "-filter_complex",
                "[1:v]scale=700:-1,format=rgba[lg];"
                "[0:v][lg]overlay=(W-w)/2:(H-h)/2-160:format=auto,"
                f"drawtext=fontfile='{FONT}':text='lorenrestobar.com':fontcolor=0xF3EEDC:fontsize=64:"
                "x=(w-text_w)/2:y=h*0.62,"
                f"fade=t=in:st=0:d=0.5,fade=t=out:st={CIERRE-0.5}:d=0.5[v]",
                "-map", "[v]", "-t", str(CIERRE), "-c:v", "libx264", "-pix_fmt", "yuv420p", card], check=True)
segs.append((card, CIERRE))

# 3) encadenar con xfade (transiciones alternas)
entradas = []
for p, _ in segs:
    entradas += ["-i", p]
filtros, prev, acumulado = [], "[0:v]", segs[0][1]
cortes_t = []
for i in range(1, len(segs)):
    tr = TRANSICIONES[(i - 1) % len(TRANSICIONES)]
    off = acumulado - XF
    salida = f"[x{i}]" if i < len(segs) - 1 else "[vx]"
    filtros.append(f"{prev}[{i}:v]xfade=transition={tr}:duration={XF}:offset={off:.2f}{salida}")
    prev = salida
    cortes_t.append(off)
    acumulado += segs[i][1] - XF
total = acumulado

# 3b) estilo de la referencia: líneas blancas que barren el encuadre + destello en cada corte
from PIL import Image
BARV = os.path.join(TMP, "barra_v.png"); BARH = os.path.join(TMP, "barra_h.png")
Image.new("RGBA", (7, 1920), (255, 255, 255, 255)).save(BARV)
Image.new("RGBA", (1080, 5), (255, 255, 255, 255)).save(BARH)
MUS_IDX = len(segs) + len(VOZ_INICIO) + 1          # índice de la polca (ver sección 4)
IDX_V, IDX_H = MUS_IDX + 1, MUS_IDX + 2             # barras añadidas al final de las entradas
nC = len(cortes_t)
filtros.append(f"[{IDX_V}:v]format=rgba,split={nC}" + "".join(f"[bv{k}]" for k in range(nC)))
filtros.append(f"[{IDX_H}:v]format=rgba,split={nC}" + "".join(f"[bh{k}]" for k in range(nC)))
prev = "[vx]"
for k, off in enumerate(cortes_t):
    o1 = f"[l{k}]"
    filtros.append(f"{prev}[bv{k}]overlay=x='(t-{off:.2f})/{XF}*1100-40':y=0:eval=frame:"
                   f"enable='between(t,{off:.2f},{off+XF:.2f})'{o1}")
    prev = o1
    o2 = f"[h{k}]"
    filtros.append(f"{prev}[bh{k}]overlay=x=0:y='(t-{off+0.1:.2f})/{XF}*1920':eval=frame:"
                   f"enable='between(t,{off+0.1:.2f},{off+XF+0.1:.2f})'{o2}")
    prev = o2
    o3 = f"[e{k}]"
    filtros.append(f"{prev}eq=brightness=0.18:enable='between(t,{off:.2f},{off+0.12:.2f})'{o3}")
    prev = o3
filtros.append(f"{prev}null[v]")

# 4) audio: voces de Loren en cada inicio + cierre, polca de fondo
mezcla = []
entradas_a = list(entradas)
voces = []
inicio_plano = 0.0
for i, (p, dur) in enumerate(segs[:-1]):
    voces_plano = {0: VOZ_INICIO[0], 1: VOZ_INICIO[1]}
    if i in voces_plano:
        voces.append((voces_plano[i], inicio_plano + 0.2))
    inicio_plano += dur - XF
voces.append((VOZ_CIERRE, inicio_plano + 0.2))
for j, (a, t0) in enumerate(voces, start=len(segs)):
    entradas_a += ["-i", os.path.join(RAIZ, a)]
    ms = int(t0 * 1000)
    filtros.append(f"[{j}:a]adelay={ms}|{ms},volume=1.6[v{j}]")
    mezcla.append(f"[v{j}]")
mus = len(segs) + len(voces)
entradas_a += ["-stream_loop", "-1", "-i", MUSICA]
entradas_a += ["-loop", "1", "-framerate", str(FPS), "-i", BARV]
entradas_a += ["-loop", "1", "-framerate", str(FPS), "-i", BARH]
filtros.append(f"[{mus}:a]atrim=0:{total:.2f},asetpts=PTS-STARTPTS,volume=0.25,"
               f"afade=t=out:st={total-1.5:.2f}:d=1.5[m]")
mezcla.append("[m]")
filtros.append(f"{''.join(mezcla)}amix=inputs={len(mezcla)}:normalize=0:duration=longest[aud]")

subprocess.run([FF, "-y", "-loglevel", "error", *entradas_a,
                "-filter_complex", ";".join(filtros),
                "-map", "[v]", "-map", "[aud]", "-t", f"{total:.2f}",
                "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "192k", SAL], check=True)
print("hecho:", SAL, f"{total:.1f}s")
