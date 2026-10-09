/* =========================================================
   LOREN RESTOBAR · Estructura común (nav, menú móvil, pie,
   flotantes, modal de pedido y visor de fotos)
   Se inyecta en #shell-top y #shell-bottom de cada página.
   ========================================================= */
(function () {
  const pagina = document.body.dataset.page || "inicio";
  const P = window.PREF || "", L = window.IDIOMA || "es";
  const archivo = (pagina === "inicio" ? "index" : pagina === "carta-clasica" ? "carta-clasica" : pagina) + ".html";
  const IDIOMAS = [["es", "ES", "Español", ""], ["ca", "CA", "Català", "ca/"], ["en", "EN", "English", "en/"]];
  const selector = (cls) => `<div class="idiomas ${cls}" role="group" aria-label="Idioma / Language">${IDIOMAS.map(([c, t, n, pre]) => `<a href="${pre}${archivo}" hreflang="${c}" lang="${c}" title="${n}" class="${c === L ? "on" : ""}" ${c === L ? 'aria-current="true"' : ""}>${t}</a>`).join("")}</div>`;
  const PAGS = [
    { id: "historia", url: P + "historia.html", txt: T("Nuestra historia"), gn: "Loren" },
    { id: "sabores", url: P + "sabores.html", txt: T("Sabores"), gn: T("de Paraguay") },
    { id: "carta", url: P + "carta.html", txt: T("Carta"), gn: "tembi'u" },
    { id: "domicilio", url: P + "domicilio.html", txt: T("A domicilio"), gn: "jaha!" },
    { id: "eventos", url: P + "eventos.html", txt: T("Eventos"), gn: "vy'a" },
    { id: "visitanos", url: P + "visitanos.html", txt: T("Visítanos"), gn: "eju!" }
  ];
  const ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';
  const WA = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15l-1.4 5 5.1-1.3A10 10 0 1 0 12 2zm5.3 14c-.2.6-1.3 1.2-1.8 1.3-.5 0-1 .3-3.4-.7-2.9-1.2-4.7-4.1-4.8-4.3-.1-.2-1.1-1.5-1.1-2.9s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 2c.1.1.1.3 0 .5l-.3.5-.4.4c-.1.2-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.1 1 2 1.3 2.3 1.4.3.1.5.1.6-.1l.9-1.1c.2-.3.4-.2.7-.1l1.9.9c.3.1.5.2.5.3.1.2.1.7-.1 1.3z"/></svg>';
  const X = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>';
  const IG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>';
  const TT = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M16.6 5.8A4.3 4.3 0 0 1 15.5 3h-3.1v12.4a2.6 2.6 0 1 1-2.6-2.6c.3 0 .5 0 .8.1V9.7a5.7 5.7 0 1 0 4.9 5.7V9a7.4 7.4 0 0 0 4.3 1.4V7.3a4.3 4.3 0 0 1-3.2-1.5z"/></svg>';
  const FB = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M14 8h3V4h-3c-2.8 0-4 1.7-4 4.3V10H7v4h3v8h4v-8h3l1-4h-4V8.6c0-.4.3-.6.7-.6z"/></svg>';

  const top = `
<header class="nav">
  <div class="wrap">
    <a href="${P}index.html" class="nav__logo" aria-label="${T("Loren Restobar, inicio")}"><img src="img/marca/logo-loren.webp" alt="Loren Restobar"></a>
    <ul class="nav__links">
      ${PAGS.map((p) => `<li><a href="${p.url}" class="${p.id === pagina ? "is-active" : ""}" ${p.id === pagina ? 'aria-current="page"' : ""}>${p.txt}</a></li>`).join("")}
    </ul>
    <div class="nav__cta">
      <a href="#" class="btn btn--ghost btn--sm" data-pedir>${T("Pedir a casa")}</a>
      <a href="#" class="btn btn--sm" data-reserva>${T("Reservar")}</a>
    </div>
    ${selector("idiomas--nav")}
    <button class="nav__burger" aria-label="${T("Abrir menú")}"><span></span></button>
  </div>
</header>
<nav class="drawer" aria-label="${T("Menú móvil")}">
  <div class="nanduti-bg" data-nanduti></div>
  <a class="drawer__link" href="${P}index.html">${T("Inicio")} <small>Mba'éichapa</small></a>
  ${PAGS.map((p) => `<a class="drawer__link" href="${p.url}">${p.txt} <small>${p.gn}</small></a>`).join("")}
  ${selector("idiomas--drawer")}
  <div class="drawer__foot">
    <a href="#" class="btn" data-reserva>${T("Reservar mesa")}</a>
    <a href="${P}carta-clasica.html" class="btn btn--ghost">${T("Carta para imprimir")}</a>
  </div>
</nav>`;

  const bottom = `
<footer class="pie">
  <div class="nanduti-bg" data-nanduti></div>
  <div class="wrap">
    <p class="pie__grande">Aguyje<span>!</span></p>
    <p class="pie__sub">${T("«Gracias» en guaraní. Por venir, por pedir, por volver.")}</p>
    <div class="pie__cols">
      <div>
        <img class="pie__logo" src="img/marca/logo-loren.webp" alt="Loren Restobar">
        <p>${T("Cocina paraguaya y española casera en el corazón de Sant Martí. Un pedacito de Paraguay en Barcelona.")}</p>
        <div class="sociales">
          <a href="#" data-link="instagram" target="_blank" rel="noopener" aria-label="Instagram">${IG}</a>
          <a href="#" data-link="tiktok" target="_blank" rel="noopener" aria-label="TikTok">${TT}</a>
          <a href="#" data-link="facebook" target="_blank" rel="noopener" aria-label="Facebook">${FB}</a>
          <a href="#" data-link="whatsapp" target="_blank" rel="noopener" aria-label="WhatsApp">${WA}</a>
        </div>
      </div>
      <div><h4>${T("Explora")}</h4><ul>
        <li><a href="${P}historia.html">${T("Nuestra historia")}</a></li><li><a href="${P}sabores.html">${T("Sabores de Paraguay")}</a></li>
        <li><a href="${P}carta.html">${T("La carta")}</a></li><li><a href="${P}carta-clasica.html">${T("Carta para imprimir")}</a></li>
        <li><a href="${P}eventos.html">${T("Eventos y catering")}</a></li></ul></div>
      <div><h4>${T("Pide")}</h4><ul>
        <li><a href="${P}domicilio.html">${T("Cómo pedir a domicilio")}</a></li>
        <li><a href="#" data-link="glovo" target="_blank" rel="noopener">Glovo</a></li><li><a href="#" data-link="uber" target="_blank" rel="noopener">Uber Eats</a></li>
        <li><a href="#" data-reserva>${T("Reservar por WhatsApp")}</a></li><li><a href="#" data-link="opentable" target="_blank" rel="noopener">${T("Reservar en OpenTable")}</a></li></ul></div>
      <div><h4>${T("Contacto")}</h4><ul>
        <li><a href="${P}visitanos.html">Carrer de la Muntanya, 115</a></li><li>08026 Barcelona</li>
        <li><a href="tel:+34602076828">602 07 68 28</a></li><li><a href="mailto:lorenza_vera@hotmail.com">lorenza_vera@hotmail.com</a></li></ul></div>
    </div>
    <div class="pie__legal"><span>© <span data-anio>2026</span> Loren Restobar · ${T("Hecho con ❤️ y mucha chipa")}</span><span><i class="bandera"></i> Paraguay · Barcelona <i class="bandera bandera--es"></i></span></div>
  </div>
</footer>

<a class="wa-flot" href="#" data-reserva aria-label="${T("Escríbenos por WhatsApp")}">${WA}<span class="bocadillo">Mba'éichapa! ${T("¿Te reservamos mesa?")} <i class="bandera"></i></span></a>

<nav class="barra-movil" aria-label="${T("Acciones rápidas")}">
  <a href="#" data-reserva><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="3" y="5" width="18" height="16" rx="3"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>${T("Reservar")}</a>
  <a href="${P}carta.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 3h11l3 3v15H5z"/><path d="M9 9h6M9 13h6M9 17h4"/></svg>${T("Carta")}</a>
  <button class="dest" data-pedir><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 18a2 2 0 1 0 4 0 2 2 0 0 0-4 0zM15 18a2 2 0 1 0 4 0 2 2 0 0 0-4 0zM7 18H4V8h9v10h-4M13 11h4l3 4v3h-1"/></svg>${T("Pedir")}</button>
  <a href="tel:+34602076828"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>${T("Llamar")}</a>
</nav>

<div class="modal" id="modal-pedir" role="dialog" aria-modal="true" aria-labelledby="modal-tit">
  <div class="modal__caja">
    <div class="nanduti-bg" data-nanduti></div>
    <button class="modal__x" aria-label="${T("Cerrar")}">${X}</button>
    <h3 id="modal-tit">${T("¿Cómo lo quieres?")}</h3>
    <p>${T("Elige tu app y en minutos tienes Paraguay en la mesa.")}</p>
    <div class="modal__opts">
      <a class="btn btn--glovo" href="#" data-link="glovo" target="_blank" rel="noopener">${T("Pedir en Glovo")} ${ARROW}</a>
      <a class="btn btn--uber" href="#" data-link="uber" target="_blank" rel="noopener">${T("Pedir en Uber Eats")} ${ARROW}</a>
      <a class="btn btn--wa" href="#" data-wa-recoger target="_blank" rel="noopener">${T("Recoger en local (WhatsApp)")} ${ARROW}</a>
    </div>
    <p style="margin:16px 0 0;font-size:.85rem"><a href="${P}domicilio.html" style="color:var(--vino);font-weight:700">${T("¿Dudas? Todo sobre el reparto →")}</a></p>
  </div>
</div>

<div class="lightbox" aria-hidden="true">
  <button class="lb-cerrar" aria-label="${T("Cerrar")}">${X}</button>
  <button class="lb-prev" aria-label="${T("Anterior")}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M15 6l-6 6 6 6"/></svg></button>
  <figure><img src="" alt=""><figcaption></figcaption></figure>
  <button class="lb-next" aria-label="${T("Siguiente")}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M9 6l6 6-6 6"/></svg></button>
</div>`;

  const t = document.getElementById("shell-top"), b = document.getElementById("shell-bottom");
  if (t) t.outerHTML = top;
  if (b) b.outerHTML = bottom;
  window.LOREN_ICO = { ARROW, WA, X };
})();
