"""REEL LARGO DEL MBEJÚ · VERSIÓN «VIRAL»: sin adornos; entre paso y paso, TRANSICIONES ESPECTACULARES de 1 s que se alternan:
  · onda expansiva (anillo de choque con aberración cromática, destello y zoom «punch»)
  · cubo 3D giratorio (una cara es el plano que sale y la otra el que entra, con perspectiva)
  · rotura de cristal (el plano se hace añicos desde el punto de impacto y los trozos salen volando dejando ver el siguiente)
Une dos vídeos propios de Loren: video/mbeju.mp4 (cocina, 59,94 fps) y el reel «¿Cómo hacer el mbejú?» (IG Dd6v3Zbs8LY).
Uso: python herramientas/promo/mbeju_viral.py <video/mbeju.mp4> <Dd6v3Zbs8LY.mp4> <carpeta_trabajo> <salida.mp4>   (servidor local en el 8123)"""
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
TW = 1.0                   # duración de cada transición (espectacular pero legible)

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
S = 2.3
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



def suave(x):
    x = min(1, max(0, x)); return x * x * (3 - 2 * x)


def zoom(img, z):
    h, w = img.shape[:2]; cw, ch = int(w / z), int(h / z); x0, y0 = (w - cw) // 2, (h - ch) // 2
    return cv2.resize(img[y0:y0 + ch, x0:x0 + cw], (w, h), interpolation=cv2.INTER_LINEAR)


# ---------------- transiciones espectaculares ----------------
YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)
CXI, CYI = W / 2.0, H * 0.5
DXG, DYG = XX - CXI, YY - CYI
RG = (np.hypot(DXG, DYG) / float(np.hypot(W / 2, H / 2))).astype(np.float32)


def onda(A, B, e):
    """Onda expansiva: un anillo de choque cruza la pantalla; dentro ya está el plano siguiente (con zoom punch), el anillo deforma y separa los colores."""
    Rt = e * 1.45 - 0.05; ancho = 0.15
    g = np.exp(-((RG - Rt) / ancho) ** 2).astype(np.float32)
    inten = math.sin(math.pi * min(1, e * 1.1))
    m = np.clip((Rt - RG) / 0.035, 0, 1)[..., None]
    base = A.astype(np.float32) * (1 - m) + zoom(B, 1.25 - 0.25 * e).astype(np.float32) * m
    base = np.clip(base, 0, 255).astype(np.uint8)
    esc = 1 - 0.22 * inten * g
    canales = []
    for c, aber in ((0, -0.028), (1, 0.0), (2, 0.028)):          # azul, verde, rojo con radios distintos = aberración cromática
        k = esc + aber * inten * g
        canales.append(cv2.remap(np.ascontiguousarray(base[..., c]), (CXI + DXG * k).astype(np.float32), (CYI + DYG * k).astype(np.float32), cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE))
    out = cv2.merge(canales).astype(np.float32)
    out += (g * inten * 70)[..., None]                              # brillo del anillo
    return np.clip(out, 0, 255).astype(np.uint8)


def cubo(A, B, e):
    """Cubo 3D: A es la cara frontal y B la lateral; el cubo gira 90° con perspectiva y sombreado."""
    th = e * math.pi / 2; c, s = math.cos(th), math.sin(th)
    a, h = W / 2.0, H / 2.0; D = 1.9 * W; cz = D + a; f = D

    def pr(x, y, z):
        dz = z - cz; xr = x * c + dz * s; zr = -x * s + dz * c + cz
        return (W / 2 + f * xr / zr, H / 2 + f * y / zr)
    src = np.float32([[0, 0], [W, 0], [W, H], [0, H]])
    caras = ((A, [pr(-a, -h, D), pr(a, -h, D), pr(a, h, D), pr(-a, h, D)], 0.45 + 0.55 * c),
             (B, [pr(a, -h, D), pr(a, -h, D + 2 * a), pr(a, h, D + 2 * a), pr(a, h, D)], 0.45 + 0.55 * s))
    fondo = cv2.resize(cv2.GaussianBlur(cv2.resize(cv2.addWeighted(A, 1 - e, B, e, 0), (54, 96)), (0, 0), 3), (W, H), interpolation=cv2.INTER_CUBIC)
    out = (fondo.astype(np.float32) * 0.30)
    for img, q, sh in caras:
        M = cv2.getPerspectiveTransform(src, np.float32(q))
        w = cv2.warpPerspective(img, M, (W, H), flags=cv2.INTER_LINEAR)
        mk = cv2.warpPerspective(np.full((H, W), 255, np.uint8), M, (W, H), flags=cv2.INTER_LINEAR).astype(np.float32)[..., None] / 255.0
        out = out * (1 - mk) + w.astype(np.float32) * sh * mk
    return np.clip(out, 0, 255).astype(np.uint8)


from scipy.spatial import Delaunay
_rng = np.random.default_rng(11)
_pts = []
for _j in range(10):
    for _i in range(6):
        _x, _y = _i * W / 5.0, _j * H / 9.0
        if 0 < _i < 5: _x += _rng.uniform(-0.30, 0.30) * W / 5
        if 0 < _j < 9: _y += _rng.uniform(-0.30, 0.30) * H / 9
        _pts.append((_x, _y))
PTS = np.array(_pts, np.float32); TRI = Delaunay(PTS).simplices
IMPACTO = np.array([W * 0.5, H * 0.42], np.float32)
CEN = PTS[TRI].mean(axis=1); DIST = np.hypot(*(CEN - IMPACTO).T); DIST = DIST / DIST.max()
DIRS = (CEN - IMPACTO) / (np.hypot(*(CEN - IMPACTO).T)[:, None] + 1e-6)
SIGNO = _rng.choice([-1.0, 1.0], len(TRI)); VEL = _rng.uniform(0.8, 1.25, len(TRI))


def rotura(A, B, e):
    """Rotura de cristal: A se hace añicos desde el punto de impacto; los trozos salen despedidos (giran, crecen y se desvanecen) y dejan ver B."""
    sacudida = 9 * math.exp(-e * 7) * math.sin(e * 90)
    out = (zoom(B, 1.06 - 0.06 * e).astype(np.float32) * (0.55 + 0.45 * e)).astype(np.uint8)
    tl = np.clip((e - 0.22 * DIST) / 0.50, 0, 1)
    est = np.zeros((H, W), np.uint8)
    for t_, tri in zip(tl, TRI):
        if t_ <= 0: cv2.fillConvexPoly(est, PTS[tri].astype(np.int32), 255)
    out[est > 0] = A[est > 0]
    for idx in np.argsort(tl):
        t_ = float(tl[idx])
        if t_ <= 0: continue
        p = t_ ** 1.5 * VEL[idx]
        al = 1 - min(1, max(0, (t_ - 0.55) / 0.45))
        if al <= 0.01: continue
        tri = PTS[TRI[idx]]; c = CEN[idx]
        M = cv2.getRotationMatrix2D((float(c[0]), float(c[1])), float(SIGNO[idx] * p * 130), 1 + 0.5 * p)
        M[:, 2] += DIRS[idx] * p * W * 1.0 + np.array([0, p * H * 0.22])
        dst = (np.hstack([tri, np.ones((3, 1), np.float32)]) @ M.T).astype(np.float32)
        x0, y0 = int(max(0, dst[:, 0].min() - 2)), int(max(0, dst[:, 1].min() - 2)); x1, y1 = int(min(W, dst[:, 0].max() + 3)), int(min(H, dst[:, 1].max() + 3))
        if x1 <= x0 or y1 <= y0: continue
        M2 = M.copy(); M2[:, 2] -= (x0, y0)
        patch = cv2.warpAffine(A, M2, (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR)
        mk = np.zeros((y1 - y0, x1 - x0), np.uint8); cv2.fillConvexPoly(mk, (dst - (x0, y0)).astype(np.int32), 255, cv2.LINE_AA)
        a = (mk.astype(np.float32) / 255.0 * al)[..., None]
        roi = out[y0:y1, x0:x1].astype(np.float32)
        out[y0:y1, x0:x1] = (roi * (1 - a) + patch.astype(np.float32) * a).astype(np.uint8)
        cv2.polylines(out, [dst.astype(np.int32)], True, (235, 235, 235), 1, cv2.LINE_AA)   # canto brillante del cristal
    fl = 120 * math.exp(-e / 0.10)                                  # destello en el impacto y sacudida
    if fl > 1:
        rr = np.hypot(XX - IMPACTO[0], YY - IMPACTO[1]) / 700.0
        out = np.clip(out.astype(np.float32) + (np.exp(-rr * rr * 4) * fl)[..., None], 0, 255).astype(np.uint8)
    sac = 9 * math.exp(-e * 7) * math.sin(e * 90)
    if abs(sac) > 0.5: out = cv2.warpAffine(out, np.float32([[1, 0, sac], [0, 1, -sac * 0.6]]), (W, H), borderMode=cv2.BORDER_REPLICATE)
    return out


TIPOS = ["onda", "cubo", "rotura"]


def mezcla(A, B, p, tipo):
    p = min(1, max(0, p))
    if tipo == "onda": return onda(A, B, 1 - (1 - p) ** 2)            # arranca fuerte y frena
    if tipo == "cubo": return cubo(A, B, 0.5 - 0.5 * math.cos(math.pi * p))
    return rotura(A, B, p)


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
