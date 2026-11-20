"""Genera navidad.html (Nochebuena y Nochevieja · sólo en español) a partir de herramientas/navidad_datos.py.
Uso: python herramientas/navidad_web.py   (después: git push)

Página «espectacular»: nieve de ñandutí y luces animadas, guirnalda con bombillas, bolas que se mecen,
dos cuentas atrás en vivo (Nochebuena 24 y Nochevieja 31 → campanadas), combos con botón «Para el 24» y
«Para el 31», tradiciones paraguayas y fuegos artificiales al final. Todo respeta «reducir movimiento».
Se enlaza desde un aviso en Inicio y Eventos que se oculta solo el 1-ene-2027 (data-hasta)."""
import json, pathlib, re, sys, urllib.parse
RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "herramientas"))
from navidad_datos import COMBOS, WHATSAPP, WA_LINK

# publicaciones del carrusel (versión 1) para verlas en grande en la web
from PIL import Image
PUB_SRC = RAIZ / "para-loren" / "navidad" / "1-instagram-carrusel"
PUB_DST = RAIZ / "img" / "navidad" / "publicaciones"
PUBS = [("01-portada", "Bocaditos para Nochebuena y Nochevieja")] + [(f"0{i + 2}-{c['id']}", f"{c['titulo']} · {c['sub']} · {c['precio']}") for i, c in enumerate(COMBOS)] + [("06-como-encargar", "¿Cómo lo encargo?")]
PUB_DST.mkdir(parents=True, exist_ok=True)
for nombre, _ in PUBS:
    if (PUB_SRC / f"{nombre}.jpg").exists():
        Image.open(PUB_SRC / f"{nombre}.jpg").convert("RGB").save(PUB_DST / f"{nombre}.webp", "WEBP", quality=84, method=6)

V = re.search(r"\?v=(\d+)", (RAIZ / "index.html").read_text(encoding="utf-8")).group(1)
URL = "https://lorenrestobar.com/navidad"
wa = lambda texto: WA_LINK + "?text=" + urllib.parse.quote(texto)
DIAS = {"24": "24 de diciembre (Nochebuena)", "31": "31 de diciembre (Nochevieja)"}


def msg(c=None, dia=None):
    d = DIAS[dia] if dia else "24 / 31 de diciembre"
    if c:
        return f"¡Hola Loren! Quiero encargar el {c['titulo']} ({c['sub']}).\n• Día: {d}\n• Cantidad: \n• Nombre: "
    return f"¡Hola Loren! Quiero encargar bocaditos para las fiestas.\n• Combo: \n• Día: {d}\n• Nombre: "


TIT = "Bocaditos para Nochebuena y Nochevieja · Loren Restobar"
DESC = ("Combos de bocaditos paraguayos para Nochebuena (24) y Nochevieja (31) en Barcelona: 50 unidades desde 65 €, "
        "tablas de embutidos y quesos para 8–10 personas. Encarga por WhatsApp y recoge en Carrer de la Muntanya 115.")


def tarjeta(c, i):
    items = "".join(f"<li>{x}</li>" for x in c["items"])
    return f"""      <article class="nv-combo rv" data-delay="{i % 2 + 1}">
        <div class="nv-combo__foto" data-nv-ver="{i + 1}" role="button" tabindex="0" aria-label="Ver la publicación del {c['titulo']} en grande"><span class="nv-lupa">🔍 Ver en grande</span><img src="img/navidad/{c['foto']}.webp" alt="{c['titulo']} de Navidad: {', '.join(c['items'][:3]).lower()}" loading="lazy">
          <span class="nv-combo__cant">{c['cantidad']}</span><span class="nv-combo__precio">{c['precio']}</span></div>
        <div class="nv-combo__cuerpo">
          <h3>{c['titulo']} <em>{c['sub']}</em></h3>
          <ul>{items}</ul>
          <div class="nv-combo__btns">
            <a class="nv-btn nv-btn--24" href="{wa(msg(c, '24'))}" target="_blank" rel="noopener">🎄 Para el 24</a>
            <a class="nv-btn nv-btn--31" href="{wa(msg(c, '31'))}" target="_blank" rel="noopener">🥂 Para el 31</a>
          </div>
        </div>
      </article>"""


ld = {"@context": "https://schema.org", "@type": "WebPage", "url": URL, "name": TIT, "description": DESC, "inLanguage": "es",
      "about": {"@id": "https://lorenrestobar.com/#restaurante"},
      "mainEntity": {"@type": "OfferCatalog", "name": "Bocaditos para Nochebuena y Nochevieja", "itemListElement": [
          {"@type": "Offer", "price": c["precio"].replace(" €", "").replace(",", "."), "priceCurrency": "EUR",
           "itemOffered": {"@type": "Product", "name": f"{c['titulo']} · {c['sub']}", "description": ", ".join(c["items"])}} for c in COMBOS]}}

CSS = r"""
/* ====== Navidad (sólo esta página) ====== */
.nv { --oro:#e8b43a; --oro2:#f4d27a; --vino:#59011d; --carb:#151012; }
.nv-hero { position:relative; overflow:hidden; isolation:isolate; color:var(--crema); text-align:center;
  padding:calc(var(--nav-h) + clamp(70px, 9vw, 120px)) 0 clamp(70px, 8vw, 110px);
  background:radial-gradient(900px 520px at 50% 20%, #5b0a26 0%, transparent 65%), radial-gradient(700px 500px at 0% 100%, #3d0014, transparent 60%),
    radial-gradient(700px 500px at 100% 100%, #2a000e, transparent 60%), var(--carb); }
.nv-hero::after { content:""; position:absolute; inset:0; z-index:-1; background:url("img/kv/textura-oscura.webp") center/cover; opacity:.35; mix-blend-mode:screen; }
#nv-nieve { position:absolute; inset:0; width:100%; height:100%; z-index:0; pointer-events:none; }
.nv-guir { position:absolute; left:0; right:0; top:var(--nav-h); height:150px; z-index:2; pointer-events:none; }
.nv-guir svg { position:absolute; inset:0; width:100%; height:100%; overflow:visible; }
.nv-bombilla { position:absolute; width:12px; height:15px; margin:-2px 0 0 -6px; border-radius:50%; animation:nv-titila 2.4s ease-in-out infinite; }
@keyframes nv-titila { 0%,100% { opacity:1; } 50% { opacity:.35; } }
.nv-adorno { position:absolute; display:flex; flex-direction:column; align-items:center; transform-origin:50% 0; animation:nv-mece 4s ease-in-out infinite; }
.nv-adorno i { width:2px; flex:1; background:linear-gradient(rgba(244,210,122,.3), var(--oro2)); }
.nv-adorno b { width:22%; height:9px; border-radius:3px 3px 1px 1px; background:linear-gradient(90deg,#8a5a10,#f4d27a 45%,#8a5a10); margin-bottom:-2px; position:relative; z-index:1; }
.nv-adorno span { border-radius:50%; position:relative; overflow:hidden; background:radial-gradient(circle at 34% 30%, #fff7dc 0, #f4d27a 22%, #c98e1e 62%, #6e4308 100%); box-shadow:0 0 30px rgba(244,210,122,.55), 0 10px 20px rgba(0,0,0,.5); }
.nv-adorno span.vino { background:radial-gradient(circle at 34% 30%, #ffd0d8 0, #b0405f 20%, #59011d 60%, #1c0009 100%); box-shadow:0 0 26px rgba(176,64,95,.55), 0 10px 20px rgba(0,0,0,.5); }
.nv-adorno span img { position:absolute; inset:9%; width:82%; height:82%; opacity:.6; mix-blend-mode:multiply; }
.nv-adorno span.vino img { mix-blend-mode:screen; filter:sepia(1) saturate(2.5) brightness(1.1); opacity:.55; }
.nv-adorno span::after { content:""; position:absolute; left:18%; top:12%; width:30%; height:20%; border-radius:50%; background:rgba(255,255,255,.55); filter:blur(3px); }
@keyframes nv-mece { 0%,100% { transform:rotate(-5deg); } 50% { transform:rotate(5deg); } }
.nv-hero .wrap { position:relative; z-index:3; }
.nv-miga { display:inline-block; margin-bottom:18px; }
.nv-eyebrow { display:inline-flex; gap:14px; align-items:center; font-weight:800; letter-spacing:.28em; text-transform:uppercase; color:var(--oro2); font-size:clamp(.72rem, 1.4vw, .95rem); }
.nv-eyebrow::before, .nv-eyebrow::after { content:"✦"; color:var(--oro); text-shadow:0 0 12px rgba(244,210,122,.9); }
.nv-h1 { font-family:var(--f-titular); font-weight:400; text-transform:uppercase; line-height:.95; margin:18px 0 0; font-size:clamp(2.9rem, 8.4vw, 6.6rem); text-shadow:0 10px 40px rgba(0,0,0,.6); }
.nv-h1 .y { display:block; font-family:var(--f-script); text-transform:none; color:var(--oro2); font-size:.6em; line-height:1.15; transform:rotate(-3deg); margin:12px 0 18px; text-shadow:0 4px 24px rgba(0,0,0,.8); }
.nv-h1 .brilla { background:linear-gradient(100deg, #f3eedc 30%, #fff8dc 45%, #f4d27a 50%, #fff8dc 55%, #f3eedc 70%); background-size:250% 100%; -webkit-background-clip:text; background-clip:text; color:transparent; animation:nv-brillo 5s linear infinite; }
@keyframes nv-brillo { from { background-position:150% 0; } to { background-position:-100% 0; } }
.nv-cinta { display:inline-block; margin-top:14px; font-family:var(--f-script); color:#2a000e; font-size:clamp(1.2rem, 2.6vw, 1.7rem); padding:.15em 1.2em .25em;
  background:linear-gradient(90deg,#c98e1e,#f4d27a 30%,#fff1c2 50%,#f4d27a 70%,#c98e1e); transform:rotate(-2deg); box-shadow:0 10px 24px -8px rgba(0,0,0,.7), 0 0 26px rgba(244,210,122,.35); position:relative; }
.nv-cinta::before, .nv-cinta::after { content:""; position:absolute; top:22%; width:.9em; height:76%; background:#a9761c; z-index:-1; }
.nv-cinta::before { left:-.55em; clip-path:polygon(0 0,100% 0,100% 100%,0 100%,40% 50%); }
.nv-cinta::after { right:-.55em; clip-path:polygon(0 0,100% 0,60% 50%,100% 100%,0 100%); }
.nv-intro { max-width:640px; margin:22px auto 0; color:rgba(243,238,220,.85); font-size:clamp(1rem, 1.6vw, 1.12rem); line-height:1.65; }
/* cuentas atrás */
.nv-cuentas { display:grid; grid-template-columns:1fr 1fr; gap:clamp(16px, 2.4vw, 30px); max-width:980px; margin:clamp(34px, 4vw, 50px) auto 0; }
.nv-cuenta { position:relative; padding:clamp(20px, 2.6vw, 30px) clamp(16px, 2vw, 26px) clamp(22px, 2.6vw, 28px); border-radius:26px; overflow:hidden;
  background:linear-gradient(160deg, rgba(243,238,220,.09), rgba(243,238,220,.03)); border:1.5px solid rgba(232,180,58,.55); backdrop-filter:blur(6px);
  box-shadow:0 30px 60px -30px rgba(0,0,0,.8), inset 0 0 40px rgba(232,180,58,.07); }
.nv-cuenta::before { content:""; position:absolute; right:-40px; top:-40px; width:170px; height:170px; background:url("img/kv/flor-kv.webp") center/contain no-repeat; opacity:.14; animation:girar 40s linear infinite; }
.nv-cuenta--31 { border-color:rgba(176,64,95,.75); background:linear-gradient(160deg, rgba(176,64,95,.18), rgba(243,238,220,.03)); }
.nv-cuenta h2 { margin:0; font-family:var(--f-script); font-weight:400; color:var(--oro2); font-size:clamp(1.9rem, 3.6vw, 2.7rem); line-height:1; }
.nv-cuenta .fecha { display:block; margin-top:6px; font-weight:800; letter-spacing:.2em; text-transform:uppercase; font-size:.75rem; color:rgba(243,238,220,.75); }
.nv-cuenta .falta { margin-top:14px; font-size:.82rem; letter-spacing:.12em; text-transform:uppercase; font-weight:700; color:rgba(243,238,220,.7); }
.nv-digitos { display:flex; justify-content:center; gap:clamp(6px, 1.2vw, 12px); margin-top:10px; }
.nv-digitos div { min-width:clamp(58px, 7.6vw, 86px); padding:10px 4px 8px; border-radius:14px; background:rgba(0,0,0,.35); border:1px solid rgba(243,238,220,.12); }
.nv-digitos b { display:block; font-family:var(--f-titular); font-weight:400; font-size:clamp(1.9rem, 4.4vw, 3.1rem); line-height:1; color:#fff; text-shadow:0 0 20px rgba(244,210,122,.45); }
.nv-digitos b.tic { animation:nv-tic .45s var(--ease); }
@keyframes nv-tic { from { transform:translateY(-8px); opacity:.2; } to { transform:none; opacity:1; } }
.nv-digitos small { display:block; margin-top:4px; font-size:.68rem; letter-spacing:.14em; text-transform:uppercase; color:rgba(243,238,220,.65); font-weight:700; }
.nv-hoy { margin-top:16px; font-family:var(--f-script); font-size:clamp(1.8rem, 3.4vw, 2.6rem); color:#fff; text-shadow:0 0 26px rgba(244,210,122,.8); }
.nv-cuenta .nv-btn { margin-top:18px; }
.nv-btn { display:inline-flex; align-items:center; justify-content:center; gap:8px; padding:.85em 1.4em; border-radius:999px; font-weight:800; font-size:.92rem; text-decoration:none; transition:transform .3s var(--ease), box-shadow .3s; }
.nv-btn:hover { transform:translateY(-3px); }
.nv-btn--24 { background:var(--oro); color:#2a000e; box-shadow:0 12px 26px -10px rgba(232,180,58,.8); }
.nv-btn--31 { background:linear-gradient(135deg,#b0405f,#59011d); color:#fff; box-shadow:0 12px 26px -10px rgba(176,64,95,.9), inset 0 0 0 2px rgba(244,210,122,.6); }
.nv-ctas { display:flex; gap:14px; justify-content:center; flex-wrap:wrap; margin-top:30px; }
/* dos noches */
.nv-sec { position:relative; overflow:hidden; padding:clamp(70px, 9vw, 120px) 0; }
.nv-sec--oscura { background:radial-gradient(800px 500px at 50% 0%, #3d0014, transparent 65%), var(--carb); color:var(--crema); }
.nv-sec--crema { background:radial-gradient(rgba(89,1,29,.035) 1px, transparent 1.4px) 0 0/7px 7px, radial-gradient(120% 80% at 50% 40%, #fbf6ea, #efe2c6); color:#2a1a1e; }
.nv-cab { text-align:center; max-width:760px; margin:0 auto clamp(34px, 4vw, 54px); }
.nv-cab h2 { margin:10px 0 0; font-family:var(--f-titular); font-weight:400; text-transform:uppercase; font-size:clamp(2.2rem, 5vw, 3.8rem); line-height:1; }
.nv-cab h2 em { font-family:var(--f-script); text-transform:none; font-style:normal; color:var(--oro); display:inline-block; transform:rotate(-3deg); }
.nv-sec--crema .nv-cab h2 { color:var(--vino); }
.nv-sec--crema .nv-cab h2 em { color:#c98e1e; }
.nv-cab p { margin:16px auto 0; opacity:.85; line-height:1.65; }
.nv-noches { display:grid; grid-template-columns:1fr 1fr; gap:clamp(16px, 2.4vw, 30px); }
.nv-noche { position:relative; min-height:440px; border-radius:30px; overflow:hidden; display:flex; flex-direction:column; justify-content:flex-end; padding:clamp(24px, 3vw, 38px); color:#fff;
  box-shadow:0 40px 70px -35px rgba(0,0,0,.9); isolation:isolate; }
.nv-noche > img { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; z-index:-2; transition:transform 1.4s var(--ease); }
.nv-noche:hover > img { transform:scale(1.06); }
.nv-noche::before { content:""; position:absolute; inset:0; z-index:-1; background:linear-gradient(180deg, rgba(21,16,18,.05) 20%, rgba(21,16,18,.92) 82%); }
.nv-noche--31::before { background:linear-gradient(180deg, rgba(42,0,14,.1) 20%, rgba(42,0,14,.95) 82%); }
.nv-noche .chip { position:absolute; top:22px; left:22px; background:var(--oro); color:#2a000e; font-weight:800; padding:.5em 1em; border-radius:999px; font-size:.85rem; letter-spacing:.06em; }
.nv-noche--31 .chip { background:#b0405f; color:#fff; }
.nv-noche h3 { margin:0; font-family:var(--f-script); font-weight:400; font-size:clamp(2.4rem, 4.6vw, 3.4rem); color:var(--oro2); line-height:1; }
.nv-noche p { margin:12px 0 18px; color:rgba(255,255,255,.88); line-height:1.6; max-width:420px; }
.nv-noche .nv-btn { align-self:flex-start; }
/* combos */
.nv-combos { display:grid; grid-template-columns:repeat(4, 1fr); gap:clamp(16px, 2vw, 26px); }
.nv-combo { background:#fffdf8; border-radius:28px; overflow:hidden; display:flex; flex-direction:column; box-shadow:0 30px 60px -32px rgba(60,10,20,.55); border:1.5px solid rgba(201,142,30,.35);
  transition:transform .5s var(--ease), box-shadow .5s; }
.nv-combo:hover { transform:translateY(-6px) rotate(-.4deg); box-shadow:0 40px 70px -30px rgba(60,10,20,.6); }
.nv-combo__foto { position:relative; aspect-ratio:4/3; }
.nv-combo__foto img { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; object-position:50% 58%; transition:transform 1.2s var(--ease); }
.nv-combo:hover .nv-combo__foto img { transform:scale(1.08); }
.nv-combo__cant { position:absolute; left:14px; top:14px; background:rgba(21,16,18,.82); color:var(--oro2); font-weight:800; font-size:.74rem; padding:.45em .9em; border-radius:999px; letter-spacing:.06em; text-transform:uppercase; }
.nv-combo__precio { position:absolute; right:12px; bottom:12px; font-family:var(--f-titular); font-size:2rem; color:#fff; background:linear-gradient(135deg,#7d0b2e,#59011d); padding:.15em .55em; border-radius:12px 26px 12px 26px; box-shadow:0 10px 24px -6px rgba(0,0,0,.6), inset 0 0 0 2px var(--oro); }
.nv-combo__cuerpo { padding:clamp(20px, 2.2vw, 28px); display:flex; flex-direction:column; flex:1; }
.nv-combo h3 { margin:0; font-family:var(--f-titular); font-weight:400; text-transform:uppercase; font-size:1.9rem; color:var(--vino); line-height:1; }
.nv-combo h3 em { display:block; font-family:var(--f-script); text-transform:none; font-style:normal; color:#c98e1e; font-size:1.1rem; margin-top:4px; }
.nv-combo ul { list-style:none; padding:0; margin:14px 0 18px; flex:1; color:#4a3a3e; font-size:.93rem; line-height:1.5; }
.nv-combo li { position:relative; padding-left:1.3em; }
.nv-combo li::before { content:"✦"; position:absolute; left:0; color:#e8b43a; }
.nv-combo__btns { display:flex; gap:10px; flex-wrap:wrap; }
.nv-combo__btns .nv-btn { flex:1 1 auto; padding:.75em .9em; font-size:.84rem; white-space:nowrap; }
.nv-nota { text-align:center; margin-top:28px; color:#6a5458; font-size:.9rem; }
/* tradiciones */
.nv-trad { display:grid; grid-template-columns:repeat(4, 1fr); gap:18px; }
.nv-trad div { text-align:center; padding:28px 20px; border-radius:24px; background:rgba(243,238,220,.05); border:1px solid rgba(243,238,220,.12); transition:transform .4s var(--ease), background .4s; }
.nv-trad div:hover { transform:translateY(-6px); background:rgba(243,238,220,.09); }
.nv-trad .ic { font-size:2.4rem; display:block; margin-bottom:10px; animation:nv-flota 4s ease-in-out infinite; }
.nv-trad div:nth-child(2) .ic { animation-delay:-1s; } .nv-trad div:nth-child(3) .ic { animation-delay:-2s; } .nv-trad div:nth-child(4) .ic { animation-delay:-3s; }
@keyframes nv-flota { 0%,100% { transform:translateY(0); } 50% { transform:translateY(-8px); } }
.nv-trad h3 { margin:0; font-family:var(--f-script); font-weight:400; color:var(--oro2); font-size:1.6rem; }
.nv-trad p { margin:8px 0 0; color:rgba(243,238,220,.75); font-size:.92rem; line-height:1.55; }
/* pasos */
.nv-pasos { display:grid; grid-template-columns:repeat(3, 1fr); gap:20px; counter-reset:p; }
.nv-pasos div { position:relative; padding:30px 24px 26px; border-radius:24px; background:#fffdf8; border:1.5px solid rgba(201,142,30,.3); box-shadow:0 20px 40px -28px rgba(60,10,20,.5); }
.nv-pasos div::before { counter-increment:p; content:counter(p); position:absolute; top:-22px; left:24px; width:46px; height:46px; border-radius:50%; display:grid; place-items:center;
  background:var(--vino); color:#fff6e0; font-family:var(--f-script); font-size:1.5rem; box-shadow:inset 0 0 0 3px var(--oro); }
.nv-pasos h3 { margin:6px 0 6px; font-family:var(--f-script); font-weight:400; color:var(--vino); font-size:1.6rem; }
.nv-pasos p { margin:0; color:#5a474b; font-size:.94rem; line-height:1.55; }
/* final con fuegos */
.nv-final { position:relative; overflow:hidden; isolation:isolate; text-align:center; color:var(--crema); padding:clamp(90px, 12vw, 160px) 0;
  background:radial-gradient(800px 500px at 50% 100%, #59011d, transparent 70%), #0e0a0b; }
#nv-fuegos { position:absolute; inset:0; width:100%; height:100%; z-index:-1; }
.nv-final h2 { margin:0; font-family:var(--f-titular); font-weight:400; text-transform:uppercase; font-size:clamp(2.4rem, 6vw, 4.6rem); line-height:1; }
.nv-final h2 em { display:block; font-family:var(--f-script); text-transform:none; font-style:normal; color:var(--oro2); font-size:.7em; margin-top:8px; }
.nv-final p { margin:18px auto 0; max-width:560px; color:rgba(243,238,220,.82); }
@media (max-width: 1100px) { .nv-combos { grid-template-columns:repeat(2, 1fr); } }
@media (max-width: 900px) {
  .nv-cuentas, .nv-noches { grid-template-columns:1fr; }
  .nv-trad { grid-template-columns:1fr 1fr; }
  .nv-pasos { grid-template-columns:1fr; gap:34px; }
}
@media (max-width: 560px) {
  .nv-combos { grid-template-columns:1fr; }
  .nv-eyebrow { letter-spacing:.14em; gap:8px; }
  .nv-trad { grid-template-columns:1fr; }
  .nv-guir { height:110px; }
}
/* ---------- visor de publicaciones ---------- */
.nv-combo__foto { cursor:zoom-in; }
.nv-lupa { position:absolute; left:50%; top:50%; z-index:2; transform:translate(-50%,-50%) scale(.9); opacity:0; background:rgba(21,16,18,.82); color:#fff; font-weight:800; font-size:.85rem;
  padding:.6em 1.1em; border-radius:999px; transition:.35s var(--ease); pointer-events:none; white-space:nowrap; }
.nv-combo__foto:hover .nv-lupa, .nv-combo__foto:focus-visible .nv-lupa { opacity:1; transform:translate(-50%,-50%) scale(1); }
@media (hover:none) { .nv-lupa { opacity:.92; transform:translate(-50%,-50%) scale(1); top:auto; bottom:12px; left:12px; transform:none; font-size:.75rem; } .nv-combo__precio { bottom:auto; top:12px; right:12px; } .nv-combo__cant { display:none; } }
.lightbox img { max-height:84vh; }
.nv-ver-todo { display:flex; justify-content:center; margin-top:26px; }
/* ---------- intro: el regalo que se abre ---------- */
#nv-intro { position:fixed; inset:0; z-index:20000; display:grid; place-items:center; overflow:hidden; color:var(--crema);
  background:radial-gradient(700px 520px at 50% 45%, #5b0a26, transparent 70%), #0e0a0b; transition:opacity .7s ease, visibility .7s; }
#nv-intro.fuera { opacity:0; visibility:hidden; }
#nv-intro .escena { position:relative; width:260px; height:260px; }
#nv-intro .caja { position:absolute; left:30px; right:30px; bottom:0; height:170px; border-radius:10px;
  background:linear-gradient(90deg, #3d0014, #7d0b2e 30%, #9c1840 50%, #7d0b2e 70%, #3d0014); box-shadow:0 30px 60px -20px rgba(0,0,0,.8); animation:nv-cae .7s cubic-bezier(.2,1.4,.4,1) both; }
#nv-intro .tapa { position:absolute; left:16px; right:16px; bottom:160px; height:46px; border-radius:8px; z-index:2;
  background:linear-gradient(90deg, #4a0019, #8a1038 30%, #ad2050 50%, #8a1038 70%, #4a0019); box-shadow:0 10px 20px -8px rgba(0,0,0,.7);
  animation:nv-cae .7s cubic-bezier(.2,1.4,.4,1) both, nv-tapa .9s 1.5s cubic-bezier(.5,0,.3,1) forwards; }
#nv-intro .cinta-v { position:absolute; left:50%; width:30px; margin-left:-15px; background:linear-gradient(90deg, #a9761c, #f4d27a 45%, #fff1c2 50%, #f4d27a 55%, #a9761c); }
#nv-intro .caja .cinta-v { top:0; bottom:0; }
#nv-intro .tapa .cinta-v { top:0; bottom:0; }
#nv-intro .lazo { position:absolute; left:50%; bottom:192px; width:150px; margin-left:-75px; z-index:3; filter:drop-shadow(0 8px 12px rgba(0,0,0,.5));
  animation:nv-cae .7s cubic-bezier(.2,1.4,.4,1) both, nv-desata .6s 1.0s ease-in forwards; transform-origin:50% 70%; }
#nv-intro .luz { position:absolute; left:50%; bottom:150px; width:30px; height:30px; margin-left:-15px; border-radius:50%; opacity:0; z-index:1;
  background:radial-gradient(circle, #fff8dc 0, #f4d27a 30%, rgba(244,210,122,0) 70%); animation:nv-luz 1.2s 1.7s ease-out forwards; }
#nv-intro .copo { position:absolute; left:50%; bottom:170px; width:34px; margin-left:-17px; opacity:0; z-index:4; animation:nv-sale 1.6s ease-out forwards; }
#nv-intro .txt { position:absolute; left:0; right:0; top:calc(50% + 160px); text-align:center; padding:0 20px; }
#nv-intro .txt b { display:block; font-family:var(--f-titular); font-weight:400; text-transform:uppercase; font-size:clamp(2.2rem, 7vw, 4.4rem); line-height:1; opacity:0; animation:nv-sube .8s 2.0s var(--ease) forwards; }
#nv-intro .txt em { display:block; font-family:var(--f-script); font-style:normal; color:var(--oro2); font-size:clamp(1.6rem, 4.6vw, 2.8rem); margin-top:6px; opacity:0; animation:nv-sube .8s 2.3s var(--ease) forwards; }
#nv-intro .txt small { display:block; margin-top:12px; font-weight:800; letter-spacing:.28em; text-transform:uppercase; color:rgba(243,238,220,.75); font-size:.8rem; opacity:0; animation:nv-sube .8s 2.6s var(--ease) forwards; }
#nv-intro .logo { position:absolute; left:50%; top:clamp(40px, 9vh, 90px); width:150px; margin-left:-75px; opacity:0; animation:nv-sube .8s .3s var(--ease) forwards; filter:drop-shadow(0 6px 14px rgba(0,0,0,.6)); }
#nv-intro .saltar { position:absolute; right:20px; bottom:22px; border:1px solid rgba(243,238,220,.35); background:rgba(243,238,220,.08); color:var(--crema); font:700 .85rem var(--f-body);
  padding:.6em 1.2em; border-radius:999px; cursor:pointer; }
@keyframes nv-cae { from { transform:translateY(-120vh) rotate(-8deg); } to { transform:none; } }
@keyframes nv-desata { to { transform:translateY(-30px) scale(1.4) rotate(14deg); opacity:0; } }
@keyframes nv-tapa { to { transform:translate(140px, -340px) rotate(38deg); opacity:0; } }
@keyframes nv-luz { 0% { opacity:0; transform:scale(1); } 30% { opacity:1; } 100% { opacity:0; transform:scale(60); } }
@keyframes nv-sale { 0% { opacity:0; transform:translate(0,0) rotate(0) scale(.4); } 15% { opacity:1; } 100% { opacity:0; transform:translate(var(--dx), var(--dy)) rotate(260deg) scale(1.1); } }
@keyframes nv-sube { from { opacity:0; transform:translateY(24px); } to { opacity:1; transform:none; } }
@media (prefers-reduced-motion: reduce) {
  #nv-intro .caja, #nv-intro .tapa, #nv-intro .lazo, #nv-intro .luz, #nv-intro .copo { animation:none !important; }
  #nv-intro .txt b, #nv-intro .txt em, #nv-intro .txt small { animation:none !important; opacity:1; }
}
@media (prefers-reduced-motion: reduce) {
  .nv-bombilla, .nv-adorno, .nv-h1 .brilla, .nv-trad .ic, .nv-cuenta::before { animation:none !important; }
}
"""

JS = r"""
(function () {
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const $ = (s) => document.querySelector(s);

  /* ---------- Intro: el regalo que se abre (una vez por visita) ---------- */
  const intro = $("#nv-intro");
  if (intro) {
    let visto = false; try { visto = sessionStorage.getItem("nv-intro") === "1"; } catch (e) {}
    const quitar = () => { intro.classList.add("fuera"); document.documentElement.style.overflow = ""; setTimeout(() => intro.remove(), 800); };
    if (visto) intro.remove();
    else {
      try { sessionStorage.setItem("nv-intro", "1"); } catch (e) {}
      document.documentElement.style.overflow = "hidden";
      intro.addEventListener("click", quitar);
      setTimeout(quitar, reduce ? 1400 : 4300);
    }
  }

  /* ---------- Ver las publicaciones en grande ---------- */
  const gal = [...document.querySelectorAll("#nv-galeria [data-lb]")];
  document.addEventListener("click", (e) => {
    const b = e.target.closest("[data-nv-ver]"); if (!b || !gal.length) return;
    e.preventDefault(); gal[Math.min(+b.dataset.nvVer, gal.length - 1)].click();
  });
  document.addEventListener("keydown", (e) => {
    const b = e.target.closest && e.target.closest("[data-nv-ver]");
    if (b && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); b.click(); }
  });
  const lbx = $(".lightbox");   // deslizar con el dedo en el visor
  let x0 = null;
  document.addEventListener("touchstart", (e) => { if (lbx && lbx.classList.contains("is-open")) x0 = e.touches[0].clientX; }, { passive: true });
  document.addEventListener("touchend", (e) => {
    if (x0 === null || !lbx) return; const dx = e.changedTouches[0].clientX - x0; x0 = null;
    if (Math.abs(dx) > 50) lbx.querySelector(dx < 0 ? ".lb-next" : ".lb-prev").click();
  }, { passive: true });

  /* ---------- Cuentas atrás (hora de España) ---------- */
  const F = (s) => new Date(s + "+01:00");
  const EVENTOS = {
    "24": { fin: F("2026-12-24T00:00:00"), hoyHasta: F("2026-12-26T00:00:00"), hoy: "¡Hoy es Nochebuena! 🎄", pasado: "¡Feliz Navidad! 🎄" },
    "31": { fin: F("2026-12-31T00:00:00"), hoyHasta: F("2027-01-01T00:00:00"), campanadas: F("2027-01-01T00:00:00"), pasado: "¡Feliz Año Nuevo! 🥂" }
  };
  const pad = (n) => String(n).padStart(2, "0");
  function pinta(id) {
    const el = document.querySelector('[data-cuenta="' + id + '"]'); if (!el) return;
    const ev = EVENTOS[id], ahora = new Date();
    let objetivo = ev.fin, txt = null, falta = "Faltan";
    if (ahora >= ev.fin) {
      if (id === "31" && ahora < ev.campanadas) { objetivo = ev.campanadas; falta = "Para las campanadas"; }
      else if (ahora < ev.hoyHasta && id === "24") txt = ev.hoy;
      else txt = ev.pasado;
    }
    el.querySelector(".falta").textContent = txt ? "" : falta;
    const dig = el.querySelector(".nv-digitos"), hoy = el.querySelector(".nv-hoy");
    if (txt) { dig.hidden = true; hoy.hidden = false; hoy.textContent = txt; return; }
    dig.hidden = false; hoy.hidden = true;
    let s = Math.max(0, Math.floor((objetivo - ahora) / 1000));
    const v = [Math.floor(s / 86400), Math.floor(s % 86400 / 3600), Math.floor(s % 3600 / 60), s % 60];
    dig.querySelectorAll("b").forEach((b, i) => {
      const t = i === 0 ? String(v[i]) : pad(v[i]);
      if (b.textContent !== t) { b.textContent = t; if (!reduce) { b.classList.remove("tic"); void b.offsetWidth; b.classList.add("tic"); } }
    });
  }
  const tic = () => { pinta("24"); pinta("31"); };
  tic(); setInterval(tic, 1000);

  /* ---------- Guirnalda con bombillas y bolas ---------- */
  const guir = $(".nv-guir");
  function guirnalda() {
    if (!guir) return;
    const W = guir.clientWidth, sag = Math.min(70, W * .06), tramos = W < 700 ? 1 : 2, gy = (x) => 10 + sag * Math.abs(Math.sin(Math.PI * x / (W / tramos)));
    let p = ""; for (let x = -10; x <= W + 10; x += 8) p += x + "," + gy(x).toFixed(1) + " ";
    let h = '<svg><polyline points="' + p + '" fill="none" stroke="#f4d27a" stroke-width="2.5" style="filter:drop-shadow(0 0 4px rgba(244,210,122,.9))"/></svg>';
    const col = ["#fff3c4", "#f4d27a", "#ffb347", "#fff3c4", "#ffd27a"];
    for (let k = 0, x = 18; x < W; x += 46, k++) {
      const c = col[k % 5];
      h += '<span class="nv-bombilla" style="left:' + x + "px;top:" + (gy(x) + 3) + "px;background:" + c + ";box-shadow:0 0 10px 3px " + c + ",0 0 24px 8px rgba(255,190,90,.4);animation-delay:" + (-(k * 0.37) % 2.4).toFixed(2) + 's"></span>';
    }
    const bolas = W < 700 ? [[.07, 18, 46], [.93, 26, 50]] : [[.06, 90, 70], [.2, 30, 48], [.8, 40, 52], [.94, 110, 76]];
    bolas.forEach(([f, l, d], i) => {
      const x = f * W, y = gy(x);
      h += '<div class="nv-adorno" style="left:' + (x - d / 2) + "px;top:" + y + "px;width:" + d + "px;height:" + (l + d + 8) + "px;animation-delay:" + (-i * 0.9) + 's"><i></i><b></b><span class="' + (i % 2 ? "vino" : "") + '" style="width:' + d + "px;height:" + d + 'px"><img src="img/kv/flor-kv.webp" alt=""></span></div>';
    });
    guir.innerHTML = h;
  }
  guirnalda(); let rt; addEventListener("resize", () => { clearTimeout(rt); rt = setTimeout(guirnalda, 200); });

  /* ---------- Nieve de ñandutí y luces desenfocadas ---------- */
  function lienzo(cv, dibuja) {
    if (!cv) return;
    const ctx = cv.getContext("2d"); let W = 0, H = 0, vis = true, t0 = performance.now();
    const size = () => { const d = Math.min(devicePixelRatio || 1, 2); W = cv.clientWidth; H = cv.clientHeight; cv.width = W * d; cv.height = H * d; ctx.setTransform(d, 0, 0, d, 0, 0); };
    size(); addEventListener("resize", size);
    new IntersectionObserver(([e]) => (vis = e.isIntersecting)).observe(cv);
    const bucle = (now) => { if (vis && !document.hidden) dibuja(ctx, W, H, (now - t0) / 1000); requestAnimationFrame(bucle); };
    if (reduce) dibuja(ctx, W, H, 0); else requestAnimationFrame(bucle);
  }
  const flor = new Image(); flor.src = "img/kv/flor-kv.webp";
  const R = (n) => { const x = Math.sin(n * 91.7) * 43758.5453; return x - Math.floor(x); };
  const COPOS = Array.from({ length: innerWidth < 700 ? 34 : 70 }, (_, i) => ({ x: R(i + 1), y: R(i + 50), s: 8 + R(i + 99) * 22, v: 18 + R(i + 7) * 40, w: R(i + 3) * 6, f: .3 + R(i + 9) * .7, a: .25 + R(i + 11) * .5 }));
  const LUCES = Array.from({ length: 16 }, (_, i) => ({ x: R(i + 300), y: R(i + 400), r: 30 + R(i + 500) * 90, f: .15 + R(i + 600) * .3, c: ["244,210,122", "255,170,80", "255,236,190", "176,64,95"][i % 4], a: .12 + R(i + 700) * .2 }));
  lienzo($("#nv-nieve"), (ctx, W, H, t) => {
    ctx.clearRect(0, 0, W, H);
    LUCES.forEach((l) => {
      const x = l.x * W + Math.sin(t * l.f + l.x * 9) * 40, y = ((l.y * H - t * 10 * l.f) % H + H) % H;
      const g = ctx.createRadialGradient(x, y, 0, x, y, l.r); g.addColorStop(0, "rgba(" + l.c + "," + l.a + ")"); g.addColorStop(1, "rgba(" + l.c + ",0)");
      ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, l.r, 0, 6.3); ctx.fill();
    });
    if (!flor.complete) return;
    COPOS.forEach((c) => {
      const y = ((c.y * (H + 60) + t * c.v) % (H + 60)) - 30, x = c.x * W + Math.sin(t * c.f + c.x * 20) * 18 * c.w / 3;
      ctx.save(); ctx.globalAlpha = c.a; ctx.translate(x, y); ctx.rotate(t * c.f * .6 + c.x * 6); ctx.drawImage(flor, -c.s / 2, -c.s / 2, c.s, c.s); ctx.restore();
    });
  });

  /* ---------- Fuegos artificiales dorados al final ---------- */
  const CH = []; let prox = 0;
  lienzo($("#nv-fuegos"), (ctx, W, H, t) => {
    ctx.globalCompositeOperation = "source-over"; ctx.fillStyle = "rgba(14,10,11,.22)"; ctx.fillRect(0, 0, W, H);
    if (reduce) return;
    if (t > prox) {
      prox = t + 0.9 + Math.random() * 0.9;
      const cx = W * (.15 + Math.random() * .7), cy = H * (.15 + Math.random() * .4), n = 46, col = Math.random() < .7 ? [244, 210, 122] : [255, 180, 200];
      for (let i = 0; i < n; i++) { const a = i / n * 6.283, v = 1.6 + Math.random() * 2.2; CH.push({ x: cx, y: cy, vx: Math.cos(a) * v, vy: Math.sin(a) * v, vida: 1, col }); }
    }
    ctx.globalCompositeOperation = "lighter";
    for (let i = CH.length - 1; i >= 0; i--) {
      const p = CH[i]; p.x += p.vx; p.y += p.vy; p.vy += .03; p.vx *= .985; p.vy *= .985; p.vida -= .012;
      if (p.vida <= 0) { CH.splice(i, 1); continue; }
      ctx.fillStyle = "rgba(" + p.col.join(",") + "," + p.vida + ")"; ctx.beginPath(); ctx.arc(p.x, p.y, 1.8, 0, 6.3); ctx.fill();
    }
  });
})();
"""


def cuenta(id_, titulo, fecha, clase, boton):
    return f"""      <div class="nv-cuenta {clase} rv" data-cuenta="{id_}">
        <h2>{titulo}</h2><span class="fecha">{fecha}</span>
        <div class="falta">Faltan</div>
        <div class="nv-digitos"><div><b>--</b><small>días</small></div><div><b>--</b><small>horas</small></div><div><b>--</b><small>min</small></div><div><b>--</b><small>seg</small></div></div>
        <div class="nv-hoy" hidden></div>
        {boton}
      </div>"""


html = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{TIT}</title>
  <meta name="description" content="{DESC}">
  <link rel="canonical" href="{URL}">
  <meta property="og:title" content="Bocaditos para Nochebuena y Nochevieja · Loren Restobar">
  <meta property="og:description" content="Nochebuena 24 y Nochevieja 31: combos caseros de bocaditos paraguayos y tablas para compartir. Encarga por WhatsApp.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{URL}">
  <meta property="og:image" content="https://lorenrestobar.com/img/redes/og-navidad-es.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:locale" content="es_ES">
  <meta property="og:site_name" content="Loren Restobar">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#151012">
  <link rel="icon" href="img/marca/favicon.webp" type="image/webp">
  <link rel="stylesheet" href="css/styles.css?v={V}">
  <link rel="stylesheet" href="css/paginas.css?v={V}">
  <link rel="preload" href="fuentes/montserrat-latin-e56e84.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="fuentes/anton-latin-a6f395.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="css/fuentes.css?v={V}">
  <link rel="stylesheet" href="css/v2.css?v={V}">
  <style>{CSS}</style>
  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body data-page="navidad" class="nv">
<div id="nv-intro" aria-hidden="true"><div class="escena"><div class="caja"><span class="cinta-v"></span></div><div class="tapa"><span class="cinta-v"></span></div><svg class="lazo" viewBox="0 0 200 160"><defs><linearGradient id="lzo" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff1c2"/><stop offset=".45" stop-color="#f4d27a"/><stop offset="1" stop-color="#a9761c"/></linearGradient></defs><path d="M93 72 L58 150 L71 141 L79 156 L104 80Z" fill="url(#lzo)"/><path d="M107 72 L142 150 L129 141 L121 156 L96 80Z" fill="url(#lzo)"/><path d="M100 70 C 62 18, 4 22, 16 64 C 26 96, 72 92, 100 76Z" fill="url(#lzo)"/><path d="M100 70 C 138 18, 196 22, 184 64 C 174 96, 128 92, 100 76Z" fill="url(#lzo)"/><path d="M96 70 C 72 46, 42 46, 40 62 C 44 76, 76 78, 96 73Z" fill="#7a4e0c" opacity=".45"/><path d="M104 70 C 128 46, 158 46, 160 62 C 156 76, 124 78, 104 73Z" fill="#7a4e0c" opacity=".45"/><rect x="85" y="56" width="30" height="30" rx="10" fill="url(#lzo)"/></svg><span class="luz"></span><img class="copo" src="img/kv/flor-kv.webp" alt="" style="--dx:-260px;--dy:-220px;animation-delay:1.75s"><img class="copo" src="img/kv/flor-kv.webp" alt="" style="--dx:240px;--dy:-260px;animation-delay:1.78s"><img class="copo" src="img/kv/flor-kv.webp" alt="" style="--dx:-180px;--dy:-380px;animation-delay:1.81s"><img class="copo" src="img/kv/flor-kv.webp" alt="" style="--dx:190px;--dy:-400px;animation-delay:1.84s"><img class="copo" src="img/kv/flor-kv.webp" alt="" style="--dx:-330px;--dy:-60px;animation-delay:1.87s"><img class="copo" src="img/kv/flor-kv.webp" alt="" style="--dx:330px;--dy:-90px;animation-delay:1.90s"><img class="copo" src="img/kv/flor-kv.webp" alt="" style="--dx:0px;--dy:-440px;animation-delay:1.93s"><img class="copo" src="img/kv/flor-kv.webp" alt="" style="--dx:-120px;--dy:-300px;animation-delay:1.96s"><img class="copo" src="img/kv/flor-kv.webp" alt="" style="--dx:120px;--dy:-320px;animation-delay:1.99s"><img class="copo" src="img/kv/flor-kv.webp" alt="" style="--dx:-280px;--dy:-330px;animation-delay:2.02s"><img class="copo" src="img/kv/flor-kv.webp" alt="" style="--dx:280px;--dy:-350px;animation-delay:2.05s"><img class="copo" src="img/kv/flor-kv.webp" alt="" style="--dx:0px;--dy:-250px;animation-delay:2.08s"></div><div class="txt"><b>Navidad</b><em>a la paraguaya</em><small>Nochebuena · Nochevieja</small></div><img class="logo" src="img/marca/logo-loren.webp" alt=""><button class="saltar" type="button">Saltar ›</button></div>
<!-- Generado por herramientas/navidad_web.py: los cambios se hacen en herramientas/navidad_datos.py y en ese script -->
<div id="shell-top"></div>
<main>

<section class="nv-hero">
  <canvas id="nv-nieve" aria-hidden="true"></canvas>
  <div class="nv-guir" aria-hidden="true"></div>
  <div class="wrap">
    <nav class="miga nv-miga" aria-label="Migas"><a href="index.html">Inicio</a> / <span>Navidad</span></nav><br>
    <span class="nv-eyebrow">Nochebuena 24 · Nochevieja 31</span>
    <h1 class="nv-h1"><span class="brilla">Bocaditos para</span><span class="y">Nochebuena y Nochevieja</span><span class="brilla">a la paraguaya</span></h1>
    <span class="nv-cinta">¡Vy'apavẽ Navidad!</span>
    <p class="nv-intro">Este año, las dos noches más especiales saben a Paraguay. Te preparamos bandejas caseras de bocaditos y tablas para compartir, listas para recoger el <b>24</b> y el <b>31 de diciembre</b>.</p>
    <div class="nv-cuentas">
{cuenta("24", "Nochebuena", "Jueves 24 de diciembre", "nv-cuenta--24", f'<a class="nv-btn nv-btn--24" href="{wa(msg(None, "24"))}" target="_blank" rel="noopener">🎄 Encargar para el 24</a>')}
{cuenta("31", "Nochevieja", "Jueves 31 de diciembre", "nv-cuenta--31", f'<a class="nv-btn nv-btn--31" href="{wa(msg(None, "31"))}" target="_blank" rel="noopener">🥂 Encargar para el 31</a>')}
    </div>
    <div class="nv-ctas"><a href="#combos" class="btn" data-nv-ver="0">Ver los combos</a></div>
  </div>
</section>

<section class="nv-sec nv-sec--oscura">
  <div class="wrap">
    <div class="nv-cab"><span class="nv-eyebrow">Dos noches, una mesa</span><h2 class="rv">Paraguay en tu <em>mesa de fiesta</em></h2></div>
    <div class="nv-noches">
      <article class="nv-noche nv-noche--24 rv" data-delay="1"><img src="img/navidad/bandeja-variada-combo2.webp" alt="Bandeja de bocaditos paraguayos para Nochebuena" loading="lazy">
        <span class="chip">24 · Nochebuena</span><h3>Nochebuena</h3>
        <p>La cena en familia, con bocaditos caseros para picar mientras llega la medianoche: empanaditas, chipa guazú, sopa paraguaya y sándwichitos.</p>
        <a class="nv-btn nv-btn--24" href="{wa(msg(None, "24"))}" target="_blank" rel="noopener">🎄 Encargar para el 24</a></article>
      <article class="nv-noche nv-noche--31 rv" data-delay="2"><img src="img/navidad/tabla-embutidos.webp" alt="Tabla de embutidos para Nochevieja" loading="lazy">
        <span class="chip">31 · Nochevieja</span><h3>Nochevieja</h3>
        <p>Despide el año a lo grande: tablas de embutidos y quesos para compartir y bocaditos para el picoteo antes de las campanadas.</p>
        <a class="nv-btn nv-btn--31" href="{wa(msg(None, "31"))}" target="_blank" rel="noopener">🥂 Encargar para el 31</a></article>
    </div>
  </div>
</section>

<section class="nv-sec nv-sec--crema" id="combos">
  <div class="wrap">
    <div class="nv-cab"><span class="nv-eyebrow" style="color:#c98e1e">Navidad y Año Nuevo</span><h2 class="rv">Elige tu <em>combo</em></h2>
      <p class="rv">Dos combos de 50 bocaditos y dos tablas para 8–10 personas. Toca «Para el 24» o «Para el 31» y te abrimos WhatsApp con el pedido ya escrito.</p></div>
    <div class="nv-combos">
{chr(10).join(tarjeta(c, i) for i, c in enumerate(COMBOS))}
    </div>
    <div class="nv-ver-todo"><a href="#" class="nv-btn nv-btn--24" data-nv-ver="0">🔍 Ver todas las publicaciones en grande</a></div>
    <div id="nv-galeria" data-lb-grupo hidden>{"".join(f'<a href="#" data-lb="img/navidad/publicaciones/{n}.webp" data-cap="{cap}"></a>' for n, cap in PUBS)}</div>
    <p class="nv-nota">⏰ Encarga con antelación · Recogida en el local, Carrer de la Muntanya 115 · WhatsApp {WHATSAPP}</p>
  </div>
</section>

<section class="nv-sec nv-sec--oscura">
  <div class="wrap">
    <div class="nv-cab"><span class="nv-eyebrow">Así se celebra en Paraguay</span><h2 class="rv">Una Navidad <em>con sabor a casa</em></h2></div>
    <div class="nv-trad">
      <div class="rv" data-delay="1"><span class="ic">🌽</span><h3>Sopa y chipa</h3><p>La sopa paraguaya y la chipa no faltan en ninguna mesa de fiesta.</p></div>
      <div class="rv" data-delay="2"><span class="ic">🍷</span><h3>Clericó</h3><p>El cóctel de frutas con vino con el que se brinda en las fiestas.</p></div>
      <div class="rv" data-delay="3"><span class="ic">🌼</span><h3>Flor de coco</h3><p>Su perfume anuncia la Navidad en cada casa paraguaya.</p></div>
      <div class="rv" data-delay="4"><span class="ic">⭐</span><h3>El pesebre</h3><p>Se adorna con frutas y flores y es el centro de la casa.</p></div>
    </div>
  </div>
</section>

<section class="nv-sec nv-sec--crema">
  <div class="wrap">
    <div class="nv-cab"><span class="nv-eyebrow" style="color:#c98e1e">Cómo funciona</span><h2 class="rv">Encargarlo es <em>muy fácil</em></h2></div>
    <div class="nv-pasos">
      <div class="rv" data-delay="1"><h3>Elige tu combo</h3><p>Combo 1, Combo 2, la tabla de embutidos o la de quesos.</p></div>
      <div class="rv" data-delay="2"><h3>Escríbenos por WhatsApp</h3><p>Al {WHATSAPP}: dinos el combo, la cantidad y el día (24 o 31 de diciembre).</p></div>
      <div class="rv" data-delay="3"><h3>Recógelo en el local</h3><p>Carrer de la Muntanya 115, Camp de l'Arpa. Encarga con antelación.</p></div>
    </div>
  </div>
</section>

<section class="nv-final">
  <canvas id="nv-fuegos" aria-hidden="true"></canvas>
  <div class="wrap">
    <h2 class="rv">Que no falte Paraguay <em>en tus fiestas</em></h2>
    <p class="rv">Escríbenos y te lo dejamos listo para recoger. ¡Vy'apavẽ Navidad y feliz Año Nuevo!</p>
    <div class="nv-ctas rv"><a class="nv-btn nv-btn--24" href="{wa(msg(None, "24"))}" target="_blank" rel="noopener">🎄 Encargar para el 24</a><a class="nv-btn nv-btn--31" href="{wa(msg(None, "31"))}" target="_blank" rel="noopener">🥂 Encargar para el 31</a></div>
  </div>
</section>

</main>
<div id="shell-bottom"></div>
<script src="js/data.js?v={V}"></script>
<script src="js/layout.js?v={V}"></script>
<script src="js/cookies.js?v={V}"></script>
<script src="js/nanduti.js?v={V}"></script>
<script src="js/paginas.js?v={V}"></script>
<script src="js/main.js?v={V}"></script>
<script src="js/v2.js?v={V}"></script>
<script>{JS}</script>
</body>
</html>
"""
(RAIZ / "navidad.html").write_text(html, encoding="utf-8")
print("navidad.html escrito (v=" + V + ")")
