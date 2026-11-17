"""Reel de RECETA con técnicas de las «ideas pro» (para-loren/IDEAS-VIDEO-PRO.md):
  · gancho al inicio (el plato terminado) → pasos → vuelve al plato (bucle)
  · transición «whip pan» (barrido horizontal con desenfoque de movimiento) en vez de barrido de rectángulos
  · un dato por plano (rótulo «Paso n» + frase corta) y texto SIEMPRE en la zona segura de Instagram (y 250-1560)
  · sin música. Vídeo de origen: reel propio de Loren (vorí vorí).
Uso: python herramientas/promo/receta.py <reel_vori.mp4> <carpeta_trabajo> <salida.mp4>   (servidor local en el 8123)"""
import os, sys, subprocess, math
import numpy as np, cv2
from PIL import Image, ImageFilter
from playwright.sync_api import sync_playwright

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
FF = os.path.join(os.path.dirname(sys.executable), "Lib", "site-packages", "imageio_ffmpeg", "binaries", "ffmpeg-win-x86_64-v7.1.exe")
REEL, TMP, SAL = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(TMP, exist_ok=True)
W, H, FPS = 1080, 1920, 30
S, TW = 1.5, 0.32                  # duración de cada plano y de cada barrido (whip pan)
FINAL_EXTRA = 1.8                  # el último plano dura más para poder leer la dirección

# (inicio_s, rótulo pequeño, frase)  — el primero es el gancho (plato terminado) y el último repite el plato (bucle)
SHOTS = [
    (84.2, "", "Así se hace"),
    (4.0, "Paso 1", "La carne"),
    (9.0, "Paso 2", "Se enharina"),
    (16.5, "Paso 3", "Se sella bien"),
    (36.5, "Paso 4", "Cebolla"),
    (44.0, "Paso 5", "Tomate"),
    (52.0, "Paso 6", "Zanahoria"),
    (60.0, "Paso 7", "A cocer despacio"),
    (72.0, "Paso 8", "La masa de maíz"),
    (79.5, "Paso 9", "Las bolitas al caldo"),
    (84.2, "", "Vorí vorí"),
]
N = len(SHOTS)
DUR = [S] * (N - 1) + [S + FINAL_EXTRA]
TB = [0.0]
for d in DUR: TB.append(TB[-1] + d)          # TB[k] = inicio del plano k
TOTAL = TB[N]
NF = int(round(TOTAL * FPS))


def capas():
    base = '''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="../../css/fuentes.css">
<style>*{margin:0;padding:0;box-sizing:border-box}html,body{background:transparent;width:1080px}
.cap{width:1080px;height:430px;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;padding-bottom:70px;font-family:Montserrat}
.e{font-weight:800;font-size:40px;letter-spacing:.3em;text-transform:uppercase;color:#f4d27a;margin-bottom:14px;text-shadow:0 0 30px rgba(0,0,0,.95),0 3px 14px rgba(0,0,0,.9)}
.n{font-family:Anton;text-transform:uppercase;color:#f3eedc;font-size:112px;line-height:1.02;text-align:center;padding:0 50px;text-shadow:0 6px 30px rgba(0,0,0,.9),0 2px 6px rgba(0,0,0,.8)}
.l{width:180px;height:6px;border-radius:3px;background:#e8b43a;margin:20px 0 0;box-shadow:0 0 18px rgba(232,180,58,.7)}
.k{font-family:"Kaushan Script";color:#f4d27a;font-size:84px;line-height:1.1;margin-top:10px;-webkit-text-stroke:2px rgba(42,0,14,.55);paint-order:stroke fill;text-shadow:0 4px 24px rgba(0,0,0,.95),0 0 40px rgba(0,0,0,.8)}
.cta{width:1080px;height:420px;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;padding-bottom:30px;font-family:Montserrat;text-align:center;color:#f3eedc}
</style></head><body>'''
    with sync_playwright() as pw:
        nav = pw.chromium.launch(); pg = nav.new_page(viewport={"width": 1080, "height": 1920})
        for k, (ini, rot, frase) in enumerate(SHOTS):
            if k == 0:
                h = base + f'<div class="cap"><div class="n">{frase}</div><div class="l"></div><div class="k">el vorí vorí, paso a paso</div></div></body></html>'
            elif k == N - 1:
                h = base + f'<div class="cap"><div class="n">{frase}</div><div class="l"></div><div style="margin-top:18px;display:inline-block;background:#e8b43a;color:#2a000e;font-weight:800;font-size:44px;padding:18px 50px;border-radius:999px;box-shadow:0 20px 44px -10px rgba(232,180,58,.6)">lorenrestobar.com</div><div style="margin-top:14px;font-weight:700;font-size:34px;color:#f3eedc;text-shadow:0 4px 24px rgba(0,0,0,.95)">Carrer de la Muntanya 115 · Barcelona</div></div></body></html>'
            else:
                h = base + f'<div class="cap"><div class="e">{rot}</div><div class="n">{frase}</div><div class="l"></div></div></body></html>'
            open(os.path.join(AQUI, "_cap.html"), "w", encoding="utf-8").write(h)
            pg.goto(f"http://localhost:8123/herramientas/promo/_cap.html?n=r{k}", wait_until="load"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(450)
            pg.locator(".cap").screenshot(path=os.path.join(TMP, f"cap{k}.png"), omit_background=True)
        nav.close()
    os.remove(os.path.join(AQUI, "_cap.html"))


if not os.path.exists(os.path.join(TMP, f"cap{N - 1}.png")):
    capas()


def rgba(p):
    a = np.array(Image.open(p).convert("RGBA")).astype(np.float32)
    return a[..., :3][..., ::-1], a[..., 3:] / 255.0
CAPS = [rgba(os.path.join(TMP, f"cap{k}.png")) for k in range(N)]
lg = Image.open(os.path.join(RAIZ, "img", "marca", "logo-loren.webp")).convert("RGBA"); lw = 330
lg = lg.resize((lw, int(lg.size[1] * lw / lg.size[0])), Image.LANCZOS)
pad = 60; lienzo = Image.new("RGBA", (lg.size[0] + 2 * pad, lg.size[1] + 2 * pad), (0, 0, 0, 0))
sombra = Image.new("RGBA", lienzo.size, (0, 0, 0, 0)); sombra.paste((0, 0, 0, 200), (pad, pad + 8), lg.split()[3]); sombra = sombra.filter(ImageFilter.GaussianBlur(14))
lienzo.alpha_composite(sombra); lienzo.alpha_composite(lg, (pad, pad))
la = np.array(lienzo).astype(np.float32); LOGO = (la[..., :3][..., ::-1], la[..., 3:] / 255.0); LX, LY = (W - lienzo.size[0]) // 2, 235

yy = np.linspace(0, 1, H)[:, None]
bot = np.where(yy > 0.50, 1 - np.clip((yy - 0.50) / 0.30, 0, 1) ** 1.2 * 0.62, 1)
SCRIM = np.clip(np.minimum(np.where(yy < 0.24, 0.38 + 0.62 * (yy / 0.24) ** 0.8, 1), bot), 0, 1)
SCRIM_U8 = (np.broadcast_to(SCRIM[:, :, None], (H, W, 3)) * 255).astype(np.uint8)


class Plano:
    """Cada plano se extrae antes con ffmpeg (búsqueda exacta) a JPG a 30 fps."""
    def __init__(self, k, ini):
        self.k = k
        d = os.path.join(TMP, f"plano{k}")
        if not os.path.isdir(d) or len(os.listdir(d)) < 20:
            os.makedirs(d, exist_ok=True)
            subprocess.run([FF, "-y", "-loglevel", "error", "-ss", str(ini), "-t", str(DUR[k] + TW + 0.3), "-i", REEL, "-vf", f"fps={FPS}", "-q:v", "2", os.path.join(d, "%04d.jpg")], check=True)
        self.fs = sorted(os.path.join(d, f) for f in os.listdir(d)); self.cache = (-1, None)

    def frame(self, tau, dur):
        i = max(0, min(len(self.fs) - 1, int(tau * FPS)))
        if self.cache[0] != i: self.cache = (i, cv2.imread(self.fs[i]))
        fr = self.cache[1]; h, w = fr.shape[:2]
        z = 1.0 + 0.07 * min(1, max(0, tau / dur))
        cw = min(w, h * W / H) / z; ch = cw * H / W
        x0, y0 = int((w - cw) / 2), int((h - ch) / 2)
        out = cv2.resize(fr[y0:y0 + int(ch), x0:x0 + int(cw)], (W, H), interpolation=cv2.INTER_CUBIC if w < W else cv2.INTER_AREA)
        bl = cv2.GaussianBlur(out, (0, 0), 2.0); out = cv2.addWeighted(out, 1.45, bl, -0.45, 0)
        hsv = cv2.cvtColor(out, cv2.COLOR_BGR2HSV).astype(np.float32); hsv[..., 1] = np.clip(hsv[..., 1] * 1.12, 0, 255); hsv[..., 2] = np.clip(hsv[..., 2] * 1.04, 0, 255)
        return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)


planos = {}
def plano(k):
    if k not in planos: planos[k] = Plano(k, SHOTS[k][0])
    return planos[k]


def desplaza(img, dx, blur):
    """Desplaza horizontalmente y aplica desenfoque de movimiento (la clave del whip pan)."""
    M = np.float32([[1, 0, dx], [0, 1, 0]])
    out = cv2.warpAffine(img, M, (W, H), borderMode=cv2.BORDER_REPLICATE)
    k = int(blur) | 1
    if k > 1: out = cv2.blur(out, (k, 1))
    return out


def suave(x): x = min(1, max(0, x)); return x * x * (3 - 2 * x)


def componer(t):
    k = min(N - 1, int(np.searchsorted(TB, t, side="right") - 1))
    # ¿estamos en una transición? (centrada en TB[j], j≥1)
    vent = None
    for j in range(1, N):
        if TB[j] - TW / 2 <= t < TB[j] + TW / 2: vent = j; break
    def local(j): return t - (TB[j] - (TW / 2 if j > 0 else 0))
    if vent:
        a, b = vent - 1, vent
        A = plano(a).frame(local(a), DUR[a] + TW); B = plano(b).frame(local(b), DUR[b] + TW)
        p = (t - (TB[vent] - TW / 2)) / TW
        e = suave(p)
        pico = math.sin(math.pi * p)                       # el desenfoque es máximo a mitad del barrido
        A2 = desplaza(A, -e * W * 0.55, 8 + 90 * pico)     # sale hacia la izquierda
        B2 = desplaza(B, (1 - e) * W * 0.55, 8 + 90 * pico)  # entra desde la derecha
        al = suave((p - 0.35) / 0.3)
        out = cv2.addWeighted(A2, 1 - al, B2, al, 0)
        cur = vent
    else:
        cur = k
        out = plano(cur).frame(local(cur), DUR[cur] + TW)
    out = cv2.multiply(out, SCRIM_U8, scale=1 / 255.0)
    # rótulo del plano: entra tras el barrido y sale al empezar el siguiente
    for kk in {k, cur}:
        t_ini = TB[kk] + 0.04; t_fin = TB[kk + 1] - TW / 2 if kk + 1 <= N else 1e9
        a = min(1, max(0, (t - t_ini) / 0.22)) * (1 if kk == N - 1 else min(1, max(0, (t_fin + 0.12 - t) / 0.12)))
        if a > 0.01:
            rgb, al = CAPS[kk]; y = 1570 - rgb.shape[0] - (int((1 - a) * 28))
            roi = out[y:y + rgb.shape[0], 0:W].astype(np.float32); out[y:y + rgb.shape[0], 0:W] = (roi * (1 - al * a) + rgb * al * a).astype(np.uint8)
    rgb, al = LOGO; h_, w_ = rgb.shape[:2]
    roi = out[LY:LY + h_, LX:LX + w_].astype(np.float32); out[LY:LY + h_, LX:LX + w_] = (roi * (1 - al) + rgb * al).astype(np.uint8)
    return out


if __name__ == "__main__":
    proc = subprocess.Popen([FF, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                             "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p", "-an", "-movflags", "+faststart", SAL], stdin=subprocess.PIPE)
    for i in range(NF):
        proc.stdin.write(componer(i / FPS).tobytes())
        if i % 120 == 0: print("fotograma", i, "de", NF, flush=True)
    proc.stdin.close(); proc.wait()
    print("hecho:", SAL, round(os.path.getsize(SAL) / 1e6, 1), "MB · duración", round(TOTAL, 1), "s")
