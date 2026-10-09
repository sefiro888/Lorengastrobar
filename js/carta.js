/* =========================================================
   LOREN RESTOBAR · Carta interactiva
   La carta es para mirar y elegir. Cada plato tiene «Pedir»:
   Glovo, Uber Eats o encargarlo por WhatsApp para recoger.
   ========================================================= */
(function () {
  const L = window.LOREN, CARTA = window.CARTA, CATS = window.CATEGORIAS;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const euro = window.EURO;
  const wa = (t) => `${L.links.whatsapp}?text=${encodeURIComponent(t)}`;
  const slug = (s) => s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");
  const norm = (s) => s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
  const enc = (sw = 0.7) => window.nanduti({ sw });
  CARTA.forEach((p, i) => { p.id = slug(p.nombre); p.orden = i; });
  const byId = (id) => CARTA.find((p) => p.id === id);
  const cat = (id) => CATS.find((c) => c.id === id);
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const TAGS = { py: T("Típico paraguayo"), top: T("Favorito"), comp: T("Para compartir"), sintrigo: T("Sin trigo*"), finde: T("Sólo finde") };
  const TCLS = { py: "tag--py", top: "tag--top", finde: "tag--finde" };
  const BANNER = {
    paraguayo: "img/platos/hl-chipa-guazu.webp", empanadas: "img/platos/hl-empanadas.webp", finde: "img/platos/hl-vori-vori.webp",
    compartir: "img/clientes/picada-paraguaya.webp", milanesas: "img/platos/hl-milanesa.webp", platos: "img/platos/hl-noquis.webp",
    sandwiches: "img/platos/hl-sandwich-milanesa.webp", postres: "img/platos/hl-flan.webp", bebidas: "img/platos/guarana.webp"
  };

  /* ---------- Botón «Pedir» ---------- */
  const BOLSA = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 8h12l-1 12H7z"/><path d="M9 8a3 3 0 0 1 6 0"/></svg>';
  const pedir = (p) => p.precio == null
    ? `<a class="pedir-btn pedir-btn--wa" href="${wa(p.cat === "finde" ? T("¡Hola Loren! ¿Este finde tenéis {x}? Quería reservar.", { x: p.n }) : T("¡Hola Loren! ¿Hoy tenéis {x}? Me gustaría pedirlo.", { x: p.n }))}" target="_blank" rel="noopener">${T(p.cat === "finde" ? "Reservar" : "Preguntar")}</a>`
    : `<button class="pedir-btn" data-pedir-plato="${p.id}" aria-label="${T("Pedir")} ${p.n}">${BOLSA}${T("Pedir")}</button>`;

  const pp = $("#pp");
  function abrirPedir(id) {
    const p = byId(id); if (!p) return;
    $("#pp-img").innerHTML = p.img ? `<img src="${p.img}" alt="">` : enc(0.9);
    $("#pp-nom").textContent = p.n;
    $("#pp-precio").textContent = euro(p.precio);
    $("#pp-glovo").href = L.links.glovo;
    $("#pp-uber").href = L.links.uber;
    $("#pp-wa").href = wa(T("¡Hola Loren! Quiero encargar {x} para recoger en el local. ¿A qué hora puedo pasar?", { x: p.n }));
    pp.classList.add("on");
  }
  const cerrarPedir = () => pp.classList.remove("on");
  pp.addEventListener("click", (e) => { if (e.target === pp || e.target.closest("[data-pp-cerrar]") || e.target.closest(".pp__op")) setTimeout(cerrarPedir, 50); });

  document.addEventListener("click", (e) => {
    const b = e.target.closest("[data-pedir-plato]");
    if (b) { e.preventDefault(); e.stopPropagation(); abrirPedir(b.dataset.pedirPlato); return; }
    const v = e.target.closest("[data-ver]");
    if (v) { e.preventDefault(); abrirFicha(v.dataset.ver); }
  });

  /* ---------- Hero: stats + tira ---------- */
  const conPrecio = CARTA.filter((p) => p.precio != null);
  $("#ch-stats").innerHTML = [
    [CARTA.length, T("platos y bebidas")],
    [CARTA.filter((p) => (p.tags || []).includes("py")).length, T("típicos paraguayos")],
    [euro(Math.min(...conPrecio.map((p) => p.precio))).replace(",00", "").replace(".00", ""), T("desde")],
    [CARTA.filter((p) => (p.tags || []).includes("sintrigo")).length, T("sin trigo*")]
  ].map(([b, s]) => `<div><b>${b}</b><span>${s}</span></div>`).join("");
  const conImg = CARTA.filter((p) => p.img && p.cat !== "bebidas");
  const mitad = Math.ceil(conImg.length / 2);
  const fila = (arr) => { const h = arr.map((p) => `<img src="${p.img}" alt="" loading="lazy">`).join(""); return h + h; };
  $("#tira1").innerHTML = fila(conImg.slice(0, mitad));
  $("#tira2").innerHTML = fila(conImg.slice(mitad));

  /* ---------- Escaparate ---------- */
  const ESTRELLAS = ["Chipa guazú", "Vorí vorí", "Milanesa a caballo", "Mbejú relleno de queso", "Picada completa", "Box de 6 empanadas"].map((n) => CARTA.find((p) => p.nombre === n)).filter(Boolean);
  const ef = $("#escap-fotos"), info = $("#escap-info");
  ef.innerHTML = ESTRELLAS.map((p) => `<img src="${p.img}" alt="${p.n}">`).join("");
  $("#escap-thumbs").innerHTML = ESTRELLAS.map((p, i) => `<button data-e="${i}" aria-label="${p.n}"><img src="${p.img}" alt=""></button>`).join("");
  $("#escap-tot").textContent = String(ESTRELLAS.length).padStart(2, "0");
  let ei = 0, eStart = 0;
  const DUR = 6000;
  function verEstrella(i) {
    ei = (i + ESTRELLAS.length) % ESTRELLAS.length;
    const p = ESTRELLAS[ei];
    $$("img", ef).forEach((im, k) => im.classList.toggle("on", k === ei));
    $$("#escap-thumbs button").forEach((b, k) => b.classList.toggle("on", k === ei));
    info.classList.add("cambia");
    setTimeout(() => {
      $("#escap-num").textContent = String(ei + 1).padStart(2, "0");
      $("#escap-nom").textContent = p.n;
      $("#escap-gn").textContent = p.g || cat(p.cat).n;
      $("#escap-desc").textContent = p.d;
      $("#escap-precio").textContent = p.precio == null ? T("Finde") : euro(p.precio);
      $("#escap-add").innerHTML = pedir(p);
      $("#escap-ver").dataset.ver = p.id;
      info.classList.remove("cambia");
    }, 300);
    eStart = performance.now();
  }
  $("#escap-thumbs").addEventListener("click", (e) => { const b = e.target.closest("[data-e]"); if (b) verEstrella(+b.dataset.e); });
  const barra = $("#escap-barra");
  let enVista = true;
  new IntersectionObserver(([e]) => (enVista = e.isIntersecting)).observe($(".escap"));
  function tick(t) {
    if (!reduce && enVista && !pp.classList.contains("on")) {
      const p = Math.min(1, (t - eStart) / DUR);
      barra.style.width = p * 100 + "%";
      if (p >= 1) verEstrella(ei + 1);
    } else eStart += 16;
    requestAnimationFrame(tick);
  }
  verEstrella(0); requestAnimationFrame(tick);

  /* ---------- Barra de categorías (fija, se esconde al bajar) ---------- */
  const cnavEl = $("#cnav"), cnav = $("#cnav-cats");
  cnav.innerHTML = CATS.map((c) => `<a href="#c-${c.id}" data-cat="${c.id}"><img src="${BANNER[c.id]}" alt="" loading="lazy">${c.n}</a>`).join("");
  let ultY = window.scrollY, saltando = false;
  cnav.addEventListener("click", () => { saltando = true; cnavEl.classList.remove("oculta"); setTimeout(() => (saltando = false), 900); });
  window.addEventListener("scroll", () => {
    const y = window.scrollY, d = y - ultY;
    const inicio = $("#c-lista").getBoundingClientRect().top + y - 140;
    if (y < inicio) cnavEl.classList.remove("oculta");
    else if (!saltando && d > 8) cnavEl.classList.add("oculta");
    else if (d < -8) cnavEl.classList.remove("oculta");
    if (Math.abs(d) > 8) ultY = y;
  }, { passive: true });

  /* ---------- Render de la carta ---------- */
  const lista = $("#c-lista");
  let filtro = null, q = "", orden = "rec", vista = "grid";

  const tarjeta = (p, i) => {
    const tags = (p.tags || []).slice(0, 3).map((t) => `<span class="tag ${TCLS[t] || ""}">${TAGS[t]}</span>`).join("");
    const img = p.img
      ? `<div class="p-card__img" data-ver="${p.id}"><img src="${p.img}" alt="${p.n}" loading="lazy"><div class="p-card__tags">${tags}</div></div>`
      : `<div class="p-card__img p-card__img--ph" data-ver="${p.id}"><div class="enc">${enc(0.8)}</div><span class="ini">${p.n}</span><div class="p-card__tags">${tags}</div></div>`;
    const precio = p.precio == null ? `<span class="precio precio--consultar">${T("Consultar")}</span>` : `<span class="precio">${euro(p.precio)}</span>`;
    return `<article class="p-card" style="animation-delay:${Math.min(i, 9) * 0.04}s">${img}
      <div class="p-card__body">
        <div class="p-card__top"><h3 data-ver="${p.id}">${p.n}</h3>${precio}</div>
        ${p.g ? `<div class="gn">${p.g}</div>` : ""}
        <p>${p.d}</p>
        <div class="p-card__pie"><button class="ver-btn" data-ver="${p.id}">${T("Ver ficha")}</button>${pedir(p)}</div>
      </div></article>`;
  };
  const bebida = (p) => `<div class="bebida"><div><b>${p.n}</b><small>${p.d}</small></div><span class="pts"></span><span class="precio">${euro(p.precio)}</span></div>`;

  function render() {
    const items = CARTA.filter((p) =>
      (!filtro || (p.tags || []).includes(filtro)) &&
      (!q || norm(p.nombre + " " + p.n + " " + p.d + " " + p.g).includes(q)));
    const ord = (arr) => orden === "rec" ? arr : [...arr].sort((a, b) => ((a.precio ?? 999) - (b.precio ?? 999)) * (orden === "asc" ? 1 : -1));
    const grupos = CATS.map((c, k) => ({ c, k, it: ord(items.filter((p) => p.cat === c.id)) })).filter((g) => g.it.length);
    lista.innerHTML = grupos.map(({ c, k, it }) => `
      <section class="cat ${c.id === "finde" ? "cat--finde" : ""}" id="c-${c.id}">
        <div class="cat__banner"><img src="${BANNER[c.id]}" alt="" loading="lazy"><div class="enc">${enc(0.6)}</div>
          <div><span class="n">${String(k + 1).padStart(2, "0")} · ${c.s}</span><h2>${c.n}</h2>${c.g ? `<span class="gn">${c.g}</span>` : ""}</div>
          <span class="cuenta">${it.length} ${T(it.length === 1 ? "plato" : c.id === "bebidas" ? "bebidas" : "platos")}</span></div>
        ${c.id === "bebidas" ? `<div class="bebidas">${it.map(bebida).join("")}</div>` : `<div class="platos ${vista === "lista" ? "lista" : ""}">${it.map(tarjeta).join("")}</div>`}
      </section>`).join("");
    $("#c-vacio").style.display = items.length ? "none" : "block";
    $$("#cnav-cats a").forEach((a) => (a.style.display = grupos.some((g) => g.c.id === a.dataset.cat) ? "" : "none"));
    observarCats();
  }

  $$(".cnav__herr .chip[data-tag]").forEach((c) => c.addEventListener("click", () => {
    filtro = filtro === c.dataset.tag ? null : c.dataset.tag;
    $$(".cnav__herr .chip[data-tag]").forEach((x) => x.classList.toggle("is-on", x.dataset.tag === filtro));
    render();
  }));
  $("#c-buscar").addEventListener("input", (e) => { q = norm(e.target.value.trim()); render(); });
  $("#c-orden").addEventListener("change", (e) => { orden = e.target.value; render(); });
  $$("[data-vista]").forEach((b) => b.addEventListener("click", () => {
    vista = b.dataset.vista; $$("[data-vista]").forEach((x) => x.classList.toggle("on", x === b)); render();
  }));

  // scroll-spy
  let obsC;
  function observarCats() {
    obsC && obsC.disconnect();
    obsC = new IntersectionObserver((ents) => ents.forEach((e) => {
      if (!e.isIntersecting) return;
      const id = e.target.id.replace("c-", "");
      $$("#cnav-cats a").forEach((a) => {
        const on = a.dataset.cat === id; a.classList.toggle("on", on);
        if (on) cnav.scrollTo({ left: a.offsetLeft - cnav.clientWidth / 2 + a.clientWidth / 2, behavior: "smooth" });
      });
    }), { rootMargin: "-40% 0px -55% 0px" });
    $$(".cat", lista).forEach((s) => obsC.observe(s));
  }
  render();

  /* ---------- Ficha (quick view) ---------- */
  const qv = $("#qv");
  const SUG = ["Chipa guazú", "Sopa paraguaya", "Mbejú relleno de queso", "Box de 6 empanadas", "Yuca brava con salsa casera", "Milanesa a caballo", "Tarta tres leches", "Guaraná", "Picada de chorizo con chimichurri"];
  function abrirFicha(id) {
    const p = byId(id); if (!p) return;
    const c = cat(p.cat);
    $("#qv-img").innerHTML = p.img ? `<img src="${p.img}" alt="${p.n}">` : `<div class="ph"><div class="enc">${enc(0.7)}</div><span>${p.n}</span></div>`;
    $("#qv-cat").textContent = c.n;
    $("#qv-nom").textContent = p.n;
    $("#qv-gn").textContent = p.g;
    $("#qv-tags").innerHTML = (p.tags || []).map((t) => `<span class="tag ${TCLS[t] || ""}">${TAGS[t]}</span>`).join("");
    $("#qv-desc").textContent = p.d;
    $("#qv-precio").innerHTML = p.precio == null ? `<span class="precio precio--consultar">${T(p.cat === "finde" ? "Consultar · fin de semana" : "Consultar")}</span>` : `<span class="precio">${euro(p.precio)}</span>`;
    $("#qv-add").innerHTML = pedir(p);
    const sug = SUG.map((n) => CARTA.find((x) => x.nombre === n)).filter((x) => x && x.id !== p.id && x.cat !== p.cat).slice(0, 3);
    $("#qv-sug").innerHTML = sug.map((s) => `<button data-ver="${s.id}">${s.img ? `<img src="${s.img}" alt="" loading="lazy">` : `<span class="ph2"></span>`}<b>${s.n}</b><small>${s.precio != null ? euro(s.precio) : T("Consultar")}</small></button>`).join("");
    qv.classList.add("on");
    $(".qv__caja", qv).scrollTop = 0;
  }
  const cerrarFicha = () => qv.classList.remove("on");
  qv.addEventListener("click", (e) => { if (e.target === qv || e.target.closest("[data-qv-cerrar]")) cerrarFicha(); });
  $("#escap-ver").addEventListener("click", () => abrirFicha($("#escap-ver").dataset.ver));
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") { cerrarFicha(); cerrarPedir(); } });

  // limpiar la bandeja antigua guardada en el navegador
  try { localStorage.removeItem("loren-bandeja"); } catch (e) {}

  // abrir ficha por hash (#plato-xxx)
  if (location.hash.startsWith("#plato-")) setTimeout(() => abrirFicha(location.hash.slice(7)), 600);
})();
