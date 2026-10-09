/* =========================================================
   Ñandutí · encaje tradicional paraguayo generado en SVG
   «Ñandutí» = tela de araña en guaraní.
   ========================================================= */
(function () {
  const P = (r, a) => [+(r * Math.cos(a)).toFixed(2), +(r * Math.sin(a)).toFixed(2)];
  const TAU = Math.PI * 2;

  function nanduti(opts = {}) {
    const o = Object.assign({ rayos: 48, petalos: 16, sw: 0.7, dibujar: false, variante: 0 }, opts);
    const k = o.dibujar ? ' class="trazo" pathLength="1"' : "";
    const out = [];
    const circ = (r, extra = "") => out.push(`<circle cx="0" cy="0" r="${r}"${k}${extra}/>`);

    // anillos
    circ(97, ' stroke-dasharray="1.5 3"');
    circ(90); circ(72); circ(46); circ(16);

    // rayos (la «tela de araña»)
    let d = "";
    for (let i = 0; i < o.rayos; i++) {
      const a = (i / o.rayos) * TAU;
      const [x1, y1] = P(16, a), [x2, y2] = P(90, a);
      d += `M${x1} ${y1}L${x2} ${y2}`;
    }
    out.push(`<path d="${d}"${k} opacity=".55"/>`);

    // festón exterior
    d = "";
    const fest = 36;
    for (let i = 0; i < fest; i++) {
      const a1 = (i / fest) * TAU, a2 = ((i + 1) / fest) * TAU, am = (a1 + a2) / 2;
      const [x1, y1] = P(90, a1), [x2, y2] = P(90, a2), [cx, cy] = P(100, am);
      d += `M${x1} ${y1}Q${cx} ${cy} ${x2} ${y2}`;
    }
    out.push(`<path d="${d}"${k}/>`);

    // pétalos grandes entre 46 y 72
    d = "";
    for (let i = 0; i < o.petalos; i++) {
      const a = (i / o.petalos) * TAU, s = (TAU / o.petalos) * 0.42;
      const [x0, y0] = P(47, a), [x1, y1] = P(64, a - s), [x2, y2] = P(64, a + s), [xt, yt] = P(72, a);
      d += `M${x0} ${y0}Q${x1} ${y1} ${xt} ${yt}Q${x2} ${y2} ${x0} ${y0}Z`;
      const [m0x, m0y] = P(52, a), [m1x, m1y] = P(66, a);
      d += `M${m0x} ${m0y}L${m1x} ${m1y}`;
    }
    out.push(`<path d="${d}"${k}/>`);

    // círculos-nudo en el anillo 81
    for (let i = 0; i < 24; i++) {
      const [x, y] = P(81, (i / 24) * TAU + TAU / 48);
      out.push(`<circle cx="${x}" cy="${y}" r="3.4"${k}/>`);
    }

    // flor interior
    d = "";
    const fi = 12;
    for (let i = 0; i < fi; i++) {
      const a = (i / fi) * TAU, s = (TAU / fi) * 0.5;
      const [x0, y0] = P(17, a - s * .2), [c1x, c1y] = P(40, a - s), [c2x, c2y] = P(40, a + s), [x1, y1] = P(17, a + s * .2), [tx, ty] = P(44, a);
      d += `M${x0} ${y0}C${c1x} ${c1y} ${tx} ${ty} ${tx} ${ty}C${tx} ${ty} ${c2x} ${c2y} ${x1} ${y1}`;
    }
    out.push(`<path d="${d}"${k}/>`);

    // zig-zag entre 16 y 46
    d = "";
    const zz = 24;
    for (let i = 0; i <= zz; i++) {
      const a = (i / zz) * TAU, [x, y] = P(i % 2 ? 26 : 34, a);
      d += (i ? "L" : "M") + x + " " + y;
    }
    out.push(`<path d="${d}"${k} opacity=".7"/>`);

    // centro
    out.push(`<circle cx="0" cy="0" r="6"${k}/>`);
    out.push(`<circle cx="0" cy="0" r="2" fill="currentColor"/>`);

    return `<svg viewBox="-102 -102 204 204" fill="none" stroke="currentColor" stroke-width="${o.sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${out.join("")}</svg>`;
  }

  window.nanduti = nanduti;

  // Inyecta en cualquier [data-nanduti]
  function pintar(root = document) {
    root.querySelectorAll("[data-nanduti]").forEach((el) => {
      if (el.dataset.ok) return;
      const sw = parseFloat(el.dataset.sw || "0.7");
      const dibujar = el.hasAttribute("data-dibujar");
      const petalos = parseInt(el.dataset.petalos || "16", 10);
      el.insertAdjacentHTML("afterbegin", nanduti({ sw, dibujar, petalos }));
      el.dataset.ok = "1";
    });
  }
  window.pintarNanduti = pintar;
  pintar();
})();
