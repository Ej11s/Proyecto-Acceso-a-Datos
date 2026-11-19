# Sistema Web de Consulta y Análisis de Datos Abiertos de Colombia

## Objetivo
Aplicación web (Flask + MVC) que consume una API pública de datos.gov.co, guarda los
registros en SQL Server sin duplicarlos y permite consultarlos, filtrarlos y ver un
resumen numérico desde el navegador.

## Dataset elegido
- **Nombre:** Casos positivos de COVID-19 en Colombia (Ministerio de Salud / INS)
- **Propósito:** practicar consumo de API, persistencia y consulta de datos reales.
- **Enlace:** https://www.datos.gov.co/Salud-y-Protecci-n-Social/Casos-positivos-de-COVID-19-en-Colombia/gt2j-8ykr
- **Endpoint (SODA):** `https://www.datos.gov.co/resource/gt2j-8ykr.json?$limit=100`

## Campos utilizados
| Campo API | Columna SQL | Significado |
|---|---|---|
| id_de_caso | id_api (UNIQUE) | Identificador del caso en la fuente (evita duplicados) |
| ciudad_municipio_nom | municipio | Municipio de residencia |
| departamento_nom | departamento | Departamento de residencia |
| sexo | sexo | F / M |
| edad | edad | Edad del paciente |
| estado | estado | Estado del caso (Leve, Moderado, Fallecido…) |
| fecha_reporte_web | fecha_registro | Fecha de reporte (AAAA-MM-DD) |
| (registro completo) | json_original | JSON original para no perder campos |

## Requisitos
Python 3.10+, SQL Server + SSMS, Microsoft ODBC Driver 18 for SQL Server, navegador.

## Instalación
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1      # Windows PowerShell
pip install -r requirements.txt
```
1. Ejecutar `script_bd.sql` en SSMS.
2. Copiar `.env.example` a `.env` y ajustar servidor/credenciales.

## Ejecución
```bash
python app.py
```
Abrir http://127.0.0.1:5000 → pulsar **Consultar API y guardar datos** → usar el buscador.

## Estructura MVC
- **Modelo:** `models/datos_model.py` (conexión pyodbc, INSERT sin duplicados, SELECT, resumen).
- **Vista:** `templates/index.html` y `static/estilos.css` (solo presentan datos, sin SQL).
- **Controlador:** `app.py` (rutas `/` y `/sincronizar`; coordina `api/api_client.py` y el modelo).
- **Servicio:** `api/api_client.py` (comunicación con la API externa).

## Prevención de duplicados
`id_api` es UNIQUE y además se verifica con `IF NOT EXISTS` antes de insertar.

## Seguridad
`.env` no se sube al repositorio; consultas parametrizadas (`?`); `debug=True` solo en local.
