import json, urllib.request, datetime, pathlib, sys
BASE='https://www.viviendometro.es/data/'
FILES=['viviendometro-ccaa.json','precio-compra-ccaa.json']
out=pathlib.Path(__file__).parent/'data';out.mkdir(exist_ok=True)
for name in FILES:
    req=urllib.request.Request(BASE+name,headers={'User-Agent':'RadarInmobiliarioResearch/1.0'})
    with urllib.request.urlopen(req,timeout=35) as r: data=json.load(r)
    if name.startswith('viviendometro'):
        rows=data.get('comunidades',[])
        if len(rows)<17 or not all('comunidad' in x for x in rows):raise ValueError('Formato inesperado de comunidades')
    else:
        if len(data.get('datos',{}))<15:raise ValueError('Formato inesperado de precios')
    (out/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    print('OK',name)
(out/'ultima_actualizacion.json').write_text(json.dumps({'descargado_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'origen':BASE},indent=2))
