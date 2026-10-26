# Radar Inmobiliario — prueba de datos reales

Esta versión **no incluye datos ficticios**. Descarga indicadores de comunidades autónomas de Viviendómetro, con atribución CC BY 4.0. Los datos de compraventa declarada proceden del Colegio de Registradores; los de alquiler, de portales inmobiliarios según la comunidad. No son homogéneos: la rentabilidad bruta es orientativa.

## Probar
1. Ejecuta `python actualizar.py` (requiere conexión a Internet).
2. Ejecuta `python -m http.server 8000` en esta carpeta.
3. Abre `http://localhost:8000`.

También puedes subir los archivos a un repositorio público de GitHub y activar GitHub Pages (rama main, raíz). GitHub Actions intentará actualizar los datos los lunes; requiere permisos de escritura para Actions. No garantiza la continuidad de fuentes externas. Si falla la ingesta, el script termina con error y no fabrica datos.

La web intenta cargar primero `data/viviendometro-ccaa.json` y después la fuente externa. En entornos con CORS restrictivo, la copia local es la vía fiable.

## Limitaciones
Sin anuncios, barrios, histórico real temporal ni alertas por email. Las variaciones anuales proceden de la fuente, no se han construido series temporales. El fichero de actualización registra fecha de descarga separada de la fecha estadística.

Fuentes: https://www.viviendometro.es/datos/ y https://www.viviendometro.es/metodologia/
