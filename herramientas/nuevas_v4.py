"""Traducciones añadidas en la v4 (pedido de varios platos por WhatsApp)."""
import json, os
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
N = {
 "Tu pedido": ("El teu encàrrec", "Your order"),
 "Aún no has añadido nada. Toca «Pedir» en los platos que quieras.": ("Encara no has afegit res. Toca «Demanar» als plats que vulguis.", "You haven't added anything yet. Tap \"Order\" on the dishes you want."),
 "Quitar uno": ("Treure'n un", "Remove one"),
 "Añadir uno": ("Afegir-ne un", "Add one"),
 "Total aprox.": ("Total aprox.", "Approx. total"),
 "¿A qué hora puedo pasar?": ("A quina hora puc passar?", "What time can I come by?"),
 "Pedir por WhatsApp": ("Demanar per WhatsApp", "Order on WhatsApp"),
 "Recoger en el local · el mensaje ya va escrito, sin comisiones": ("Recollir al local · el missatge ja va escrit, sense comissions", "Pick-up at the restaurant · message already written, no fees"),
 "Añadir más platos": ("Afegir més plats", "Add more dishes"),
 "¿Prefieres a domicilio? Pide en su página:": ("Prefereixes a domicili? Demana a la seva pàgina:", "Prefer delivery? Order on their page:"),
 "Vaciar pedido": ("Buidar encàrrec", "Clear order"),
 "Cerrar": ("Tancar", "Close"),
}
for i, lang in enumerate(("ca", "en")):
    ruta = os.path.join(RAIZ, "i18n", lang + ".json")
    d = json.load(open(ruta, encoding="utf-8"))
    for k, v in N.items():
        d.setdefault(k, v[i])
    json.dump(d, open(ruta, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", len(N))
