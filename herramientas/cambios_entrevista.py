"""Cambios acordados en la entrevista con Loren:
- Pira caldo sale de los especiales del finde; entra el asado a la olla
- Lomito árabe fuera de la carta
- Pastafrola nueva en postres
- Bandeja Clásica sólo para la Noche de San Juan
"""
import os, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def editar(f, cambios):
    p = os.path.join(R, f); s = open(p, encoding="utf-8").read()
    for a, b in cambios:
        assert a in s, (f, a[:80])
        s = s.replace(a, b)
    open(p, "w", encoding="utf-8").write(s)

# ---------- data.js ----------
p = os.path.join(R, "js", "data.js"); s = open(p, encoding="utf-8").read()
asado = re.search(r'  \{ cat: "paraguayo", nombre: "Asado a la olla".*?\},\n', s, re.S).group(0)
s = s.replace(asado, "")
s = re.sub(r'  \{ cat: "finde", nombre: "Pira caldo".*?\},\n', "", s, flags=re.S)
s = re.sub(r'  \{ cat: "sandwiches", nombre: "Lomito árabe".*?\},\n\n?', "", s, flags=re.S)
nuevo_asado = asado.replace('cat: "paraguayo"', 'cat: "finde"').replace('tags: ["py"]', 'tags: ["py", "finde"]')
vori = re.search(r'  \{ cat: "finde", nombre: "Vorí vorí".*?\},\n', s, re.S).group(0)
s = s.replace(vori, vori + nuevo_asado)
choco = re.search(r'  \{ cat: "postres", nombre: "Tarta de chocolate".*?\},\n', s, re.S).group(0)
s = s.replace(choco, choco + '''  { cat: "postres", nombre: "Pastafrola", precio: null, img: null,
    desc: "Tarta casera de masa quebrada rellena de dulce, con su clásico enrejado por encima.", tags: ["py"] },
''')
open(p, "w", encoding="utf-8").write(s)

# ---------- guía de sabores: el asado a la olla sustituye al pira caldo ----------
p = os.path.join(R, "js", "paginas.js"); s = open(p, encoding="utf-8").read()
pira = re.search(r'    \{ id: "pira-caldo".*?\},\n', s, re.S).group(0)
s = s.replace(pira, '''    { id: "asado-olla", n: "Asado a la olla", oir: "asado a la olla", pron: "a-SA-do a la O-lla", img: "img/platos/hl-asado-olla.webp", carta: "Asado a la olla", finde: true,
      lema: "El guiso de los domingos en casa",
      que: "Carne de ternera hecha despacio en la olla, hasta que queda tierna por dentro y dorada por fuera. Un clásico de la cocina casera y ahora uno de nuestros especiales del fin de semana.",
      como: "Costilla de ternera cocinada a fuego lento durante horas en la olla, con mandioca.",
      come: "Con mandioca y un trozo de chipa guazú o sopa paraguaya al lado.", marida: "Mandioca · Chipa guazú · Sopa paraguaya" },
''')
open(p, "w", encoding="utf-8").write(s)

editar("js/main.js", [('T("¡Es finde! Hoy hay vorí vorí y pira caldo")', 'T("¡Es finde! Hoy hay vorí vorí y asado a la olla")')])

# ---------- páginas ----------
editar("index.html", [
    ('<span>Pira caldo</span>', '<span>Asado a la olla</span>'),
    ('<div class="finde__plato"><div class="foto" data-nanduti data-sw="1"></div><div><h3>Pira caldo <small>pira = pez</small></h3><p>Nuestro caldo de pescado, espeso y reconfortante.</p></div></div>',
     '<div class="finde__plato"><div class="foto"><img src="img/platos/hl-asado-olla.webp" alt="Asado a la olla" loading="lazy"></div><div><h3>Asado a la olla <small>a fuego lento</small></h3><p>Costilla de ternera hecha despacio en la olla, tierna y dorada.</p></div></div>'),
    ('<a href="https://www.instagram.com/lorenrestobar_/reel/Ddethzus-4E/" target="_blank" rel="noopener"><img src="img/redes/ig-pira.webp" alt="" loading="lazy"><span>Pira caldo cada finde</span></a>',
     '<a href="https://www.instagram.com/lorenrestobar_/reel/DdrXHNhMc55/" target="_blank" rel="noopener"><img src="img/redes/ig-anos.webp" alt="" loading="lazy"><span>Hoy cumplimos 6 años</span></a>'),
])
editar("domicilio.html", [("El vorí vorí, el pira caldo y el soyo se preparan", "El vorí vorí, el asado a la olla y el soyo se preparan")])
editar("historia.html", [("su vorí vorí, su pira caldo o el soyo con tortillita", "su vorí vorí, su asado a la olla o el soyo con tortillita")])
editar("sabores.html", [("vorí vorí, pira caldo, soyo y más", "vorí vorí, asado a la olla, soyo y más")])
editar("visitanos.html", [
    ("Vorí vorí, pira caldo y soyo. Es cuando más se llena", "Vorí vorí, asado a la olla y soyo. Es cuando más se llena"),
    ("<summary>¿Cuándo hay vorí vorí y pira caldo?</summary>", "<summary>¿Cuándo hay vorí vorí y asado a la olla?</summary>"),
])
editar("eventos.html", [('<div class="bandeja-card__body"><h3>Bandeja Clásica</h3>',
    '<div class="bandeja-card__body"><span class="sanjuan">🔥 Sólo para la Noche de San Juan</span><h3>Bandeja Clásica</h3>')])
print("ok")
