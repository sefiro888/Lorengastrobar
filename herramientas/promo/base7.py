"""Pista de vídeo base del promo 2: recortes de los reels de Loren (720p) con zoom lento y color; negro en las escenas gráficas.
Uso: python herramientas/promo/base2.py <carpeta_con_reels> <salida.mp4>"""
import os, subprocess, sys
FF = os.path.join(os.path.dirname(sys.executable), "Lib", "site-packages", "imageio_ffmpeg", "binaries", "ffmpeg-win-x86_64-v7.1.exe")
REELS, SAL = sys.argv[1], sys.argv[2]
FPS = 24
# (reel, desde, hasta, zoom) ; None = negro
TRAMOS = [
    (None, 0, 6.0, 0),
    ("DIwE2CFMYMI", 0.5, 8.0, +1),
    ("DfRzpyRspVP", 35.0, 42.5, +1),
    ("DdCWXbbM0z1", 80.0, 88.0, -1),
    ("DIwE2CFMYMI", 10.0, 16.5, +1),
    ("DfRzpyRspVP", 22.0, 28.5, -1),
    (None, 0, 6.0, 0),
]
entradas, filtros, etiquetas = [], [], []
for i, (r, a, b, z) in enumerate(TRAMOS):
    d = b - a if r else b
    if r is None:
        filtros.append(f"color=c=black:s=1080x1920:r={FPS}:d={d}[t{i}]")
    else:
        entradas += ["-ss", str(a), "-t", str(d), "-i", os.path.join(REELS, r + ".mp4")]
        n = len([1 for x in TRAMOS[:i] if x[0]])  # índice de entrada
        k = 0.075
        zexp = f"(1+{k}*t/{d})" if z > 0 else f"(1+{k}-{k}*t/{d})"
        filtros.append(
            f"[{n}:v]fps={FPS},setpts=PTS-STARTPTS,scale=w='1080*{zexp}':h='1920*{zexp}':eval=frame,crop=1080:1920,"
            f"eq=contrast=1.08:saturation=1.2:brightness=-0.03,unsharp=5:5:0.7,noise=alls=7:allf=t,setsar=1,format=yuv420p[t{i}]")
    etiquetas.append(f"[t{i}]")
filtros.append("".join(etiquetas) + f"concat=n={len(TRAMOS)}:v=1:a=0[v]")
cmd = [FF, "-y", "-loglevel", "error"] + entradas + ["-filter_complex", ";".join(filtros), "-map", "[v]", "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", SAL]
subprocess.run(cmd, check=True)
print("ok", SAL, round(os.path.getsize(SAL) / 1e6, 1), "MB")
