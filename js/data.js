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
  email: "lorenza_vera@hotmail.com",
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
    { dia: "Domingo",   abre: 10, cierra: 17 },
    { dia: "Lunes",     abre: 9,  cierra: 17 },
    { dia: "Martes",    abre: 9,  cierra: 17 },
    { dia: "Miércoles", abre: 9,  cierra: 23 },
    { dia: "Jueves",    abre: 9,  cierra: 23 },
    { dia: "Viernes",   abre: 9,  cierra: 24 },
    { dia: "Sábado",    abre: 10, cierra: 24.5 }
  ]
};

/* Categorías de la carta (orden de aparición) */
window.CATEGORIAS = [
  { id: "paraguayo",  nombre: "Tembi'u paraguayo", sub: "Los clásicos de la abuela", gn: "tembi'u = comida" },
  { id: "empanadas",  nombre: "Empanadas",          sub: "Masa casera, rellenas a mano" },
  { id: "finde",      nombre: "Especiales del finde", sub: "Sólo sábados y domingos", gn: "sábado ha domingo" },
  { id: "compartir",  nombre: "Para compartir",     sub: "Picadas, tapas y raciones" },
  { id: "milanesas",  nombre: "Milanesas",          sub: "Nuestra especialidad, rebozadas al momento" },
  { id: "platos",     nombre: "Platos y pastas",    sub: "Ñoquis y tallarines caseros" },
  { id: "sandwiches", nombre: "Sándwiches y burger",sub: "Con patatas fritas" },
  { id: "postres",    nombre: "Postres",            sub: "El final dulce" },
  { id: "bebidas",    nombre: "Bebidas",            sub: "Frías, como el tereré" }
];

/*
  tags: py = típico paraguayo · top = favorito de la casa · comp = para compartir
        sintrigo = elaborado sin harina de trigo · finde = sólo fin de semana
  precio: null => "Consultar"
*/
window.CARTA = [
  /* --- TEMBI'U PARAGUAYO --- */
  { cat: "paraguayo", nombre: "Chipa guazú", precio: 4.40, img: "img/platos/hl-chipa-guazu.webp",
    desc: "Pastel horneado de maíz tierno, cebolla, huevo, cuajada y queso fresco. Esponjoso por dentro y dorado por fuera.",
    gn: "«Chipa grande» en guaraní", tags: ["py", "top", "sintrigo"] },
  { cat: "paraguayo", nombre: "Sopa paraguaya", precio: 4.40, img: "img/platos/sopa-paraguaya-pro.webp",
    desc: "La única sopa del mundo que se come con tenedor: harina de maíz, huevo, cuajada, queso tierno, cebolla y un toque de anís.",
    gn: "Patrimonio de la mesa paraguaya", tags: ["py", "top", "sintrigo"] },
  { cat: "paraguayo", nombre: "Mbejú tradicional", precio: 4.80, img: "img/platos/mbeju.webp",
    desc: "Torta crujiente de almidón de mandioca, harina de maíz, queso, leche y mantequilla, hecha a la plancha.",
    gn: "Se pronuncia «mbeyú»", tags: ["py", "sintrigo"] },
  { cat: "paraguayo", nombre: "Mbejú relleno de queso", precio: 5.90, img: "img/platos/hl-mbeju.webp",
    desc: "Nuestro mbejú con corazón de mozzarella fundida. El que estira.",
    tags: ["py", "top", "sintrigo"] },
  { cat: "paraguayo", nombre: "Mandi'ó chyryry", precio: 12.30, img: "img/platos/hl-chyryry.webp",
    desc: "Mandioca salteada con patata, queso, jamón, cebolla de verdeo y huevo frito por encima.",
    gn: "«Mandioca que chisporrotea en la sartén»", tags: ["py", "comp"] },
  { cat: "paraguayo", nombre: "Mandi'ó chyryry con bacon", precio: 13.50, img: null,
    desc: "La versión más golosa del salteado de mandioca, con bacon crujiente.", tags: ["py", "comp"] },
  { cat: "paraguayo", nombre: "Yuca brava con salsa casera", precio: 9.99, img: "img/platos/yuca-brava-pro.webp",
    desc: "Nuestra respuesta paraguaya a las bravas: mandioca frita crujiente con salsa de la casa.",
    tags: ["py", "comp", "top"] },
  { cat: "paraguayo", nombre: "Ración de mandioca", precio: 1.90, img: "img/platos/mandioca.webp",
    desc: "Mandioca (yuca) hervida, el pan de cada día en Paraguay. Para acompañar todo.", tags: ["py", "sintrigo"] },

  { cat: "paraguayo", nombre: "Jopara", precio: null, img: "img/platos/hl-jopara.webp",
    desc: "Guiso tradicional de maíz y poroto con carne y verduras, de los que se cocinan a fuego lento.",
    gn: "«Mezcla» en guaraní", tags: ["py"] },
  { cat: "paraguayo", nombre: "Asado a la olla", precio: null, img: "img/platos/hl-asado-olla.webp",
    desc: "Costilla de ternera cocinada lentamente en olla hasta quedar tierna y dorada, con mandioca.",
    tags: ["py"] },

  /* --- EMPANADAS --- */
  { cat: "empanadas", nombre: "Box de 6 empanadas", precio: 22.50, img: "img/platos/hl-empanadas.webp",
    desc: "Carne, pollo, jamón y queso y choclo. Para compartir (o no).", tags: ["comp", "top"] },
  { cat: "empanadas", nombre: "Empanada de carne", precio: 4.30, img: "img/platos/empanada-carne.webp",
    desc: "Ternera, cebolla, pimiento, ajo, huevo duro, comino y pimienta. La más pedida.", tags: ["top"] },
  { cat: "empanadas", nombre: "Empanada de pollo", precio: 3.90, img: "img/platos/empanada-pollo.webp",
    desc: "Pechuga de pollo con cebolla, pimiento verde y rojo, ajo y huevo duro." },
  { cat: "empanadas", nombre: "Empanada de jamón y queso", precio: 3.90, img: "img/platos/empanada-jyq.webp",
    desc: "Jamón dulce y mozzarella fundida." },
  { cat: "empanadas", nombre: "Empanada de choclo", precio: 3.90, img: null,
    desc: "Maíz tierno y mozzarella. Dulce, suave y muy paraguaya.", tags: ["py"] },

  /* --- ESPECIALES DEL FINDE --- */
  { cat: "finde", nombre: "Vorí vorí", precio: null, img: "img/platos/hl-vori-vori.webp",
    desc: "Caldo de gallina casera con bolitas de harina de maíz y queso. El plato con el que Loren representó a Paraguay en el Mundial de Comidas de Ibai.",
    gn: "De «bolita» → vorí", tags: ["py", "top", "finde"] },
  { cat: "finde", nombre: "Pira caldo", precio: null, img: null,
    desc: "Nuestro famoso caldo de pescado, espeso y reconfortante, como en las orillas del río Paraguay.",
    gn: "pira = pez", tags: ["py", "finde"] },
  { cat: "finde", nombre: "Soyo con tortillita", precio: null, img: null,
    desc: "Sopa de carne machacada, acompañada de tortillita paraguaya y mandioca.",
    gn: "De «so'o josopy», carne machacada", tags: ["py", "finde"] },
  { cat: "finde", nombre: "Parrillada paraguaya", precio: null, img: "img/platos/parrillada-paraguaya.webp",
    desc: "Servida en brasero: asado, chorizo, chinchulín, pollo, mandioca y chipa guazú. Para dos o más.",
    tags: ["py", "comp", "top"] },

  /* --- PARA COMPARTIR --- */
  { cat: "compartir", nombre: "Picada completa", precio: 39.90, img: "img/clientes/picada-paraguaya.webp",
    desc: "Milanesa, asado, chorizo, yuca frita y chipa guazú. Una mesa entera de Paraguay.",
    tags: ["py", "comp", "top"] },
  { cat: "compartir", nombre: "Parrillada mixta", precio: null, img: "img/platos/parrillada-mixta.webp",
    desc: "Carnes a la brasa con verduras y limón, servidas en plancha de hierro.", tags: ["comp"] },
  { cat: "compartir", nombre: "Picada de milanesa con miel y mostaza", precio: 13.50, img: "img/platos/picada-milanesa.webp",
    desc: "Milanesitas crujientes con salsa de miel y mostaza.", tags: ["comp"] },
  { cat: "compartir", nombre: "Picada de chorizo con chimichurri", precio: 12.50, img: "img/platos/hl-chorizo.webp",
    desc: "Chorizo criollo a la brasa con nuestro chimichurri.", tags: ["comp"] },
  { cat: "compartir", nombre: "Tequeños con miel y mostaza", precio: 8.90, img: "img/platos/hl-tequenos.webp",
    desc: "5 unidades.", tags: ["comp"] },
  { cat: "compartir", nombre: "Alitas de pollo", precio: 8.90, img: "img/platos/hl-alitas.webp",
    desc: "7 unidades, bien doradas.", tags: ["comp"] },
  { cat: "compartir", nombre: "Tiras de pollo con chili dulce", precio: 8.90, img: null,
    desc: "Pollo rebozado con salsa de chili dulce. Picante suave.", tags: ["comp"] },
  { cat: "compartir", nombre: "Calamares a la romana", precio: 11.20, img: null,
    desc: "Anillas de calamar rebozadas y fritas.", tags: ["comp"] },
  { cat: "compartir", nombre: "Tapas españolas", precio: null, img: "img/platos/hl-tapas-espanolas.webp",
    desc: "Jamón ibérico con pan con tomate y un vermut: el lado español de la casa.", tags: ["comp"] },
  { cat: "compartir", nombre: "Huevo estrellado con jamón", precio: 10.90, img: "img/platos/huevo-estrellado.webp",
    desc: "Patatas, huevos rotos y jamón." },
  { cat: "compartir", nombre: "Patatas bravas", precio: 6.70, img: "img/platos/hl-bravas.webp",
    desc: "Con salsa brava casera.", tags: ["comp"] },
  { cat: "compartir", nombre: "Croquetas de jamón", precio: 5.90, img: "img/platos/hl-croquetas.webp",
    desc: "3 unidades, cremosas por dentro y crujientes por fuera." },
  { cat: "compartir", nombre: "Ensalada de la casa", precio: 12.30, img: "img/platos/ensalada.webp",
    desc: "Lechuga, tomate, cebolla, zanahoria, pepino y pimiento verde." },
  { cat: "compartir", nombre: "Ensalada de queso de cabra", precio: 14.60, img: null,
    desc: "Con reducción de Módena." },

  /* --- MILANESAS --- */
  { cat: "milanesas", nombre: "Milanesa a caballo", precio: 18.90, img: "img/platos/mila-caballo-pro.webp",
    desc: "Milanesa de ternera con cebolla frita, dos huevos fritos y guarnición.", tags: ["top"] },
  { cat: "milanesas", nombre: "Milanesa a la napolitana", precio: 19.90, img: "img/platos/hl-milanesa.webp",
    desc: "Tomate frito, jamón, queso y huevo, con patatas fritas.", tags: ["top"] },
  { cat: "milanesas", nombre: "Milanesa a la americana", precio: 19.90, img: "img/platos/mila-americana-pro.webp",
    desc: "Tomate frito, bacon, queso y huevo, con patatas fritas." },
  { cat: "milanesas", nombre: "Milanesa cuatro quesos", precio: 19.90, img: "img/platos/mila-4quesos.webp",
    desc: "Bañada en salsa de cuatro quesos, con patatas fritas." },
  { cat: "milanesas", nombre: "Milanesa fugazzeta", precio: 19.90, img: "img/platos/mila-fugazzeta.webp",
    desc: "Con cebolla y queso fundido, al estilo porteño-paraguayo." },
  { cat: "milanesas", nombre: "Milanesa de pollo a la napolitana", precio: 18.90, img: "img/platos/mila-pollo-napo.webp",
    desc: "Pechuga rebozada, salsa de tomate, gouda, jamón dulce y huevo frito." },
  { cat: "milanesas", nombre: "Milanesa de ternera", precio: 17.90, img: "img/platos/mila-ternera.webp",
    desc: "La clásica, con limón y guarnición." },
  { cat: "milanesas", nombre: "Milanesa de mondongo", precio: 17.90, img: null,
    desc: "Para los de verdad: mondongo rebozado, con guarnición.", tags: ["py"] },
  { cat: "milanesas", nombre: "Milanesa a la caprese", precio: 15.50, img: "img/platos/mila-caprese.webp",
    desc: "Con tomate cherry, mozzarella y albahaca." },
  { cat: "milanesas", nombre: "Bife a caballo", precio: 17.90, img: "img/platos/bife-caballo.webp",
    desc: "Filete de ternera con cebolla pochada, dos huevos fritos y patatas." },

  /* --- PLATOS Y PASTAS --- */
  { cat: "platos", nombre: "Ñoquis de ternera", precio: 17.90, img: "img/platos/hl-noquis.webp",
    desc: "Ñoquis caseros con carne de ternera guisada en su salsa.", tags: ["top"] },
  { cat: "platos", nombre: "Tallarín de ternera", precio: 17.90, img: "img/platos/tallarin.webp",
    desc: "Tallarines con ternera estofada, como los del domingo en casa." },

  /* --- SÁNDWICHES --- */
  { cat: "sandwiches", nombre: "Sándwich de milanesa completo", precio: 14.99, img: "img/platos/hl-sandwich-milanesa.webp",
    desc: "Milanesa, lechuga, tomate, jamón dulce, gouda y huevo frito. Con patatas.", tags: ["top"] },
  { cat: "sandwiches", nombre: "Sándwich de lomito", precio: 14.90, img: "img/platos/sandwich-lomito.webp",
    desc: "Filete de lomo de ternera, lechuga, tomate, gouda, jamón, huevo y alioli. Con patatas." },
  { cat: "sandwiches", nombre: "Sándwich de milanesa tradicional", precio: 13.99, img: "img/platos/sandwich-milanesa-pro.webp",
    desc: "Milanesa con lechuga y tomate." },
  { cat: "sandwiches", nombre: "Sándwich de pollo completo", precio: 14.50, img: null,
    desc: "Pollo, lechuga, tomate, jamón, queso y huevo." },
  { cat: "sandwiches", nombre: "Hamburguesa de ternera completa", precio: 12.90, img: "img/platos/hl-hamburguesa.webp",
    desc: "Ternera, lechuga, tomate, gouda, jamón dulce y huevo frito. Con patatas." },

  { cat: "sandwiches", nombre: "Lomito árabe", precio: null, img: "img/platos/hl-lomito-arabe.webp",
    desc: "El clásico callejero de Paraguay: lomito en pan árabe a la plancha, con salsa y patatas fritas.", tags: ["py"] },

  /* --- POSTRES --- */
  { cat: "postres", nombre: "Tarta tres leches", precio: 5.50, img: "img/platos/hl-postres.webp",
    desc: "Bizcocho empapado en tres leches, suave y fresquito.", tags: ["top"] },
  { cat: "postres", nombre: "Tarta de queso", precio: 4.90, img: null,
    desc: "Cremosa, casera." },
  { cat: "postres", nombre: "Flan casero", precio: null, img: "img/platos/hl-flan.webp",
    desc: "Flan de la casa con caramelo. Irresistible.", tags: ["top"] },
  { cat: "postres", nombre: "Alfajores Loren", precio: null, img: "img/platos/hl-alfajores.webp",
    desc: "Alfajores caseros de dulce de leche con coco.", tags: ["py"] },
  { cat: "postres", nombre: "Tarta de chocolate", precio: null, img: "img/platos/hl-tarta-chocolate.webp",
    desc: "Para los muy golosos." },

  /* --- BEBIDAS --- */
  { cat: "bebidas", nombre: "Guaraná", precio: 2.50, img: "img/platos/guarana.webp",
    desc: "El refresco de Sudamérica. Lata 33 cl.", tags: ["py"] },
  { cat: "bebidas", nombre: "Cerveza Corona", precio: 3.30, img: null, desc: "33 cl." },
  { cat: "bebidas", nombre: "Cerveza Budweiser", precio: 3.00, img: null, desc: "33 cl." },
  { cat: "bebidas", nombre: "Cerveza Miller", precio: 3.00, img: null, desc: "33 cl." },
  { cat: "bebidas", nombre: "Refrescos", precio: 2.50, img: null,
    desc: "Coca-Cola, Coca-Cola Zero, Fanta Naranja, Aquarius Limón, Nestea." }
];

/* Textos para mostrar, ya traducidos (los nombres en español se usan como identificadores) */
window.CATEGORIAS.forEach((c) => { c.n = T(c.nombre); c.s = T(c.sub); c.g = c.gn ? T(c.gn) : ""; });
window.CARTA.forEach((p) => { p.n = T(p.nombre); p.d = T(p.desc); p.g = p.gn ? T(p.gn) : ""; });
