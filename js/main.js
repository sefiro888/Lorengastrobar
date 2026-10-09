/* =========================================================
   LOREN RESTOBAR · Interacciones
   ========================================================= */
(function () {
  const L = window.LOREN;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const euro = (n) => n.toFixed(2).replace(".", ",") + " €";
  const wa = (txt) => `${L.links.whatsapp}?text=${encodeURIComponent(txt)}`;

  const ICO = {
    flecha: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    wa: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.5 14.4c-.3-.1-1.7-.8-2-.9-.3-.1-.5-.1-.7.1-.2.3-.8.9-.9 1.1-.2.2-.3.2-.6.1-.3-.1-1.2-.5-2.3-1.4-.9-.8-1.4-1.7-1.6-2-.2-.3 0-.5.1-.6l.4-.5c.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.7-.7 2-1.4.2-.7.2-1.2.2-1.4-.1-.1-.3-.2-.6-.3zM12 21.8c-1.8 0-3.5-.5-5-1.4l-.4-.2-3.7 1 1-3.6-.2-.4C2.7 15.6 2.2 13.8 2.2 12 2.2 6.6 6.6 2.2 12 2.2c2.6 0 5.1 1 6.9 2.9 1.8 1.8 2.9 4.3 2.9 6.9 0 5.4-4.4 9.8-9.8 9.8zM20.5 3.5C18.2 1.2 15.2 0 12 0 5.4 0 0 5.4 0 12c0 2.1.6 4.2 1.6 6L0 24l6.2-1.6c1.8 1 3.8 1.5 5.8 1.5 6.6 0 12-5.4 12-12 0-3.2-1.2-6.2-3.5-8.4z"/></svg>',
    x: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>'
  };

  /* ---------- Enlaces internos (#) — necesario en /ca/ y /en/ por la etiqueta <base> ---------- */
  document.addEventListener("click", (e) => {
    const a = e.target.closest('a[href^="#"]');
    if (!a) return;
    const h = a.getAttribute("href");
    if (h.length < 2) return;
    const dest = document.getElementById(decodeURIComponent(h.slice(1)));
    if (!dest) return;
    e.preventDefault();
    dest.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" });
    history.replaceState(null, "", location.pathname + location.search + h);
  });

  /* ---------- Loader ---------- */
  const loader = $(".loader");
  const quitarLoader = () => loader && loader.classList.add("is-done");
  window.addEventListener("load", () => setTimeout(quitarLoader, 900));
  setTimeout(quitarLoader, 2600);

  /* ---------- Nav ---------- */
  const nav = $(".nav");
  const barra = $(".barra-movil");
  const hero = $(".hero");
  const onScroll = () => {
    const y = window.scrollY;
    nav.classList.toggle("is-scrolled", y > 40);
    if (barra) barra.classList.toggle("is-on", y > (hero ? hero.offsetHeight * 0.7 : 400));
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  $(".nav__burger")?.addEventListener("click", () => document.body.classList.toggle("menu-open"));
  $$(".drawer a").forEach((a) => a.addEventListener("click", () => document.body.classList.remove("menu-open")));
  $$(".drawer a.drawer__link").forEach((a, i) => (a.style.transitionDelay = 0.15 + i * 0.05 + "s"));

  // enlace activo
  const enlaces = $$(".nav__links a[href^='#']");
  const obsNav = new IntersectionObserver((ents) => {
    ents.forEach((e) => {
      if (e.isIntersecting) enlaces.forEach((a) => a.classList.toggle("is-active", a.getAttribute("href") === "#" + e.target.id));
    });
  }, { rootMargin: "-45% 0px -50% 0px" });
  $$("main section[id]").forEach((s) => obsNav.observe(s));

  /* ---------- Plato giratorio del hero ---------- */
  const platos = [
    { img: "img/platos/caldo-gallina.webp", nom: "Vorí vorí", sub: T("Caldo de gallina casera · finde") },
    { img: "img/platos/mila-caballo-pro.webp", nom: T("Milanesa a caballo"), sub: T("Dos huevos y patatas") },
    { img: "img/platos/mbeju-queso.webp", nom: T("Mbejú con queso"), sub: T("Almidón de mandioca") },
    { img: "img/platos/parrillada-mixta.webp", nom: T("Parrillada"), sub: T("A la brasa, en hierro") },
    { img: "img/platos/mila-americana-pro.webp", nom: T("Milanesa americana"), sub: T("Bacon, queso y huevo") },
    { img: "img/platos/noquis.webp", nom: T("Ñoquis de ternera"), sub: T("Pasta casera") }
  ];
  const fotos = $(".plato__fotos");
  if (fotos) {
    fotos.innerHTML = platos.map((p, i) => `<img src="${p.img}" alt="${p.nom}" ${i ? 'loading="lazy"' : ""}>`).join("");
    const imgs = $$("img", fotos);
    const num = $(".plato__etiqueta .num"), nom = $(".plato__etiqueta b"), sub = $(".plato__etiqueta small"), txt = $(".plato__etiqueta .txt");
    let i = 0;
    const mostrar = (n) => {
      imgs.forEach((im, k) => im.classList.toggle("is-on", k === n));
      txt.style.opacity = 0;
      setTimeout(() => {
        num.textContent = String(n + 1).padStart(2, "0");
        nom.textContent = platos[n].nom;
        sub.textContent = platos[n].sub;
        txt.style.opacity = 1;
      }, 250);
    };
    mostrar(0);
    if (!reduce) setInterval(() => { i = (i + 1) % platos.length; mostrar(i); }, 3800);
  }

  /* ---------- Brasas (canvas) ---------- */
  const cv = $("#brasas");
  if (cv && !reduce) {
    const ctx = cv.getContext("2d");
    let W, H, dpr, chispas = [];
    const size = () => {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = cv.offsetWidth; H = cv.offsetHeight;
      cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    };
    size(); window.addEventListener("resize", size);
    const N = window.innerWidth < 700 ? 34 : 70;
    const nueva = (inicio) => ({
      x: Math.random() * W, y: inicio ? Math.random() * H : H + 10,
      r: Math.random() * 2.2 + 0.6, v: Math.random() * 0.7 + 0.25,
      w: Math.random() * 2 * Math.PI, ws: Math.random() * 0.03 + 0.008,
      vida: Math.random() * 0.6 + 0.4, hue: 18 + Math.random() * 30
    });
    for (let k = 0; k < N; k++) chispas.push(nueva(true));
    let visible = true;
    new IntersectionObserver(([e]) => (visible = e.isIntersecting)).observe(cv);
    const tick = () => {
      if (visible) {
        ctx.clearRect(0, 0, W, H);
        ctx.globalCompositeOperation = "lighter";
        chispas.forEach((c, k) => {
          c.y -= c.v; c.w += c.ws; c.x += Math.sin(c.w) * 0.5;
          const a = Math.max(0, Math.min(1, c.y / H)) * c.vida;
          const g = ctx.createRadialGradient(c.x, c.y, 0, c.x, c.y, c.r * 4);
          g.addColorStop(0, `hsla(${c.hue},100%,70%,${a})`);
          g.addColorStop(1, `hsla(${c.hue},100%,50%,0)`);
          ctx.fillStyle = g; ctx.beginPath(); ctx.arc(c.x, c.y, c.r * 4, 0, Math.PI * 2); ctx.fill();
          if (c.y < -10) chispas[k] = nueva(false);
        });
      }
      requestAnimationFrame(tick);
    };
    tick();
  }

  /* ---------- Reveal + contadores ---------- */
  const obs = new IntersectionObserver((ents) => {
    ents.forEach((e) => {
      if (!e.isIntersecting) return;
      e.target.classList.add("is-in");
      if (e.target.dataset.count) contar(e.target);
      obs.unobserve(e.target);
    });
  }, { threshold: 0.15, rootMargin: "0px 0px -40px 0px" });
  $$(".rv, [data-count]").forEach((el) => obs.observe(el));

  function contar(el) {
    const fin = parseFloat(el.dataset.count), dec = (el.dataset.count.split(".")[1] || "").length;
    const pre = el.dataset.pre || "", suf = el.dataset.suf || "";
    const t0 = performance.now(), dur = 1800;
    const paso = (t) => {
      const p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 4);
      const num = (fin * e).toFixed(dec);
      el.textContent = pre + (window.IDIOMA === "en" ? num : num.replace(".", ",")) + suf;
      if (p < 1) requestAnimationFrame(paso);
    };
    requestAnimationFrame(paso);
  }

  /* ---------- Tarjetas sabores (tap en móvil) ---------- */
  $$(".sabor").forEach((s) => {
    s.addEventListener("click", () => s.classList.toggle("is-flip"));
    s.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); s.classList.toggle("is-flip"); } });
  });

  /* ---------- Horario: abierto ahora ---------- */
  const H = L.horario;
  const fmt = (h) => {
    const hh = Math.floor(h) % 24, mm = Math.round((h % 1) * 60);
    return String(hh).padStart(2, "0") + ":" + String(mm).padStart(2, "0");
  };
  function estadoAhora() {
    const d = new Date(), dia = d.getDay(), h = d.getHours() + d.getMinutes() / 60;
    const hoy = H[dia], ayer = H[(dia + 6) % 7];
    if (ayer.cierra > 24 && h < ayer.cierra - 24) return { abierto: true, hasta: ayer.cierra };
    if (h >= hoy.abre && h < hoy.cierra) return { abierto: true, hasta: hoy.cierra };
    // próxima apertura
    if (h < hoy.abre) return { abierto: false, abre: T("hoy a las {h}", { h: fmt(hoy.abre) }) };
    const man = H[(dia + 1) % 7];
    return { abierto: false, abre: T("mañana a las {h}", { h: fmt(man.abre) }) };
  }
  const lista = $(".horario");
  if (lista) {
    const hoyIdx = new Date().getDay();
    const orden = [1, 2, 3, 4, 5, 6, 0];
    lista.innerHTML = orden.map((k) => `<li class="${k === hoyIdx ? "is-hoy" : ""}"><span>${T(H[k].dia)}${k === hoyIdx ? " · " + T("hoy") : ""}</span><span>${fmt(H[k].abre)} – ${fmt(H[k].cierra)}</span></li>`).join("");
  }
  const pintarEstado = () => {
    const e = estadoAhora();
    $$("[data-estado]").forEach((el) => {
      el.className = "estado " + (e.abierto ? "estado--abierto" : "estado--cerrado");
      el.innerHTML = e.abierto ? `<i></i> ${T("Abierto ahora · hasta las {h}", { h: fmt(e.hasta) })}` : `<i></i> ${T("Cerrado · abrimos {x}", { x: e.abre })}`;
    });
  };
  pintarEstado(); setInterval(pintarEstado, 60000);

  /* ---------- Cuenta atrás del finde (sábado 10:00 – domingo 17:00) ---------- */
  const cuenta = $(".finde__cuenta");
  if (cuenta) {
    const est = $(".finde__estado span");
    const tick = () => {
      const now = new Date(), dia = now.getDay(), h = now.getHours() + now.getMinutes() / 60;
      const enFinde = (dia === 6 && h >= 10) || (dia === 0 && h < 17);
      if (enFinde) {
        est.textContent = T("¡Es finde! Hoy hay vorí vorí y pira caldo");
        cuenta.innerHTML = `<div><b>🍲</b><span>${T("en la olla")}</span></div><div><b>${T(dia === 6 ? "Sáb" : "Dom")}</b><span>${T("hoy")}</span></div>`;
        return;
      }
      const obj = new Date(now);
      obj.setDate(now.getDate() + ((6 - dia + 7) % 7));
      obj.setHours(10, 0, 0, 0);
      if (obj <= now) obj.setDate(obj.getDate() + 7);
      let s = Math.floor((obj - now) / 1000);
      const D = Math.floor(s / 86400); s -= D * 86400;
      const Hh = Math.floor(s / 3600); s -= Hh * 3600;
      const M = Math.floor(s / 60); s -= M * 60;
      est.textContent = T("Cuenta atrás para el próximo vorí vorí");
      cuenta.innerHTML = [[D, T("días")], [Hh, T("horas")], [M, T("min")], [s, T("seg")]].map(([v, l]) => `<div><b>${String(v).padStart(2, "0")}</b><span>${l}</span></div>`).join("");
    };
    tick(); setInterval(tick, 1000);
  }

  /* ---------- Carta interactiva ---------- */
  const CATS = window.CATEGORIAS, CARTA = window.CARTA;
  const cont = $("#carta-lista");
  const tabsEl = $(".carta__tabs");
  const buscador = $("#buscar-plato");
  let catSel = "todo", filtro = null, q = "";
  const TAGS = { py: "Típico paraguayo", top: "Favorito", comp: "Para compartir", sintrigo: "Sin trigo*", finde: "Sólo finde" };
  const tagCls = { py: "tag--py", top: "tag--top", finde: "tag--finde" };
  const norm = (s) => s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");

  if (tabsEl) {
    tabsEl.innerHTML = `<button class="tab is-on" data-cat="todo">Toda la carta <span class="cnt">${CARTA.length}</span></button>` +
      CATS.map((c) => `<button class="tab" data-cat="${c.id}">${c.nombre} <span class="cnt">${CARTA.filter((p) => p.cat === c.id).length}</span></button>`).join("");
    tabsEl.addEventListener("click", (e) => {
      const b = e.target.closest(".tab"); if (!b) return;
      catSel = b.dataset.cat;
      $$(".tab", tabsEl).forEach((t) => t.classList.toggle("is-on", t === b));
      b.scrollIntoView({ behavior: "smooth", inline: "center", block: "nearest" });
      render();
    });
  }
  $$(".chip[data-tag]").forEach((c) => c.addEventListener("click", () => {
    filtro = filtro === c.dataset.tag ? null : c.dataset.tag;
    $$(".chip[data-tag]").forEach((x) => x.classList.toggle("is-on", x.dataset.tag === filtro));
    render();
  }));
  buscador?.addEventListener("input", () => { q = norm(buscador.value.trim()); render(); });

  function tarjeta(p, idx) {
    const tags = (p.tags || []).filter((t) => t !== "sintrigo" || true).slice(0, 3)
      .map((t) => `<span class="tag ${tagCls[t] || ""}">${TAGS[t]}</span>`).join("");
    const img = p.img
      ? `<div class="plato-card__img" data-lb="${p.img}" data-cap="${p.nombre}"><img src="${p.img}" alt="${p.nombre}" loading="lazy"><div class="plato-card__tags">${tags}</div></div>`
      : `<div class="plato-card__img plato-card__img--vacio">${window.nanduti({ sw: 0.8 })}<span>${p.nombre}</span><div class="plato-card__tags">${tags}</div></div>`;
    const precio = p.precio == null ? `<span class="precio precio--consultar">Consultar</span>` : `<span class="precio">${euro(p.precio)}</span>`;
    const acc = p.cat === "finde" || p.precio == null
      ? `<a class="w" href="${wa(`¡Hola Loren! ¿Este finde tenéis ${p.nombre}? Quería reservar.`)}" target="_blank" rel="noopener">${ICO.wa} Reservar</a>`
      : `<a class="g" href="${L.links.glovo}" target="_blank" rel="noopener">Glovo</a><a class="u" href="${L.links.uber}" target="_blank" rel="noopener">Uber Eats</a>`;
    return `<article class="plato-card" style="animation-delay:${Math.min(idx, 8) * 0.04}s">${img}
      <div class="plato-card__body">
        <div class="plato-card__top"><h4>${p.nombre}</h4>${precio}</div>
        ${p.gn ? `<div class="plato-card__gn">${p.gn}</div>` : ""}
        <p class="plato-card__desc">${p.desc}</p>
        <div class="plato-card__acc">${acc}</div>
      </div></article>`;
  }

  function render() {
    if (!cont) return;
    const lista = CARTA.filter((p) =>
      (catSel === "todo" || p.cat === catSel) &&
      (!filtro || (p.tags || []).includes(filtro)) &&
      (!q || norm(p.nombre + " " + p.desc + " " + (p.gn || "")).includes(q))
    );
    const grupos = CATS.filter((c) => lista.some((p) => p.cat === c.id));
    cont.innerHTML = grupos.map((c) => {
      const items = lista.filter((p) => p.cat === c.id);
      return `<div class="carta__grupo" id="cat-${c.id}">
        <div class="carta__grupo-cab"><h3>${c.nombre}</h3><p>${c.sub}</p>${c.gn ? `<span class="gn">${c.gn}</span>` : ""}</div>
        ${c.id === "bebidas"
          ? `<div class="carta__lista">${items.map((p) => `<div class="carta__fila"><b>${p.nombre}</b><small>${p.desc}</small><span class="precio">${euro(p.precio)}</span></div>`).join("")}</div>`
          : `<div class="carta__grid">${items.map(tarjeta).join("")}</div>`}</div>`;
    }).join("");
    $(".carta__vacio").style.display = lista.length ? "none" : "block";
  }
  render();

  /* ---------- Lightbox ---------- */
  const lb = $(".lightbox");
  let lbLista = [], lbI = 0;
  const lbImg = $("img", lb), lbCap = $("figcaption", lb);
  const lbVer = (i) => {
    lbI = (i + lbLista.length) % lbLista.length;
    lbImg.src = lbLista[lbI].src; lbImg.alt = lbLista[lbI].cap; lbCap.textContent = lbLista[lbI].cap;
  };
  document.addEventListener("click", (e) => {
    const t = e.target.closest("[data-lb]");
    if (!t) return;
    e.preventDefault();
    const grupo = t.closest("[data-lb-grupo]") || document;
    const items = $$("[data-lb]", grupo);
    lbLista = items.map((x) => ({ src: x.dataset.lb, cap: x.dataset.cap || "" }));
    lbVer(items.indexOf(t));
    lb.classList.add("is-open");
  });
  const lbCerrar = () => lb.classList.remove("is-open");
  $(".lb-cerrar", lb).addEventListener("click", lbCerrar);
  $(".lb-prev", lb).addEventListener("click", () => lbVer(lbI - 1));
  $(".lb-next", lb).addEventListener("click", () => lbVer(lbI + 1));
  lb.addEventListener("click", (e) => { if (e.target === lb) lbCerrar(); });

  /* ---------- Modal pedir ---------- */
  const modal = $("#modal-pedir");
  const abrirModal = (e) => { e.preventDefault(); modal.classList.add("is-open"); };
  const cerrarModal = () => modal.classList.remove("is-open");
  $$("[data-pedir]").forEach((b) => b.addEventListener("click", abrirModal));
  $(".modal__x", modal)?.addEventListener("click", cerrarModal);
  modal?.addEventListener("click", (e) => { if (e.target === modal) cerrarModal(); });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") { lbCerrar(); cerrarModal(); document.body.classList.remove("menu-open"); }
    if (lb.classList.contains("is-open")) {
      if (e.key === "ArrowRight") lbVer(lbI + 1);
      if (e.key === "ArrowLeft") lbVer(lbI - 1);
    }
  });

  /* ---------- Formulario de eventos → WhatsApp ---------- */
  const form = $("#form-evento");
  form?.addEventListener("submit", (e) => {
    e.preventDefault();
    const f = new FormData(form);
    const fecha = f.get("fecha") ? new Date(f.get("fecha") + "T12:00").toLocaleDateString(LOCALE, { weekday: "long", day: "numeric", month: "long" }) : T("por definir");
    const msg = T("¡Mba'éichapa, Loren! Me gustaría organizar un evento:") + `\n\n• ${T("Nombre")}: ${f.get("nombre")}\n• ${T("Tipo")}: ${f.get("tipo")}\n• ${T("Personas")}: ${f.get("personas")}\n• ${T("Fecha")}: ${fecha}\n• ${T("Formato")}: ${f.get("formato")}\n${f.get("mensaje") ? "• " + T("Detalles") + ": " + f.get("mensaje") + "\n" : ""}\n${T("¡Gracias!")}`;
    window.open(wa(msg), "_blank", "noopener");
  });

  /* ---------- Enlaces centralizados ---------- */
  $$("[data-link]").forEach((a) => { const u = L.links[a.dataset.link]; if (u) a.href = u; });
  $$("[data-wa-recoger]").forEach((a) => (a.href = wa(T("¡Hola Loren! Quería encargar para recoger en el local:") + "\n• \n• \n" + T("Hora aproximada de recogida:") + " ")));

  /* ---------- Reserva rápida ---------- */
  $$("[data-reserva]").forEach((a) => {
    a.href = wa(T("¡Hola Loren! Me gustaría reservar una mesa 🙂") + "\n• " + T("Día") + ": \n• " + T("Hora") + ": \n• " + T("Personas") + ": ");
    a.target = "_blank"; a.rel = "noopener";
  });

  /* ---------- Bocadillo WhatsApp ---------- */
  const wf = $(".wa-flot");
  if (wf) {
    setTimeout(() => wf.classList.add("is-hola"), 7000);
    setTimeout(() => wf.classList.remove("is-hola"), 14000);
  }

  /* ---------- Vídeo: reproducir sólo cuando se ve ---------- */
  $$("video[data-auto]").forEach((v) => {
    new IntersectionObserver(([e]) => { e.isIntersecting ? v.play().catch(() => {}) : v.pause(); }, { threshold: 0.3 }).observe(v);
  });

  /* ---------- Año footer ---------- */
  $$("[data-anio]").forEach((el) => (el.textContent = new Date().getFullYear()));
})();
