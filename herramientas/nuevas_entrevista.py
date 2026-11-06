"""Traducciones de los cambios acordados en la entrevista."""
import json, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = "<span>Chipa guazú</span><span>{sp}</span><span>Mbejú</span><span>Vorí vorí</span><span>{em}</span><span>Mandi'ó chyryry</span><span>{as}</span><span>Milanesa a caballo</span><span>{pa}</span><span>Tres leches</span>"
def marq(sp, em, as_, pa):
    m = M.format(sp=sp, em=em, **{"as": as_}, pa=pa)
    return m + " " + m
N = {
 marq("Sopa paraguaya", "Empanadas caseras", "Asado a la olla", "Parrillada al brasero"): (
    marq("Sopa paraguaiana", "Empanades casolanes", "Rostit a l'olla", "Graellada al braser"),
    marq("Sopa paraguaya", "Homemade empanadas", "Pot roast", "Brazier grill")),
 "Asado a la olla <small>a fuego lento</small>": ("Rostit a l'olla <small>a foc lent</small>", "Pot roast <small>slow-cooked</small>"),
 "Costilla de ternera hecha despacio en la olla, tierna y dorada.": ("Costella de vedella feta a poc a poc a l'olla, tendra i daurada.", "Beef ribs slow-cooked in the pot, tender and golden."),
 "Los fines de semana, gran parte de nuestras mesas se llenan de familias paraguayas que vienen desde toda Barcelona —y desde otras ciudades— a buscar su vorí vorí, su asado a la olla o el soyo con tortillita que les recuerda a casa.": (
    "Els caps de setmana, bona part de les nostres taules s'omplen de famílies paraguaianes que vénen de tot Barcelona —i d'altres ciutats— a buscar el seu vorí vorí, el seu rostit a l'olla o el soyo amb truiteta que els recorda casa seva.",
    "At weekends, many of our tables fill up with Paraguayan families who come from all over Barcelona —and from other cities— for their vorí vorí, their pot roast or the soyo with tortillita that reminds them of home."),
 "Guía de la comida paraguaya: chipa guazú, sopa paraguaya, mbejú, vorí vorí, asado a la olla, soyo y más. Qué es cada plato, cómo se pronuncia y cómo lo cocinamos en Loren Restobar.": (
    "Guia del menjar paraguaià: chipa guazú, sopa paraguaiana, mbejú, vorí vorí, rostit a l'olla, soyo i més. Què és cada plat, com es pronuncia i com el cuinem a Loren Restobar.",
    "A guide to Paraguayan food: chipa guazú, sopa paraguaya, mbejú, vorí vorí, pot roast, soyo and more. What each dish is, how to pronounce it and how we cook it at Loren Restobar."),
 "El vorí vorí, el asado a la olla y el soyo se preparan los fines de semana y en cantidad limitada. Escríbenos por WhatsApp y te decimos si quedan para llevar.": (
    "El vorí vorí, el rostit a l'olla i el soyo es preparen els caps de setmana i en quantitat limitada. Escriu-nos per WhatsApp i et direm si en queden per emportar.",
    "Vorí vorí, pot roast and soyo are made at weekends in limited quantities. Message us on WhatsApp and we'll tell you if there's any left to take away."),
 "🔥 Sólo para la Noche de San Juan": ("🔥 Només per a la Revetlla de Sant Joan", "🔥 Only for Saint John's Eve (Sant Joan)"),
 "Vorí vorí, asado a la olla y soyo. Es cuando más se llena: <strong>reserva</strong> y llega con hambre.": (
    "Vorí vorí, rostit a l'olla i soyo. És quan més s'omple: <strong>reserva</strong> i arriba amb gana.",
    "Vorí vorí, pot roast and soyo. It's our busiest time: <strong>book</strong> and come hungry."),
 "¿Cuándo hay vorí vorí y asado a la olla?": ("Quan hi ha vorí vorí i rostit a l'olla?", "When is there vorí vorí and pot roast?"),
 "Pastafrola": ("Pastafrola", "Pastafrola"),
 "Tarta casera de masa quebrada rellena de dulce, con su clásico enrejado por encima.": (
    "Pastís casolà de pasta trencada farcit de dolç, amb el seu clàssic enreixat al damunt.",
    "Homemade shortcrust tart filled with fruit paste, topped with its classic lattice."),
 "¡Es finde! Hoy hay vorí vorí y asado a la olla": ("És cap de setmana! Avui hi ha vorí vorí i rostit a l'olla", "It's the weekend! Today there's vorí vorí and pot roast"),
 "a-SA-do a la O-lla": ("a-SA-do a la O-lla", "a-SA-do a la O-ya"),
 "El guiso de los domingos en casa": ("El guisat dels diumenges a casa", "The Sunday stew at home"),
 "Carne de ternera hecha despacio en la olla, hasta que queda tierna por dentro y dorada por fuera. Un clásico de la cocina casera y ahora uno de nuestros especiales del fin de semana.": (
    "Carn de vedella feta a poc a poc a l'olla, fins que queda tendra per dins i daurada per fora. Un clàssic de la cuina casolana i ara un dels nostres especials del cap de setmana.",
    "Beef cooked slowly in the pot until it's tender inside and golden outside. A home-cooking classic and now one of our weekend specials."),
 "Costilla de ternera cocinada a fuego lento durante horas en la olla, con mandioca.": (
    "Costella de vedella cuinada a foc lent durant hores a l'olla, amb mandioca.",
    "Beef ribs slow-cooked for hours in the pot, with cassava."),
 "Con mandioca y un trozo de chipa guazú o sopa paraguaya al lado.": (
    "Amb mandioca i un tros de chipa guazú o sopa paraguaiana al costat.",
    "With cassava and a piece of chipa guazú or sopa paraguaya on the side."),
 "Mandioca · Chipa guazú · Sopa paraguaya": ("Mandioca · Chipa guazú · Sopa paraguaiana", "Cassava · Chipa guazú · Sopa paraguaya"),
}
for i, lang in enumerate(("ca", "en")):
    ruta = os.path.join(R, "i18n", lang + ".json")
    d = json.load(open(ruta, encoding="utf-8"))
    for k, v in N.items():
        d[k] = v[i]
    json.dump(d, open(ruta, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", len(N))
