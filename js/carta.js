/* =========================================================
   LOREN RESTOBAR · Carta interactiva + Mi bandeja
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

  const TAGS = { py: T("Típico paraguayo"), top: T("Favorito"), comp: T("Para compartir"), sintrigo: T("Sin trigo*"), finde: T("Sólo finde") };
  const TCLS = { py: "tag--py", top: "tag--top", finde: "tag--finde" };
  const BANNER = {
    paraguayo: "img/platos/chipa-guazu.webp", empanadas: "img/platos/box-empanadas.webp", finde: "img/platos/caldo-gallina.webp",
    compartir: "img/clientes/picada-paraguaya.webp", milanesas: "img/platos/mila-caballo-pro.webp", platos: "img/platos/noquis.webp",
    sandwiches: "img/platos/sandwich-milanesa-completa.webp", postres: "img/platos/tres-leches.webp", bebidas: "img/platos/guarana.webp"
  };

  /* ---------- Bandeja (estado) ---------- */
  const KEY = "loren-bandeja";
  let B = {};
  try { B = JSON.parse(localStorage.getItem(KEY) || "{}") || {}; } catch (e) { B = {}; }
  const guardar = () => { try { localStorage.setItem(KEY, JSON.stringify(B)); } catch (e) {} };
  const qty = (id) => B[id] || 0;
  const poner = (id, n, aviso) => {
    const p = byId(id); if (!p) return;
    const antes = qty(id);
    if (n <= 0) delete B[id]; else B[id] = n;
    guardar(); refrescar(id);
    if (aviso && n > antes) toast(T("{x} añadido a tu bandeja", { x: p.n }));
  };

  const ctrl = (p, txt = true) => {
    if (p.precio == null) return `<a class="btn btn--sm" href="${wa(p.cat === "finde" ? T("¡Hola Loren! ¿Este finde tenéis {x}? Quería reservar.", { x: p.n }) : T("¡Hola Loren! ¿Hoy tenéis {x}? Me gustaría pedirlo.", { x: p.n }))}" target="_blank" rel="noopener" style="padding:.6em 1em">${T(p.cat === "finde" ? "Reservar" : "Preguntar")}</a>`;
    const q = qty(p.id);
    return q
      ? `<span class="add" data-ctrl="${p.id}"><button data-menos="${p.id}" aria-label="${T("Quitar uno")}">−</button><span class="q">${q}</span><button data-mas="${p.id}" aria-label="${T("Añadir uno")}">+</button></span>`
      : `<span class="add" data-ctrl="${p.id}"><button class="mas-txt" data-mas="${p.id}" aria-label="${T("Añadir")} ${p.n}"><i>+</i>${txt ? T("Añadir") : ""}</button></span>`;
  };
  function refrescar(id) {
    $$(`[data-ctrl-wrap="${id}"]`).forEach((w) => { w.innerHTML = ctrl(byId(id), w.dataset.txt !== "0"); const a = $(".add", w); a && a.classList.add("pop"); });
    pintarBandeja();
  }

  document.addEventListener("click", (e) => {
    const m = e.target.closest("[data-mas]"), n = e.target.closest("[data-menos]");
    if (m) { e.stopPropagation(); poner(m.dataset.mas, qty(m.dataset.mas) + 1, true); fabPop(); }
    if (n) { e.stopPropagation(); poner(n.dataset.menos, qty(n.dataset.menos) - 1); }
    const v = e.target.closest("[data-ver]");
    if (v && !m && !n) { e.preventDefault(); abrirFicha(v.dataset.ver); }
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
  let ei = 0, eT = null, eStart = 0;
  const DUR = 6000;
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
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
      const w = $("#escap-add"); w.dataset.ctrlWrap = p.id; w.innerHTML = ctrl(p);
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
    if (!reduce && enVista) {
      const p = Math.min(1, (t - eStart) / DUR);
      barra.style.width = p * 100 + "%";
      if (p >= 1) verEstrella(ei + 1);
    } else eStart += 16;
    requestAnimationFrame(tick);
  }
  verEstrella(0); requestAnimationFrame(tick);

  /* ---------- Navegación de categorías ---------- */
  const cnav = $("#cnav-cats");
  cnav.innerHTML = CATS.map((c) => `<a href="#c-${c.id}" data-cat="${c.id}"><img src="${BANNER[c.id]}" alt="" loading="lazy">${c.n}</a>`).join("");

  /* ---------- Render de la carta ---------- */
  const lista = $("#c-lista");
  let filtro = null, q = "", orden = "rec", vista = "grid";

  const tarjeta = (p, i) => {
    const tags = (p.tags || []).slice(0, 3).map((t) => `<span class="tag ${TCLS[t] || ""}">${TAGS[t]}</span>`).join("");
    const img = p.img
      ? `<div class="p-card__img" data-ver="${p.id}"><img src="${p.img}" alt="${p.n}" loading="lazy"><div class="p-card__tags">${tags}</div></div>`
      : `<div class="p-card__img p-card__img--ph" data-ver="${p.id}"><div class="enc">${enc(0.8)}</div><span class="ini">${p.n}</span><div class="p-card__tags">${tags}</div></div>`;
    const precio = p.precio == null ? `<span class="precio precio--consultar">${T("Consultar")}</span>` : `<span class="precio">${euro(p.precio)}</span>`;
    const links = p.precio == null ? "" : `<span class="links"><a class="g" href="${L.links.glovo}" target="_blank" rel="noopener">Glovo</a><a class="u" href="${L.links.uber}" target="_blank" rel="noopener">Uber</a></span>`;
    return `<article class="p-card" style="animation-delay:${Math.min(i, 9) * 0.04}s">${img}
      <div class="p-card__body">
        <div class="p-card__top"><h3 data-ver="${p.id}">${p.n}</h3>${precio}</div>
        ${p.g ? `<div class="gn">${p.g}</div>` : ""}
        <p>${p.d}</p>
        <div class="p-card__pie">${links}<span data-ctrl-wrap="${p.id}">${ctrl(p)}</span></div>
      </div></article>`;
  };
  const bebida = (p) => `<div class="bebida"><div><b>${p.n}</b><small>${p.d}</small></div><span class="pts"></span><span class="precio">${euro(p.precio)}</span><span data-ctrl-wrap="${p.id}" data-txt="0">${ctrl(p, false)}</span></div>`;

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

  $$(".cnav .chip[data-tag]").forEach((c) => c.addEventListener("click", () => {
    filtro = filtro === c.dataset.tag ? null : c.dataset.tag;
    $$(".cnav .chip[data-tag]").forEach((x) => x.classList.toggle("is-on", x.dataset.tag === filtro));
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
        if (on) a.scrollIntoView({ block: "nearest", inline: "center", behavior: "smooth" });
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
    const w = $("#qv-add"); w.dataset.ctrlWrap = p.id; w.innerHTML = ctrl(p);
    $("#qv-links").innerHTML = p.precio == null ? "" : `<a class="btn btn--glovo btn--sm" href="${L.links.glovo}" target="_blank" rel="noopener">Glovo</a><a class="btn btn--uber btn--sm" href="${L.links.uber}" target="_blank" rel="noopener">Uber Eats</a>`;
    const sug = SUG.map((n) => CARTA.find((x) => x.nombre === n)).filter((x) => x && x.id !== p.id && x.cat !== p.cat).slice(0, 3);
    $("#qv-sug").innerHTML = sug.map((s) => `<button data-ver="${s.id}">${s.img ? `<img src="${s.img}" alt="" loading="lazy">` : `<span class="ph2"></span>`}<b>${s.n}</b><small>${s.precio != null ? euro(s.precio) : T("Consultar")}</small></button>`).join("");
    qv.classList.add("on");
    $(".qv__caja", qv).scrollTop = 0;
  }
  const cerrarFicha = () => qv.classList.remove("on");
  qv.addEventListener("click", (e) => { if (e.target === qv || e.target.closest("[data-qv-cerrar]")) cerrarFicha(); });
  $("#escap-ver").addEventListener("click", () => abrirFicha($("#escap-ver").dataset.ver));

  /* ---------- Panel bandeja ---------- */
  const fab = $("#fab-bandeja"), panel = $("#bandeja");
  const abrirB = () => panel.classList.add("on");
  const cerrarB = () => panel.classList.remove("on");
  fab.addEventListener("click", abrirB);
  panel.addEventListener("click", (e) => { if (e.target.closest("[data-b-cerrar]")) cerrarB(); });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") { cerrarFicha(); cerrarB(); } });
  const fabPop = () => { fab.classList.remove("pop"); void fab.offsetWidth; fab.classList.add("pop"); };

  function pintarBandeja() {
    const ids = Object.keys(B).filter((id) => byId(id));
    const n = ids.reduce((s, id) => s + B[id], 0);
    const total = ids.reduce((s, id) => s + B[id] * (byId(id).precio || 0), 0);
    $("#fab-n").textContent = n;
    $("#fab-total").textContent = euro(total);
    $("#b-total").textContent = euro(total);
    fab.classList.toggle("on", n > 0);
    $("#b-lista").innerHTML = ids.length
      ? ids.map((id) => { const p = byId(id); return `<div class="b-item">${p.img ? `<img src="${p.img}" alt="">` : `<span class="ph"></span>`}<div><b>${p.n}</b><small>${euro(p.precio * B[id])}</small></div><span data-ctrl-wrap="${id}" data-txt="0">${ctrl(p, false)}</span></div>`; }).join("")
      : `<div class="bandeja__vacia"><div class="enc">${enc(0.8)}</div><p>${T("Tu bandeja está vacía.")}<br>${T("¡Empieza por una chipa guazú!")}</p></div>`;
    actualizarWa();
  }
  function actualizarWa() {
    const ids = Object.keys(B).filter((id) => byId(id));
    const total = ids.reduce((s, id) => s + B[id] * (byId(id).precio || 0), 0);
    const lineas = ids.map((id) => `• ${B[id]} × ${byId(id).n} — ${euro(byId(id).precio * B[id])}`).join("\n");
    const nom = $("#b-nombre").value.trim(), hora = $("#b-hora").value.trim(), nota = $("#b-nota").value.trim();
    $("#b-wa").href = wa(T("¡Mba'éichapa, Loren! Quiero encargar para recoger en el local:") + `\n\n${lineas}\n\n${T("Total orientativo")}: ${euro(total)}${nom ? `\n${T("Nombre")}: ${nom}` : ""}${hora ? `\n${T("Hora de recogida")}: ${hora}` : ""}${nota ? `\n${T("Notas")}: ${nota}` : ""}\n\n¡Aguyje!`);
    $("#b-wa").classList.toggle("is-off", !ids.length);
    $("#b-wa").style.pointerEvents = ids.length ? "" : "none";
    $("#b-wa").style.opacity = ids.length ? "" : ".5";
  }
  ["#b-nombre", "#b-hora", "#b-nota"].forEach((s) => $(s).addEventListener("input", actualizarWa));
  $("#b-vaciar").addEventListener("click", () => { B = {}; guardar(); render(); pintarBandeja(); verEstrella(ei); });
  pintarBandeja();

  /* ---------- Combos ---------- */
  $$("[data-combo]").forEach((b) => b.addEventListener("click", () => {
    const art = b.closest("[data-pack]");
    art.dataset.pack.split("|").forEach((x) => {
      const [n, k] = x.split("*"); const p = CARTA.find((c) => c.nombre === n.trim());
      if (p) B[p.id] = qty(p.id) + parseInt(k || "1", 10);
    });
    guardar(); render(); pintarBandeja(); fabPop();
    toast(T("Combo «{x}» añadido", { x: art.dataset.nombre }));
    setTimeout(abrirB, 500);
  }));

  /* ---------- Toast ---------- */
  let tT;
  function toast(t) {
    const el = $("#toast"); $("span", el).textContent = t; el.classList.add("on");
    clearTimeout(tT); tT = setTimeout(() => el.classList.remove("on"), 2200);
  }

  // abrir ficha por hash (#plato-xxx)
  if (location.hash.startsWith("#plato-")) setTimeout(() => abrirFicha(location.hash.slice(7)), 600);
})();
