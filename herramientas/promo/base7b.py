"""Base de vídeo de la parte 1 con DISOLVENCIAS (xfade) y ritmo uniforme: 7 escenas de L s con solape X s.
Uso: python base7b.py <carpeta_reels> <salida.mp4>"""
import os, subprocess, sys
FF = os.path.join(os.path.dirname(sys.executable), "Lib", "site-packages", "imageio_ffmpeg", "binaries", "ffmpeg-win-x86_64-v7.1.exe")
REELS, SAL = sys.argv[1], sys.argv[2]
FPS, L, X = 24, 6.5, 1.2
TRAMOS = [(None, 0, +0), ("DIwE2CFMYMI", 0.5, +1), ("DfRzpyRspVP", 35.0, +1), ("DdCWXbbM0z1", 80.0, +1),
          ("DIwE2CFMYMI", 10.0, -1), ("DfRzpyRspVP", 22.0, -1), (None, 0, 0)]
entradas, filtros = [], []
for i, (r, a, z) in enumerate(TRAMOS):
    d = L + (X / 2 if i in (0, len(TRAMOS) - 1) else X)
    if r is None:
        filtros.append(f"color=c=black:s=1080x1920:r={FPS}:d={d},format=yuv420p,settb=AVTB,fps={FPS}[t{i}]")
    else:
        n = len(entradas) // 6
        entradas += ["-ss", str(a), "-t", str(d), "-i", os.path.join(REELS, r + ".mp4")]
        k = 0.06
        zexp = f"(1+{k}*t/{d})" if z > 0 else f"(1+{k}-{k}*t/{d})"
        filtros.append(f"[{n}:v]fps={FPS},setpts=PTS-STARTPTS,scale=w='1080*{zexp}':h='1920*{zexp}':eval=frame,crop=1080:1920,"
                       f"eq=contrast=1.08:saturation=1.2:brightness=-0.03,unsharp=5:5:0.7,setsar=1,format=yuv420p,settb=AVTB,fps={FPS}[t{i}]")
prev = "[t0]"
for i in range(1, len(TRAMOS)):
    off = round(i * L - X / 2, 3)
    filtros.append(f"{prev}[t{i}]xfade=transition=fade:duration={X}:offset={off}[x{i}]")
    prev = f"[x{i}]"
cmd = [FF, "-y", "-loglevel", "error"] + entradas + ["-filter_complex", ";".join(filtros), "-map", prev, "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-t", str(len(TRAMOS) * L), SAL]
subprocess.run(cmd, check=True)
print("ok", SAL, round(os.path.getsize(SAL) / 1e6, 1), "MB")
