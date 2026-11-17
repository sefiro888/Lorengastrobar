"""REEL LARGO DEL MBEJÚ · VERSIÓN FINAL (sin bandera): ñandutí giratorio en las esquinas, brasas doradas, fina barra de progreso dorada con una pequeña roseta de ñandutí que avanza
y TRANSICIONES SUAVES Y ELEGANTES (0,8 s, bordes difuminados, sin rayas ni líneas): zoom con disolvencia, barrido vertical con paralaje, destello de luz, iris difuminado y empuje con paralaje.
Une dos vídeos propios de Loren: video/mbeju.mp4 (cocina, 59,94 fps) y el reel «¿Cómo hacer el mbejú?» (IG Dd6v3Zbs8LY).
Uso: python herramientas/promo/mbeju_formas.py <video/mbeju.mp4> <Dd6v3Zbs8LY.mp4> <carpeta_trabajo> <salida.mp4>   (servidor local en el 8123)"""
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
TW = 0.8                   # duración de cada transición (calmada)

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
S = 2.1
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
.l{width:190px;height:6px;border-radius:3px;background:#e8b43a;margin:20px 0 0;box-shadow:0 0 18px rgba(232,180,58,.7)}
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


rr = np.random.default_rng(7)
BRASAS = [(rr.uniform(0, W), rr.uniform(60, 160), rr.uniform(0, 2000), rr.uniform(14, 40), rr.uniform(1, 3), rr.uniform(3, 6)) for _ in range(26)]


def decora(out, t):
    # ñandutí giratorio en dos esquinas (suave, para no tapar la comida)
    for cx, cy, sg in ((30, 600, 1), (1050, 1330, -1)):
        M = cv2.getRotationMatrix2D((450, 450), sg * t * 7, 1.0)
        pon(out, cv2.warpAffine(FLOR, M, (900, 900), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0)), cx, cy, 0.24)
    # brasas doradas que suben
    ov = np.zeros((H, W, 3), np.uint8)
    for x, v, ph, w_, f, r in BRASAS:
        y = 1960 - ((t * v + ph) % 2000); xx = x + math.sin(t * 0.9 + ph) * w_
        al = (0.35 + 0.6 * abs(math.sin(t * f + ph))) * min(1, max(0, min(y, 1900 - y) / 260 + 0.1))
        cv2.circle(ov, (int(xx), int(y)), int(r), (int(122 * al), int(210 * al), int(244 * al)), -1, cv2.LINE_AA)
    glow = cv2.GaussianBlur(ov, (0, 0), 9)
    return cv2.add(cv2.add(out, ov), glow)


def encima(out, t):
    # fina barra de progreso dorada con una pequeña roseta de ñandutí que avanza
    frac = min(1, max(0, t / TOTAL)); x0, x1, y0 = 170, 910, 548
    xf = int(x0 + frac * (x1 - x0))
    sombra = out.copy(); cv2.line(sombra, (x0, y0), (x1, y0), (15, 10, 12), 9, cv2.LINE_AA); out = cv2.addWeighted(out, 0.6, sombra, 0.4, 0)
    cv2.line(out, (x0, y0), (x1, y0), (200, 190, 170), 2, cv2.LINE_AA)
    if xf > x0: cv2.line(out, (x0, y0), (xf, y0), (58, 180, 232), 6, cv2.LINE_AA)
    M = cv2.getRotationMatrix2D((450, 450), t * 40, 1.0)
    rosa = cv2.resize(cv2.warpAffine(FLOR, M, (900, 900), borderValue=(0, 0, 0, 0)), (70, 70), interpolation=cv2.INTER_AREA)
    pon(out, rosa, xf, y0, 1.0)
    return out


def suave(x):
    x = min(1, max(0, x)); return x * x * (3 - 2 * x)


# ---------------- transiciones suaves (máscaras suaves a baja resolución) ----------------
MW, MH = 270, 480
_xs, _ys = np.meshgrid(np.linspace(-0.5, 0.5, MW, dtype=np.float32), np.linspace(-0.5, 0.5, MH, dtype=np.float32))
GX, GY = _xs * W, (_ys + 0.02) * H
R = np.hypot(GX, GY); RMAX = float(np.hypot(W / 2, H / 2)) * 1.02; TH = np.arctan2(GY, GX)
CAMPOS = {
    "iris": R / RMAX,
    "rombo": (np.abs(GX) / (W / 2) + np.abs(GY) / (H / 2)) / 2.0,
    "ola": np.clip((0.5 - _ys) * 0.9 + 0.07 * (0.5 + 0.5 * np.sin(2 * math.pi * 2.0 * (_xs + 0.5))), 0, 1) / 1.0,
}
_u = (_xs + 0.5) * W * 0.5 + (_ys + 0.5) * H * 0.866; _u = _u / _u.max(); _s = _u * 9; _k = np.floor(np.minimum(_s, 8.999)); CAMPOS["persianas"] = (0.55 * _k / 8 + 0.45 * (_s - _k)).astype(np.float32)
TIPOS = ["zoom", "barrido", "luz", "iris", "empuje"]
CAMPOS = {"barrido": (1.0 - (_ys + 0.5)).astype(np.float32), "iris": (R / RMAX).astype(np.float32)}


def zoom(img, z):
    h, w = img.shape[:2]; cw, ch = int(w / z), int(h / z); x0, y0 = (w - cw) // 2, (h - ch) // 2
    return cv2.resize(img[y0:y0 + ch, x0:x0 + cw], (w, h), interpolation=cv2.INTER_LINEAR)


def desfoca(img, k):
    k = int(k) | 1
    return cv2.GaussianBlur(img, (k, k), 0) if k > 1 else img


def mover(img, dx, dy):
    return cv2.warpAffine(img, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REPLICATE)


def mascara(d, e, blando):
    """Máscara con borde muy difuminado (sin línea): d es el 'instante de llegada' de cada punto (0..1)."""
    m = np.clip((e * (1 + blando) - d) / blando, 0, 1).astype(np.float32)
    m = m * m * (3 - 2 * m)
    return cv2.resize(m, (W, H), interpolation=cv2.INTER_CUBIC)[..., None].clip(0, 1)


def mezcla(A, B, p, tipo):
    e = 0.5 - 0.5 * math.cos(math.pi * min(1, max(0, p)))          # curva de seno: arranca y frena con suavidad
    pico = math.sin(math.pi * e)
    if tipo == "zoom":              # empuje hacia dentro: A se acerca y se funde con B, que llega desde un poco más cerca
        A2 = desfoca(zoom(A, 1 + 0.10 * e), 1 + 10 * pico); B2 = desfoca(zoom(B, 1.10 - 0.10 * e), 1 + 10 * pico)
        al = suave((e - 0.1) / 0.8)
        return cv2.addWeighted(A2, 1 - al, B2, al, 0)
    if tipo == "luz":               # disolvencia con un destello cálido de luz en el centro del cambio
        A2 = zoom(A, 1 + 0.05 * e); B2 = zoom(B, 1.05 - 0.05 * e); al = suave((e - 0.05) / 0.9)
        out = cv2.addWeighted(A2, 1 - al, B2, al, 0).astype(np.float32)
        out += pico * 46 * np.array([0.78, 0.9, 1.0], np.float32)
        return np.clip(out, 0, 255).astype(np.uint8)
    if tipo == "empuje":            # las dos imágenes se desplazan con paralaje (B más rápida) y se funden; desenfoque mínimo
        A2 = desfoca(mover(A, -e * W * 0.22, 0), 1 + 8 * pico); B2 = desfoca(mover(B, (1 - e) * W * 0.34, 0), 1 + 8 * pico)
        al = suave((e - 0.15) / 0.7)
        return cv2.addWeighted(A2, 1 - al, B2, al, 0)
    # barrido vertical e iris: máscara blanda (borde ancho, sin línea) + paralaje suave
    if tipo == "barrido":
        A2 = mover(A, 0, -e * 70); B2 = mover(B, 0, (1 - e) * 70); m = mascara(CAMPOS["barrido"], e, 0.55)
    else:
        A2 = zoom(A, 1 + 0.04 * e); B2 = zoom(B, 1.10 - 0.10 * e); m = mascara(CAMPOS["iris"], e, 0.45)
    return np.clip(A2.astype(np.float32) * (1 - m) + B2.astype(np.float32) * m, 0, 255).astype(np.uint8)


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
        out = mezcla(A, B, p, TIPOS[(vent - 1) % len(TIPOS)])
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
