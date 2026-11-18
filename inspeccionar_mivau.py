"""Inspección reproducible del CSV oficial MIVAU antes de construir el importador.

Ejecutar: python inspeccionar_mivau.py
No altera datos ni publica series sin validar su esquema.
"""
import csv
import io
import urllib.request

URL = "https://cdn.mivau.gob.es/portal-web-mivau/Datos_MIVAU/CSV/VDP006_01.csv"
request = urllib.request.Request(URL, headers={"User-Agent": "RadarInmobiliarioResearch/3.0"})
with urllib.request.urlopen(request, timeout=90) as response:
    raw = response.read(30_000_000)
print("Fuente:", URL)
print("Bytes:", len(raw))
text = raw.decode("utf-8-sig", errors="replace")
lines = text.splitlines()
print("Primeras 8 líneas del CSV:")
for line in lines[:8]:
    print(repr(line[:500]))
try:
    dialect = csv.Sniffer().sniff("\n".join(lines[:10]), delimiters=";,\t|")
    reader = csv.reader(io.StringIO(text), dialect)
    for i, row in enumerate(reader):
        if i >= 5:
            break
        print("Fila", i, "columnas:", len(row), "valores:", row[:15])
except csv.Error as exc:
    print("No se ha podido inferir delimitador:", exc)
