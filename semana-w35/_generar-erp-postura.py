"""Carrusel de Instagram del 27-ago (W35) — pilar Postura, "ERP médico".

El texto en pantalla viene tal cual del borrador y **no se toca**:
`vault/30-Contenido/borradores/2026-08-27-instagram-carrusel-erp-postura.md`.
Aquí solo se le pone forma. Si alguien quiere cambiar una frase, se cambia en
el borrador y se vuelve a correr esto — no al revés.

Anatomía copiada de `mes2-w37-w39/_generar.py`, para que la semana W35 se vea
de la misma familia que el mes 2: etiqueta arriba en IBM Plex Mono, titular al
centro en Archivo Bold, acción y marca abajo. El esqueleto vive una sola vez;
las diez láminas son datos.

Paleta: la de `unattended-site/src/app/globals.css` y ninguna otra. Toda la
pieza va sobre fondo oscuro con un solo acento teal claro, como pide la nota
visual del borrador.

Correr desde esta carpeta:  python _generar-erp-postura.py
Deja los PNG en ../img/ con el prefijo `w35-erp-postura-`.
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
TMP = AQUI / "_tmp-erp-postura"
PREFIJO = "w35-erp-postura-"
LADO = 1080

# ── Paleta ────────────────────────────────────────────────────────────
# globals.css es la fuente. Fondo oscuro #101013 (--field), tinta sobre
# oscuro #f4f1ea, acento sobre oscuro #7ad0c6 (--accent-soft).
BG = "#101013"
TINTA = "#f4f1ea"
ACENTO = "#7ad0c6"
ETIQUETA = "rgba(244,241,234,.55)"   # etiqueta y pie
APOYO = "rgba(244,241,234,.72)"      # texto secundario
LINEA = "rgba(244,241,234,.22)"      # trazos de diagrama
TENUE = "rgba(244,241,234,.50)"      # lo atenuado a propósito

SANS = "Archivo, 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'IBM Plex Mono', ui-monospace, 'Cascadia Mono', Consolas, monospace"


def ac(t):
    """Acento teal claro. Uno solo por lámina."""
    return '<span style="color:' + ACENTO + ';">' + t + "</span>"


def tenue(t):
    """Lo que la lámina 1 descarta: presente, pero apagado."""
    return '<span style="color:' + TENUE + ';">' + t + "</span>"


# ── Esqueleto: una sola vez ───────────────────────────────────────────
PLANTILLA = """<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>{id}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
  <style>
    html, body {{ margin: 0; padding: 0; background: {bg}; }}
    body {{ font-family: {sans}; }}
  </style>
</head>
<body>
<!-- {nota} -->
<div style="width: {lado}px; height: {lado}px; box-sizing: border-box; background: {bg}; color: {tinta}; padding: 90px; display: flex; flex-direction: column;">

  <span style="font-family: {mono}; font-size: 21px; letter-spacing: 0.16em; color: {etiqueta};">{eyebrow}</span>

  <div style="flex-grow: 1; display: flex; flex-direction: column; justify-content: center; align-items: {alinea_caja}; text-align: {alinea}; gap: 40px;">
{cuerpo}
  </div>

  <div style="display: flex; align-items: flex-end; justify-content: space-between; gap: 40px; min-height: 38px;">
    <span style="font-family: {mono}; font-size: 21px; letter-spacing: 0.08em; color: {etiqueta};">{accion}</span>
    {marca}
  </div>

</div>
</body>
</html>
"""

MARCA = ('<span style="font-weight: 700; font-size: 30px; letter-spacing: -0.03em;">'
         'unattended<span style="color: ' + ACENTO + ';">|</span></span>')


def titular(txt, tam, ancho, centro=False):
    return ('    <h1 style="margin: 0; font-weight: 700; font-size: ' + str(tam)
            + 'px; line-height: 1.05; letter-spacing: -0.04em; max-width: '
            + str(ancho) + 'ch;' + ('' if not centro else ' text-wrap: balance;')
            + '">' + txt + "</h1>")


# ── Los dibujos que pide cada nota visual ─────────────────────────────

# L2 — el sistema completo, con sus módulos. Cuatro apagados; el único que
# importa, encendido y ocupando el ancho entero.
def _chip(t, viva=False):
    borde = ACENTO if viva else LINEA
    color = ACENTO if viva else ETIQUETA
    ancho = "grid-column: 1 / -1;" if viva else ""
    return ('<div style="' + ancho + ' border: 2px solid ' + borde
            + '; border-radius: 10px; padding: 15px 20px; font-family: ' + MONO
            + '; font-size: 23px; color: ' + color + ';">' + t + "</div>")


MODULOS = ('    <div style="width: 760px; border: 2px solid ' + LINEA
           + '; border-radius: 16px; overflow: hidden;">'
           '<div style="display: flex; gap: 10px; padding: 17px 22px; border-bottom: 2px solid ' + LINEA + ';">'
           + "".join('<span style="width:13px;height:13px;border-radius:99px;background:'
                     + TENUE + ';"></span>' for _ in range(3))
           + '</div>'
           '<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; padding: 22px;">'
           + _chip("agenda") + _chip("expediente") + _chip("facturación")
           + _chip("inventario") + _chip("reagendado", viva=True)
           + "</div></div>")

# L3 — el tamaño del problema contra el tamaño de la compra, a escala.
CAJAS = ('    <div style="display: flex; align-items: flex-end; gap: 30px;">'
         '<div style="width: 540px; height: 210px; border: 2px solid ' + LINEA
         + '; border-radius: 12px; display: flex; align-items: center; justify-content: center; '
         'font-family: ' + MONO + '; font-size: 25px; color: ' + ETIQUETA + ';">ERP completo</div>'
         '<div style="width: 320px; height: 96px; border: 2px solid ' + ACENTO
         + '; border-radius: 12px; display: flex; align-items: center; justify-content: center; '
         'text-align: center; font-family: ' + MONO + '; font-size: 20px; color: ' + ACENTO
         + '; line-height: 1.3;">recordatorio<br>+ reagendado</div>'
         "</div>")

# L4 — las tres sesiones del tratamiento. La segunda es la que no ocurre.
CALENDARIO = """    <svg width="780" height="252" viewBox="0 0 780 252" aria-hidden="true">
      <g fill="none" stroke="{linea}" stroke-width="3">
        <rect x="2" y="26" width="776" height="220" rx="14"></rect>
        <line x1="2" y1="78" x2="778" y2="78"></line>
        <line x1="196" y1="8" x2="196" y2="44" stroke-linecap="round"></line>
        <line x1="584" y1="8" x2="584" y2="44" stroke-linecap="round"></line>
      </g>
      <circle cx="196" cy="170" r="15" fill="{tenue}"></circle>
      <circle cx="390" cy="170" r="17" fill="none" stroke="{acento}" stroke-width="5"></circle>
      <circle cx="584" cy="170" r="15" fill="{tenue}"></circle>
      <text x="390" y="136" text-anchor="middle" font-family="{mono}" font-size="44" fill="{acento}">?</text>
      <g font-family="{mono}" font-size="26" text-anchor="middle" fill="{etiqueta}">
        <text x="196" y="226">1</text>
        <text x="390" y="226" fill="{acento}">2</text>
        <text x="584" y="226">3</text>
      </g>
    </svg>""".format(linea=LINEA, tenue=TENUE, acento=ACENTO, mono=MONO.replace("'", ""),
                     etiqueta=ETIQUETA)

# L5 — el esquema de seguimiento: puntos de control programados por diseño.
# Uno queda hueco, y ese es el que se cae.
LINEA_TIEMPO = """    <svg width="860" height="170" viewBox="0 0 860 170" aria-hidden="true">
      <line x1="30" y1="60" x2="830" y2="60" stroke="{linea}" stroke-width="3" stroke-linecap="round"></line>
      <circle cx="60" cy="60" r="13" fill="{tenue}"></circle>
      <circle cx="240" cy="60" r="13" fill="{tenue}"></circle>
      <circle cx="430" cy="60" r="17" fill="none" stroke="{acento}" stroke-width="5"></circle>
      <circle cx="620" cy="60" r="13" fill="{tenue}"></circle>
      <circle cx="800" cy="60" r="13" fill="{tenue}"></circle>
      <line x1="430" y1="86" x2="430" y2="108" stroke="{acento}" stroke-width="3" stroke-linecap="round"></line>
      <text x="430" y="142" text-anchor="middle" font-family="{mono}" font-size="24" fill="{acento}">cita perdida</text>
    </svg>""".format(linea=LINEA, tenue=TENUE, acento=ACENTO, mono=MONO.replace("'", ""))

# L7 — jerarquía invertida a propósito: lo chico se ve grande, porque es por
# donde se empieza; lo grande se ve chico, porque todavía no se justifica.
FLECHA = ('    <div style="display: flex; align-items: baseline; gap: 34px;">'
          '<span style="font-size: 96px; font-weight: 700; letter-spacing: -0.04em; color: '
          + ACENTO + ';">chico</span>'
          '<span style="font-size: 52px; color: ' + TENUE + '; line-height: 1;">&#8594;</span>'
          '<span style="font-size: 34px; font-weight: 500; letter-spacing: -0.01em; color: '
          + TENUE + ';">grande</span>'
          "</div>")

# L9 — el globo de comentario. El CTA de la pieza es un comentario, no un DM.
COMENTARIO = """    <svg width="132" height="112" viewBox="0 0 132 112" aria-hidden="true">
      <path d="M12 8 H120 A8 8 0 0 1 128 16 V74 A8 8 0 0 1 120 82 H60 L34 106 V82 H12 A8 8 0 0 1 4 74 V16 A8 8 0 0 1 12 8 Z"
            fill="none" stroke="{acento}" stroke-width="5" stroke-linejoin="round"></path>
      <g fill="{acento}">
        <circle cx="40" cy="45" r="7"></circle>
        <circle cx="66" cy="45" r="7"></circle>
        <circle cx="92" cy="45" r="7"></circle>
      </g>
    </svg>""".format(acento=ACENTO)


# ── Las diez láminas ──────────────────────────────────────────────────
# `texto` es literal del borrador; el marcado solo colorea, no reescribe.
# `arriba` va antes del titular, `abajo` después.
LAMINAS = [
    dict(
        id="01", eyebrow="( postura )", tam=94, ancho=15, accion="desliza &#8594;",
        marca=False,
        texto=tenue("No necesitas un ERP médico.") + " Necesitas que alguien "
              + ac("reagende") + ".",
        nota="L1 gancho. Fondo oscuro, sin logo, una sola idea. Lo que NO hace "
             "falta va apagado; lo que sí, encendido. Ese contraste es la pieza.",
    ),
    dict(
        id="02", eyebrow="02 / 09", tam=60, ancho=21,
        texto="Compras el sistema completo. El paciente sigue sin volver a su "
              "segunda sesión.",
        abajo=MODULOS,
        nota="L2. Los cuatro módulos del ERP apagados; 'reagendado' encendido y "
             "a lo ancho: es el único que mueve el ingreso.",
    ),
    dict(
        id="03", eyebrow="03 / 09", tam=62, ancho=20,
        texto="El dolor real casi nunca es tan grande como el sistema que se compra.",
        abajo=CAJAS,
        nota="L3. Dos cajas de tamaño desigual, a escala: la compra contra el dolor.",
    ),
    dict(
        id="04", eyebrow="04 / 09", tam=58, ancho=21,
        texto="En tratamientos por sesión, el ingreso depende de que el paciente "
              "vuelva.",
        abajo=CALENDARIO,
        nota="L4. Calendario con tres sesiones; la segunda, en duda. Redactada en "
             "tercera persona: lógica de negocio, no observación de clínicas.",
    ),
    dict(
        id="05", eyebrow="05 / 09", tam=54, ancho=23,
        texto="Pasa igual en control prenatal y esquemas de vacunación: son citas "
              "de seguimiento.",
        abajo=LINEA_TIEMPO,
        nota="L5. Línea de tiempo con puntos de control; el hueco es la cita perdida.",
    ),
    dict(
        id="06", eyebrow="06 / 09", tam=80, ancho=17,
        texto="Comprar el sistema completo antes de arreglar el reagendado es pagar "
              + ac("la demo") + ".",
        nota="L6. Frase destacada, sin ícono. El acento cae en lo que de verdad "
             "se está comprando.",
    ),
    dict(
        id="07", eyebrow="07 / 09", tam=56, ancho=22,
        texto="Empieza por lo chico. Decide con evidencia si hace falta algo más "
              "grande.",
        abajo=FLECHA,
        nota="L7. Jerarquía invertida a propósito: 'chico' grande y encendido, "
             "'grande' chico y atenuado.",
    ),
    dict(
        id="08", eyebrow="08 / 09", tam=94, ancho=15,
        texto="El problema no es tu sistema de agenda. Es " + ac("el reagendado") + ".",
        nota="L8. Conclusión citable, sola y en el tamaño más grande del carrusel.",
    ),
    dict(
        id="09", eyebrow="09 / 09", tam=70, ancho=18, centro=True,
        accion="unattended.io",
        texto="Comenta 'reagendar' si quieres ver cómo se arma esto.",
        arriba=COMENTARIO,
        nota="L9 CTA. Globo de comentario en teal, texto centrado.",
    ),
    dict(
        id="10", eyebrow="( unattended )", tam=46, ancho=36, centro=True,
        texto="unattended.io &#8212; automatización y datos para operaciones "
              "reales, no para demos.",
        nota="L10, opcional. Lámina de marca: wordmark y una sola frase sobre "
             "fondo oscuro.",
    ),
]


def escribe(l):
    centro = l.get("centro", False)
    cuerpo = "\n".join(
        p for p in (l.get("arriba", ""),
                    titular(l["texto"], l["tam"], l["ancho"], centro),
                    l.get("abajo", "")) if p)
    html = PLANTILLA.format(
        id=PREFIJO + l["id"], nota=l["nota"], lado=LADO, bg=BG, tinta=TINTA,
        etiqueta=ETIQUETA, sans=SANS, mono=MONO, eyebrow=l["eyebrow"],
        cuerpo=cuerpo, accion=l.get("accion", ""),
        alinea="center" if centro else "left",
        alinea_caja="center" if centro else "flex-start",
        marca=MARCA if l.get("marca", True) else "<span></span>")
    ruta = AQUI / (PREFIJO + l["id"] + ".html")
    io.open(ruta, "w", encoding="utf-8").write(html)
    return ruta


def render(ruta, indice):
    destino = SALIDA / (ruta.stem + ".png")
    # Perfil propio por llamada: dos Chrome seguidos se pelean por el mismo
    # y el segundo falla sin decir nada.
    r = subprocess.run(
        [CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
         "--user-data-dir=" + str(TMP / ("perfil-" + str(indice))),
         "--force-device-scale-factor=1",
         "--window-size=%d,%d" % (LADO, LADO),
         "--virtual-time-budget=15000",
         "--screenshot=" + str(destino),
         "file:///" + str(ruta).replace("\\", "/")],
        capture_output=True, text=True, timeout=180)
    salida = (r.stdout or "") + (r.stderr or "")
    if "written to file" not in salida:
        raise SystemExit("falló " + ruta.name + ": " + salida[-400:])
    print("  ok  " + destino.name + "   %dx%d" % (LADO, LADO))


if __name__ == "__main__":
    SALIDA.mkdir(exist_ok=True)
    TMP.mkdir(exist_ok=True)
    print("\n  %d láminas -> PNG\n" % len(LAMINAS))
    for i, lam in enumerate(LAMINAS):
        render(escribe(lam), i)
    shutil.rmtree(TMP, ignore_errors=True)
    print("\n  En " + str(SALIDA) + "\n")
