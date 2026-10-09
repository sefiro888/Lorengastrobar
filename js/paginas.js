/* =========================================================
   LOREN RESTOBAR · Lógica de páginas interiores
   ========================================================= */
(function () {
  const L = window.LOREN, CARTA = window.CARTA || [];
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const euro = window.EURO;
  const wa = (t) => `${L.links.whatsapp}?text=${encodeURIComponent(t)}`;
  const plato = (n) => CARTA.find((p) => p.nombre === n);
  const ALTAVOZ = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 5 6 9H2v6h4l5 4V5z"/><path d="M15.5 8.5a5 5 0 0 1 0 7M19 5a10 10 0 0 1 0 14"/></svg>';

  /* ---------- Pronunciar (voz del navegador) ---------- */
  function decir(txt) {
    if (!("speechSynthesis" in window)) return;
    speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(txt);
    u.lang = "es-ES"; u.rate = 0.82;
    const v = speechSynthesis.getVoices().find((x) => /es-(ES|MX|US|AR)/.test(x.lang));
    if (v) u.voice = v;
    speechSynthesis.speak(u);
  }
  document.addEventListener("click", (e) => {
    const b = e.target.closest("[data-oir]");
    if (b) { e.preventDefault(); e.stopPropagation(); decir(b.dataset.oir); }
  });
  $$("[data-oir]").forEach((b) => { if (!b.innerHTML.trim()) b.innerHTML = ALTAVOZ; b.setAttribute("aria-label", "Escuchar pronunciación"); });

  /* ---------- Barras de votación ---------- */
  const votos = $(".votos");
  if (votos) {
    new IntersectionObserver(([e], o) => {
      if (!e.isIntersecting) return;
      $$(".voto__barra div", votos).forEach((d) => (d.style.width = d.dataset.w + "%"));
      o.disconnect();
    }, { threshold: 0.3 }).observe(votos);
  }

  /* ---------- Enciclopedia de sabores ---------- */
  const SABORES = [
    { id: "chipa-guazu", n: "Chipa guazú", oir: "chipa guazú", pron: "chi-pa gua-SÚ", img: "img/platos/chipa-guazu.webp", carta: "Chipa guazú",
      lema: "El orgullo de cualquier asado paraguayo",
      que: "Un pastel horneado de choclo (maíz tierno) que queda esponjoso por dentro y dorado por fuera. «Guazú» significa «grande» en guaraní: es la versión en fuente de la chipa.",
      como: "Maíz tierno, cebolla, huevos, cuajada, queso tierno, grasa de cerdo y sal. Al horno hasta que se dora.",
      come: "Caliente, en porciones, como entrante o acompañando la parrillada.", marida: "Parrillada paraguaya · Vorí vorí · una Guaraná bien fría" },
    { id: "sopa-paraguaya", n: "Sopa paraguaya", oir: "sopa paraguaya", pron: "so-pa pa-ra-GUA-ya", img: "img/platos/sopa-paraguaya-pro.webp", carta: "Sopa paraguaya",
      lema: "La única sopa del mundo que se come con tenedor",
      que: "A pesar del nombre, es un bizcocho salado de maíz. Cuenta la leyenda que la cocinera del presidente Carlos Antonio López echó demasiada harina de maíz a una sopa… y el «error» se convirtió en plato nacional.",
      como: "Harina de maíz, huevos, cuajada, queso tierno, cebolla, leche, grasa de cerdo, un toque de anís y sal.",
      come: "Templada, sola o junto a carnes. Se repite seguro.", marida: "Milanesa a caballo · Picada completa · Chipa guazú" },
    { id: "mbeju", n: "Mbejú", oir: "mbeyú", pron: "mbe-YÚ", img: "img/platos/mbeju-queso.webp", carta: "Mbejú relleno de queso",
      lema: "Crujiente por fuera, el queso estira por dentro",
      que: "Una torta a la plancha de almidón de mandioca de herencia guaraní. Nuestro reel enseñando cómo lo hacemos superó los 2.400 «me gusta».",
      como: "Almidón de mandioca, harina de maíz, queso rallado, leche, mantequilla y sal. El relleno lleva mozzarella fundida.",
      come: "Recién hecho. En Paraguay se toma en el desayuno o la merienda con cocido o café con leche.", marida: "Café con leche · Sopa paraguaya" },
    { id: "vori-vori", n: "Vorí vorí", oir: "borí borí", pron: "bo-RÍ bo-RÍ", img: "img/platos/caldo-gallina.webp", carta: "Vorí vorí", finde: true,
      lema: "El plato con el que representamos a Paraguay",
      que: "Un caldo de gallina casera con bolitas de harina de maíz y queso. El nombre viene de «bolita». Con este plato Loren llevó a Paraguay al Mundial de Comidas de Ibai Llanos.",
      como: "Gallina casera cocida a fuego lento, verduras y bolitas de harina de maíz amasadas con queso.",
      come: "Bien caliente, con cuchara grande. En invierno se pide más que nunca.", marida: "Chipa guazú · Mandioca" },
    { id: "pira-caldo", n: "Pira caldo", oir: "pira caldo", pron: "pi-RA CAL-do", img: null, carta: "Pira caldo", finde: true,
      lema: "«Pira» significa pez en guaraní",
      que: "Un caldo de pescado espeso y reconfortante, típico de las zonas de río de Paraguay. Lo preparamos cada fin de semana.",
      como: "Pescado, verduras, leche y queso hasta lograr un caldo cremoso.",
      come: "En plato hondo, para entrar en calor.", marida: "Sopa paraguaya · Mandioca" },
    { id: "soyo", n: "Soyo", oir: "soyo", pron: "SO-yo", img: "img/redes/ig-soyo.webp", carta: "Soyo con tortillita", finde: true,
      lema: "Viene de «so'o josopy»: carne machacada",
      que: "Una sopa espesa de carne machacada, de las más queridas de la cocina paraguaya. Con el profe de guaraní Mbo'ehára Marce contamos en Instagram el origen de su nombre.",
      como: "Carne machacada, verduras y caldo. Se sirve con tortillita paraguaya y mandioca.",
      come: "Caliente, alternando cucharada y trozo de tortillita.", marida: "Mandioca · Tortillita" },
    { id: "chyryry", n: "Mandi'ó chyryry", oir: "mandió chiriri", pron: "man-di-Ó chy-ry-RY", img: null, carta: "Mandi'ó chyryry",
      lema: "«Chyryry» imita el chisporroteo de la sartén",
      que: "Un salteado de mandioca: el plato estrella de nuestro segundo local y uno de los más pedidos para compartir.",
      como: "Mandioca, patata, queso, jamón, cebolla de verdeo y un huevo frito por encima. También con bacon.",
      come: "Al centro de la mesa, rompiendo el huevo sobre la mandioca.", marida: "Cerveza bien fría · Picada de chorizo" },
    { id: "empanadas", n: "Empanadas", oir: "empanadas", pron: "carne · pollo · jamón y queso · choclo", img: "img/platos/box-empanadas.webp", carta: "Box de 6 empanadas",
      lema: "Lo más nombrado en nuestras reseñas",
      que: "Masa casera y relleno jugoso. Son el plato que más aparece en nuestras reseñas de Google.",
      como: "La de carne lleva ternera, cebolla, pimiento verde, ajo, huevo duro, comino y pimienta. También de pollo, jamón y queso, y choclo con mozzarella.",
      come: "Con la mano y sin miedo. El box de seis es perfecto para probarlas todas.", marida: "Guaraná · Yuca brava" },
    { id: "parrillada", n: "Parrillada paraguaya", oir: "parrillada paraguaya", pron: "el asado del domingo", img: "img/platos/parrillada-paraguaya.webp", carta: "Parrillada paraguaya",
      lema: "En Paraguay el asado es un ritual familiar",
      que: "La mesa paraguaya de domingo, servida humeante en brasero.",
      como: "Asado, chorizo, chinchulín y pollo, con mandioca y chipa guazú.",
      come: "Para dos o más, en el centro y sin prisa.", marida: "Chipa guazú · Ensalada de la casa" },
    { id: "milanesa", n: "Milanesa", oir: "milanesa a caballo", pron: "a caballo · napolitana · fugazzeta", img: "img/platos/mila-caballo-pro.webp", carta: "Milanesa a caballo",
      lema: "Diez maneras de comer el plato más popular",
      que: "En Paraguay la milanesa es casi un plato nacional. Aquí la empanamos al momento y la servimos en raciones que desbordan el plato.",
      como: "Ternera o pollo rebozados al momento. A caballo (dos huevos fritos), napolitana, americana, cuatro quesos, fugazzeta, caprese… o en sándwich.",
      come: "Con patatas fritas, limón y apetito.", marida: "Sopa paraguaya · Coca-Cola fría" }
  ];
  const enciclo = $("#enciclopedia");
  if (enciclo) {
    $("#enciclo-indice").innerHTML = SABORES.map((s) => `<a href="#${s.id}">${T(s.n)}</a>`).join("");
    enciclo.innerHTML = SABORES.map((s, i) => {
      const p = plato(s.carta);
      const precio = p && p.precio != null ? `<span class="precio">${euro(p.precio)}</span>` : `<span class="precio precio--consultar">${T(s.finde ? "Sólo fines de semana" : "Consultar")}</span>`;
      const foto = s.img ? `<div class="disco"><img src="${s.img}" alt="${T(s.n)}" loading="lazy"></div>` : `<div class="disco disco--vacio"><div data-nanduti data-sw="0.8"></div></div>`;
      return `<article class="entrada rv" id="${s.id}">
        <div class="entrada__foto"><div class="enc" data-nanduti data-sw="0.5"></div>${foto}<span class="num">${String(i + 1).padStart(2, "0")}</span></div>
        <div>
          <h3>${T(s.n)}</h3>
          <div class="pron"><button class="oir" data-oir="${s.oir}"></button>${T(s.pron)}</div>
          <div class="lema-e">${T(s.lema)}</div>
          <p>${T(s.que)}</p>
          <dl class="ficha">
            <div><dt>${T("Cómo lo hacemos")}</dt><dd>${T(s.como)}</dd></div>
            <div><dt>${T("Cómo se come")}</dt><dd>${T(s.come)}</dd></div>
            <div><dt>${T("Va genial con")}</dt><dd>${T(s.marida)}</dd></div>
          </dl>
          <div class="entrada__pie">${precio}
            ${s.finde ? `<a class="btn btn--sm" href="${wa(T("¡Hola Loren! ¿Este finde tenéis {x}? Quería reservar.", { x: T(s.n) }))}" target="_blank" rel="noopener">${T("Reservar para el finde")}</a>` : `<a class="btn btn--sm btn--vino" href="${PREF}carta.html">${T("Ver en la carta")}</a><a class="btn btn--sm btn--glovo" href="${L.links.glovo}" target="_blank" rel="noopener">${T("Pedir en Glovo")}</a>`}
          </div>
        </div></article>`;
    }).join("");
    window.pintarNanduti && window.pintarNanduti(enciclo);
    $$("[data-oir]", enciclo).forEach((b) => (b.innerHTML = ALTAVOZ));
  }

  /* ---------- Rutas / packs con total calculado ---------- */
  $$("[data-pack]").forEach((el) => {
    const items = el.dataset.pack.split("|").map((x) => { const [n, q] = x.split("*"); return { p: plato(n.trim()), q: parseInt(q || "1", 10) }; }).filter((x) => x.p);
    const total = items.reduce((s, x) => s + (x.p.precio || 0) * x.q, 0);
    $("ul", el).innerHTML = items.map((x) => `<li>${x.p.img ? `<img src="${x.p.img}" alt="" loading="lazy">` : `<span class="ph"></span>`}<span>${x.q > 1 ? x.q + " × " : ""}${T(x.p.nombre)}</span><span class="p">${euro(x.p.precio * x.q)}</span></li>`).join("");
    const personas = parseInt(el.dataset.personas || "1", 10);
    $(".ruta__total", el).insertAdjacentHTML("afterbegin", `<div><small>${T("Total orientativo")}</small><b>${euro(total)}</b>${personas > 1 ? `<small>≈ ${T("{x} por persona", { x: euro(total / personas) })}</small>` : ""}</div>`);
    const btn = $("[data-pack-wa]", el);
    if (btn) {
      btn.href = wa(T("¡Hola Loren! Quiero pedir «{x}» para recoger:", { x: el.dataset.nombre }) + "\n" + items.map((x) => `• ${x.q} × ${T(x.p.nombre)}`).join("\n") + `\n\n${T("Total orientativo")}: ${euro(total)}`);
      btn.target = "_blank"; btn.rel = "noopener";
    }
  });

  /* ---------- Quiz ---------- */
  const quiz = $(".quiz");
  if (quiz) {
    const pasos = $$(".quiz__paso", quiz), prog = $$(".quiz__prog i", quiz);
    const punt = {};
    const RES = {
      chipa: { n: "Chipa guazú", img: "img/platos/chipa-guazu.webp", t: "Eres el alma de la fiesta: generoso, cálido y siempre presente en las reuniones. Combinas con todo y nadie se olvida de ti.", c: "Chipa guazú" },
      vori: { n: "Vorí vorí", img: "img/platos/caldo-gallina.webp", t: "Eres abrazo y hogar. Tu gente acude a ti cuando necesita consuelo, y sabes que lo bueno lleva su tiempo.", c: "Vorí vorí" },
      mbeju: { n: "Mbejú", img: "img/platos/mbeju-queso.webp", t: "Crujiente por fuera, tierno por dentro. Madrugas con alegría y siempre tienes un plan para el desayuno.", c: "Mbejú relleno de queso" },
      mila: { n: "Milanesa a caballo", img: "img/platos/mila-caballo-pro.webp", t: "Lo tuyo es a lo grande: sin medias tintas y con dos huevos encima. Nadie se queda con hambre a tu lado.", c: "Milanesa a caballo" }
    };
    let i = 0;
    const ir = (n) => {
      pasos.forEach((p, k) => p.classList.toggle("on", k === n));
      prog.forEach((p, k) => p.classList.toggle("on", k <= n));
    };
    quiz.addEventListener("click", (e) => {
      const b = e.target.closest("[data-r]");
      if (b) {
        punt[b.dataset.r] = (punt[b.dataset.r] || 0) + 1;
        i++;
        if (i < pasos.length - 1) return ir(i);
        const gan = Object.entries(punt).sort((a, b) => b[1] - a[1])[0][0];
        const r = RES[gan], p = plato(r.c), rn = T(r.n);
        $(".quiz__res", quiz).innerHTML = `<div class="disco"><img src="${r.img}" alt="${rn}"></div>
          <div><div class="eres">${T("Tú eres…")}</div><h4>${rn}</h4><p>${T(r.t)}</p>
          <div class="hero__ctas"><a class="btn" href="${p && p.cat === "finde" ? wa(T("¡Hola Loren! Según vuestro test soy {x} 😄 ¿Lo tenéis este finde?", { x: rn })) : L.links.glovo}" target="_blank" rel="noopener">${T(p && p.cat === "finde" ? "Reservar para el finde" : "Pedirlo ahora")}</a>
          <button class="btn btn--ghost" data-reinicio>${T("Repetir el test")}</button></div></div>`;
        ir(pasos.length - 1);
      }
      if (e.target.closest("[data-reinicio]")) { Object.keys(punt).forEach((k) => delete punt[k]); i = 0; ir(0); }
    });
    ir(0);
  }

  /* ---------- Configurador de eventos ---------- */
  const fe = $("#form-evento2");
  if (fe) {
    const r = $("input[type=range]", fe), out = $("output", fe);
    const upd = () => (out.textContent = r.value + (r.value == r.max ? "+" : ""));
    r.addEventListener("input", upd); upd();
    fe.addEventListener("submit", (e) => {
      e.preventDefault();
      const f = new FormData(fe);
      const boc = f.getAll("bocaditos");
      const fecha = f.get("fecha") ? new Date(f.get("fecha") + "T12:00").toLocaleDateString(LOCALE, { weekday: "long", day: "numeric", month: "long" }) : T("por definir");
      const msg = T("¡Mba'éichapa, Loren! Quiero organizar un evento:") + `\n\n• ${T("Nombre")}: ${f.get("nombre")}\n• ${T("Tipo")}: ${f.get("tipo")}\n• ${T("Personas")}: ${f.get("personas")}\n• ${T("Fecha")}: ${fecha}\n• ${T("Formato")}: ${f.get("formato")}\n${boc.length ? "• " + T("Me apetece") + ": " + boc.join(", ") + "\n" : ""}${f.get("presupuesto") ? "• " + T("Presupuesto aprox.") + ": " + f.get("presupuesto") + "\n" : ""}${f.get("mensaje") ? "• " + T("Detalles") + ": " + f.get("mensaje") + "\n" : ""}\n${T("¡Gracias!")}`;
      window.open(wa(msg), "_blank", "noopener");
    });
  }

  /* ---------- Formulario de reserva ---------- */
  const fr = $("#form-reserva");
  if (fr) {
    const fecha = $("input[name=fecha]", fr);
    if (fecha) fecha.min = new Date().toISOString().slice(0, 10);
    fr.addEventListener("submit", (e) => {
      e.preventDefault();
      const f = new FormData(fr);
      const d = f.get("fecha") ? new Date(f.get("fecha") + "T12:00").toLocaleDateString(LOCALE, { weekday: "long", day: "numeric", month: "long" }) : "";
      const msg = T("¡Hola Loren! Me gustaría reservar mesa 🙂") + `\n• ${T("Nombre")}: ${f.get("nombre")}\n• ${T("Día")}: ${d}\n• ${T("Hora")}: ${f.get("hora")}\n• ${T("Personas")}: ${f.get("personas")}\n• ${T("Zona")}: ${f.get("zona")}\n${f.get("nota") ? "• " + T("Nota") + ": " + f.get("nota") : ""}`;
      window.open(wa(msg), "_blank", "noopener");
    });
  }

  /* ---------- Semana en barras ---------- */
  const sem = $(".semana");
  if (sem) {
    const H = L.horario, ini = 8, fin = 25, rango = fin - ini;
    const now = new Date(), hoy = now.getDay(), ahora = now.getHours() + now.getMinutes() / 60;
    const f = (h) => { const hh = Math.floor(h) % 24, mm = Math.round((h % 1) * 60); return String(hh).padStart(2, "0") + ":" + String(mm).padStart(2, "0"); };
    sem.innerHTML = [1, 2, 3, 4, 5, 6, 0].map((k) => {
      const d = H[k], l = ((d.abre - ini) / rango) * 100, w = ((d.cierra - d.abre) / rango) * 100;
      const marca = k === hoy && ahora >= ini ? `<span class="ahora" style="left:${((ahora - ini) / rango) * 100}%"></span>` : "";
      return `<div class="dia ${k === hoy ? "hoy" : ""}"><b>${T(d.dia)}${k === hoy ? " · " + T("hoy") : ""}</b><div class="dia__barra"><i style="left:${l}%;width:${w}%"></i>${marca}</div><span>${f(d.abre)} – ${f(d.cierra)}</span></div>`;
    }).join("") + `<div class="horas-eje"><span></span><div><span>8h</span><span>12h</span><span>16h</span><span>20h</span><span>24h</span></div><span></span></div>`;
  }
})();
