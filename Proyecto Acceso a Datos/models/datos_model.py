import os
import json
import pyodbc
from dotenv import load_dotenv

load_dotenv()


def obtener_conexion():
    servidor = os.getenv("DB_SERVER")
    base_datos = os.getenv("DB_NAME")
    driver = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server")
    trusted = os.getenv("DB_TRUSTED", "yes").lower() == "yes"

    if trusted:
        cadena = (
            f"DRIVER={{{driver}}};"
            f"SERVER={servidor};"
            f"DATABASE={base_datos};"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
        )
    else:
        usuario = os.getenv("DB_USER")
        clave = os.getenv("DB_PASSWORD")
        cadena = (
            f"DRIVER={{{driver}}};"
            f"SERVER={servidor};"
            f"DATABASE={base_datos};"
            f"UID={usuario};PWD={clave};"
            "TrustServerCertificate=yes;"
        )
    return pyodbc.connect(cadena)


def _a_entero(valor):
    try:
        return int(float(valor))
    except (TypeError, ValueError):
        return None


def guardar_registros(registros):
    """Inserta los registros de la API evitando duplicar id_api."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    insertados = 0

    try:
        for registro in registros:
            identificador = str(registro.get("id_de_caso") or "").strip()
            if not identificador:
                continue

            fecha = (registro.get("fecha_reporte_web") or "")[:10] or None

            cursor.execute(
                """
                IF NOT EXISTS (
                    SELECT 1 FROM RegistrosAPI WHERE id_api = ?
                )
                INSERT INTO RegistrosAPI
                    (id_api, municipio, departamento, sexo, edad,
                     estado, fecha_registro, json_original)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                identificador,
                identificador,
                registro.get("ciudad_municipio_nom"),
                registro.get("departamento_nom"),
                registro.get("sexo"),
                _a_entero(registro.get("edad")),
                registro.get("estado"),
                fecha,
                json.dumps(registro, ensure_ascii=False),
            )
            if cursor.rowcount > 0:
                insertados += 1

        conexion.commit()
        return insertados
    except Exception:
        conexion.rollback()
        raise
    finally:
        cursor.close()
        conexion.close()


_COLUMNAS = "id_api, municipio, departamento, sexo, edad, estado, fecha_registro"


def consultar_registros(filtro=""):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        if filtro:
            cursor.execute(
                f"""
                SELECT TOP 100 {_COLUMNAS}
                FROM RegistrosAPI
                WHERE municipio LIKE ? OR departamento LIKE ?
                ORDER BY id DESC
                """,
                f"%{filtro}%",
                f"%{filtro}%",
            )
        else:
            cursor.execute(
                f"SELECT TOP 100 {_COLUMNAS} FROM RegistrosAPI ORDER BY id DESC"
            )

        columnas = [c[0] for c in cursor.description]
        return [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
    finally:
        cursor.close()
        conexion.close()


def obtener_resumen(filtro=""):
    """Resumen numérico básico: total, edad promedio y casos por sexo."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        donde = "WHERE municipio LIKE ? OR departamento LIKE ?" if filtro else ""
        params = [f"%{filtro}%", f"%{filtro}%"] if filtro else []

        cursor.execute(
            f"""
            SELECT COUNT(*) AS total,
                   AVG(CAST(edad AS FLOAT)) AS edad_promedio,
                   SUM(CASE WHEN sexo = 'F' THEN 1 ELSE 0 END) AS mujeres,
                   SUM(CASE WHEN sexo = 'M' THEN 1 ELSE 0 END) AS hombres
            FROM RegistrosAPI {donde}
            """,
            *params,
        )
        fila = cursor.fetchone()
        return {
            "total": fila.total or 0,
            "edad_promedio": round(fila.edad_promedio, 1) if fila.edad_promedio else 0,
            "mujeres": fila.mujeres or 0,
            "hombres": fila.hombres or 0,
        }
    finally:
        cursor.close()
        conexion.close()
