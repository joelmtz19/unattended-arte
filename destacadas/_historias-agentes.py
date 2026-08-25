# Genera las historias destacadas de los cinco agentes.
#
# Cada una abre nombrando el momento en que pierdes y después dice qué hace el
# agente con él — la misma forma que ya tienen las fichas del sitio. En una
# historia se leen dos segundos: si la primera línea no duele, no hay segunda.
#
# 1080x1920 con 300 px arriba y 384 abajo: es lo que tapa la interfaz de
# Instagram (el nombre de la cuenta arriba, la caja de responder abajo). Todo
# lo que importa vive en la franja de en medio.
#
#   python _historias-agentes.py
#
# Deja los PNG en ../img/. Necesita Chrome; no hay ImageMagick en esta máquina.

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
TMP = os.path.join(AQUI, "_tmp")

AGENTES = [
    {
        "slug": "lead-tracker",
        "n": "01",
        "dolor": "el lead del sábado a las diez de la noche se contesta el lunes.",
        "nombre": "Lead Tracker",
        "hace": "Contesta en el momento en que entra, a la hora que entre. Y vuelve solo sobre el que no cerró.",
        "no": "No negocia condiciones. Eso lo pasa a una persona.",
    },
    {
        "slug": "onboarding-bot",
        "n": "02",
        "dolor": "el mismo dato, tecleado tres veces.",
        "nombre": "Onboarding Bot",
        "hace": "Lo levanta una sola vez en la conversación, lo valida ahí mismo y lo deja en tu sistema.",
        "no": "Si el RFC no pasa, lo devuelve en el momento. No lo guarda para después.",
    },
    {
        "slug": "report-agent",
        "n": "03",
        "dolor": "dos áreas llegan a la junta con dos números del mismo mes.",
        "nombre": "Report Agent",
        "hace": "Arma el reporte solo, a la misma hora, y te dice de dónde salió cada cifra.",
        "no": "Cuando dos archivos no cuadran, no escoge uno: desarma la diferencia.",
    },
    {
        "slug": "support-l1",
        "n": "04",
        "dolor": "cinco preguntas repetidas todo el día, contestadas por quien esté libre.",
        "nombre": "Support L1",
        "hace": "Responde eso a cualquier hora, con el contexto ya recogido.",
        "no": "Lo que se sale del guion lo escala a una persona, sin que el cliente repita nada.",
    },
    {
        "slug": "data-entry",
        "n": "05",
        "dolor": "el dígito mal leído aparece semanas después, cuando algo no cuadra.",
        "nombre": "Data Entry",
        "hace": "Extrae, normaliza y valida en el momento en que el documento llega.",
        "no": "Si un dato no se lee con certeza, se detiene y lo manda a revisión.",
    },
]

CAB = """<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400&display=swap">
<style>
  *{box-sizing:border-box} body{margin:0}
  .h{width:1080px;height:1920px;padding:300px 90px 384px;display:flex;
     flex-direction:column;font-family:Archivo,Helvetica,Arial,sans-serif}
  .claro{background:#fbfbfd;color:#1d1d1f}
  .oscuro{background:#0f0f10;color:#f4f1ea}
  .etq{font-family:'IBM Plex Mono',monospace;font-size:24px;letter-spacing:.16em;color:#6e6e73}
  .oscuro .etq{color:rgba(244,241,234,.55)}
  .medio{flex-grow:1;display:flex;flex-direction:column;justify-content:center;gap:44px}
  h1{margin:0;font-weight:700;font-size:76px;line-height:1.06;letter-spacing:-.04em;max-width:15ch}
  .nombre{font-weight:700;font-size:46px;letter-spacing:-.03em;color:#0f6862}
  .oscuro .nombre{color:#7ad0c6}
  p{margin:0;font-size:38px;line-height:1.45;color:#57575c;max-width:22ch}
  .limite{border-left:6px solid #0f6862;padding-left:28px;font-size:32px;
          line-height:1.4;color:#57575c;max-width:24ch}
  .marca{font-weight:700;font-size:34px;letter-spacing:-.03em}
  .barra{color:#0f6862} .oscuro .barra{color:#7ad0c6}
</style></head><body>"""


def portada():
    return f"""{CAB}
<div class="h oscuro">
  <span class="etq">( destacada )</span>
  <div class="medio">
    <h1>cinco agentes,<br>y lo que <span style="color:#7ad0c6">no hace</span> cada uno.</h1>
    <p style="color:rgba(244,241,234,.72)">Lead Tracker · Onboarding Bot · Report Agent · Support L1 · Data Entry</p>
  </div>
  <span class="marca">unattended<span class="barra">|</span></span>
</div></body></html>"""


def historia(a):
    return f"""{CAB}
<div class="h claro">
  <span class="etq">( agente {a['n']} )</span>
  <div class="medio">
    <h1>{a['dolor']}</h1>
    <div>
      <div class="nombre">{a['nombre']}</div>
      <p style="margin-top:16px">{a['hace']}</p>
    </div>
    <div class="limite">{a['no']}</div>
  </div>
  <span class="marca">unattended<span class="barra">|</span></span>
</div></body></html>"""


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
    print("\n  Historias destacadas — agentes\n")
    render("destacada-agentes-portada", portada())
    for a in AGENTES:
        render(f"destacada-agente-{a['slug']}", historia(a))
    print(f"\n  En {SALIDA}")
    print("  Súbelas como historias y agrégalas a la destacada «Agentes».")
    print("  La API de Instagram no puede crear destacadas: eso es a mano.\n")
