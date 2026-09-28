"""Genera las piezas de arte de las semanas W38 y W39 del mes 2.

Las 21 piezas comparten anatomía —etiqueta arriba, titular al centro, acción y
marca abajo— así que escribirlas a mano sería copiar el mismo esqueleto veinte
veces y arriesgar que una quede desalineada. Aquí el esqueleto vive una vez.

Correr desde esta carpeta:  python _generar.py
"""

import pathlib

PLANTILLA = """<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;700&family=IBM+Plex+Mono:wght@400&display=swap">
  <style>
    body {{ margin: 0; font-family: Archivo, Helvetica, Arial, sans-serif; }}
    a {{ color: #0f6862; }} a:hover {{ color: #0b4f4a; }}
  </style>
</helmet>

<!-- {nota} -->
<div style="width: 1080px; height: 1080px; box-sizing: border-box; background: {bg}; color: {tinta}; padding: 90px; display: flex; flex-direction: column;">

  <span style="font-family: 'IBM Plex Mono', monospace; font-size: 21px; letter-spacing: 0.16em; color: {etiqueta};">{eyebrow}</span>

  <div style="flex-grow: 1; display: flex; flex-direction: column; justify-content: center; gap: 34px;">
    <h1 style="margin: 0; font-weight: 700; font-size: {tam}px; line-height: 1.05; letter-spacing: -0.04em; max-width: {ancho}ch;">{titular}</h1>
{extra}
  </div>

  <div style="display: flex; align-items: flex-end; justify-content: space-between; gap: 40px;">
    <span style="font-family: 'IBM Plex Mono', monospace; font-size: 21px; letter-spacing: 0.08em; color: {pie};">{accion}</span>
    <span style="font-weight: 700; font-size: 30px; letter-spacing: -0.03em;">unattended<span style="color: {acento};">|</span></span>
  </div>

</div>
</x-dc>
</body>
</html>
"""

OSC = dict(bg="#0f0f10", tinta="#f4f1ea", acento="#7ad0c6",
           etiqueta="rgba(244,241,234,.55)", pie="rgba(244,241,234,.55)")
CLA = dict(bg="#fbfbfd", tinta="#1d1d1f", acento="#0f6862",
           etiqueta="#6e6e73", pie="#6e6e73")


def ac(t, tema):
    return '<span style="color: ' + tema["acento"] + ';">' + t + "</span>"


def apoyo(txt, tema):
    if not txt:
        return ""
    c = "rgba(244,241,234,.72)" if tema is OSC else "#57575c"
    return ('    <p style="margin: 0; font-size: 34px; line-height: 1.45; color: '
            + c + '; max-width: 26ch;">' + txt + "</p>")


def escribe(nombre, tema, eyebrow, tam, ancho, titular,
            texto="", accion="", nota="", extra=None):
    pathlib.Path(nombre + ".dc.html").write_text(
        PLANTILLA.format(
            nota=nota or "Pieza del mes 2.", eyebrow=eyebrow, tam=tam,
            ancho=ancho, titular=titular,
            extra=extra if extra is not None else apoyo(texto, tema),
            accion=accion, **tema),
        encoding="utf-8")
    return nombre


hechas = []

# ═══ W38 · AGENCIAS AUTOMOTRICES ══════════════════════════════════════
hechas += [
    escribe("A0", OSC, "( embudo )", 92, 15,
            "no te faltan leads. " + ac("se te van", OSC) + ".",
            "Y no por el embudo: por lo que hay debajo.", "desliza →",
            "Portada W38. Oscura para cortar el scroll."),
    escribe("A1", CLA, "01 / 05", 80, 17,
            "entran de cuatro portales distintos, todos a la vez.",
            "Y cada uno los deja en un lugar distinto."),
    escribe("A2", CLA, "02 / 05", 82, 16,
            "el DMS y el CRM " + ac("no se hablan", CLA) + ".",
            "Uno sabe qué unidad hay. El otro, de dónde vino el cliente. "
            "Ninguno sabe las dos cosas."),
    escribe("A3", CLA, "03 / 05", 74, 19,
            "pero el lead no se pierde entre ellos: se va por "
            + ac("un tercer lugar", CLA) + ".",
            "El WhatsApp personal del vendedor. Ahí se negocia, y ahí se queda."),
    escribe("A4", OSC, "04 / 05", 84, 16,
            "el CRM se queda " + ac("vacío", OSC) + ", y el reporte con él.",
            "Cuando el vendedor se va, el historial se va con él.",
            "", "Oscura: aquí cae el costo real."),
    escribe("A5", CLA, "05 / 05", 72, 20,
            "sin acción registrada → se marca estancado → "
            + ac("se escala", CLA) + ".",
            "No decide por el vendedor. Le quita al gerente perseguir "
            "actualizaciones a mano.",
            "diagnóstico gratis → unattended.io"),
]

# El embudo ya lleno, con la fuga lateral. La llave gotea arriba: entra más,
# pero se sale por un lado. Ese es el argumento entero, dibujado.
EMBUDO = """    <svg width="580" height="430" viewBox="0 0 580 430" aria-hidden="true">
      <path d="M132 74 L428 74 L322 214 L238 214 Z" fill="rgba(29,29,31,.10)"></path>
      <g fill="none" stroke="#1d1d1f" stroke-width="3">
        <path d="M120 60 L440 60 L320 220 L320 340 L240 380 L240 220 Z"></path>
      </g>
      <g stroke="#0f6862" stroke-width="6" stroke-linecap="round">
        <line x1="280" y1="8" x2="280" y2="32"></line>
      </g>
      <circle cx="280" cy="46" r="7" fill="#0f6862"></circle>
      <line x1="322" y1="200" x2="470" y2="252" stroke="#b4451f" stroke-width="5" stroke-linecap="round"></line>
      <circle cx="486" cy="258" r="9" fill="#b4451f"></circle>
      <text x="392" y="302" font-family="IBM Plex Mono, monospace" font-size="22" fill="#b4451f">se va por aquí</text>
    </svg>"""

hechas.append(escribe(
    "PosturaW38", CLA, "( postura )", 74, 19,
    "no necesitas más leads. necesitas "
    + ac("dejar de perder", CLA) + " los que ya tienes.",
    nota="Visual de LinkedIn W38, pieza 17 del plan: la llave goteando sobre "
         "un embudo que ya está lleno, con la fuga lateral marcada.",
    extra=EMBUDO))

# ═══ W39 · CONSULTORIOS Y DESPACHOS ═══════════════════════════════════
hechas += [
    escribe("D0", OSC, "( expediente )", 88, 16,
            "«¿cómo va mi caso?» " + ac("otra vez", OSC) + ".",
            "Y no preguntan por desconfianza.", "desliza →",
            "Portada W39."),
    escribe("D1", CLA, "01 / 05", 82, 16,
            "el expediente " + ac("no vive en un solo lugar", CLA) + ".",
            "Por eso nadie puede contestar sin ir a buscar primero."),
    escribe("D2", CLA, "02 / 05", 74, 19,
            "parte en el chat, parte en una carpeta, parte en "
            + ac("la cabeza de alguien", CLA) + ".",
            "Las tres versiones son ciertas. Ninguna está completa."),
    escribe("D3", OSC, "03 / 05", 84, 16,
            "el costo aparece cuando " + ac("esa persona no está", OSC) + ".",
            "Vacaciones, un día saturado, o una renuncia.",
            "", "Oscura: el golpe."),
    escribe("D4", CLA, "04 / 05", 74, 19,
            "una sola bitácora. " + ac("cuatro etapas", CLA)
            + ". visible de los dos lados.",
            "Recibido · En proceso · Esperando documento · Resuelto"),
    escribe("D5", CLA, "05 / 05", 78, 17,
            "cambia de etapa → " + ac("se avisa solo", CLA) + ".",
            "No decide el caso ni sustituye tu criterio. Quita el reporte a mano.",
            "diagnóstico gratis → unattended.io"),
]

# La bitácora con la notificación ya disparada en la tercera etapa. La cuarta
# va apagada a propósito: el caso sigue abierto, y así se ve.
BITACORA = """    <div style="display: flex; flex-direction: column; gap: 0; max-width: 780px;">
      <div style="display: flex; align-items: center; gap: 24px;"><div style="width:22px;height:22px;border-radius:99px;background:#0f6862;"></div><span style="font-size:36px;font-weight:700;letter-spacing:-.02em;">Recibido</span></div>
      <div style="width:3px;height:42px;background:#0f6862;margin-left:10px;"></div>
      <div style="display: flex; align-items: center; gap: 24px;"><div style="width:22px;height:22px;border-radius:99px;background:#0f6862;"></div><span style="font-size:36px;font-weight:700;letter-spacing:-.02em;">En proceso</span></div>
      <div style="width:3px;height:42px;background:#0f6862;margin-left:10px;"></div>
      <div style="display: flex; align-items: center; gap: 20px; flex-wrap: wrap;"><div style="width:22px;height:22px;border-radius:99px;background:#0f6862;"></div><span style="font-size:36px;font-weight:700;letter-spacing:-.02em;">Esperando documento</span><span style="border:2px solid #0f6862;border-radius:999px;padding:7px 18px;font-family:'IBM Plex Mono',monospace;font-size:19px;color:#0f6862;">aviso enviado</span></div>
      <div style="width:3px;height:42px;background:rgba(29,29,31,.12);margin-left:10px;"></div>
      <div style="display: flex; align-items: center; gap: 24px;"><div style="width:22px;height:22px;border-radius:99px;border:3px solid rgba(29,29,31,.18);box-sizing:border-box;"></div><span style="font-size:36px;color:#6e6e73;letter-spacing:-.02em;">Resuelto</span></div>
    </div>"""

hechas.append(escribe(
    "PosturaW39", CLA, "( cómo se hace )", 72, 20,
    "la bitácora que evita la llamada de "
    + ac("«¿cómo va mi caso?»", CLA),
    nota="Visual de LinkedIn W39, pieza 24 del plan: la bitácora con la "
         "notificación automática ya disparada.",
    extra=BITACORA))

print(str(len(hechas)) + " piezas escritas: " + ", ".join(hechas))
