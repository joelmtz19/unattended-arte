# -*- coding: utf-8 -*-
"""Carrusel de Instagram del 27-ago — pilar «Caso en abstracto».

Fuente del texto (literal, no se reescribe aquí):
  vault/30-Contenido/borradores/2026-08-27-instagram-carrusel-caso-agenda.md

Anatomía copiada de ../mes2-w37-w39/_generar.py, para que estas 10 láminas se
vean de la misma familia que las 21 del mes 2: etiqueta arriba en IBM Plex
Mono, titular al centro en Archivo Bold, acción abajo a la izquierda y la marca
abajo a la derecha. El esqueleto vive una sola vez, en PLANTILLA; lo que cambia
lámina a lámina vive en LAMINAS.

Paleta: unattended-site/src/app/globals.css. Nada fuera de ahí.

Correr desde esta carpeta:  python _generar-caso-agenda.py
Deja los PNG en ../img/ con el prefijo w35-caso-agenda- y numerados.
"""

import io
import pathlib
import shutil
import subprocess
import sys

for _f in (sys.stdout, sys.stderr):
    try:
        _f.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
AQUI = pathlib.Path(__file__).resolve().parent
SALIDA = AQUI.parent / "img"
TMP = AQUI / "_tmp"
PREFIJO = "w35-caso-agenda-"
LADO = 1080

# ── Paleta ────────────────────────────────────────────────────────────────
# Las 10 láminas van sobre fondo oscuro, así que el acento es el de fondo
# oscuro (#7ad0c6). El #0f6862 sobre #101013 no alcanza contraste legible.
BG = "#101013"
TINTA = "#f4f1ea"
ACENTO = "#7ad0c6"

PLANTILLA = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
  html, body { margin:0; padding:0; background:#101013; }

  .lienzo { width:1080px; height:1080px; box-sizing:border-box;
            background:#101013; color:#f4f1ea; padding:90px;
            display:flex; flex-direction:column;
            font-family: Archivo, "Helvetica Neue", Helvetica, Arial, sans-serif; }

  .etiqueta { font-family:"IBM Plex Mono","Courier New",ui-monospace,monospace;
              font-size:21px; letter-spacing:.16em; color:rgba(244,241,234,.55); }

  .centro { flex-grow:1; display:flex; flex-direction:column;
            justify-content:center; gap:@@GAP@@px; }

  h1 { margin:0; font-weight:700; font-size:@@TAM@@px; line-height:1.06;
       letter-spacing:-.035em; }

  .pie { display:flex; align-items:flex-end; justify-content:space-between; gap:40px; }
  .accion { font-family:"IBM Plex Mono","Courier New",ui-monospace,monospace;
            font-size:21px; letter-spacing:.08em; color:rgba(244,241,234,.55); }
  .marca { font-weight:700; font-size:30px; letter-spacing:-.03em; }

  .ac { color:#7ad0c6; }
  .centrado .centro { align-items:center; text-align:center; }

  /* ── mockup genérico de un hilo de chat (sin captura ni marca real) ── */
  .hilo { width:620px; box-sizing:border-box; background:rgba(244,241,234,.04);
          border:2px solid rgba(244,241,234,.14); border-radius:26px;
          padding:24px 26px; display:flex; flex-direction:column; gap:16px; }
  .hilo .barra { display:flex; align-items:center; gap:16px;
                 padding-bottom:16px; border-bottom:1px solid rgba(244,241,234,.12); }
  .av { width:32px; height:32px; border-radius:99px; background:rgba(244,241,234,.20); }
  .fila { display:flex; align-items:center; gap:16px; }
  .fila.der { flex-direction:row-reverse; }
  .burbuja { background:rgba(244,241,234,.07); border-radius:18px;
             padding:16px 20px; display:flex; flex-direction:column; gap:9px; }
  .burbuja.mia { background:rgba(122,208,198,.13); }
  .raya { height:10px; border-radius:99px; background:rgba(244,241,234,.24); }
  .chip { font-family:"IBM Plex Mono","Courier New",ui-monospace,monospace;
          font-size:19px; color:#7ad0c6; border:2px solid rgba(122,208,198,.55);
          border-radius:99px; padding:5px 14px; white-space:nowrap; }

  .col { flex:1; display:flex; flex-direction:column; gap:20px; }
  .col b { font-size:40px; font-weight:700; letter-spacing:-.02em; line-height:1.15; }
  .boton { font-family:"IBM Plex Mono","Courier New",ui-monospace,monospace;
           font-size:26px; border-radius:14px; padding:18px 30px; }
</style>
</head>
<body>
<!-- @@NOTA@@ -->
<div class="lienzo @@ALINEA@@">

  <span class="etiqueta">@@ETIQUETA@@</span>

  <div class="centro">
    <h1>@@TITULAR@@</h1>
@@EXTRA@@
  </div>

  <div class="pie">
    <span class="accion">@@ACCION@@</span>
    @@MARCA@@
  </div>

</div>
</body>
</html>
"""

MARCA = '<span class="marca">unattended<span class="ac">|</span></span>'


def ac(t):
    """Pinta un fragmento del titular con el acento. No cambia el texto."""
    return '<span class="ac">' + t + "</span>"


# ── Piezas del mockup ─────────────────────────────────────────────────────

def burbuja(anchos, mia=False, chip=None, der=False):
    rayas = "".join(
        '<div class="raya" style="width:' + str(w) + 'px;"></div>' for w in anchos)
    b = ('<div class="burbuja' + (" mia" if mia else "") + '">' + rayas + "</div>")
    c = ('<span class="chip">' + chip + "</span>") if chip else ""
    return '<div class="fila' + (" der" if der else "") + '">' + b + c + "</div>"


def hilo(filas):
    barra = ('<div class="barra"><div class="av"></div>'
             '<div class="raya" style="width:180px;"></div></div>')
    return '<div class="hilo">' + barra + "".join(filas) + "</div>"


# L2 — el mismo hilo hace de todo: cada burbuja lleva su etiqueta encima.
HILO_ETIQUETADO = "    " + hilo([
    burbuja([210, 130], chip="agenda"),
    burbuja([150], mia=True, chip="confirma", der=True),
    burbuja([240, 120], chip="dudas"),
    burbuja([180, 110], mia=True, chip="reagenda", der=True),
])

# L3 — el mismo mockup, ya sin etiquetas: mensajes distintos apilados sin
# orden, y la lupa encima del desorden.
LUPA = """    <div style="position:relative; width:620px;">
""" + hilo([
    burbuja([230, 140]),
    burbuja([120], mia=True, der=True),
    burbuja([190]),
    burbuja([260, 90], mia=True, der=True),
    burbuja([160, 210]),
]) + """
      <svg width="300" height="300" viewBox="0 0 300 300" aria-hidden="true"
           style="position:absolute; right:-72px; bottom:-46px;">
        <circle cx="128" cy="128" r="110" fill="rgba(122,208,198,.10)"
                stroke="#7ad0c6" stroke-width="7"></circle>
        <line x1="207" y1="207" x2="278" y2="278" stroke="#7ad0c6"
              stroke-width="16" stroke-linecap="round"></line>
      </svg>
    </div>"""

# L4 — el recordatorio que se escribe a mano: un mensaje a medio teclear y el
# reloj de arena al lado. Dice «cuando alcanza», no «siempre».
MANUAL = """    <div style="display:flex; align-items:center; gap:64px;">
      <div class="burbuja" style="padding:26px 30px; gap:14px;">
        <div class="raya" style="width:300px;"></div>
        <div class="raya" style="width:230px;"></div>
        <div style="display:flex; align-items:center; gap:14px; margin-top:6px;">
          <div style="width:17px;height:17px;border-radius:99px;background:rgba(244,241,234,.55);"></div>
          <div style="width:17px;height:17px;border-radius:99px;background:rgba(244,241,234,.38);"></div>
          <div style="width:17px;height:17px;border-radius:99px;background:rgba(244,241,234,.22);"></div>
        </div>
      </div>
      <svg width="150" height="200" viewBox="0 0 140 190" aria-hidden="true">
        <g stroke="#7ad0c6" stroke-width="6" fill="none" stroke-linecap="round">
          <line x1="24" y1="10" x2="116" y2="10"></line>
          <line x1="24" y1="180" x2="116" y2="180"></line>
          <path d="M34 10 C34 60 70 82 70 95 C70 108 34 130 34 180"></path>
          <path d="M106 10 C106 60 70 82 70 95 C70 108 106 130 106 180"></path>
        </g>
        <path d="M42 26 L98 26 C98 58 70 84 70 92 C70 84 42 58 42 26 Z"
              fill="rgba(122,208,198,.45)"></path>
        <path d="M52 166 L88 166 C88 150 78 132 70 128 C62 132 52 150 52 166 Z"
              fill="rgba(122,208,198,.45)"></path>
      </svg>
    </div>"""

# L5 — un solo chat que se parte en dos flujos, cada uno con su ícono.
BIFURCACION = """    <svg width="900" height="300" viewBox="0 0 900 300" aria-hidden="true">
      <g fill="none" stroke="#f4f1ea" stroke-width="5" stroke-linejoin="round">
        <rect x="8" y="86" width="180" height="118" rx="22"></rect>
        <path d="M46 204 L46 244 L86 204"></path>
      </g>
      <g stroke="rgba(244,241,234,.30)" stroke-width="4" stroke-linecap="round">
        <line x1="42" y1="122" x2="154" y2="122"></line>
        <line x1="42" y1="148" x2="128" y2="148"></line>
        <line x1="42" y1="174" x2="146" y2="174"></line>
      </g>

      <path d="M206 145 C310 145 350 66 470 66" fill="none" stroke="#7ad0c6" stroke-width="5"></path>
      <path d="M456 52 L478 66 L456 80 Z" fill="#7ad0c6"></path>
      <path d="M206 145 C310 145 350 230 470 230" fill="none" stroke="rgba(244,241,234,.55)" stroke-width="5"></path>
      <path d="M456 216 L478 230 L456 244 Z" fill="rgba(244,241,234,.55)"></path>

      <circle cx="536" cy="66" r="34" fill="none" stroke="#7ad0c6" stroke-width="5"></circle>
      <path d="M519 66 L531 78 L554 54" fill="none" stroke="#7ad0c6" stroke-width="6"
            stroke-linecap="round" stroke-linejoin="round"></path>
      <text x="590" y="80" font-family="Archivo, Helvetica, Arial, sans-serif"
            font-size="38" font-weight="700" fill="#7ad0c6">confirmación</text>

      <circle cx="536" cy="216" r="17" fill="none" stroke="rgba(244,241,234,.85)" stroke-width="5"></circle>
      <path d="M508 258 C508 232 564 232 564 258" fill="none"
            stroke="rgba(244,241,234,.85)" stroke-width="5" stroke-linecap="round"></path>
      <text x="590" y="242" font-family="Archivo, Helvetica, Arial, sans-serif"
            font-size="38" font-weight="700" fill="#f4f1ea">atención</text>
    </svg>"""

# L6 — dos columnas, una línea teal en medio. Nada más.
DOS_COLUMNAS = """    <div style="display:flex; align-items:stretch; gap:52px; width:100%;">
      <div class="col">
        <svg width="66" height="66" viewBox="0 0 66 66" aria-hidden="true">
          <circle cx="33" cy="33" r="29" fill="none" stroke="#7ad0c6" stroke-width="5"></circle>
          <path d="M19 34 L29 44 L48 22" fill="none" stroke="#7ad0c6" stroke-width="6"
                stroke-linecap="round" stroke-linejoin="round"></path>
        </svg>
        <b class="ac">Confirmación<br>automática</b>
      </div>
      <div style="width:3px; background:#7ad0c6; border-radius:99px;"></div>
      <div class="col">
        <svg width="66" height="66" viewBox="0 0 66 66" aria-hidden="true">
          <circle cx="33" cy="20" r="13" fill="none" stroke="#f4f1ea" stroke-width="5"></circle>
          <path d="M11 56 C11 38 55 38 55 56" fill="none" stroke="#f4f1ea"
                stroke-width="5" stroke-linecap="round"></path>
        </svg>
        <b>Atención<br>humana</b>
      </div>
    </div>"""

# L7 — la ventana, marcada sobre la línea del tiempo, y el botón al final.
VENTANA = """    <div style="display:flex; flex-direction:column; gap:44px; width:100%;">
      <svg width="900" height="170" viewBox="0 0 900 170" aria-hidden="true">
        <line x1="8" y1="98" x2="862" y2="98" stroke="rgba(244,241,234,.20)" stroke-width="4"></line>
        <line x1="250" y1="98" x2="560" y2="98" stroke="#7ad0c6" stroke-width="9" stroke-linecap="round"></line>
        <g stroke="#7ad0c6" stroke-width="5" stroke-linecap="round">
          <line x1="250" y1="72" x2="250" y2="124"></line>
          <line x1="560" y1="72" x2="560" y2="124"></line>
        </g>
        <text x="250" y="48" text-anchor="middle" font-family="IBM Plex Mono, monospace"
              font-size="28" fill="#7ad0c6">-48 h</text>
        <text x="560" y="48" text-anchor="middle" font-family="IBM Plex Mono, monospace"
              font-size="28" fill="#7ad0c6">-24 h</text>
        <text x="405" y="150" text-anchor="middle" font-family="IBM Plex Mono, monospace"
              font-size="26" fill="rgba(244,241,234,.55)">ventana fija</text>
        <circle cx="862" cy="98" r="13" fill="#f4f1ea"></circle>
      </svg>
      <div style="display:flex; gap:22px;">
        <span class="boton" style="background:#7ad0c6; color:#101013;">Confirmar</span>
        <span class="boton" style="border:2px solid rgba(244,241,234,.45); color:#f4f1ea;">Reagendar</span>
      </div>
    </div>"""

# L9 — el ícono de comentario, grande, en teal.
COMENTARIO = """    <svg width="230" height="230" viewBox="0 0 230 230" aria-hidden="true">
      <path d="M22 34 H208 A18 18 0 0 1 226 52 V150 A18 18 0 0 1 208 168 H92 L44 208 V168 H22
               A18 18 0 0 1 4 150 V52 A18 18 0 0 1 22 34 Z"
            fill="none" stroke="#7ad0c6" stroke-width="9" stroke-linejoin="round"></path>
      <g fill="#7ad0c6">
        <circle cx="78" cy="101" r="12"></circle>
        <circle cx="115" cy="101" r="12"></circle>
        <circle cx="152" cy="101" r="12"></circle>
      </g>
    </svg>"""

# L10 — cierre de marca. Aquí el logo es la pieza, no el pie.
CIERRE = """    <div style="display:flex; flex-direction:column; align-items:center; gap:34px;">
      <span style="font-weight:700; font-size:88px; letter-spacing:-.045em;">unattended<span class="ac">.io</span></span>
      <span style="font-size:34px; color:rgba(244,241,234,.72); letter-spacing:-.01em;">automatización y datos para operación real.</span>
    </div>"""


# ── Las láminas ───────────────────────────────────────────────────────────
# (etiqueta, tamaño del titular, titular, extra, acción, alineación, gap, nota)
LAMINAS = [
    dict(etiqueta="( caso en abstracto )", tam=86, alinea="centrado", gap=0,
         titular="De un chat de WhatsApp a un flujo con "
                 + ac("confirmación") + ".",
         accion="desliza →",
         nota="L1 Portada. Solo tipografía, acento único en «confirmación»."),

    dict(etiqueta="01 / 06", tam=60, gap=48,
         titular="Así opera hoy una clínica típica de dos sedes.",
         extra=HILO_ETIQUETADO,
         nota="L2. Un solo hilo con las cuatro etiquetas encima."),

    dict(etiqueta="02 / 06", tam=58, gap=40,
         titular="Confirmaciones, dudas y reagendados, mezclados en un hilo.",
         extra=LUPA,
         nota="L3. Mismo mockup, ahora con la lupa sobre el desorden."),

    dict(etiqueta="03 / 06", tam=64, gap=64,
         titular="Un recordatorio manual, mandado cuando hay tiempo, no basta.",
         extra=MANUAL,
         nota="L4. Mensaje a medio escribir y reloj de arena: «cuando alcanza»."),

    dict(etiqueta="04 / 06", tam=66, gap=48,
         titular="La solución no es más mensajes. Es "
                 + ac("separar los flujos") + ".",
         extra=BIFURCACION,
         nota="L5. Un chat que se parte en dos flujos con su propio ícono."),

    dict(etiqueta="05 / 06", tam=66, gap=70,
         titular="Confirmación por un lado. Atención por otro.",
         extra=DOS_COLUMNAS,
         nota="L6. Dos columnas separadas por la línea teal."),

    dict(etiqueta="06 / 06", tam=56, gap=54,
         titular="Ventana fija: 24–48 h antes, con botón de confirmar o reagendar.",
         extra=VENTANA,
         nota="L7. Línea de tiempo con la ventana marcada y el botón doble."),

    dict(etiqueta="( conclusión )", tam=72, alinea="centrado", gap=0,
         titular="El cuello de botella no era falta de personal. Era falta de "
                 + ac("un momento definido para confirmar") + ".",
         nota="L8. Solo tipografía, centrada, pensada para citarse tal cual."),

    dict(etiqueta="( tu turno )", tam=64, alinea="centrado", gap=56,
         titular="Comenta " + ac("«agenda»")
                 + " si quieres ver cómo se armaría en la tuya.",
         extra=COMENTARIO,
         nota="L9. CTA con el ícono de comentario grande en teal."),

    dict(etiqueta="( unattended.io )", tam=0, alinea="centrado", gap=0,
         titular="", extra=CIERRE, marca="",
         nota="L10. Cierre de marca: el logo centrado y una línea de apoyo."),
]


def html(l):
    s = PLANTILLA
    for tok, val in (
        ("@@GAP@@", str(l.get("gap", 44))),
        ("@@TAM@@", str(l.get("tam", 64))),
        ("@@NOTA@@", l.get("nota", "")),
        ("@@ALINEA@@", l.get("alinea", "")),
        ("@@ETIQUETA@@", l.get("etiqueta", "")),
        ("@@TITULAR@@", l.get("titular", "")),
        ("@@EXTRA@@", l.get("extra", "")),
        ("@@ACCION@@", l.get("accion", "")),
        ("@@MARCA@@", MARCA if l.get("marca", MARCA) else ""),
    ):
        s = s.replace(tok, val)
    return s


def render(n, l):
    TMP.mkdir(exist_ok=True)
    SALIDA.mkdir(exist_ok=True)
    nombre = PREFIJO + "%02d" % n
    tmp_html = TMP / (nombre + ".html")
    io.open(tmp_html, "w", encoding="utf-8").write(html(l))
    destino = SALIDA / (nombre + ".png")
    # Un perfil propio por llamada: dos Chrome seguidos se pelean por el mismo
    # y el segundo falla sin decir nada.
    r = subprocess.run(
        [CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
         "--user-data-dir=" + str(TMP / ("perfil-" + nombre)),
         "--force-device-scale-factor=1",
         "--window-size=%d,%d" % (LADO, LADO),
         "--virtual-time-budget=12000",
         "--screenshot=" + str(destino),
         "file:///" + str(tmp_html).replace("\\", "/")],
        capture_output=True, text=True, timeout=180)
    salida = (r.stdout or "") + (r.stderr or "")
    if "written to file" not in salida:
        raise SystemExit("falló " + nombre + ": " + salida[-400:])
    print("  ok  " + destino.name + "   %dx%d" % (LADO, LADO))


if __name__ == "__main__":
    print("\n  " + str(len(LAMINAS)) + " láminas -> PNG\n")
    for i, lam in enumerate(LAMINAS, start=1):
        render(i, lam)
    shutil.rmtree(TMP, ignore_errors=True)
    print("\n  En " + str(SALIDA) + "\n")
