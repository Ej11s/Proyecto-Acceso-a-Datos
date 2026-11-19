CREATE DATABASE DatosAbiertosDB;
GO

USE DatosAbiertosDB;
GO

CREATE TABLE RegistrosAPI (
    id             INT IDENTITY(1,1) PRIMARY KEY,
    id_api         NVARCHAR(100) NOT NULL UNIQUE,   -- id_de_caso (clave estable de la fuente)
    municipio      NVARCHAR(150) NULL,              -- ciudad_municipio_nom
    departamento   NVARCHAR(150) NULL,              -- departamento_nom
    sexo           NVARCHAR(10)  NULL,              -- sexo
    edad           INT           NULL,              -- edad
    estado         NVARCHAR(50)  NULL,              -- estado (Leve, Moderado, Fallecido...)
    fecha_registro NVARCHAR(50)  NULL,              -- fecha_reporte_web (AAAA-MM-DD)
    json_original  NVARCHAR(MAX) NULL,
    fecha_captura  DATETIME2 NOT NULL DEFAULT SYSDATETIME()
);
GO
