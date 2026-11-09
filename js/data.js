/* =========================================================
   LOREN RESTOBAR · Datos compartidos (web + carta imprimible)
   Edita aquí precios, platos, horarios y enlaces.
   ========================================================= */

/* ---------- Idioma ---------- */
window.IDIOMA = window.IDIOMA || "es";
window.PREF = window.PREF || "";
window.LOCALE = { es: "es-ES", ca: "ca-ES", en: "en-GB" }[window.IDIOMA];
/* T("texto en español", {variables}) → traducción (o el mismo texto si no hay) */
window.T = function (s, v) {
  if (s == null) return s;
  const d = window.I18N && window.I18N[window.IDIOMA];
  let r = (d && d[s]) || s;
  if (v) Object.keys(v).forEach((k) => (r = r.split("{" + k + "}").join(v[k])));
  return r;
};
window.EURO = (n) => window.IDIOMA === "en" ? "€" + n.toFixed(2) : n.toFixed(2).replace(".", ",") + " €";

window.LOREN = {
  nombre: "Loren Restobar",
  lema: "Somos lo que te hacemos sentir",
  telefono: "602 07 68 28",
  telefonoIntl: "34602076828",
  telefonoFijo: "935 05 24 91",
  email: "grupolorenrestobarsl@gmail.com",
  razonSocial: "Grupo Loren Restobar S.L.",
  cif: "B-93814853",
  direccion: "Carrer de la Muntanya, 115",
  cp: "08026 Barcelona",
  barrio: "El Camp de l'Arpa · Sant Martí",
  coords: { lat: 41.41277, lng: 2.18289 },
  links: {
    glovo: "https://glovoapp.com/es/es/barcelona/stores/gastrobar-loren-barcelona",
    uber: "https://www.ubereats.com/es/store/loren-gastrobar/y6M32ynvUwe-7RRwnYxhhw",
    opentable: "https://www.opentable.es/r/loren-restobar-barcelona",
    maps: "https://maps.app.goo.gl/TBXBmcyFdx3NDJSJ7",
    instagram: "https://www.instagram.com/lorenrestobar_/",
    tiktok: "https://www.tiktok.com/@lorenrestobar",
    facebook: "https://www.facebook.com/lorenrestobar",
    whatsapp: "https://wa.me/34602076828"
  },
  /* 0 = domingo … 6 = sábado. Horas en formato decimal (24.5 = 00:30) */
  horario: [
    { dia: "Domingo",   abre: 9, cierra: 17 },
    { dia: "Lunes",     abre: 9, cierra: 17 },
    { dia: "Martes",    abre: 9, cierra: 23 },
    { dia: "Miércoles", abre: 9, cierra: 23 },
    { dia: "Jueves",    abre: 9, cierra: 23 },
    { dia: "Viernes",   abre: 9, cierra: 24 },
    { dia: "Sábado",    abre: 9, cierra: 24 }
  ]
};

/* Categorías de la carta (orden de aparición, como en la carta impresa del local) */
window.CATEGORIAS = [
  { id: "paraguayo",  nombre: "Para picar",          sub: "Los clásicos paraguayos", gn: "tembi'u = comida" },
  { id: "empanadas",  nombre: "Empanadas",           sub: "Masa casera, rellenas a mano" },
  { id: "finde",      nombre: "Especiales del finde", sub: "Sólo viernes, sábados y domingos" },
  { id: "sandwiches", nombre: "Sabores paraguayos entre panes", sub: "Sándwiches de milanesa, lomito y hamburguesa" },
  { id: "milanesas",  nombre: "Milanesas",           sub: "Nuestra especialidad, con guarnición" },
  { id: "parrilla",   nombre: "Parrilladas",         sub: "Picadas para compartir y carnes" },
  { id: "platos",     nombre: "Pastas",              sub: "Ñoquis y tallarines caseros" },
  { id: "compartir",  nombre: "Las tapas de siempre", sub: "El lado español de la casa" },
  { id: "ensaladas",  nombre: "Ensaladas",           sub: "Frescas, para acompañar" },
  { id: "postres",    nombre: "Postres",             sub: "El final dulce" },
  { id: "bebidas",    nombre: "Bebidas",             sub: "Cervezas, vinos, cócteles y refrescos" }
];

/*
  tags: py = típico paraguayo · top = favorito de la casa · comp = para compartir
        sintrigo = elaborado sin harina de trigo · finde = sólo fin de semana
  precio: null => "Consultar" · grupo: sólo en bebidas (para la carta impresa)
*/
window.CARTA = [
  /* --- PARA PICAR --- */
  { cat: "paraguayo", nombre: "Chipa guazú", precio: 3.90, img: "img/platos/hl-chipa-guazu.webp",
    desc: "Pastel horneado de maíz tierno, cebolla, huevo, cuajada y queso fresco. Esponjoso por dentro y dorado por fuera.",
    gn: "«Chipa grande» en guaraní", tags: ["py", "top", "sintrigo"] },
  { cat: "paraguayo", nombre: "Sopa paraguaya", precio: 3.90, img: "img/platos/sopa-paraguaya-pro.webp",
    desc: "La única sopa del mundo que se come con tenedor: harina de maíz, huevo, cuajada, queso tierno, cebolla y un toque de anís.",
    gn: "Patrimonio de la mesa paraguaya", tags: ["py", "top", "sintrigo"] },
  { cat: "paraguayo", nombre: "Yucas bravas", precio: 8.90, img: "img/platos/yuca-brava-pro.webp",
    desc: "Nuestra respuesta paraguaya a las bravas: mandioca frita crujiente con salsa de la casa.",
    tags: ["py", "comp", "top"] },
  { cat: "paraguayo", nombre: "Mbejú tradicional", precio: 4.50, img: "img/platos/mbeju.webp",
    desc: "Torta crujiente de almidón de mandioca, harina de maíz, queso, leche y mantequilla, hecha a la plancha.",
    gn: "Se pronuncia «mbeyú»", tags: ["py", "sintrigo"] },
  { cat: "paraguayo", nombre: "Mbejú relleno de queso", precio: 5.50, img: "img/platos/hl-mbeju.webp", disco: "img/platos/plato-mbeju.webp",
    desc: "Nuestro mbejú con corazón de mozzarella fundida. El que estira.",
    tags: ["py", "top", "sintrigo"] },
  { cat: "paraguayo", nombre: "Mandi'ó chyryry", precio: 11.50, img: "img/platos/hl-chyryry.webp",
    desc: "Yuca salteada con patata, queso, jamón, cebolla de verdeo y huevo frito por encima.",
    gn: "«Mandioca que chisporrotea en la sartén»", tags: ["py", "comp"] },
  { cat: "paraguayo", nombre: "Picada de milanesa con miel y mostaza", precio: 11.90, img: "img/platos/picada-milanesa.webp",
    desc: "Milanesitas crujientes con salsa de miel y mostaza.", tags: ["comp"] },
  { cat: "paraguayo", nombre: "Picada de chorizo con chimichurri", precio: 11.90, img: "img/platos/hl-chorizo.webp",
    desc: "Chorizo criollo con nuestro chimichurri.", tags: ["comp"] },

  /* --- EMPANADAS --- */
  { cat: "empanadas", nombre: "Empanada de ternera", precio: 3.80, img: "img/platos/empanada-carne.webp",
    desc: "Ternera, cebolla, pimiento, ajo, huevo duro, comino y pimienta. La más pedida.", tags: ["top"] },
  { cat: "empanadas", nombre: "Empanada de pollo", precio: 3.60, img: "img/platos/empanada-pollo.webp",
    desc: "Pechuga de pollo con cebolla, pimiento verde y rojo, ajo y huevo duro." },
  { cat: "empanadas", nombre: "Empanada de jamón y queso", precio: 3.40, img: "img/platos/empanada-jyq.webp",
    desc: "Jamón dulce y mozzarella fundida." },
  { cat: "empanadas", nombre: "Empanada de choclo", precio: 3.40, img: "img/platos/hl-empanadas.webp",
    desc: "Maíz tierno y mozzarella. Dulce, suave y muy paraguaya.", tags: ["py"] },
  { cat: "empanadas", nombre: "Suplemento de mandioca", precio: 1.90, img: "img/platos/mandioca.webp",
    desc: "Mandioca (yuca) hervida, el pan de cada día en Paraguay. Para acompañar.", tags: ["py", "sintrigo"] },

  /* --- ESPECIALES DEL FINDE (viernes, sábados y domingos) --- */
  { cat: "finde", nombre: "Vorí vorí", precio: 15.90, img: "img/platos/hl-vori-vori.webp", disco: "img/platos/plato-vori.webp",
    desc: "Caldo casero con bolitas de harina de maíz y queso. El plato con el que Loren representó a Paraguay en el Mundial de Comidas de Ibai.",
    gn: "De «bolita» → vorí", tags: ["py", "top", "finde"] },
  { cat: "finde", nombre: "Asado a la olla", precio: 17.90, img: "img/platos/hl-asado-olla.webp",
    desc: "Ternera cocinada lentamente en olla hasta quedar tierna y dorada.",
    tags: ["py", "finde"] },

  /* --- SABORES PARAGUAYOS ENTRE PANES --- */
  { cat: "sandwiches", nombre: "Sándwich de milanesa de ternera completo", precio: 13.90, img: "img/platos/hl-sandwich-milanesa.webp",
    desc: "Lechuga, tomate, jamón, queso y huevo.", tags: ["top"] },
  { cat: "sandwiches", nombre: "Sándwich de milanesa de pollo completo", precio: 12.90, img: null,
    desc: "Lechuga, tomate, jamón, queso y huevo." },
  { cat: "sandwiches", nombre: "Sándwich de milanesa clásico", precio: 12.90, img: "img/platos/sandwich-milanesa-pro.webp",
    desc: "Lechuga y tomate." },
  { cat: "sandwiches", nombre: "Sándwich de milanesa con salsa especial", precio: 12.90, img: null,
    desc: "Lechuga, tomate, pepinillo y cebolla caramelizada." },
  { cat: "sandwiches", nombre: "Sándwich de milanesa picante", precio: 13.90, img: null,
    desc: "Lechuga, tomate, queso cheddar, cebolla morada y jalapeño." },
  { cat: "sandwiches", nombre: "Sándwich de milanesa criolla", precio: 13.90, img: null,
    desc: "Lechuga, tomate, cebolla morada, cilantro, jamón, queso y huevo." },
  { cat: "sandwiches", nombre: "Sándwich de milanesa suprema", precio: 14.90, img: null,
    desc: "Lechuga, tomate, bacon crujiente, cebolla caramelizada, queso cheddar y huevo." },
  { cat: "sandwiches", nombre: "Sándwich de lomito", precio: 13.90, img: "img/platos/sandwich-lomito.webp",
    desc: "Lomo de ternera con cebolla caramelizada y salsa de ajo, con patatas fritas." },
  { cat: "sandwiches", nombre: "Hamburguesa de ternera completa", precio: 12.90, img: "img/platos/hl-hamburguesa.webp",
    desc: "Ternera, lechuga, tomate, queso, jamón y huevo frito. Incluye patatas fritas." },

  /* --- MILANESAS (con guarnición) --- */
  { cat: "milanesas", nombre: "Milanesa a la napolitana", precio: 17.90, img: "img/platos/hl-milanesa.webp",
    desc: "De ternera o de pollo, con salsa de tomate casera, jamón, mozzarella fundida y huevo.", tags: ["top"] },
  { cat: "milanesas", nombre: "Milanesa a la americana", precio: 17.90, img: "img/platos/mila-americana-pro.webp",
    desc: "Cebolla caramelizada, salsa barbacoa, mozzarella fundida, bacon y huevo." },
  { cat: "milanesas", nombre: "Milanesa ibérica Loren", precio: 18.90, img: null,
    desc: "La de la casa: salsa de tomate casera, mozzarella fundida y jamón ibérico.", tags: ["top"] },
  { cat: "milanesas", nombre: "Milanesa fugazzeta", precio: 17.90, img: "img/platos/mila-fugazzeta.webp",
    desc: "Con cebolla y queso fundido, al estilo porteño-paraguayo." },
  { cat: "milanesas", nombre: "Milanesa a caballo", precio: 16.90, img: "img/platos/mila-caballo-pro.webp", disco: "img/platos/plato-mila-caballo.webp",
    desc: "Milanesa de ternera con cebolla frita y dos huevos fritos.", tags: ["top"] },
  { cat: "milanesas", nombre: "Milanesa clásica", precio: 15.90, img: "img/platos/mila-ternera.webp",
    desc: "La de siempre, con limón. Suplemento de bacon, queso o huevo: +1 €." },
  { cat: "milanesas", nombre: "Milanesa de pollo", precio: 15.90, img: null,
    desc: "Pechuga rebozada al momento. Suplemento de bacon, queso o huevo: +1 €." },
  { cat: "milanesas", nombre: "Milanesa de mondongo", precio: 15.90, img: null,
    desc: "Para los de verdad: mondongo rebozado.", tags: ["py"] },
  { cat: "milanesas", nombre: "Bife a caballo", precio: 15.90, img: "img/platos/bife-caballo.webp",
    desc: "Filete de ternera con cebolla y huevo." },

  /* --- PARRILLADAS --- */
  { cat: "parrilla", nombre: "Picada completa", precio: 39.90, img: "img/clientes/picada-paraguaya.webp",
    desc: "Milanesa, asado, chorizo, yuca frita y sopa paraguaya o chipa guazú. Una mesa entera de Paraguay.",
    tags: ["py", "comp", "top"] },
  { cat: "parrilla", nombre: "Picada paraguaya", precio: 32.90, img: "img/platos/parrillada-paraguaya.webp",
    desc: "Chorizo criollo, butifarra, milanesa, sopa paraguaya, mbejú y yuca.", tags: ["py", "comp"] },
  { cat: "parrilla", nombre: "Entrecot de ternera con chorizo", precio: 17.90, img: null,
    desc: "Entrecot a la brasa acompañado de chorizo criollo." },
  { cat: "parrilla", nombre: "Entraña con chimichurri", precio: 17.90, img: null,
    desc: "Entraña de ternera con nuestra salsa chimichurri." },
  { cat: "parrilla", nombre: "Parrillada de verdura", precio: 11.90, img: "img/platos/parrillada-mixta.webp",
    desc: "Verduras de temporada a la brasa." },

  /* --- PASTAS --- */
  { cat: "platos", nombre: "Ñoquis de ternera", precio: 15.90, img: "img/platos/hl-noquis.webp",
    desc: "Ñoquis caseros con carne de ternera guisada en su salsa.", tags: ["top"] },
  { cat: "platos", nombre: "Tallarín de ternera", precio: 15.90, img: "img/platos/tallarin.webp",
    desc: "Tallarines con carne de ternera, como los del domingo en casa." },

  /* --- LAS TAPAS DE SIEMPRE --- */
  { cat: "compartir", nombre: "Platillo de jamón ibérico", precio: 14.50, img: "img/platos/hl-tapas-espanolas.webp",
    desc: "Jamón ibérico cortado para compartir.", tags: ["comp"] },
  { cat: "compartir", nombre: "Croquetas de jamón", precio: 4.90, img: "img/platos/hl-croquetas.webp",
    desc: "3 unidades, cremosas por dentro y crujientes por fuera." },
  { cat: "compartir", nombre: "Tequeños", precio: 7.90, img: "img/platos/hl-tequenos.webp",
    desc: "Palitos de queso envueltos en masa crujiente.", tags: ["comp"] },
  { cat: "compartir", nombre: "Alitas de pollo", precio: 7.90, img: "img/platos/hl-alitas.webp",
    desc: "Bien doradas.", tags: ["comp"] },
  { cat: "compartir", nombre: "Tiras de pollo rebozado", precio: 7.90, img: null,
    desc: "Pollo rebozado y crujiente.", tags: ["comp"] },
  { cat: "compartir", nombre: "Olivas rellenas", precio: 2.50, img: null,
    desc: "Para abrir el apetito." },
  { cat: "compartir", nombre: "Patatas bravas", precio: 5.90, img: "img/platos/hl-bravas.webp",
    desc: "Con salsa brava casera.", tags: ["comp"] },
  { cat: "compartir", nombre: "Huevo roto con jamón ibérico", precio: 8.90, img: "img/platos/huevo-estrellado.webp",
    desc: "Patatas, huevos rotos y jamón ibérico." },

  /* --- ENSALADAS --- */
  { cat: "ensaladas", nombre: "Ensalada mixta", precio: 10.90, img: "img/platos/ensalada.webp",
    desc: "Lechuga, tomate, cebolla, zanahoria y pepino." },
  { cat: "ensaladas", nombre: "Ensalada césar al estilo de la casa", precio: 11.90, img: null,
    desc: "Nuestra versión de la clásica césar." },

  /* --- POSTRES (no salen en la carta impresa: precio a consultar) --- */
  { cat: "postres", nombre: "Tarta tres leches", precio: null, img: "img/platos/tres-leches.webp",
    desc: "Bizcocho empapado en tres leches, suave y fresquito.", tags: ["top"] },
  { cat: "postres", nombre: "Flan casero", precio: null, img: "img/platos/hl-flan.webp",
    desc: "Flan de la casa con caramelo. Irresistible.", tags: ["top"] },
  { cat: "postres", nombre: "Alfajores Loren", precio: null, img: "img/platos/hl-alfajores.webp",
    desc: "Alfajores caseros de dulce de leche con coco.", tags: ["py"] },

  /* --- BEBIDAS --- */
  ...[
    ["Cervezas", "Estrella Damm caña", 2.30], ["Cervezas", "Estrella Damm zurito", 1.70], ["Cervezas", "Estrella Damm jarra", 3.40, "500 ml"],
    ["Cervezas", "Estrella Damm mediana", 2.50], ["Cervezas", "Estrella Damm quinto", 1.90],
    ["Cervezas", "Turia caña", 2.80], ["Cervezas", "Turia zurito", 2.40], ["Cervezas", "Turia jarra", 4.10, "500 ml"],
    ["Cervezas", "Damm Lemon caña", 2.50], ["Cervezas", "Damm Lemon jarra", 3.60, "500 ml"],
    ["Cervezas", "Estrella Galicia mediana", 2.50], ["Cervezas", "Estrella Galicia 0,0 mediana", 2.50], ["Cervezas", "Estrella Galicia 0,0 tostada", 2.50],
    ["Cervezas", "Daura sin gluten", 3.00], ["Cervezas", "Voll-Damm", 3.00], ["Cervezas", "Bohemia Damm", 3.00],
    ["Cervezas", "Budweiser", 2.30, "Botella 330 ml"], ["Cervezas", "Miller", 2.30, "Botella 330 ml"], ["Cervezas", "Heineken", 2.30, "Botella 330 ml"],
    ["Cervezas", "Corona", 3.00, "Botella 330 ml"], ["Cervezas", "Pilsen tradicional", 3.90, "Botella 330 ml · la cerveza de Paraguay", ["py"]],
    ["Cervezas", "Cubo de 6 Bud, Miller o Heineken", 12.50], ["Cervezas", "Cubo de 6 Corona", 16.50], ["Cervezas", "Cubo de 6 Pilsen", 22.00, "", ["py"]],
    ["Cava y vino", "Copa de cava", 2.50], ["Cava y vino", "Copa de vino", 2.90, "Tinto o blanco"],
    ["Cava y vino", "Botella de vino", 9.90, "Tinto o verdejo"], ["Cava y vino", "Botella de cava", 10.90],
    ["Cócteles y vermut", "Mojito", 7.50], ["Cócteles y vermut", "Mojito de sabor", 7.50], ["Cócteles y vermut", "Mojito de cerveza", 7.50],
    ["Cócteles y vermut", "Margarita", 7.50], ["Cócteles y vermut", "Tequila sunrise", 7.50], ["Cócteles y vermut", "Caipiriña", 7.50],
    ["Cócteles y vermut", "Caipiroska", 7.50], ["Cócteles y vermut", "Cubata", 6.50], ["Cócteles y vermut", "Sex on the beach", 7.50],
    ["Cócteles y vermut", "Verano sunrise", 7.50], ["Cócteles y vermut", "Gin-tonic", 7.50],
    ["Cócteles y vermut", "Vermut", 4.50], ["Cócteles y vermut", "Vermut de la casa", 2.90],
    ["Cócteles y vermut", "Sangría", 4.90], ["Cócteles y vermut", "Tinto de verano", 2.90],
    ["Cócteles y vermut", "Jarra de sangría de vino", 12.50], ["Cócteles y vermut", "Jarra de sangría de cava", 13.50],
    ["Refrescos", "Coca-Cola", 2.50, "Botella 330 ml"], ["Refrescos", "Coca-Cola Zero", 2.50, "Botella 330 ml"],
    ["Refrescos", "Fanta Naranja", 2.50, "Botella 330 ml"], ["Refrescos", "Fanta Limón", 2.50, "Botella 330 ml"],
    ["Refrescos", "Sprite", 2.50, "Botella 330 ml"], ["Refrescos", "Nestea", 2.50, "Botella 330 ml"], ["Refrescos", "Aquarius", 2.50, "Botella 330 ml"],
    ["Refrescos", "Guaraná", 2.30, "El refresco de Sudamérica · lata 330 ml", ["py"], "img/platos/guarana.webp"],
    ["Refrescos", "Vichy Catalán", 2.30, "Botella 330 ml"], ["Refrescos", "Agua Cristal", 2.00, "Botella 500 ml"],
    ["Refrescos", "Zumo", 1.90, "Botella 200 ml"], ["Refrescos", "Bitter Kas", 2.00], ["Refrescos", "Tónica", 2.30]
  ].map(([grupo, nombre, precio, desc = "", tags, img = null]) => ({ cat: "bebidas", grupo, nombre, precio, img, desc, tags }))
];
window.AVISO_TERRAZA = "Consumo en terraza: 0,10 € adicionales por consumición.";

/* Textos para mostrar, ya traducidos (los nombres en español se usan como identificadores) */
window.CATEGORIAS.forEach((c) => { c.n = T(c.nombre); c.s = T(c.sub); c.g = c.gn ? T(c.gn) : ""; });
window.CARTA.forEach((p) => { p.n = T(p.nombre); p.d = T(p.desc); p.g = p.gn ? T(p.gn) : ""; });
