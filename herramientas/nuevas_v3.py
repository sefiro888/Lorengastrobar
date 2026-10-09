"""Traducciones añadidas en la v3 (carta sin bandeja)."""
import json, os
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
N = {
 "La carta completa de Loren Restobar: chipa guazú, sopa paraguaya, mbejú, empanadas, milanesas, parrillada y especiales del fin de semana. Pide por Glovo, Uber Eats o encarga para recoger por WhatsApp.": (
  "La carta completa de Loren Restobar: chipa guazú, sopa paraguaiana, mbejú, empanades, milaneses, graellada i especials del cap de setmana. Demana per Glovo, Uber Eats o encarrega per recollir per WhatsApp.",
  "The full menu at Loren Restobar: chipa guazú, sopa paraguaya, mbejú, empanadas, milanesas, mixed grill and weekend specials. Order on Glovo or Uber Eats, or order for pick-up via WhatsApp."),
 'Todo lo que sale de la cocina de Loren: clásicos paraguayos, milanesas que desbordan el plato y los caldos del fin de semana. Toca cualquier plato para verlo en grande y, cuando lo tengas claro, pídelo por <strong style="color:var(--maiz)">Glovo, Uber Eats o WhatsApp</strong>.': (
  'Tot el que surt de la cuina de la Loren: clàssics paraguaians, milaneses que desborden el plat i els brous del cap de setmana. Toca qualsevol plat per veure\'l en gran i, quan ho tinguis clar, demana\'l per <strong style="color:var(--maiz)">Glovo, Uber Eats o WhatsApp</strong>.',
  'Everything that comes out of Loren\'s kitchen: Paraguayan classics, milanesas that overflow the plate and the weekend broths. Tap any dish to see it full-size and, once you\'ve decided, order it on <strong style="color:var(--maiz)">Glovo, Uber Eats or WhatsApp</strong>.'),
 "Un toque y te abrimos WhatsApp con el combo ya escrito para recogerlo en el local. Para envío a domicilio, pídelo en Glovo o Uber Eats.": (
  "Un toc i t'obrim WhatsApp amb el combo ja escrit per recollir-lo al local. Per a enviament a domicili, demana'l a Glovo o Uber Eats.",
  "One tap and we'll open WhatsApp with the combo already written for pick-up at the restaurant. For home delivery, order it on Glovo or Uber Eats."),
 '<a class="btn btn--sm btn--wa" data-pack-wa="" href="#">Encargar por WhatsApp</a>': (
  '<a class="btn btn--sm btn--wa" data-pack-wa="" href="#">Encarregar per WhatsApp</a>',
  '<a class="btn btn--sm btn--wa" data-pack-wa="" href="#">Order on WhatsApp</a>'),
 '<a class="pp__op pp__op--g" href="#" id="pp-glovo" rel="noopener" target="_blank"><b>Glovo</b><span>A domicilio · busca «Loren Gastrobar»</span></a> <a class="pp__op pp__op--u" href="#" id="pp-uber" rel="noopener" target="_blank"><b>Uber Eats</b><span>A domicilio · acepta Ticket Restaurant®</span></a> <a class="pp__op pp__op--w" href="#" id="pp-wa" rel="noopener" target="_blank"><b>Recoger en el local</b><span>Te lo dejamos listo · por WhatsApp, sin comisiones</span></a>': (
  '<a class="pp__op pp__op--g" href="#" id="pp-glovo" rel="noopener" target="_blank"><b>Glovo</b><span>A domicili · cerca «Loren Gastrobar»</span></a> <a class="pp__op pp__op--u" href="#" id="pp-uber" rel="noopener" target="_blank"><b>Uber Eats</b><span>A domicili · accepta Ticket Restaurant®</span></a> <a class="pp__op pp__op--w" href="#" id="pp-wa" rel="noopener" target="_blank"><b>Recollir al local</b><span>T\'ho deixem a punt · per WhatsApp, sense comissions</span></a>',
  '<a class="pp__op pp__op--g" href="#" id="pp-glovo" rel="noopener" target="_blank"><b>Glovo</b><span>Delivery · search for "Loren Gastrobar"</span></a> <a class="pp__op pp__op--u" href="#" id="pp-uber" rel="noopener" target="_blank"><b>Uber Eats</b><span>Delivery · accepts Ticket Restaurant®</span></a> <a class="pp__op pp__op--w" href="#" id="pp-wa" rel="noopener" target="_blank"><b>Pick up at the restaurant</b><span>We\'ll have it ready · via WhatsApp, no fees</span></a>'),
 "¡Hola Loren! Quiero encargar {x} para recoger en el local. ¿A qué hora puedo pasar?": (
  "Hola, Loren! Vull encarregar {x} per recollir al local. A quina hora puc passar?",
  "Hi Loren! I'd like to order {x} for pick-up at the restaurant. What time can I come by?"),
}
for i, lang in enumerate(("ca", "en")):
    ruta = os.path.join(RAIZ, "i18n", lang + ".json")
    d = json.load(open(ruta, encoding="utf-8"))
    for k, v in N.items():
        d[k] = v[i]
    json.dump(d, open(ruta, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", len(N))
