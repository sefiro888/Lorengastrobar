# Instrucciones para trabajar en este proyecto (cualquier IA o persona)

Lee primero `README.md` (estructura y comandos). El **estado del proyecto, lo pendiente y el historial**
están en `para-loren/ESTADO-PROYECTO.md` (carpeta local, no está en GitHub).

## Reglas
- Responde **en español**.
- La web publicada es la **versión 2** (fondo carbón, Anton + Kaushan Script + Montserrat, dorado maíz, encaje de ñandutí).
  Al usuario le gusta cómo se ve: **no cambies el aspecto** sin preguntar. Las optimizaciones no deben notarse.
- Edita sólo las páginas en español de la raíz y `js/`, `css/`, `i18n/*.json`. **Nunca** `ca/`, `en/` ni `js/i18n.js` a mano.
- Tras cada cambio: `python herramientas/i18n.py construir` y después `python herramientas/seo.py`.
  Si `construir` avisa de textos sin traducir, añade su traducción a `i18n/ca.json` e `i18n/en.json`.
- Al cambiar CSS o JS, sube `?v=N` en todos los `*.html` de la raíz y en `herramientas/i18n.py`.
- Comprueba los cambios en un navegador (Playwright con `python -m http.server`) antes de publicar:
  sin errores de JavaScript, en los tres idiomas y en móvil.
- Publicar = `git push` a `main` (GitHub Pages). Haz commits descriptivos en español.
- El repositorio es **público**: nunca subas `para-loren/`, `materialnuevo/` ni `tarjeta/` (están en `.gitignore`),
  ni datos privados del usuario o de Loren.
- La contraseña del wifi del local **no debe aparecer nunca** en la web.
- No publiques alérgenos en la carta hasta tener la lista completa confirmada por Loren
  (`para-loren/alergenos-confirmados.md`).
- Cuando falte un dato (precio, foto, contenido de un combo…), pregunta; no lo inventes.
