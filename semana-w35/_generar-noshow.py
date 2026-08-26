"""Carrusel de Instagram del 26-ago: "El no-show como síntoma, no la causa".

El texto en pantalla viene literal del borrador aprobado por Marco:
`vault/30-Contenido/borradores/2026-08-26-instagram-carrusel-noshow-diagnostico.md`
Aquí NO se reescribe: se maqueta. Si alguien cambia una frase, se cambia allá
primero y luego aquí, nunca al revés.

La anatomía es la misma de las 21 piezas del mes 2 (`mes2-w37-w39/_generar.py`):
etiqueta arriba en IBM Plex Mono, titular al centro en Archivo Bold, acción y
marca abajo. El esqueleto vive una sola vez; las nueve láminas son datos.

Paleta: la única que existe, la de `unattended-site/src/app/globals.css`.
Todo el carrusel va sobre fondo oscuro con un solo acento teal por lámina.

Correr desde esta carpeta:  python _generar-noshow.py
Deja los PNG en ../img/ con el prefijo `w35-noshow-`, de 01 a 09, 1080×1080.
"""

import io
import math
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
TMP = AQUI / "_tmp-noshow"
LADO = 1080

# ═══ PALETA ═══════════════════════════════════════════════════════════
# Fuente: unattended-site/src/app/globals.css. No hay otra.
BG = "#101013"          # fondo oscuro (--field)
TINTA = "#f4f1ea"       # tinta sobre oscuro
ACENTO = "#7ad0c6"      # acento sobre oscuro (--accent-soft)
TENUE = "rgba(244,241,234,.55)"   # etiqueta y pie
GRIS = "rgba(244,241,234,.35)"    # trazo de apoyo en los íconos
GRIS_RELLENO = "rgba(244,241,234,.10)"


def ac(t):
    """Envuelve en el acento. Uno solo por lámina — nunca dos."""
    return '<span style="color:' + ACENTO + ';">' + t + "</span>"


# ═══ ÍCONOS ═══════════════════════════════════════════════════════════
# Mockups genéricos a propósito: las clínicas del scoring son prospectos,
# no clientes, así que ninguna captura real puede aparecer aquí.

# L2 — burbuja de chat gris con doble check sin leer en teal.
CHAT_SIN_LEER = f"""    <svg width="560" height="212" viewBox="0 0 560 212" aria-hidden="true">
      <path d="M46 0 H500 A30 30 0 0 1 530 30 V166 A30 30 0 0 1 500 196 H46
               L46 196 L14 212 L22 196 A30 30 0 0 1 16 0 Z"
            fill="{GRIS_RELLENO}"/>
      <g fill="rgba(244,241,234,.26)">
        <rect x="56" y="46" width="392" height="15" rx="7.5"/>
        <rect x="56" y="86" width="318" height="15" rx="7.5"/>
        <rect x="56" y="126" width="214" height="15" rx="7.5"/>
      </g>
      <g fill="none" stroke="{ACENTO}" stroke-width="6"
         stroke-linecap="round" stroke-linejoin="round">
        <path d="M416 158 l13 13 l28 -32"/>
        <path d="M444 158 l13 13 l28 -32"/>
      </g>
    </svg>"""

# L3 — un chat, tres flechas, tres puertas de consultorio.
_puertas_l3 = "".join(
    f'<rect x="448" y="{y - 37}" width="62" height="74" rx="3"/>'
    f'<circle cx="498" cy="{y}" r="4" fill="{GRIS}" stroke="none"/>'
    for y in (37, 135, 233))
_flechas_l3 = "".join(
    f'<path d="M128 135 C 268 135, 300 {y}, 432 {y}"/>'
    f'<path d="M420 {y - 8} L436 {y} L420 {y + 8}"/>'
    for y in (37, 135, 233))
UN_CHAT_TRES_PUERTAS = f"""    <svg width="620" height="270" viewBox="0 0 620 270" aria-hidden="true">
      <g fill="none" stroke="{GRIS}" stroke-width="4" stroke-linejoin="round">
        <path d="M26 78 H100 A22 22 0 0 1 122 100 V144 A22 22 0 0 1 100 166
                 H62 L36 194 V166 H26 A22 22 0 0 1 4 144 V100
                 A22 22 0 0 1 26 78 Z"/>
        {_puertas_l3}
      </g>
      <g fill="none" stroke="{ACENTO}" stroke-width="4"
         stroke-linecap="round" stroke-linejoin="round">
        {_flechas_l3}
      </g>
    </svg>"""

# L4 — pila de burbujas; la del centro resaltada, el resto apagadas.
_pila = "".join(
    f'<rect x="{x}" y="{y}" width="{w}" height="42" rx="21"'
    f' fill="{GRIS_RELLENO}"/>'
    for x, y, w in ((0, 0, 430), (180, 52, 440), (250, 156, 370), (0, 208, 400)))
UNA_ENTRE_MUCHAS = f"""    <svg width="620" height="250" viewBox="0 0 620 250" aria-hidden="true">
      {_pila}
      <rect x="0" y="104" width="480" height="42" rx="21"
            fill="rgba(122,208,198,.16)" stroke="{ACENTO}" stroke-width="3"/>
    </svg>"""


def _punto(ang_grados, radio, cx=125, cy=125):
    a = math.radians(ang_grados)
    return cx + radio * math.sin(a), cy - radio * math.cos(a)


_marcas = "".join(
    '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>'
    % (_punto(30 * i, 95) + _punto(30 * i, 108))
    for i in range(12))
_hora = _punto(305, 62)      # 10:10 — hora neutra, no es un dato
_minuto = _punto(60, 88)
# L5 — reloj análogo con las manecillas en teal.
RELOJ = f"""    <svg width="250" height="250" viewBox="0 0 250 250" aria-hidden="true">
      <circle cx="125" cy="125" r="118" fill="none" stroke="{GRIS}"
              stroke-width="5"/>
      <g stroke="rgba(244,241,234,.4)" stroke-width="4"
         stroke-linecap="round">{_marcas}</g>
      <g stroke="{ACENTO}" stroke-linecap="round">
        <line x1="125" y1="125" x2="{_hora[0]:.1f}" y2="{_hora[1]:.1f}"
              stroke-width="8"/>
        <line x1="125" y1="125" x2="{_minuto[0]:.1f}" y2="{_minuto[1]:.1f}"
              stroke-width="6"/>
      </g>
      <circle cx="125" cy="125" r="7" fill="{ACENTO}"/>
    </svg>"""

# L6 — calendario con una celda tachada y el "$" tenue debajo.
_celdas = "".join(
    f'<rect x="{x}" y="{y}" width="58" height="42" rx="6"/>'
    for y in (104, 158, 212) for x in (34, 102, 170, 238, 306))
CALENDARIO = f"""    <svg width="420" height="372" viewBox="0 0 420 372" aria-hidden="true">
      <g stroke="rgba(244,241,234,.4)" stroke-width="6" stroke-linecap="round">
        <line x1="118" y1="2" x2="118" y2="36"/>
        <line x1="282" y1="2" x2="282" y2="36"/>
      </g>
      <g fill="none" stroke="{GRIS}">
        <rect x="10" y="26" width="380" height="272" rx="18" stroke-width="4"/>
        <line x1="10" y1="88" x2="390" y2="88" stroke-width="3"/>
      </g>
      <g fill="rgba(244,241,234,.12)">{_celdas}</g>
      <rect x="170" y="158" width="58" height="42" rx="6"
            fill="rgba(122,208,198,.14)"/>
      <g stroke="{ACENTO}" stroke-width="6" stroke-linecap="round">
        <line x1="181" y1="167" x2="217" y2="191"/>
        <line x1="217" y1="167" x2="181" y2="191"/>
      </g>
      <text x="199" y="356" text-anchor="middle" font-size="66"
            font-family="Archivo, Helvetica, Arial, sans-serif"
            font-weight="700" fill="rgba(244,241,234,.3)">$</text>
    </svg>"""

# L7 — una puerta y varias puertas, a la misma escala, con la misma alerta.
_puertas_l7 = "".join(
    f'<rect x="{x}" y="150" width="56" height="104" rx="3"/>'
    f'<circle cx="{x + 44}" cy="202" r="4" fill="{GRIS}" stroke="none"/>'
    for x in (70, 400, 470, 540))
_alertas = "".join(
    f'<path d="M{cx - 39} 110 L{cx} 40 L{cx + 39} 110 Z"/>'
    f'<line x1="{cx}" y1="66" x2="{cx}" y2="86"/>'
    f'<circle cx="{cx}" cy="97" r="3.5" fill="{ACENTO}" stroke="none"/>'
    for cx in (98, 498))
MISMA_ESCALA = f"""    <svg width="660" height="266" viewBox="0 0 660 266" aria-hidden="true">
      <g fill="none" stroke="{GRIS}" stroke-width="4">{_puertas_l7}</g>
      <line x1="300" y1="46" x2="300" y2="254"
            stroke="rgba(244,241,234,.14)" stroke-width="2"/>
      <g fill="none" stroke="{ACENTO}" stroke-width="5"
         stroke-linejoin="round" stroke-linecap="round">{_alertas}</g>
    </svg>"""

# L9 — el ícono de guardar, en la esquina inferior derecha. Va absoluto y no
# en el flujo: dentro de la columna central el titular se descentraba y el
# marcador aterrizaba encima del wordmark.
GUARDAR = f"""    <div style="position:absolute;right:90px;bottom:172px;">
      <svg width="80" height="110" viewBox="0 0 80 110" aria-hidden="true">
        <path d="M6 4 H74 V106 L40 76 L6 106 Z" fill="{ACENTO}"/>
      </svg>
    </div>"""


# ═══ LAS NUEVE LÁMINAS ════════════════════════════════════════════════
# `titular` = el texto en pantalla del borrador, literal. `nota` = la nota
# visual que lo acompaña, para que el siguiente que abra esto sepa por qué
# cada lámina se ve como se ve.
LAMINAS = [
    dict(
        n=1, eyebrow="( diagnóstico )", tam=104, ancho=13, marca=False,
        titular="El no-show no es mala suerte del paciente" + ac("."),
        accion="desliza →",
        nota="Portada. Una sola idea, sin logo, acento solo en el punto "
             "final. Aquí vive el 80% del alcance del carrusel."),
    dict(
        n=2, eyebrow="02 / 09", tam=60, ancho=21, icono=CHAT_SIN_LEER,
        titular="Recordatorio: 'Nos vemos mañana.' Nadie confirma, "
                "nadie reagenda.",
        nota="Mockup genérico de burbuja de chat —ninguna clínica es "
             "cliente— con doble check sin leer en teal."),
    dict(
        n=3, eyebrow="03 / 09", tam=57, ancho=22, icono=UN_CHAT_TRES_PUERTAS,
        titular="Un mismo WhatsApp agenda y resuelve dudas de varios "
                "consultorios a la vez.",
        nota="Un chat, tres flechas, tres puertas de consultorio. "
             "[VERIFICAR] el patrón viene del scoring del 09-ago, no de "
             "una auditoría operativa."),
    dict(
        n=4, eyebrow="04 / 09", tam=60, ancho=21, icono=UNA_ENTRE_MUCHAS,
        titular="El mensaje que debía confirmar la cita se pierde entre "
                "otros veinte.",
        nota="Pila de burbujas: la del centro resaltada, el resto apagadas."),
    dict(
        n=5, eyebrow="05 / 09", tam=57, ancho=22, icono=RELOJ,
        titular="Nadie contesta. El horario sigue bloqueado hasta que el "
                "paciente no llega.",
        nota="Reloj análogo, manecillas en teal marcando la hora de la cita."),
    dict(
        n=6, eyebrow="06 / 09", tam=58, ancho=21, icono=CALENDARIO,
        titular="Lo caro no es la cita perdida. Es el horario que no se "
                "vendió a tiempo.",
        nota="Calendario con una celda tachada en teal y el signo $ tenue "
             "debajo de esa celda."),
    dict(
        n=7, eyebrow="07 / 09", tam=57, ancho=22, icono=MISMA_ESCALA,
        titular="Pasa igual en un consultorio solo que en un centro de "
                "diez especialistas.",
        nota="Una puerta contra varias puertas, a la misma escala y con la "
             "misma alerta. [VERIFICAR] igual que L3."),
    dict(
        n=8, eyebrow="08 / 09", tam=90, ancho=15,
        titular="Confirmar una cita y avisarla " + ac("no es lo mismo") + ".",
        nota="Conclusión citable: la frase sola, más grande que el resto, "
             "acento solo en «no es lo mismo»."),
    dict(
        n=9, eyebrow="09 / 09", tam=62, ancho=20, icono=GUARDAR,
        titular="Guarda esto si tu recordatorio todavía es "
                "'nos vemos mañana'.",
        nota="Ícono de guardar en teal, en la esquina inferior derecha, "
             "arriba de la franja del pie."),
]


# ═══ EL ESQUELETO, UNA SOLA VEZ ═══════════════════════════════════════
PLANTILLA = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;700&family=IBM+Plex+Mono:wght@400&display=swap">
<style>
  html, body {{ margin: 0; padding: 0; background: {bg}; }}
  body {{ font-family: Archivo, "Helvetica Neue", Helvetica, Arial, sans-serif;
          -webkit-font-smoothing: antialiased; }}
  .mono {{ font-family: "IBM Plex Mono", ui-monospace, "Courier New", monospace; }}
</style>
</head>
<body>

<!-- {nota} -->
<div style="position: relative; width: {lado}px; height: {lado}px;
            box-sizing: border-box; background: {bg}; color: {tinta};
            padding: 90px; display: flex; flex-direction: column;">

  <span class="mono" style="font-size: 21px; letter-spacing: 0.16em;
        color: {tenue};">{eyebrow}</span>

  <div style="flex-grow: 1; display: flex; flex-direction: column;
              justify-content: {reparto}; gap: 40px;">
    <h1 style="margin: 0; font-weight: 700; font-size: {tam}px;
               line-height: 1.05; letter-spacing: -0.04em;
               max-width: {ancho}ch;">{titular}</h1>
{icono}
  </div>

  <div style="display: flex; align-items: flex-end;
              justify-content: space-between; gap: 40px;">
    <span class="mono" style="font-size: 21px; letter-spacing: 0.08em;
          color: {tenue};">{accion}</span>
    {marca}
  </div>

</div>
</body>
</html>
"""

MARCA = ('<span style="font-weight: 700; font-size: 30px; '
         'letter-spacing: -0.03em;">unattended'
         '<span style="color: ' + ACENTO + ';">|</span></span>')


def html_de(lam):
    return PLANTILLA.format(
        lado=LADO, bg=BG, tinta=TINTA, tenue=TENUE,
        nota=lam["nota"], eyebrow=lam["eyebrow"], tam=lam["tam"],
        ancho=lam["ancho"], titular=lam["titular"],
        reparto=lam.get("reparto", "center"),
        icono=lam.get("icono", ""), accion=lam.get("accion", ""),
        marca=MARCA if lam.get("marca", True) else "<span></span>")


def render(lam):
    nombre = "w35-noshow-%02d" % lam["n"]
    tmp_html = TMP / (nombre + ".html")
    io.open(tmp_html, "w", encoding="utf-8").write(html_de(lam))
    destino = SALIDA / (nombre + ".png")
    # Perfil propio por llamada: dos Chrome seguidos se pelean por el mismo
    # y el segundo falla sin decir nada.
    r = subprocess.run(
        [CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
         f"--user-data-dir={TMP / ('perfil-' + nombre)}",
         "--force-device-scale-factor=1", f"--window-size={LADO},{LADO}",
         "--virtual-time-budget=12000", f"--screenshot={destino}",
         "file:///" + str(tmp_html).replace("\\", "/")],
        capture_output=True, text=True, timeout=180)
    salida = (r.stdout or "") + (r.stderr or "")
    if "written to file" not in salida:
        raise SystemExit(f"falló {nombre}: {salida[-400:]}")
    print(f"  ok  {destino.name}   {LADO}x{LADO}")


if __name__ == "__main__":
    TMP.mkdir(exist_ok=True)
    SALIDA.mkdir(exist_ok=True)
    print(f"\n  {len(LAMINAS)} laminas -> PNG\n")
    for lam in LAMINAS:
        render(lam)
    shutil.rmtree(TMP, ignore_errors=True)
    print(f"\n  En {SALIDA}\n")
