"""Sustituye el ñandutí dibujado por el encaje real (img/marca/nanduti-aro.webp)
en el plato del inicio, la intro y el escaparate de la carta."""
import os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def editar(f, cambios):
    p = os.path.join(R, f); s = open(p, encoding="utf-8").read()
    for a, b in cambios:
        assert a in s, (f, a[:70]); s = s.replace(a, b)
    open(p, "w", encoding="utf-8").write(s)

ARO = '<img class="{c}" src="img/marca/nanduti-aro.webp" alt="" aria-hidden="true">'
editar("index.html", [
    ('<div data-nanduti data-dibujar data-sw="0.9"></div>\n    <img src="img/marca/logo-tabla.webp" alt="">',
     ARO.format(c="loader__encaje") + '\n    <img class="loader__logo" src="img/marca/logo-tabla.webp" alt="">'),
    ('<div class="plato__encaje" data-nanduti data-sw="0.55"></div>\n      <div class="plato__encaje plato__encaje--2" data-nanduti data-sw="0.6" data-petalos="12"></div>',
     ARO.format(c="plato__encaje")),
])
editar("carta.html", [('<div class="enc" data-nanduti data-sw="0.5"></div>', ARO.format(c="enc"))])

editar("css/styles.css", [
    (".loader__inner { position: relative; width: min(60vw, 280px); aspect-ratio: 1; display: grid; place-items: center; }",
     ".loader__inner { position: relative; width: min(78vw, 360px); aspect-ratio: 1; display: grid; place-items: center; animation: encajeEntra 1.3s var(--ease) both; }"),
    (".loader__inner svg { position: absolute; inset: 0; width: 100%; height: 100%; color: var(--crema); animation: girar 14s linear infinite; }",
     ".loader__encaje { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: contain; animation: girar 30s linear infinite; filter: drop-shadow(0 18px 40px rgba(0,0,0,.35)); }"),
    (".loader__inner svg .trazo { stroke-dasharray: 1; stroke-dashoffset: 1; animation: dibujar 1.6s var(--ease) forwards; }",
     "@keyframes encajeEntra { from { opacity: 0; transform: scale(.55) rotate(-90deg); } }"),
    (".loader__inner img { width: 68%; position: relative; animation: aparecer .9s .3s var(--ease) both; }",
     ".loader__logo { width: 58%; position: relative; animation: aparecer .9s .45s var(--ease) both; filter: drop-shadow(0 8px 22px rgba(0,0,0,.5)); }"),
    (".plato__encaje { position: absolute; inset: -4%; color: var(--crema); opacity: .9; animation: girar 90s linear infinite; }",
     ".plato__encaje { position: absolute; left: -15%; top: -15%; width: 130%; height: 130%; max-width: none; object-fit: contain; animation: girar 140s linear infinite; filter: drop-shadow(0 30px 50px rgba(0,0,0,.35)); pointer-events: none; }"),
    (".plato__encaje--2 { inset: 9%; opacity: .35; animation-direction: reverse; animation-duration: 60s; color: var(--maiz); }", ""),
    (".plato__fotos { position: absolute; inset: 19%; border-radius: 50%;", ".plato__fotos { position: absolute; inset: 21%; border-radius: 50%;"),
])
p = os.path.join(R, "css", "styles.css"); s = open(p, encoding="utf-8").read()
i = s.index(".plato__aro {"); j = s.index("}", i) + 1
s = s[:i] + ".plato__aro { position: absolute; inset: 19%; border-radius: 50%; box-shadow: 0 40px 80px -20px rgba(0,0,0,.7), 0 0 0 6px rgba(243,238,220,.9); }" + s[j:]
open(p, "w", encoding="utf-8").write(s)

editar("css/carta.css", [
    (".escap__disco .enc { position: absolute; inset: -5%; color: var(--crema); opacity: .55; animation: girar 80s linear infinite; }",
     ".escap__disco .enc { position: absolute; left: -15%; top: -15%; width: 130%; height: 130%; max-width: none; object-fit: contain; animation: girar 140s linear infinite; filter: drop-shadow(0 30px 50px rgba(0,0,0,.35)); pointer-events: none; }"),
    (".escap__disco .aro { position: absolute; inset: 12%; border-radius: 50%; box-shadow: 0 50px 90px -30px rgba(0,0,0,.8), 0 0 0 12px rgba(243,238,220,.1), 0 0 0 13px rgba(243,238,220,.3); }",
     ".escap__disco .aro { position: absolute; inset: 19%; border-radius: 50%; box-shadow: 0 50px 90px -30px rgba(0,0,0,.8), 0 0 0 6px rgba(243,238,220,.9); }"),
    (".escap__disco .fotos { position: absolute; inset: 14%; border-radius: 50%; overflow: hidden; }",
     ".escap__disco .fotos { position: absolute; inset: 21%; border-radius: 50%; overflow: hidden; }"),
])
print("ok")
