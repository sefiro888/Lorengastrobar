"""Segundo lote de material de Loren (fotos del fotógrafo, reportaje de SNT y vídeo de receta) -> v2/img/nuevo y v2/video.
Los originales se guardan en materialnuevo/lote2/ (no se suben al repositorio).
Uso: python herramientas/v2_material2.py <carpeta con las imágenes pegadas> <carpeta de descargas>
"""
import os, shutil, subprocess, sys, glob
from PIL import Image
import imageio_ffmpeg

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIG = os.path.join(R, "materialnuevo", "lote2")
O = os.path.join(R, "v2", "img", "nuevo")
VO = os.path.join(R, "v2", "video")
for d in (ORIG, O, VO):
    os.makedirs(d, exist_ok=True)

IMGS, DESC = sys.argv[1], sys.argv[2]
FOTOS = {  # número de imagen pegada -> nombre, recorte (fracciones izq, arr, der, abj) o None, lado máximo
    23: ("chorizo", None, 1400),
    24: ("fanny-jennifer", None, 1300),
    26: ("jose-terraza", None, 1300),
    28: ("loren-empanada", None, 1300),
    29: ("noquis", None, 1400),
    31: ("yuca-brava", (0.03, 0.04, 0.80, 1.0), 1400),  # sin el logo de la esquina
}
for n, (nombre, rec, lado) in FOTOS.items():
    src = glob.glob(os.path.join(IMGS, f"{n}.*"))[0]
    shutil.copy(src, os.path.join(ORIG, nombre + os.path.splitext(src)[1]))
    im = Image.open(src).convert("RGB")
    if rec:
        w, h = im.size
        im = im.crop((int(w * rec[0]), int(h * rec[1]), int(w * rec[2]), int(h * rec[3])))
    im.thumbnail((lado, lado), Image.LANCZOS)
    im.save(os.path.join(O, nombre + ".webp"), "WEBP", quality=82, method=6)
    print(nombre, im.size)

FF = imageio_ffmpeg.get_ffmpeg_exe()
VIDEOS = {
    # Reportaje de SNT: sólo el fragmento en que habla Loren (con su sonido), con crédito en la web
    "snt-loren": ("WhatsApp Video 2026-11-09 at 19.19.03.mp4", ["-ss", "160", "-t", "22"], "scale=640:-2", "8"),
    # Receta completa con la voz de la cocina
    "receta-chipa": ("WhatsApp Video 2026-11-09 at 19.13.57.mp4", [], "scale=480:-2", "52"),
}
for n, (f, corte, esc, poster) in VIDEOS.items():
    src = os.path.join(DESC, f)
    shutil.copy(src, os.path.join(ORIG, f))
    dst = os.path.join(VO, n + ".mp4")
    subprocess.run([FF, "-y", "-loglevel", "error", *corte, "-i", src, "-vf", esc, "-c:v", "libx264", "-preset", "slow", "-crf", "26",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", dst], check=True)
    subprocess.run([FF, "-y", "-loglevel", "error", "-ss", poster, "-i", dst, "-frames:v", "1", "-q:v", "4", os.path.join(VO, n + ".jpg")], check=True)
    print("vídeo", n, os.path.getsize(dst) // 1024, "KB")
