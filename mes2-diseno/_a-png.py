"""Convierte los artboards de esta carpeta en PNG para Instagram.

Los `.dc.html` son artboards del lienzo de Claude Design: traen un `<x-dc>` y
un `support.js` que solo existen dentro del editor. Abiertos en Chrome a secas
no pintan nada.

Pero adentro de ese envoltorio el arte es HTML normal —un `<div>` de 1080×1080
con estilos en línea—, así que aquí se le quita la cáscara y se rinde el
contenido tal cual. **No se vuelve a dibujar el arte**: si se reescribiera
aparte, el día que alguien edite un artboard el PNG dejaría de corresponder y
nadie se daría cuenta hasta verlo publicado.

Correr desde esta carpeta:  python _a-png.py

Copia del de mes2-w37-w39: el arte de hotelería (W36) se había quedado solo
en artboards y nunca salió a PNG.

Deja los PNG en ../img/ con el prefijo `mes2-hotel-`.
"""

import io
import os
import pathlib
import re
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


def destripar(ruta: pathlib.Path) -> tuple[str, int, int]:
    """Saca de un .dc.html el `<helmet>` y el arte, y mide el lienzo."""
    s = io.open(ruta, encoding="utf-8").read()
    m = re.search(r"<helmet>(.*?)</helmet>", s, re.S)
    cabeza = m.group(1) if m else ""
    cuerpo = re.sub(r"<helmet>.*?</helmet>", "", s, flags=re.S)
    m2 = re.search(r"<x-dc>(.*?)</x-dc>", cuerpo, re.S)
    if not m2:
        raise SystemExit(f"{ruta.name}: no encontré el bloque <x-dc>")
    arte = m2.group(1).strip()
    med = re.search(r"width:\s*(\d+)px;\s*height:\s*(\d+)px", arte)
    if not med:
        raise SystemExit(f"{ruta.name}: no pude leer el tamaño del lienzo")
    return (f"<!doctype html><html><head><meta charset=\"utf-8\">{cabeza}"
            f"<style>html,body{{margin:0;padding:0}}</style></head><body>"
            f"{arte}</body></html>", int(med.group(1)), int(med.group(2)))


def render(ruta: pathlib.Path) -> None:
    html, ancho, alto = destripar(ruta)
    TMP.mkdir(exist_ok=True)
    SALIDA.mkdir(exist_ok=True)
    tmp_html = TMP / (ruta.stem + ".html")
    io.open(tmp_html, "w", encoding="utf-8").write(html)
    destino = SALIDA / f"mes2-hotel-{ruta.stem.lower()}.png"
    # Perfil propio por llamada: dos Chrome seguidos se pelean por el mismo y
    # el segundo falla sin decir nada.
    r = subprocess.run(
        [CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
         f"--user-data-dir={TMP / ('perfil-' + ruta.stem)}",
         "--force-device-scale-factor=1", f"--window-size={ancho},{alto}",
         "--virtual-time-budget=12000", f"--screenshot={destino}",
         "file:///" + str(tmp_html).replace("\\", "/")],
        capture_output=True, text=True, timeout=180)
    salida = (r.stdout or "") + (r.stderr or "")
    if "written to file" not in salida:
        raise SystemExit(f"falló {ruta.name}: {salida[-300:]}")
    print(f"  ✓ {destino.name}   {ancho}×{alto}")


if __name__ == "__main__":
    piezas = sorted(AQUI.glob("*.dc.html"))
    print(f"\n  {len(piezas)} artboards → PNG\n")
    for p in piezas:
        render(p)
    import shutil
    shutil.rmtree(TMP, ignore_errors=True)
    print(f"\n  En {SALIDA}\n")
