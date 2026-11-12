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

  // Vídeos de cocina: parados con su portada; sólo se descargan y reproducen al pulsar play (uno cada vez)
  const vids = [...document.querySelectorAll(".video video")];
  const PLAY = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5.5v13l10.5-6.5z" fill="currentColor"/></svg>';
  const PAUSA = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 5h3.6v14H7zM13.4 5H17v14h-3.6z" fill="currentColor"/></svg>';
  vids.forEach((v) => {
    const fig = v.closest(".video");
    const nombre = (fig.querySelector("figcaption b") || {}).textContent || "";
    const btn = document.createElement("button");
    btn.type = "button"; btn.className = "video__play"; btn.innerHTML = PLAY;
    btn.setAttribute("aria-label", "Reproducir vídeo: " + nombre);
    fig.appendChild(btn);
    const pintar = () => {
      fig.classList.toggle("is-on", !v.paused);
      btn.innerHTML = v.paused ? PLAY : PAUSA;
      btn.setAttribute("aria-label", (v.paused ? "Reproducir vídeo: " : "Pausar vídeo: ") + nombre);
    };
    fig.addEventListener("click", () => {
      if (v.paused) { vids.forEach((o) => o !== v && o.pause()); v.preload = "auto"; v.muted = false; v.volume = 1; v.play().catch(() => {}); }
      else v.pause();
    });
    v.addEventListener("play", pintar); v.addEventListener("pause", pintar); v.addEventListener("ended", pintar);
  });
  // si el vídeo que suena sale de la pantalla, se pausa
  if (vids.length && "IntersectionObserver" in window) {
    const io = new IntersectionObserver((es) => es.forEach((e) => { if (!e.isIntersecting) e.target.pause(); }), { threshold: 0.2 });
    vids.forEach((v) => io.observe(v));
  }

})();

/* Vídeo de Instagram: no se carga nada de Instagram hasta que el visitante pulsa «play». */
document.addEventListener("click", (e) => {
  const b = e.target.closest("[data-ig]");
  if (!b) return;
  const f = document.createElement("iframe");
  f.src = "https://www.instagram.com/reel/" + b.dataset.ig + "/embed/";
  f.title = "Instagram";
  f.setAttribute("allowfullscreen", "");
  f.setAttribute("loading", "lazy");
  f.className = "ig-video__frame";
  b.closest(".ig-video")?.classList.add("ig-video--on");
  b.replaceWith(f);
});

/* Vídeos de creadores en marco de móvil: play propio y sólo uno sonando a la vez. */
document.addEventListener("click", (e) => {
  const b = e.target.closest(".movil-v__play");
  if (!b) return;
  const v = b.parentElement.querySelector("video");
  if (v) v.play();
});
document.addEventListener("play", (e) => {
  const v = e.target;
  if (!v.closest || !v.closest(".movil-v")) return;
  document.querySelectorAll(".movil-v video").forEach((o) => { if (o !== v) o.pause(); });
  v.parentElement.classList.add("is-playing");
}, true);
document.addEventListener("ended", (e) => {
  const v = e.target;
  if (v.closest && v.closest(".movil-v")) v.parentElement.classList.remove("is-playing");
}, true);
