/* =========================================================
   LOREN RESTOBAR · Carta clásica (A4)
   CartaClasica.render(el)  → hojas a tamaño real (carta-clasica.html)
   CartaClasica.visor(el)   → visor apilado en el inicio
   ========================================================= */
(function () {
  const L = window.LOREN, C = window.CARTA, CATS = window.CATEGORIAS;
  const enc = (sw = 0.9, petalos = 16) => window.nanduti({ sw, petalos });
  const euro = window.EURO;
  const cat = (id) => CATS.find((c) => c.id === id);

  const item = (p) => {
    const ico = (p.tags || []).filter((t) => t === "py" || t === "top").map((t) => `<i class="${t}">${t === "py" ? "PY" : "★"}</i>`).join("");
    const pr = p.precio == null ? `<span class="pr cons">${T("Consultar")}</span>` : `<span class="pr">${euro(p.precio)}</span>`;
    return `<div class="item"><div class="fila"><b>${p.n}${ico ? `<span class="ico">${ico}</span>` : ""}</b><span class="pts"></span>${pr}</div>
      <p>${p.d}${p.g ? ` <span class="gn">${p.g}</span>` : ""}</p></div>`;
  };
  const grupo = (id, destacado) => {
    const c = cat(id), items = C.filter((p) => p.cat === id);
    return `<section class="grupo ${destacado ? "destacado" : ""}">${destacado ? `<div class="bg">${enc(0.7)}</div>` : ""}
      <h2><span class="orn">${enc(1.6, 10)}</span>${c.n}</h2><div class="gsub">${c.s}</div><div class="linea"></div>
      ${items.map(item).join("")}</section>`;
  };
  const esquinas = () => `<div class="esq esq--tl">${enc(1)}</div><div class="esq esq--tr">${enc(1)}</div><div class="esq esq--bl">${enc(1)}</div><div class="esq esq--br">${enc(1)}</div><div class="franja"><i></i><i></i><i></i></div>`;
  const mini = (txt) => `<div class="cab cab--mini"><img src="img/marca/logo-loren.webp" alt="Loren Restobar"><span>${txt}</span></div>`;

  function paginas() {
    return [
      `<div class="cab"><div class="logo"><img src="img/marca/logo-loren.webp" alt="Loren Restobar"></div>
        <p class="lema">«${T(L.lema)}»</p><div class="sub">${T("Cocina paraguaya casera · Barcelona")}</div></div>
       <div class="cols">${grupo("paraguayo")}${grupo("empanadas")}${grupo("finde", true)}</div>
       <p class="leyenda"><i style="background:#59011d;color:#f3eedc">PY</i> ${T("típico paraguayo")} &nbsp;·&nbsp; <i style="background:#e8b43a;color:#2a000e">★</i> ${T("favorito de la casa")}</p>`,
      `${mini("Mba'éichapa! " + T("Bienvenidos"))}<div class="cols">${grupo("compartir")}${grupo("milanesas")}</div>
       <div class="caviso"><div class="r">${enc(1)}</div><div><h3>${T("¿Celebras algo?")}</h3><p>${T("Cumpleaños, bautizos, comidas de empresa… Preparamos bandejas de bocaditos paraguayos —empanadas, chipas, croquetas, sándwiches de miga y sopa paraguaya— o te reservamos el local con menú a medida.")}</p></div><div class="tel"><small>${T("Pregúntanos")}</small>${L.telefono}</div></div>`,
      `${mini("Vy'apavẽ! " + T("Que lo disfrutes"))}<div class="cols">${grupo("platos")}${grupo("sandwiches")}${grupo("postres")}${grupo("bebidas")}</div>
       <div class="dicc"><div class="rueda">${enc(0.9)}</div><div>
         <h3>${T("Pequeño diccionario guaraní de la mesa")}</h3><div class="s">${T("para pedir como un paraguayo")}</div>
         <dl>
           <div><dt>Mba'éichapa</dt><dd>${T("¿qué tal?")}</dd></div><div><dt>Aguyje</dt><dd>${T("gracias")}</dd></div>
           <div><dt>Tembi'u</dt><dd>${T("comida")}</dd></div><div><dt>Guazú</dt><dd>${T("grande")}</dd></div>
           <div><dt>Mandi'ó</dt><dd>${T("mandioca")}</dd></div><div><dt>Pira</dt><dd>${T("pez, pescado")}</dd></div>
           <div><dt>Chyryry</dt><dd>${T("el chisporroteo de la sartén")}</dd></div><div><dt>Vy'a</dt><dd>${T("alegría")}</dd></div>
           <div><dt>Ñandutí</dt><dd>${T("«tela de araña», nuestro encaje")}</dd></div><div><dt>Jaha!</dt><dd>${T("¡vamos!")}</dd></div>
         </dl></div></div>
       <div class="cpie"><span class="gr">Aguyje!</span>
        <b>${L.direccion} · ${L.cp}</b> · ${T("Reservas y pedidos")} <b>${L.telefono}</b> (${T("también WhatsApp")})<br>
        ${T("Pídenos también en Glovo y Uber Eats")} · @lorenrestobar_<br>
        ${T("IVA incluido. Consulta alérgenos al personal. Precios sujetos a cambios.")}</div>`
    ];
  }
  const hoja = (h, i) => `<article class="hoja" aria-label="${T("Página {n} de la carta", { n: i + 1 })}">${esquinas()}${h}</article>`;

  function render(el) { el.innerHTML = paginas().map(hoja).join(""); }

  const A4W = 793.7; // 210mm en px CSS
  function visor(el) {
    const hojas = paginas();
    const mesa = el.querySelector(".visor__mesa");
    const dots = el.querySelector(".visor__dots");
    mesa.innerHTML = hojas.map((h, i) => `<div class="hoja-wrap" data-i="${i}">${hoja(h, i)}</div>`).join("");
    dots.innerHTML = ["Clásicos", "Compartir y milanesas", "Platos y postres"].map((t, i) => `<button data-ir="${i}">${i + 1} · ${T(t)}</button>`).join("");
    const wraps = [...mesa.children];
    let actual = 0;
    const colocar = () => {
      wraps.forEach((w, i) => (w.dataset.pos = (i - actual + 3) % 3));
      [...dots.children].forEach((d, i) => d.classList.toggle("on", i === actual));
    };
    const medir = () => {
      const ancho = Math.min(el.clientWidth * (el.clientWidth < 700 ? 0.78 : 0.62), 520);
      const esc = ancho / A4W;
      el.style.setProperty("--esc", esc);
      el.style.setProperty("--alto", ancho * 1.4142 + 10 + "px");
    };
    medir(); colocar();
    window.addEventListener("resize", medir);
    mesa.addEventListener("click", (e) => {
      const w = e.target.closest(".hoja-wrap"); if (!w) return;
      const i = +w.dataset.i;
      if (i === actual) abrirLector(i); else { actual = i; colocar(); }
    });
    dots.addEventListener("click", (e) => { const b = e.target.closest("[data-ir]"); if (b) { actual = +b.dataset.ir; colocar(); } });
    el.querySelector("[data-prev]").addEventListener("click", () => { actual = (actual + 2) % 3; colocar(); });
    el.querySelector("[data-next]").addEventListener("click", () => { actual = (actual + 1) % 3; colocar(); });

    // deslizar en móvil
    let x0 = null;
    mesa.addEventListener("touchstart", (e) => (x0 = e.touches[0].clientX), { passive: true });
    mesa.addEventListener("touchend", (e) => {
      if (x0 == null) return;
      const dx = e.changedTouches[0].clientX - x0; x0 = null;
      if (Math.abs(dx) > 40) { actual = (actual + (dx < 0 ? 1 : 2)) % 3; colocar(); }
    });

    // lector a tamaño grande
    const lector = document.createElement("div");
    lector.className = "lector cc";
    lector.innerHTML = `<div class="lector__barra"><a class="btn btn--sm" href="${window.PREF || ""}carta-clasica.html">${T("Imprimir / PDF")}</a><button class="btn btn--sm btn--ghost" data-cerrar>${T("Cerrar")} ✕</button></div>${hojas.map((h, i) => `<div class="hoja-wrap" id="lector-${i}">${hoja(h, i)}</div>`).join("")}`;
    document.body.appendChild(lector);
    const escL = () => lector.style.setProperty("--esc-l", Math.min(1, (window.innerWidth - 32) / A4W));
    function abrirLector(i) {
      escL(); lector.classList.add("on"); document.body.style.overflow = "hidden";
      setTimeout(() => lector.querySelector("#lector-" + i).scrollIntoView({ block: "start" }), 50);
    }
    const cerrar = () => { lector.classList.remove("on"); document.body.style.overflow = ""; };
    lector.addEventListener("click", (e) => { if (e.target === lector || e.target.closest("[data-cerrar]")) cerrar(); });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") cerrar();
      if (!lector.classList.contains("on") && el.getBoundingClientRect().top < innerHeight && el.getBoundingClientRect().bottom > 0) {
        if (e.key === "ArrowRight") { actual = (actual + 1) % 3; colocar(); }
        if (e.key === "ArrowLeft") { actual = (actual + 2) % 3; colocar(); }
      }
    });
    window.addEventListener("resize", escL);
  }

  window.CartaClasica = { render, visor, paginas };
})();
