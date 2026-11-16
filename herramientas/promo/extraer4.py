"""Extrae los fotogramas (30 fps) de los tramos del vídeo de la receta para la animación del reel 4.
Uso: python herramientas/promo/extraer4.py <video_original.mp4>   → para-loren/promo/frames4/<tramo>/0000.jpg ..."""
import os, sys, shutil, subprocess
FF = os.path.join(os.path.dirname(sys.executable), "Lib", "site-packages", "imageio_ffmpeg", "binaries", "ffmpeg-win-x86_64-v7.1.exe")
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SAL = os.path.join(RAIZ, "para-loren", "promo", "frames4")
ORIG = sys.argv[1]
# nombre: (desde, duración en el original, velocidad)   — velocidad <1 = cámara lenta (se mezclan fotogramas)
TRAMOS = {
    "hook":     (67.0, 1.6, 0.6),
    "griselda": (0.5, 3.4, 1.0),
    "jamon":    (6.0, 3.4, 1.0),
    "bechamel": (9.3, 3.4, 1.0),
    "masa":     (19.5, 3.4, 1.0),
    "relleno":  (38.5, 3.4, 1.0),
    "cerrar":   (43.5, 3.4, 1.0),
    "frita":    (56.0, 3.4, 1.0),
    "queso":    (66.3, 3.4, 0.6),
}
shutil.rmtree(SAL, ignore_errors=True); os.makedirs(SAL)
for n, (a, d, v) in TRAMOS.items():
    os.makedirs(os.path.join(SAL, n))
    vf = "scale=576:1024:flags=lanczos"
    if v < 1:
        vf = f"setpts=PTS/{v},minterpolate=fps=30:mi_mode=blend,{vf}"
        d_out = d
    else:
        vf = f"fps=30,{vf}"
    subprocess.run([FF, "-y", "-loglevel", "error", "-ss", str(a), "-t", str(d), "-i", ORIG, "-vf", vf, "-q:v", "3", os.path.join(SAL, n, "%04d.jpg")], check=True)
    print(n, len(os.listdir(os.path.join(SAL, n))), "fotogramas")
