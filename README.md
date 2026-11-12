# Loren Restobar · web

Web de **Loren Restobar**, restaurante paraguayo en Carrer de la Muntanya 115, Barcelona.
Publicada en **https://lorenrestobar.com** (GitHub Pages, dominio en DonDominio, HTTPS forzado).

Web estática (HTML + CSS + JavaScript, sin framework ni compilación) en **tres idiomas**:
español en la raíz, catalán en `ca/` y inglés en `en/`.

## Estructura

| Ruta | Qué es |
|---|---|
| `index.html`, `carta.html`, `sabores.html`, `historia.html`, `domicilio.html`, `eventos.html`, `visitanos.html`, `aviso-legal.html` | Páginas en español (**son la fuente**: se editan éstas) |
| `ca/`, `en/` | Páginas traducidas. **Se generan**, no se editan a mano |
| `404.html` | Página de error (sólo ES, `<base href="/">`) |
| `resena/index.html` | Redirige a "Escribir reseña" de Google. Es el destino de los QR impresos: si cambia el enlace de Google, se cambia aquí |
| `carta-clasica.html`, `v2/` | Sólo redirecciones de versiones antiguas |
| `js/data.js` | **Datos**: carta (`window.CARTA`, 107 platos y bebidas), categorías, horario, teléfonos y enlaces (`window.LOREN`) |
| `js/layout.js` | Cabecera, menú móvil, pie y modales comunes (se inyectan en `#shell-top` / `#shell-bottom`) |
| `js/main.js` | Lógica común: loader, brasas, horario y "abierto ahora", vídeos, reservas, WhatsApp |
| `js/paginas.js` | Lógica por página: enciclopedia de sabores, combos, quiz, formulario de reservas |
| `js/carta.js` | Carta interactiva y pedido por WhatsApp |
| `js/cookies.js` | Aviso de cookies (Google Maps sólo se carga con permiso) |
| `js/i18n.js` | Diccionario de traducciones. **Generado** |
| `css/` | `styles.css` (base), `paginas.css`, `carta.css`, `v2.css` (línea gráfica actual), `fuentes.css` |
| `fuentes/` | Tipografías alojadas en la propia web (Anton, Kaushan Script, Montserrat) |
| `i18n/ca.json`, `i18n/en.json` | Traducciones `{ "texto en español": "traducción" }` |
| `img/`, `video/` | Imágenes (WebP) y vídeos |
| `sitemap.xml`, `robots.txt` | **Generados** por `herramientas/seo.py` |
| `herramientas/` | Scripts de mantenimiento (ver abajo) |

## Cómo se trabaja

Requisitos: Python 3 con `beautifulsoup4`, `playwright` (`python -m playwright install chromium`), `Pillow` y `segno`.

Después de **cualquier** cambio en textos, páginas o `js/data.js`:

```bash
python herramientas/i18n.py construir   # genera ca/ y en/ y js/i18n.js (avisa de textos sin traducir)
python herramientas/seo.py              # prerender + canonical/hreflang + JSON-LD + sitemap.xml + robots.txt
```

- **Textos nuevos:** se añade la traducción en `i18n/ca.json` y `i18n/en.json` (la clave es el texto en español tal cual).
  `construir` lista los que faltan.
- **Caché:** al cambiar CSS o JS, subir el número `?v=N` en todos los `*.html` de la raíz y en `herramientas/i18n.py` (`js/i18n.js?v=N`).
- **No editar a mano** el contenido entre `data-pre ... <!--/pre-->` ni entre `<!--seo-->` y `<!--/seo-->`: lo reescribe `seo.py`
  (la carta, la cabecera, el pie y la enciclopedia se guardan prerenderizados para que Google los lea sin JavaScript).
- **Comillas:** usar “ ” en los textos (las tipografías Anton y Kaushan pintan « como <<).
- **Horario:** en `js/data.js` → `horario` (0 = domingo; horas decimales, 23.5 = 23:30; `{ dia, cerrado: true }` para cerrar).
- **Publicar:** `git push` a `main`; GitHub Pages despliega solo en 1–2 minutos.

## Herramientas

| Script | Para qué |
|---|---|
| `herramientas/i18n.py` | `extraer` (lista textos) y `construir` (genera CA/EN) |
| `herramientas/seo.py` | SEO: prerender, etiquetas, datos estructurados, sitemap y robots |
| `herramientas/og.py` | Imágenes para compartir (1200×630) por página e idioma → `img/redes/og-*.jpg` |
| `herramientas/resenas.py` | Material impreso con QR de reseñas (sale en una carpeta local, no en la web) |
| `herramientas/claves_js.js` | Extrae los textos `T("…")` de los JS para traducirlos |
| `herramientas/archivo/` | Scripts antiguos, ya no se usan |

## Comprobar

Servidor local: `python -m http.server 8000` y abrir http://localhost:8000.
Velocidad y SEO en móvil: https://pagespeed.web.dev con `https://lorenrestobar.com`.
Google Search Console: propiedad de dominio `lorenrestobar.com` (verificada con un registro TXT en DonDominio; **no borrarlo**).

## Versión anterior

La primera versión de la web está guardada en la etiqueta de git `version-1-antigua`.
