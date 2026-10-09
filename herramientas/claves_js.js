// Extrae los textos traducibles del JavaScript → i18n/claves_js.json
const fs = require("fs"), path = require("path");
const R = path.join(__dirname, "..");
global.window = {}; global.T = (s) => s;
eval(fs.readFileSync(path.join(R, "js/data.js"), "utf8").replace(/window\.T = function[\s\S]*?\n};/, "window.T = (s) => s;"));
const set = new Set();
const add = (s) => { if (s && /[A-Za-zÀ-ÿ]/.test(s)) set.add(s); };
const str = (raw) => JSON.parse('"' + raw + '"');
window.CATEGORIAS.forEach((c) => [c.nombre, c.sub, c.gn].forEach(add));
window.CARTA.forEach((p) => [p.nombre, p.desc, p.gn].forEach(add));
window.LOREN.horario.forEach((h) => add(h.dia));
add(window.LOREN.lema);
const RE_T = /T\("((?:[^"\\]|\\.)*)"/g;
const RE_COND = /T\([^)]*?\?\s*"((?:[^"\\]|\\.)*)"\s*:\s*"((?:[^"\\]|\\.)*)"/g;
const RE_CAMPOS = /\b(?:n|pron|lema|que|como|come|marida|t): "((?:[^"\\]|\\.)*)"/g;
for (const f of ["layout.js", "main.js", "paginas.js", "carta.js", "carta-clasica.js"]) {
  const src = fs.readFileSync(path.join(R, "js", f), "utf8");
  for (const m of src.matchAll(RE_T)) add(str(m[1]));
  for (const m of src.matchAll(RE_COND)) { add(str(m[1])); add(str(m[2])); }
  if (f === "paginas.js") for (const m of src.matchAll(RE_CAMPOS)) add(str(m[1]));
}
["Sáb", "Dom", "plato", "bebidas", "platos", "Reservar", "Preguntar", "Consultar · fin de semana", "Consultar",
 "Sólo fines de semana", "Reservar para el finde", "Pedirlo ahora", "Clásicos", "Compartir y milanesas", "Platos y postres"].forEach(add);
const html = fs.readFileSync(path.join(R, "index.html"), "utf8");
for (const m of html.matchAll(RE_T)) add(str(m[1]));
const out = [...set];
fs.writeFileSync(path.join(R, "i18n/claves_js.json"), JSON.stringify(out, null, 1));
console.log(out.length, "textos JS");
