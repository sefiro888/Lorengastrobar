"""Datos de los combos de Navidad y Fin de Año 2026 (hoja que mandó Loren el 19-nov-2026).
Si Loren cambia algo, se cambia AQUÍ y se regenera todo:
  python herramientas/navidad.py              (imágenes de Instagram, WhatsApp e imprenta)
  python herramientas/promo/navidad_video.py  (reel)
"""
WHATSAPP = "602 07 68 28"
WA_LINK = "https://wa.me/34602076828"
WEB = "lorenrestobar.com/navidad"

COMBOS = [
    {"id": "combo1", "titulo": "Combo 1", "sub": "bocaditos de Fin de Año", "foto": "sandwichitos-lechuga-tomate",
     "items": ["Sándwichitos de peceto al vitel toné", "Sándwichitos de lengua a la vinagreta",
               "Sándwichitos de milanesitas de ternera", "Matambrito relleno", "Sopa paraguaya"],
     "cantidad": "50 unidades", "precio": "70,00 €"},
    {"id": "combo2", "titulo": "Combo 2", "sub": "bocaditos de Fin de Año", "foto": "bandeja-variada-combo2",
     "items": ["Empanaditas de ternera", "Croquetitas de ternera", "Chipa guazú", "Milanesitas",
               "Sándwichitos de pollo desmechado"],
     "cantidad": "50 unidades", "precio": "65,00 €"},
    {"id": "embutidos", "titulo": "Embutidos", "sub": "tabla surtida", "foto": "tabla-embutidos",
     "items": ["Salchichón ibérico", "Fuet", "Jamón ibérico", "Lomo ibérico", "Chorizo ibérico", "Longaniza", "Frutos secos"],
     "cantidad": "Para 8 a 10 personas", "precio": "44,90 €"},
    {"id": "quesos", "titulo": "Quesos", "sub": "tabla surtida", "foto": None,
     "items": ["Queso manchego", "Queso brie", "Queso de cabra", "Queso gouda curado", "Frutos secos, uvas, fresas y picos de pan"],
     "cantidad": "Para 8 a 10 personas", "precio": "42,90 €"},
]

def mensaje_wa(combo=None):
    if combo:
        return f"¡Hola Loren! Quiero encargar el {combo['titulo']} ({combo['sub']}) de Navidad.\n• Día: 24 / 31 de diciembre\n• Cantidad: \n• Nombre: "
    return "¡Hola Loren! Quiero encargar bocaditos de Navidad.\n• Combo: \n• Día: 24 / 31 de diciembre\n• Nombre: "
