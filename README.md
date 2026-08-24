# unattended-arte

Hospeda las imágenes de redes sociales de unattended.io para que la API de
Instagram pueda descargarlas.

## Por qué existe este repo

La API de contenido de Instagram **no acepta subir archivos**: solo lee una URL
pública que Meta pueda alcanzar. Los PNG tienen que estar publicados en algún
sitio, y GitHub Pages lo hace gratis.

**Este repo está separado del repo del vault a propósito.** Aquel contiene las
notas de cuenta con datos de contacto, los playbooks de precios y la estrategia
comercial: nada de eso puede ser público. Aquí solo hay imágenes que de todas
formas van a publicarse en redes.

## Qué NO va aquí

- Nada del vault: cuentas, prospectos, playbooks, contenido sin publicar.
- Ningún `.env`, credencial o token.
- Arte de prueba o borradores. Solo lo que está listo para publicarse.

Todo lo que se sube aquí es **público y queda indexable**. Si una imagen no
puede verse antes de publicarse en Instagram, no la subas todavía.

## Cómo se actualiza

Desde el repo del vault:

```bash
python scripts/sincronizar_arte.py --aplicar --publicar
```

Copia solo los PNG que cambiaron, hace commit y push. GitHub Pages tarda uno o
dos minutos en reflejarlo.

## Las URLs

```
https://<usuario>.github.io/unattended-arte/img/<archivo>.png
```

Esa base es la que espera el publicador:

```bash
python scripts/publicar_instagram.py \
    --calendario data/calendario-ig.json \
    --base-url https://<usuario>.github.io/unattended-arte/img \
    --publicar
```

## Configurar GitHub Pages (una sola vez)

En el repo de GitHub: **Settings → Pages → Source: Deploy from a branch →
Branch: `main` / `(root)` → Save.**

Comprueba que sirve abriendo cualquier imagen de `img/` en el navegador. Si da
404, espera un minuto: el primer despliegue tarda más.

## Las demos

`demos/` hospeda las cinco demos de producto para poder mandarlas por link —
por WhatsApp abren en cualquier celular, cosa que un HTML adjunto no hace.

La fuente vive en `unattended-agents/demos/`. Lo de aquí son copias con dos
etiquetas `noindex` añadidas, más el `Disallow` del `robots.txt`. No es por los
datos, que son simulados y están rotulados: es que una demo suelta en Google se
lee como un producto en operación, y unattended.io todavía no tiene clientes.

Para actualizarlas, se copian de nuevo desde la fuente y se les vuelve a poner
el `noindex`.
