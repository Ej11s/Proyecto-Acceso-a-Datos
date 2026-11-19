# Sistema Web de Consulta y Analisis de Datos Abiertos de Colombia

## Objetivo
Aplicacion web (Flask + MVC) que consume una API publica de datos.gov.co, guarda los
registros en SQL Server sin duplicarlos y permite consultarlos, filtrarlos y ver un
resumen numerico desde el navegador.

## Dataset elegido
- **Nombre:** Casos positivos de COVID-19 en Colombia (Ministerio de Salud / INS)
- **Proposito:** practicar consumo de API, persistencia y consulta de datos reales.
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
- **Modelo:** `models/datos_model.py` (conexion pyodbc, INSERT sin duplicados, SELECT, resumen).
- **Vista:** `templates/index.html` y `static/estilos.css` (solo presentan datos, sin SQL).
- **Controlador:** `app.py` (rutas `/` y `/sincronizar`; coordina `api/api_client.py` y el modelo).
- **Servicio:** `api/api_client.py` (comunicacion con la API externa).

## Prevención de duplicados
`id_api` es UNIQUE y además se verifica con `IF NOT EXISTS` antes de insertar.

## Seguridad
`.env` no se sube al repositorio; consultas parametrizadas (`?`); `debug=True` solo en local.

## Integrantes y responsabilidades
- **Samuel Camelo– API y datos**
   Tuve la responsabilidad de investigar y escoger el conjunto de datos abiertos que utilizariamos para el proyecto, seguidamente despues de ver varios cojunto de datos y compararlos les presente opciones a mis compañeros y decidimos trabajar con el cojunto de datos de casos positivos de COVID-19 en colombia, ya que este cumplia con los requisitos para trabajar la actividad.
   
   Por otra parte, tambien me encargue de revisar la documentacion de la API y analizar la estructura de datos que te habia, teniendo en cuenta eso, seleccione los campos que podriamos utilizar dentro del sistema, los que escogi fueron:
   - el identificador del caso (id_de_caso).
   - el municipio (ciudad_municipio_nom).
   - el departamento (departamento_nom).
   - tambien otros como el sexo, edad y el estado del paciente

   estos campos fueron los que se selecciono para tener en cuenta y luego almacenarlos en la base de datos y asi mostrarlos luego en la aplicacion, ademas, tambien ayude en el desarrollo del archivo api_client.py que se encargaba de realizar la conexion con la API.

- **Emanuel Barriga– SQL Server y Modelo**
   Yo estuve a cargo de diseñar y construir la base de datos utilizada en el proyecto, teniendo en cuenta la informacion que utilizariamos, como que campos eran necesarios para almacenar la informacion que mi compañero me compartio que seria la que utilizariamos de la API, ahora bien, a partir de eso cree la base de datos DatosAbiertosDB y la tabla RegistrosAPI y una vez esto cree las columnas necesarias para guardar la informacion que mi compañero me compartio como: el identificador del caso, municipio, departamento, sexo, edad, estado y fecha de reporte.

   Tambien ayude con el desarrollo del archivo datos_model.py que fue donde se implementaron las funciones que se encargarian de guardar los registros obtenidos de la API, hacer que no se registraran datos duplicados y todo aquello que hiciera posible realizar las consultas necesarias para mostrar la informacion al usuario.

- **Ever Lozano – Controlador y Vista**
   Yo me encargue de realizar la parte visible de aplicacion y integrar todos los componentes para que la aplicacion funcionara correctamente, por lo tanto, se puede decir que mi trabajo consistio en construir la interfaz web que componen los archivos index.html y estilos.css, lo cual es una interfaz sencilla que permitiria al usuario consultar la informacion almacenada y realizar busquedas por municipio o departamento y que luego esta se visualice de forma organizada en una tabla.

- **Trabajo en equipo**
   El trabajo en equipo que realizamos todos fue organizar todo nuestro proyecto uniendo todas las partes que el equipo trabajo individualmente, entre ellos se trabajo archivos como el de app.py que es el controlador principal de la aplicacion, que se encargaba de implementar todas las rutas necesarias para mostrar los datos en pantalla y ejecutar el proceso de sincronizacion con la API, entonces dicho de otro modo, hubo cosas que se pudieron hacer indivualmente pero hubo otras en las que teniamos que coordinarnos, por eso todos trabajamos en la integracion de todos los trabajos que se realizaron de modo que era necesario verificar que la comunicacion entre la API, la base de datos y la interfaz funcionara correctamente, por eso fue facil detectar los errores durante la integracion y pudimos cumplir con los requisitos de la actividad. 

# Evidencias del proyecto

### Evidencia 1: respuesta JSON de la API
![Evidencia 1](evidencias/evidencia%201.jpeg)

### Evidencia 2: registros almacenados en SQL Server
![Evidencia 2](evidencias/evidencia%202.jpeg)

### Evidencia 3: captura de la pagina principal
![Evidencia 3](evidencias/evidencia%203.jpeg)

### Evidencia 4: captura de la sincronizacion
![Evidencia 4](evidencias/evidencia%204.jpeg)

### Evidencia 5: captura de la consulta filtrada
![Evidencia 5](evidencias/evidencia%205.jpeg)
