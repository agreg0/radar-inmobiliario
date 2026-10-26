"""Descarga indicadores y conserva observaciones por fecha real de publicación."""
import datetime as dt
import json
import pathlib
import urllib.request

BASE = "https://www.viviendometro.es/data/"
FILES = ("viviendometro-ccaa.json", "precio-compra-ccaa.json")
OUT = pathlib.Path(__file__).resolve().parent / "data"
OUT.mkdir(exist_ok=True)
TODAY = dt.datetime.now(dt.timezone.utc).isoformat()

def get_json(filename):
    request = urllib.request.Request(BASE + filename, headers={"User-Agent": "RadarInmobiliarioResearch/2.0"})
    with urllib.request.urlopen(request, timeout=35) as response:
        return json.load(response)

downloaded = {}
for filename in FILES:
    downloaded[filename] = get_json(filename)

ccaa = downloaded["viviendometro-ccaa.json"]
rows = ccaa.get("comunidades", [])
if len(rows) < 17 or not all(isinstance(x, dict) and x.get("id") and x.get("comunidad") for x in rows):
    raise ValueError("Formato inesperado: comunidades")
if len(downloaded["precio-compra-ccaa.json"].get("datos", {})) < 15:
    raise ValueError("Formato inesperado: precio de compra")

source_date = ccaa.get("meta", {}).get("generado")
if not isinstance(source_date, str):
    raise ValueError("Falta fecha de generación de la fuente")
dt.date.fromisoformat(source_date)

for filename, data in downloaded.items():
    (OUT / filename).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

history_path = OUT / "historico-observaciones.json"
history = {"version": 1, "observaciones": []}
if history_path.exists():
    history = json.loads(history_path.read_text(encoding="utf-8"))
observations = history.get("observaciones", [])
if not isinstance(observations, list):
    raise ValueError("Histórico inválido")
if not any(x.get("fecha_fuente") == source_date for x in observations):
    observations.append({
        "fecha_fuente": source_date,
        "fecha_primera_descarga_utc": TODAY,
        "fuente": BASE + "viviendometro-ccaa.json",
        "territorios": [{
            "id": x["id"],
            "comunidad": x["comunidad"],
            "precio_compra_eur_m2": x.get("precio_compra_eur_m2"),
            "alquiler_eur_m2": x.get("alquiler_eur_m2"),
            "precio_compra_var_anual_pct": x.get("precio_compra_var_anual_pct"),
            "alquiler_var_interanual_pct": x.get("alquiler_var_interanual_pct")
        } for x in rows]
    })
    observations.sort(key=lambda x: x["fecha_fuente"])
    print("Nueva observación histórica:", source_date)
else:
    print("La fuente no ha cambiado; sin duplicar el histórico:", source_date)
history_path.write_text(json.dumps({"version": 1, "observaciones": observations}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(OUT / "ultima_actualizacion.json").write_text(json.dumps({
    "descargado_utc": TODAY, "fecha_fuente": source_date, "origen": BASE,
    "observaciones_historicas": len(observations)
}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Descarga válida:", len(rows), "territorios; histórico:", len(observations))
