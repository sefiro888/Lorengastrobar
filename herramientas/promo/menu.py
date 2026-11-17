"""Promo «Tu mesa, paso a paso» (de las tapas al postre, solo fotos de la carta), mismo estilo que tiles.py.
(base copiada de) Promo «Sabores» al estilo de barrido de rectángulos: planos de comida a pantalla completa, todos de la misma duración,
logo fijo y nombre + precio de cada plato. SIN música.
Uso: python herramientas/promo/tiles.py <carpeta_reels_720p> <carpeta_trabajo> <salida.mp4>   (servidor local en el 8123)"""
import os, sys, subprocess, math
import numpy as np, cv2
from PIL import Image, ImageFilter
from playwright.sync_api import sync_playwright

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
FF = os.path.join(os.path.dirname(sys.executable), "Lib", "site-packages", "imageio_ffmpeg", "binaries", "ffmpeg-win-x86_64-v7.1.exe")
REELS, TMP, SAL = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(TMP, exist_ok=True)
W, H, FPS = 1080, 1920, 30
S, TW = 1.8, 0.6            # duración de cada plano y de cada barrido
V = lambda f: os.path.join(RAIZ, "video", f)
IM = lambda f: os.path.join(RAIZ, "img", "platos", f)
DESC = r"C:/Users/sefir/Downloads/WhatsApp Video 2026-11-16 at 23.44.37.mp4"
# (tipo, fuente, inicio_s, nombre, precio, sección)  — solo fotos profesionales de la carta (ninguna usada en los otros promos)
E, F, D = "Para empezar", "Plato fuerte", "Dulce final"
SHOTS = [
    ("i", IM("hl-empanadas.webp"), 0, "Empanadas caseras", "", E),
    ("i", IM("hl-croquetas.webp"), 0, "Croquetas de jamón", "4,90 €", E),
    ("i", IM("hl-alitas.webp"), 0, "Alitas de pollo", "7,90 €", E),
    ("i", IM("hl-bravas.webp"), 0, "Patatas bravas", "5,90 €", E),
    ("i", IM("hl-tequenos.webp"), 0, "Tequeños", "7,90 €", E),
    ("i", IM("hl-tapas-espanolas.webp"), 0, "Jamón ibérico", "14,50 €", E),
    ("i", IM("hl-chorizo.webp"), 0, "Picada de chorizo", "11,90 €", F),
    ("i", IM("hl-asado-olla.webp"), 0, "Asado a la olla", "17,90 €", F),
    ("i", IM("hl-noquis.webp"), 0, "Ñoquis de ternera", "15,90 €", F),
    ("i", IM("hl-hamburguesa.webp"), 0, "Hamburguesa completa", "12,90 €", F),
    ("i", IM("hl-flan.webp"), 0, "Flan casero", "", D),
    ("i", IM("tres-leches.webp"), 0, "Tarta tres leches", "", D),
    ("i", IM("postre-alfajor-cafe.webp"), 0, "Alfajores Loren", "", D),
    ("i", IM("postre-tarta-chocolate.webp"), 0, "Tarta de chocolate", "", D),
]
N = len(SHOTS)
CTA = ("v", V("chipa.mp4"), 12.0)
CTA_DUR = 3.8
TB = [k * S for k in range(N + 1)]          # instante de cada cambio (el último es el cierre)
TOTAL = TB[N] + CTA_DUR
NF = int(round(TOTAL * FPS))

# ---------- capas gráficas (PNG con transparencia) renderizadas con las tipografías de la web
def capas():
    css = '@import url("../../css/fuentes.css");'
    base = f'''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="../../css/fuentes.css">
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{background:transparent;width:1080px}}
.cap{{width:1080px;height:430px;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;padding-bottom:70px;font-family:Montserrat}}
.n{{font-family:Anton;text-transform:uppercase;color:#f3eedc;font-size:112px;line-height:1.02;text-align:center;padding:0 50px;text-shadow:0 6px 30px rgba(0,0,0,.9),0 2px 6px rgba(0,0,0,.8)}}
.e{{font-weight:800;font-size:36px;letter-spacing:.3em;text-transform:uppercase;color:#f4d27a;margin-bottom:14px;text-shadow:0 0 30px rgba(0,0,0,.95),0 3px 14px rgba(0,0,0,.9)}}
.l{{width:180px;height:6px;border-radius:3px;background:#e8b43a;margin:22px 0 12px;box-shadow:0 0 18px rgba(232,180,58,.7)}}
.p{{font-family:"Kaushan Script";color:#f4d27a;font-size:84px;line-height:1;text-shadow:0 4px 24px rgba(0,0,0,.95),0 0 40px rgba(0,0,0,.8);-webkit-text-stroke:2px rgba(42,0,14,.55);paint-order:stroke fill}}
.cta{{width:1080px;height:1920px;position:relative;font-family:Montserrat;color:#f3eedc;text-align:center}}
.cta>*{{position:absolute;left:0;right:0}}
</style></head><body>'''
    with sync_playwright() as pw:
        nav = pw.chromium.launch(); pg = nav.new_page(viewport={"width": 1080, "height": 1920})
        for k, sh in enumerate(SHOTS):
            nombre, precio = sh[3], sh[4]
            h = base + f'<div class="cap"><div class="e">{sh[5]}</div><div class="n">{nombre}</div>' + ('<div class="l"></div>' + f'<div class="p">{precio}</div>' if precio else '<div class="l" style="margin-bottom:0"></div>') + '</div></body></html>'
            open(os.path.join(AQUI, "_cap.html"), "w", encoding="utf-8").write(h)
            pg.goto(f"http://localhost:8123/herramientas/promo/_cap.html?n={k}", wait_until="load"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(500)
            pg.locator(".cap").screenshot(path=os.path.join(TMP, f"cap{k}.png"), omit_background=True)
        h = base + '''<div class="cta">
<div style="top:560px;font-family:Anton;text-transform:uppercase;font-size:230px;line-height:.95;text-shadow:0 8px 40px rgba(0,0,0,.9)">Visítanos</div>
<div style="top:830px;font-family:'Kaushan Script';color:#f4d27a;font-size:96px;text-shadow:0 4px 30px rgba(0,0,0,.95);-webkit-text-stroke:2px rgba(42,0,14,.55);paint-order:stroke fill">tu mesa te espera</div>
<div style="top:1020px;font-weight:700;font-size:48px;line-height:1.4;text-shadow:0 4px 24px rgba(0,0,0,.9)">Carrer de la Muntanya 115<br>Camp de l'Arpa · Barcelona</div>
<div style="top:1260px"><span style="display:inline-block;background:#e8b43a;color:#2a000e;font-weight:800;font-size:50px;padding:26px 62px;border-radius:999px;box-shadow:0 20px 44px -10px rgba(232,180,58,.6)">lorenrestobar.com</span></div>
<div style="top:1420px;font-weight:600;font-size:36px;text-shadow:0 4px 20px rgba(0,0,0,.9)">Miércoles a domingo · También a domicilio</div></div></body></html>'''
        open(os.path.join(AQUI, "_cap.html"), "w", encoding="utf-8").write(h)
        pg.goto("http://localhost:8123/herramientas/promo/_cap.html?n=cta", wait_until="load"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(500)
        pg.locator(".cta").screenshot(path=os.path.join(TMP, "cta.png"), omit_background=True)
        nav.close()
    os.remove(os.path.join(AQUI, "_cap.html"))
if not os.path.exists(os.path.join(TMP, f"cap{N - 1}.png")) or not os.path.exists(os.path.join(TMP, "cta.png")):
    capas()

def rgba(p):
    a = np.array(Image.open(p).convert("RGBA")).astype(np.float32)
    return a[..., :3][..., ::-1], a[..., 3:] / 255.0          # BGR, alfa
CAPS = [rgba(os.path.join(TMP, f"cap{k}.png")) for k in range(N)]
CTA_IMG = rgba(os.path.join(TMP, "cta.png"))
# logo fijo arriba, con sombra
lg = Image.open(os.path.join(RAIZ, "img", "marca", "logo-loren.webp")).convert("RGBA"); lw = 360
lg = lg.resize((lw, int(lg.size[1] * lw / lg.size[0])), Image.LANCZOS)
pad = 60; lienzo = Image.new("RGBA", (lg.size[0] + 2 * pad, lg.size[1] + 2 * pad), (0, 0, 0, 0))
sombra = Image.new("RGBA", lienzo.size, (0, 0, 0, 0)); sombra.paste((0, 0, 0, 200), (pad, pad + 8), lg.split()[3]); sombra = sombra.filter(ImageFilter.GaussianBlur(14))
lienzo.alpha_composite(sombra); lienzo.alpha_composite(lg, (pad, pad))
la = np.array(lienzo).astype(np.float32); LOGO = (la[..., :3][..., ::-1], la[..., 3:] / 255.0); LX, LY = (W - lienzo.size[0]) // 2, 70

# sombreado fijo (arriba y abajo) para que se lea siempre
yy = np.linspace(0, 1, H)[:, None]
top = np.clip(1 - (1 - yy / 0.24) * 0.62, 0.38, 1) * (yy < 0.24) + (yy >= 0.24)
bot = np.where(yy > 0.62, 1 - np.clip((yy - 0.62) / 0.38, 0, 1) ** 1.4 * 0.66, 1)
SCRIM = np.clip(np.minimum(np.where(yy < 0.24, 0.38 + 0.62 * (yy / 0.24) ** 0.8, 1), bot), 0, 1)
SCRIM = np.broadcast_to(SCRIM[:, :, None], (H, W, 3)).copy()
SCRIM_U8 = (SCRIM * 255).astype(np.uint8)

# ---------- fuentes de imagen
class Fuente:
    """Cada plano de vídeo se extrae antes con ffmpeg (búsqueda exacta) a una secuencia de JPG."""
    def __init__(self, tipo, ruta, ini, k, vel=1.0):
        self.tipo, self.ini, self.k = tipo, ini, k
        if tipo == "i":
            im = cv2.imread(ruta); h, w = im.shape[:2]
            esc = max(W / w, H / h) * 1.12; self.im = cv2.resize(im, (int(w * esc), int(h * esc)), interpolation=cv2.INTER_CUBIC)
        else:
            d = os.path.join(TMP, f"plano{k}")
            if not os.path.isdir(d) or len(os.listdir(d)) < 20:
                os.makedirs(d, exist_ok=True)
                dur = (S + TW + 0.2) if k < N else (CTA_DUR + TW + 0.2)
                vf = f"setpts=PTS/{vel},minterpolate=fps={FPS}:mi_mode=blend" if vel < 1 else f"fps={FPS}"
                subprocess.run([FF, "-y", "-loglevel", "error", "-ss", str(ini), "-t", str(round(dur * vel, 3)), "-i", ruta, "-vf", vf, "-q:v", "2", os.path.join(d, "%04d.jpg")], check=True)
            self.fs = sorted(os.path.join(d, f) for f in os.listdir(d)); self.cache = (-1, None)
    def crudo(self, tau):
        if self.tipo == "i": return self.im
        i = max(0, min(len(self.fs) - 1, int(tau * FPS)))
        if self.cache[0] != i: self.cache = (i, cv2.imread(self.fs[i]))
        return self.cache[1]
    def frame(self, tau, dur):
        fr = self.crudo(tau); h, w = fr.shape[:2]
        z = 1.0 + 0.075 * min(1, max(0, tau / dur))
        if self.tipo == "i": z = 1.0 + 0.06 * min(1, max(0, tau / dur))
        cw = min(w, h * W / H) / z; ch = cw * H / W
        cx, cy = w / 2, h / 2
        x0, y0 = int(cx - cw / 2), int(cy - ch / 2); x0 = max(0, min(w - int(cw), x0)); y0 = max(0, min(h - int(ch), y0))
        rec = fr[y0:y0 + int(ch), x0:x0 + int(cw)]
        out = cv2.resize(rec, (W, H), interpolation=cv2.INTER_CUBIC if w < W else cv2.INTER_AREA)
        bl = cv2.GaussianBlur(out, (0, 0), 2.0); out = cv2.addWeighted(out, 1.45, bl, -0.45, 0)
        hsv = cv2.cvtColor(out, cv2.COLOR_BGR2HSV).astype(np.float32); hsv[..., 1] = np.clip(hsv[..., 1] * 1.12, 0, 255); hsv[..., 2] = np.clip(hsv[..., 2] * 1.04, 0, 255)
        return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_BGR2HSV if False else cv2.COLOR_HSV2BGR)

fuentes = {}
def fuente(k):
    if k not in fuentes:
        if k < N:
            s = SHOTS[k]; t, ruta, ini = s[0], s[1], s[2]; vel = s[5] if len(s) > 5 else 1.0
        else:
            t, ruta, ini = CTA; vel = 1.0
        fuentes[k] = Fuente(t, ruta, ini, k, vel)
    return fuentes[k]
def fin_fuente(k):
    f = fuentes.pop(k, None)
    return

# ---------- barrido de rectángulos (cuadrícula irregular como en el vídeo de referencia)
COLS = [0, 0.34, 0.67, 1.0]; FIL = [0, 0.21, 0.38, 0.60, 0.80, 1.0]
CELDAS = [(int(COLS[c] * W), int(FIL[f] * H), int(COLS[c + 1] * W), int(FIL[f + 1] * H)) for f in range(len(FIL) - 1) for c in range(len(COLS) - 1)]
NT = len(CELDAS)
def orden(k):
    r = np.random.default_rng(100 + k); return r.permutation(NT)

def componer(t):
    # plano actual y, si hay barrido, el siguiente
    k = min(N, int(t // S)) if t < TB[N] else N
    ventana = None
    for j in range(1, N + 1):
        if TB[j] - TW / 2 <= t < TB[j] + TW / 2: ventana = j; break
    def local(j): return t - (TB[j] - TW / 2) if j > 0 else t
    cur = (ventana - 1) if ventana else k
    f_cur = fuente(cur); dur_cur = (S + TW) if cur < N else CTA_DUR + TW
    A = f_cur.frame(local(cur), dur_cur)
    if ventana:
        f_nxt = fuente(ventana); B = f_nxt.frame(local(ventana), (S + TW) if ventana < N else CTA_DUR + TW)
        p = (t - (TB[ventana] - TW / 2)) / TW; o = orden(ventana)
        out = A.copy(); linea = []
        for i, (x0, y0, x1, y1) in enumerate(CELDAS):
            tile_t = (o[i] + 0.5) / NT * 0.86            # instante (0..1) en que salta cada rectángulo
            if p >= tile_t:
                out[y0:y1, x0:x1] = B[y0:y1, x0:x1]
                if p - tile_t < 0.07: out[y0:y1, x0:x1] = cv2.add(out[y0:y1, x0:x1], np.full((y1 - y0, x1 - x0, 3), 26, np.uint8))
        a = 0.55 * math.sin(math.pi * min(1, max(0, p)))
        if a > 0.02:
            ov = out.copy()
            for xv in COLS[1:-1]: cv2.line(ov, (int(xv * W), 0), (int(xv * W), H), (255, 255, 255), 2)
            for yv in FIL[1:-1]: cv2.line(ov, (0, int(yv * H)), (W, int(yv * H)), (255, 255, 255), 2)
            out = cv2.addWeighted(out, 1 - a, ov, a, 0)
        cur_sig = ventana
    else:
        out = A; cur_sig = cur
    out = cv2.multiply(out, SCRIM_U8, scale=1 / 255.0)
    # nombre y precio del plato: entra tras el barrido y sale al empezar el siguiente
    for kk in {cur, cur_sig}:
        if kk >= N: continue
        t_ini = (TB[kk] + 0.02) if kk > 0 else 0.15; t_fin = TB[kk + 1] - TW / 2 if kk + 1 <= N else 1e9
        a = min(1, max(0, (t - t_ini) / 0.28)) * min(1, max(0, (t_fin + 0.22 - t) / 0.22))
        if a > 0.01:
            rgb, al = CAPS[kk]; y = H - rgb.shape[0] - 10
            roi = out[y:y + rgb.shape[0], 0:W].astype(np.float32); out[y:y + rgb.shape[0], 0:W] = (roi * (1 - al * a) + rgb * al * a).astype(np.uint8)
    # cierre
    if cur_sig == N:
        a0 = min(1, max(0, (t - (TB[N] - TW / 2)) / TW))
        out = cv2.addWeighted(out, 1, np.zeros_like(out), 0, 0)
        oscuro = (out.astype(np.float32) * (1 - 0.55 * a0)).astype(np.uint8); out = oscuro
        rgb, al = CTA_IMG; a = min(1, max(0, (t - TB[N] - 0.1) / 0.5)); roi = out.astype(np.float32)
        out = (roi * (1 - al * a) + rgb * al * a).astype(np.uint8)
    # logo fijo
    rgb, al = LOGO; h_, w_ = rgb.shape[:2]
    roi = out[LY:LY + h_, LX:LX + w_].astype(np.float32); out[LY:LY + h_, LX:LX + w_] = (roi * (1 - al) + rgb * al).astype(np.uint8)
    return out

if __name__ == "__main__":
    proc = subprocess.Popen([FF, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                             "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p", "-an", "-movflags", "+faststart", SAL], stdin=subprocess.PIPE)
    prev = -1
    for i in range(NF):
        t = i / FPS
        k = int(t // S)
        if k != prev:
            for j in list(fuentes):
                if j < k - 1: fin_fuente(j)
            prev = k
        proc.stdin.write(componer(t).tobytes())
        if i % 150 == 0: print("fotograma", i, "de", NF, flush=True)
    proc.stdin.close(); proc.wait()
    print("hecho:", SAL, round(os.path.getsize(SAL) / 1e6, 1), "MB · duración", round(TOTAL, 1), "s")
