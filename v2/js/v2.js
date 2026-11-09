/* LOREN · VERSIÓN 2 — chispas, vídeos que se reproducen al verse y distintivo de versión */
(function () {
  const reducido = matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Chispas subiendo en las secciones oscuras principales
  if (!reducido) {
    document.querySelectorAll(".hero, .phero, .ch, .mdd, .cocina").forEach((sec) => {
      const c = document.createElement("div");
      c.className = "chispas"; c.setAttribute("aria-hidden", "true");
      const n = innerWidth < 700 ? 14 : 26;
      let h = "";
      for (let i = 0; i < n; i++) {
        const t = (2 + Math.random() * 3.5).toFixed(1);
        h += `<i style="left:${(Math.random() * 100).toFixed(1)}%;--t:${t}px;--d:${(6 + Math.random() * 7).toFixed(1)}s;--r:-${(Math.random() * 12).toFixed(1)}s;--x:${(Math.random() * 160 - 80).toFixed(0)}px"></i>`;
      }
      c.innerHTML = h;
      sec.prepend(c);
    });
  }

  // Vídeos: sólo se cargan y reproducen cuando están en pantalla
  const vids = document.querySelectorAll(".video video");
  if (vids.length && "IntersectionObserver" in window) {
    const io = new IntersectionObserver((es) => es.forEach((e) => {
      const v = e.target;
      if (e.isIntersecting) { if (v.preload === "none") v.preload = "auto"; if (!reducido) v.play().catch(() => {}); }
      else v.pause();
    }), { threshold: 0.35 });
    vids.forEach((v) => io.observe(v));
  }

  // Distintivo para comparar con la versión 1
  const pagina = location.pathname.split("/").pop() || "index.html";
  const chip = document.createElement("div");
  chip.className = "v2-chip";
  chip.innerHTML = `<b>VERSIÓN 2</b><span>propuesta</span><a href="../${pagina}">Ver versión 1</a>`;
  document.body.appendChild(chip);
})();
