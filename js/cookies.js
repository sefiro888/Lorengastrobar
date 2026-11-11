/* =========================================================
   LOREN RESTOBAR · Aviso de cookies y servicios de terceros
   - Nada de terceros se carga sin permiso: el mapa de Google Maps
     (iframe con data-src) espera a que el visitante acepte.
   - «Aceptar» y «Rechazar» con el mismo peso; se puede cambiar
     en cualquier momento desde «Configurar cookies» (pie de página).
   - La elección se guarda en el navegador 12 meses (es técnica, no necesita permiso).
   ========================================================= */
(function () {
  const T = window.T || ((s) => s), P = window.PREF || "";
  const CLAVE = "loren-cookies", VERSION = 1, DURA = 365 * 24 * 3600 * 1000;

  const leer = () => {
    try {
      const d = JSON.parse(localStorage.getItem(CLAVE) || "null");
      if (d && d.v === VERSION && Date.now() - d.fecha < DURA) return d;
    } catch (e) {}
    return null;
  };
  const guardar = (mapas) => {
    try { localStorage.setItem(CLAVE, JSON.stringify({ v: VERSION, fecha: Date.now(), mapas })); } catch (e) {}
  };

  /* ---------- Mapas de Google: bloqueados hasta tener permiso ---------- */
  const mapas = [...document.querySelectorAll("iframe[data-src]")];
  const cargarMapas = () => mapas.forEach((f) => {
    if (!f.src) f.src = f.dataset.src;
    const caja = f.parentElement.querySelector(".mapa__bloqueo");
    if (caja) caja.remove();
  });
  mapas.forEach((f) => {
    const caja = document.createElement("div");
    caja.className = "mapa__bloqueo";
    caja.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.6"/></svg>
      <b>${T("Mapa de Google Maps")}</b>
      <p>${T("Al cargarlo, Google puede usar cookies y recibir datos de tu navegación.")}</p>
      <button type="button" class="btn btn--sm">${T("Ver el mapa")}</button>
      <a href="#" data-cookies-config>${T("Configurar cookies")}</a>`;
    caja.querySelector("button").addEventListener("click", () => { guardar(true); cargarMapas(); ocultar(); });
    f.parentElement.insertBefore(caja, f.nextSibling);
  });

  /* ---------- Aviso ---------- */
  const aviso = document.createElement("div");
  aviso.className = "cookies";
  aviso.setAttribute("role", "dialog");
  aviso.setAttribute("aria-label", T("Aviso de cookies"));
  aviso.innerHTML = `<div class="cookies__caja">
    <div class="cookies__txt">
      <b>${T("Usamos cookies de terceros")} 🍪</b>
      <p>${T("Esta web no usa cookies propias de publicidad ni de analítica. Sólo el mapa de Google Maps usa cookies de Google, y únicamente si lo aceptas.")} <a href="${P}aviso-legal.html#cookies">${T("Política de cookies")}</a></p>
      <label class="cookies__op" hidden><input type="checkbox" checked disabled> <span><b>${T("Necesarias")}</b> · ${T("recordar tu elección de cookies y los platos que apuntas en la carta. Siempre activas.")}</span></label>
      <label class="cookies__op" hidden><input type="checkbox" data-op="mapas"> <span><b>${T("Mapas (Google Maps)")}</b> · ${T("ver el mapa del local dentro de la web.")}</span></label>
    </div>
    <div class="cookies__btns">
      <button type="button" class="btn btn--sm" data-c="aceptar">${T("Aceptar")}</button>
      <button type="button" class="btn btn--sm" data-c="rechazar">${T("Rechazar")}</button>
      <button type="button" class="cookies__conf" data-c="configurar">${T("Configurar")}</button>
      <button type="button" class="btn btn--sm" data-c="guardar" hidden>${T("Guardar mi elección")}</button>
    </div>
  </div>`;
  document.body.appendChild(aviso);
  const $ = (s) => aviso.querySelector(s);
  const mostrar = (config) => {
    const d = leer();
    $("[data-op=mapas]").checked = !!(d && d.mapas);
    aviso.querySelectorAll(".cookies__op").forEach((l) => (l.hidden = !config));
    $("[data-c=configurar]").hidden = !!config;
    $("[data-c=guardar]").hidden = !config;
    aviso.classList.add("is-on");
  };
  const ocultar = () => aviso.classList.remove("is-on");
  const decidir = (mapasOk) => {
    const antes = leer();
    guardar(mapasOk);
    ocultar();
    if (mapasOk) cargarMapas();
    else if (antes && antes.mapas) location.reload(); // retirar un permiso ya dado: se recarga sin el mapa
  };
  $("[data-c=aceptar]").addEventListener("click", () => decidir(true));
  $("[data-c=rechazar]").addEventListener("click", () => decidir(false));
  $("[data-c=configurar]").addEventListener("click", () => mostrar(true));
  $("[data-c=guardar]").addEventListener("click", () => decidir($("[data-op=mapas]").checked));
  document.addEventListener("click", (e) => {
    const a = e.target.closest("[data-cookies-config]");
    if (a) { e.preventDefault(); mostrar(true); }
  });

  const d = leer();
  if (d && d.mapas) cargarMapas();
  if (!d) setTimeout(() => mostrar(false), document.querySelector(".loader") ? 2300 : 600); // después de la bienvenida
})();
