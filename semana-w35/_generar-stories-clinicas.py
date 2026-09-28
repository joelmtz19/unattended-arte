# Historias de Instagram del 24-ago — pilar "Detrás de cámaras", sector salud.
#
# El texto viene literal del borrador y no se toca aquí:
#   vault/30-Contenido/borradores/2026-08-24-instagram-stories-revision-clinicas.md
# Este archivo solo lo convierte en PNG. Si el texto cambia, cambia allá primero.
#
# 1080x1920 con 300 px arriba y 384 abajo: es lo que tapa la interfaz de
# Instagram (el nombre de la cuenta arriba, la caja de responder abajo). Todo
# lo que importa vive en la franja de en medio. Misma anatomía que
# ../destacadas/_historias-agentes.py.
#
# Dos cosas del borrador NO se dibujan, a propósito:
#   - La encuesta (Story 3) y la caja de preguntas (Story 4) son stickers
#     nativos de Instagram; se ponen en la app al subir. El arte les deja el
#     hueco vacío dentro de la franja segura (constante RESERVA).
#   - La Story 2 está detenida: afirma como hecho observado "vimos cómo
#     confirman sus citas" y "ni una usa un sistema con confirmación
#     automática". El borrador mismo la marca [VERIFICAR] y dice que no sale
#     con esa redacción hasta que Joel confirme. Cuando confirme, pon
#     PERMITIR_STORY_2 = True y sale con el texto que ya está abajo.
#
#   python _generar-stories-clinicas.py
#
# Deja los PNG en ../img/. Necesita Chrome; no hay ImageMagick ni Pillow.

import io
import os
import subprocess
import sys

for _f in (sys.stdout, sys.stderr):
    try:
        _f.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
AQUI = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.abspath(os.path.join(AQUI, "..", "img"))
TMP = os.path.join(AQUI, "_tmp-stories-clinicas")  # propio: la carpeta es compartida
PREFIJO = "w35-stories-clinicas-"

# Story 2 detenida hasta que Joel confirme la cifra y el verbo. Ver cabecera.
PERMITIR_STORY_2 = False

# Hueco que se le deja al sticker nativo de IG dentro de la franja segura.
RESERVA_ENCUESTA = 620
RESERVA_PREGUNTAS = 460

# Paleta única, fuente: unattended-site/src/app/globals.css
# fondo oscuro #101013 · tinta #f4f1ea · acento sobre oscuro #7ad0c6
CAB = """<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400&display=swap">
<style>
  *{box-sizing:border-box} body{margin:0}
  .h{width:1080px;height:1920px;padding:300px 90px 384px;display:flex;
     flex-direction:column;background:#101013;color:#f4f1ea;
     font-family:Archivo,'Segoe UI Emoji',Helvetica,Arial,sans-serif}
  .etq{font-family:'IBM Plex Mono',monospace;font-size:24px;letter-spacing:.16em;
       color:rgba(244,241,234,.55)}
  /* El hueco del sticker cuenta como parte del bloque: centrando todo
     junto, el sticker cae al centro de la franja segura y no al borde. */
  .medio{flex-grow:1;display:flex;flex-direction:column;gap:48px;
         justify-content:center}
  h1{margin:0;font-weight:700;font-size:76px;line-height:1.08;
     letter-spacing:-.04em;max-width:15ch}
  h1.ancho{max-width:none}
  .ac{color:#7ad0c6}
  p{margin:0;font-size:40px;line-height:1.45;color:rgba(244,241,234,.72);
    max-width:22ch}
  .marca{font-weight:700;font-size:34px;letter-spacing:-.03em}
  .barra{color:#7ad0c6}
  /* Barra del resultado: los tracks van vacíos a propósito. El porcentaje
     real se llena cuando cierre la encuesta; aquí no se inventa ninguno. */
  .fila{display:flex;align-items:center;gap:28px}
  .op{font-weight:700;font-size:40px;width:80px;letter-spacing:-.02em}
  .track{flex-grow:1;height:38px;border-radius:999px;
         border:3px solid rgba(122,208,198,.42)}
  .pct{font-family:'IBM Plex Mono',monospace;font-size:30px;color:#7ad0c6;
       width:110px;text-align:right}
</style></head><body>"""


def pieza(etiqueta, cuerpo, reserva=0):
    hueco = ('<div style="height:%dpx" aria-hidden="true"></div>' % reserva
             if reserva else "")
    return f"""{CAB}
<div class="h">
  <span class="etq">{etiqueta}</span>
  <div class="medio">
{cuerpo}
{hueco}
  </div>
  <span class="marca">unattended<span class="barra">|</span></span>
</div></body></html>"""


# ── Story 1 — Contexto ────────────────────────────────────────────────
def story_1():
    return pieza(
        "( detrás de cámaras )",
        '    <h1>Esta semana revisamos algo en '
        '<span class="ac">clínicas de CDMX</span>.</h1>')


# ── Story 2 — Detrás de cámaras (DETENIDA) ────────────────────────────
# Texto literal del borrador, listo para cuando Joel confirme.
def story_2():
    return pieza(
        "( detrás de cámaras )",
        '    <h1>Vimos cómo confirman sus citas: casi todo por '
        '<span class="ac">WhatsApp, a mano</span>.</h1>\n'
        '    <p>Ni una usa un sistema con confirmación automática.</p>')


# ── Story 3 — Encuesta ────────────────────────────────────────────────
# El sticker de encuesta va abajo, puesto en la app. Aquí solo el hueco.
def story_3():
    return pieza(
        "( encuesta )",
        '    <h1 class="ancho">Ayúdanos con esto 👇</h1>',
        reserva=RESERVA_ENCUESTA)


# ── Story 4 — Resultado ───────────────────────────────────────────────
# Plantilla: los corchetes se sustituyen con el resultado real 24 h después.
# La caja de preguntas ("¿Cómo lo haces en tu clínica? Cuéntame.") es sticker
# nativo y va en el hueco de abajo.
def story_4():
    return pieza(
        "( resultado )",
        '    <h1><span class="ac">Así votaron:</span> [% Sí] / [% No]</h1>\n'
        '    <div style="display:flex;flex-direction:column;gap:30px">\n'
        '      <div class="fila"><span class="op">Sí</span>'
        '<span class="track"></span><span class="pct">[ % ]</span></div>\n'
        '      <div class="fila"><span class="op">No</span>'
        '<span class="track"></span><span class="pct">[ % ]</span></div>\n'
        '    </div>',
        reserva=RESERVA_PREGUNTAS)


def render(nombre, html):
    os.makedirs(TMP, exist_ok=True)
    os.makedirs(SALIDA, exist_ok=True)
    ruta_html = os.path.join(TMP, nombre + ".html")
    io.open(ruta_html, "w", encoding="utf-8").write(html)
    destino = os.path.join(SALIDA, nombre + ".png")
    # Cada llamada con su propio perfil: dos Chrome seguidos se pelean por el
    # mismo y el segundo falla en silencio.
    r = subprocess.run(
        [CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
         f"--user-data-dir={os.path.join(TMP, 'perfil-' + nombre)}",
         "--force-device-scale-factor=1", "--window-size=1080,1920",
         "--virtual-time-budget=12000", f"--screenshot={destino}",
         "file:///" + ruta_html.replace("\\", "/")],
        capture_output=True, text=True, timeout=180)
    salida = (r.stdout or "") + (r.stderr or "")
    if "written to file" not in salida:
        raise SystemExit(f"falló {nombre}: {salida[-300:]}")
    print(f"  ✓ {nombre}.png")


if __name__ == "__main__":
    print("\n  Historias — revisión de clínicas (24-ago)\n")
    render(PREFIJO + "01-contexto", story_1())
    if PERMITIR_STORY_2:
        render(PREFIJO + "02-detras-camaras", story_2())
    else:
        print("  · 02-detras-camaras: DETENIDA — falta confirmación de Joel")
    render(PREFIJO + "03-encuesta", story_3())
    render(PREFIJO + "04-resultado", story_4())
    print(f"\n  En {SALIDA}")
    print("  Al subir: encuesta nativa en la 03, caja de preguntas en la 04.")
    print("  La 04 se publica hasta tener el resultado real de la encuesta.\n")
