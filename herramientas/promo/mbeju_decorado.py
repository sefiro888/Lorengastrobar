"""VERSIÓN DECORADA del reel largo del mbejú: añade motivos paraguayos —ñandutí giratorio en las esquinas, brasas doradas, BARRA DE CARGA con la bandera de Paraguay
(rojo-blanco-azul) que avanza con una banderita ondeando en la punta, bandera ondeando grande en el gancho y en el cierre, y línea tricolor bajo cada rótulo.
Uso: python herramientas/promo/mbeju_decorado.py <video/mbeju.mp4> <Dd6v3Zbs8LY.mp4> <carpeta_trabajo> <salida.mp4>
(base: mbeju_largo.py) REEL LARGO DEL MBEJÚ (receta completa, ~28 s): une dos vídeos propios de Loren: video/mbeju.mp4 (cocina, 60 fps) y el reel «¿Cómo hacer el mbejú?» (IG Dd6v3Zbs8LY, Loren amasando y comiéndolo).
Uso: python herramientas/promo/mbeju_largo.py <video/mbeju.mp4> <Dd6v3Zbs8LY.mp4> <carpeta_trabajo> <salida.mp4>
(base: mbeju_receta.py) REEL DEL MBEJÚ (receta paso a paso, versión mejorada). Copia de receta.py con: cámara lenta REAL (el origen es de 59,94 fps) en el queso estirado,
gancho al inicio y cierre en el queso, 8 pasos y whip pan.
Uso: python herramientas/promo/mbeju_receta.py <video/mbeju.mp4> <carpeta_trabajo> <salida.mp4>
(base: receta.py) Reel de RECETA con técnicas de las «ideas pro» (para-loren/IDEAS-VIDEO-PRO.md):
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
SRC = {"m": sys.argv[1], "d": sys.argv[2]}
TMP, SAL = sys.argv[3], sys.argv[4]
os.makedirs(TMP, exist_ok=True)
W, H, FPS = 1080, 1920, 30
TW = 0.32                  # duración de cada plano y de cada barrido (whip pan)

# (fuente m=video/mbeju.mp4 | d=reel de Loren, inicio_s, rótulo, frase, velocidad)
SHOTS = [
    ("m", 45.0, "", "Así se hace", 0.5),
    ("d", 12.0, "Paso 1", "El almidón", 1.0),
    ("d", 14.4, "Paso 2", "La harina de maíz", 1.0),
    ("d", 16.3, "Paso 3", "El queso", 1.0),
    ("d", 17.8, "Paso 4", "La mantequilla", 1.0),
    ("d", 20.5, "Paso 5", "La leche", 1.0),
    ("d", 27.5, "Paso 6", "Se amasa a mano", 1.0),
    ("m", 0.8, "Paso 7", "Mantequilla en la sartén", 1.0),
    ("m", 10.2, "Paso 8", "La masa a la sartén", 1.0),
    ("m", 19.8, "Paso 9", "Al fuego", 1.0),
    ("m", 25.0, "Paso 10", "Se da la vuelta", 1.0),
    ("m", 28.3, "Paso 11", "Dorado", 1.0),
    ("m", 36.4, "Paso 12", "A la mesa", 1.0),
    ("m", 41.0, "Paso 13", "Al abrirlo", 1.0),
    ("d", 59.2, "", "Pruébalo en Loren", 1.0),
]
N = len(SHOTS)
S = 1.8
DUR = [2.4] + [S] * (N - 2) + [3.8]
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
.l{width:230px;height:9px;border-radius:4px;background:linear-gradient(90deg,#d52b1e 0 33.3%,#fff 33.3% 66.6%,#0038a8 66.6%);margin:20px 0 0;box-shadow:0 0 14px rgba(0,0,0,.55)}
.k{font-family:"Kaushan Script";color:#f4d27a;font-size:84px;line-height:1.1;margin-top:10px;-webkit-text-stroke:2px rgba(42,0,14,.55);paint-order:stroke fill;text-shadow:0 4px 24px rgba(0,0,0,.95),0 0 40px rgba(0,0,0,.8)}
.cta{width:1080px;height:420px;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;padding-bottom:30px;font-family:Montserrat;text-align:center;color:#f3eedc}
</style></head><body>'''
    with sync_playwright() as pw:
        nav = pw.chromium.launch(); pg = nav.new_page(viewport={"width": 1080, "height": 1920})
        for k, (fte, ini, rot, frase, vel) in enumerate(SHOTS):
            if k == 0:
                h = base + f'<div class="cap"><div class="n">{frase}</div><div class="l"></div><div class="k">el mbejú de Loren</div></div></body></html>'
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
    def __init__(self, k, ini, vel=1.0, ruta=None):
        self.k = k
        d = os.path.join(TMP, f"plano{k}")
        if not os.path.isdir(d) or len(os.listdir(d)) < 20:
            os.makedirs(d, exist_ok=True)
            subprocess.run([FF, "-y", "-loglevel", "error", "-ss", str(ini), "-t", str(round((DUR[k] + TW + 0.3) * vel, 3)), "-i", ruta, "-vf", f"fps={FPS / vel}", "-q:v", "2", os.path.join(d, "%04d.jpg")], check=True)
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
    if k not in planos: planos[k] = Plano(k, SHOTS[k][1], SHOTS[k][4], SRC[SHOTS[k][0]])
    return planos[k]


def desplaza(img, dx, blur):
    """Desplaza horizontalmente y aplica desenfoque de movimiento (la clave del whip pan)."""
    M = np.float32([[1, 0, dx], [0, 1, 0]])
    out = cv2.warpAffine(img, M, (W, H), borderMode=cv2.BORDER_REPLICATE)
    k = int(blur) | 1
    if k > 1: out = cv2.blur(out, (k, 1))
    return out



# ---------------- motivos paraguayos (decoración) ----------------
FLOR = np.array(Image.open(os.path.join(RAIZ, "img", "kv", "flor-kv.webp")).convert("RGBA").resize((900, 900), Image.LANCZOS)).astype(np.uint8)
FLOR = FLOR[..., [2, 1, 0, 3]].copy()                      # BGRA


def pon(dst, rgba, cx, cy, op=1.0):
    """Mezcla una imagen BGRA centrada en (cx, cy) sobre dst (BGR), recortando lo que se sale."""
    h, w = rgba.shape[:2]; x0, y0 = int(cx - w / 2), int(cy - h / 2)
    X0, Y0, X1, Y1 = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
    if X0 >= X1 or Y0 >= Y1: return
    sub = rgba[Y0 - y0:Y1 - y0, X0 - x0:X1 - x0].astype(np.float32); a = sub[..., 3:] / 255.0 * op
    roi = dst[Y0:Y1, X0:X1].astype(np.float32); dst[Y0:Y1, X0:X1] = (roi * (1 - a) + sub[..., :3] * a).astype(np.uint8)


def bandera(w, h):
    f = np.zeros((h, w, 4), np.uint8)
    f[:h // 3, :, :3] = (30, 43, 213); f[h // 3:2 * h // 3, :, :3] = (255, 255, 255); f[2 * h // 3:, :, :3] = (168, 56, 0); f[..., 3] = 255
    cx, cy, r = w // 2, h // 2, int(h * 0.15)
    cv2.circle(f, (cx, cy), r, (62, 143, 30), max(2, h // 36), cv2.LINE_AA)
    pts = np.array([[cx + int(r * 0.62 * math.sin(math.radians(a))), cy - int(r * 0.62 * math.cos(math.radians(a)))] for a in (0, 144, 288, 432, 576)], np.int32)
    cv2.fillPoly(f, [pts], (0, 209, 255), cv2.LINE_AA)
    return f


def ondea(base, t, amp):
    """Bandera ondeando: la onda crece hacia el extremo libre y el brillo sigue la onda."""
    h, w = base.shape[:2]; lienzo = np.zeros((h + 2 * amp, w, 4), np.uint8); lienzo[amp:amp + h] = base
    xs = np.arange(w, dtype=np.float32); fase = 2 * math.pi * (xs / (w * 0.9) - t * 0.9); env = 0.2 + 0.8 * xs / w
    off = amp * np.sin(fase) * env
    mx = np.tile(xs, (lienzo.shape[0], 1)); my = np.arange(lienzo.shape[0], dtype=np.float32)[:, None] - off[None, :]
    o = cv2.remap(lienzo, mx, my.astype(np.float32), cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    o[..., :3] = np.clip(o[..., :3].astype(np.float32) * (1 + 0.20 * np.cos(fase) * env)[None, :, None], 0, 255).astype(np.uint8)
    return o


BANDERA = bandera(300, 200); BANDERA_FIN = bandera(250, 167); BANDERITA = bandera(84, 56)
rr = np.random.default_rng(7)
BRASAS = [(rr.uniform(0, W), rr.uniform(60, 160), rr.uniform(0, 2000), rr.uniform(14, 40), rr.uniform(1, 3), rr.uniform(3, 6)) for _ in range(26)]


def decora(out, t):
    # ñandutí giratorio en dos esquinas (suave, para no tapar la comida)
    for cx, cy, sg in ((30, 600, 1), (1050, 1330, -1)):
        M = cv2.getRotationMatrix2D((450, 450), sg * t * 7, 1.0)
        pon(out, cv2.warpAffine(FLOR, M, (900, 900), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0)), cx, cy, 0.30)
    # brasas doradas que suben
    ov = np.zeros((H, W, 3), np.uint8)
    for x, v, ph, w_, f, r in BRASAS:
        y = 1960 - ((t * v + ph) % 2000); xx = x + math.sin(t * 0.9 + ph) * w_
        al = (0.35 + 0.6 * abs(math.sin(t * f + ph))) * min(1, max(0, min(y, 1900 - y) / 260 + 0.1))
        cv2.circle(ov, (int(xx), int(y)), int(r), (int(122 * al), int(210 * al), int(244 * al)), -1, cv2.LINE_AA)
    glow = cv2.GaussianBlur(ov, (0, 0), 9)
    return cv2.add(cv2.add(out, ov), glow)


def encima(out, t):
    # bandera ondeando grande en el gancho y en el cierre
    en_gancho = t < TB[1] + 0.2; en_final = t >= TB[N - 1]
    if en_gancho or en_final:
        a = 1.0
        if en_gancho: a = min(1, t / 0.4) * min(1, max(0, (TB[1] + 0.2 - t) / 0.3))
        else: a = min(1, (t - TB[N - 1]) / 0.4)
        if en_gancho: pon(out, ondea(BANDERA, t, 14), 880, 700, a)
        else: pon(out, ondea(BANDERA_FIN, t, 12), 925, 760, a)
    # barra de carga con la bandera de Paraguay: se llena con el avance del vídeo
    frac = min(1, max(0, t / TOTAL)); x0, x1, y0, hh = 150, 930, 548, 24
    ov = out.copy(); cv2.rectangle(ov, (x0 - 4, y0 - 4), (x1 + 4, y0 + hh + 4), (20, 14, 16), -1); out = cv2.addWeighted(out, 0.45, ov, 0.55, 0)
    xf = int(x0 + frac * (x1 - x0))
    if xf > x0:
        sw = hh // 3
        cv2.rectangle(out, (x0, y0), (xf, y0 + sw), (30, 43, 213), -1); cv2.rectangle(out, (x0, y0 + sw), (xf, y0 + 2 * sw), (255, 255, 255), -1); cv2.rectangle(out, (x0, y0 + 2 * sw), (xf, y0 + hh), (168, 56, 0), -1)
    cv2.rectangle(out, (x0 - 4, y0 - 4), (x1 + 4, y0 + hh + 4), (244, 210, 122), 2, cv2.LINE_AA)
    # mástil con banderita ondeando en la punta de la barra
    cv2.line(out, (xf, y0 + hh), (xf, y0 - 62), (235, 235, 235), 3, cv2.LINE_AA)
    pon(out, ondea(BANDERITA, t, 5), xf + 42, y0 - 36, 1.0)
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
    out = decora(out, t)
    # rótulo del plano: entra tras el barrido y sale al empezar el siguiente
    for kk in {k, cur}:
        t_ini = TB[kk] + 0.04; t_fin = TB[kk + 1] - TW / 2 if kk + 1 <= N else 1e9
        a = min(1, max(0, (t - t_ini) / 0.22)) * (1 if kk == N - 1 else min(1, max(0, (t_fin + 0.12 - t) / 0.12)))
        if a > 0.01:
            rgb, al = CAPS[kk]; y = 1570 - rgb.shape[0] - (int((1 - a) * 28))
            roi = out[y:y + rgb.shape[0], 0:W].astype(np.float32); out[y:y + rgb.shape[0], 0:W] = (roi * (1 - al * a) + rgb * al * a).astype(np.uint8)
    out = encima(out, t)
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
