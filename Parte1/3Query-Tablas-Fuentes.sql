---Parte 1. Modelado y Arquitectura de Datos (Teórico - Diseño)
USE bancoBogotaColombia;
GO

--Crear Tablas 

CREATE TABLE dim.Ciudad (
    id_ciudad      INT PRIMARY KEY,
    ciudad         VARCHAR(100)      NOT NULL,
)
GO


CREATE TABLE dim.Producto (
    id_producto     INT PRIMARY KEY,
    tipo_producto   VARCHAR(50)       NOT NULL, 
)
GO


CREATE TABLE dim.Tiempo (
    id_tiempo   INT PRIMARY KEY,   -- formato YYYYMMDD, no autoincremental
    fecha       DATE NOT NULL,
    anno        INT NOT NULL,
    mes         INT NOT NULL,
    dia         INT NOT NULL,
    trimestre   VARCHAR(60) NOT NULL,
    nombre_mes  VARCHAR(60) NOT NULL,
    dia_semana  VARCHAR(60) NOT NULL,
)
GO


CREATE TABLE dim.Cliente (
    id_cliente             INT PRIMARY KEY,
    tipo_identificacion    VARCHAR(60)       NOT NULL,
    numero_identificacion  VARCHAR(60)       NOT NULL, 
    nombres                VARCHAR(200)      NOT NULL,
    fecha_nacimiento       DATE              NULL,
    direccion              VARCHAR(200)      NULL,
    telefono               VARCHAR(60)       NULL,
    correo                 VARCHAR(150)      NULL,
    id_ciudad              INT FOREIGN KEY REFERENCES dim.Ciudad(id_ciudad)
                               ON DELETE NO ACTION
                               ON UPDATE NO ACTION
)
GO



CREATE TABLE fact.Transacciones (
    id_transaccion      BIGINT PRIMARY KEY,
    id_cliente          INT FOREIGN KEY REFERENCES dim.Cliente(id_cliente)
                            ON DELETE NO ACTION
                            ON UPDATE NO ACTION,
    id_producto         INT FOREIGN KEY REFERENCES dim.Producto(id_producto)
                            ON DELETE NO ACTION
                            ON UPDATE NO ACTION,
    id_tiempo           INT FOREIGN KEY REFERENCES dim.Tiempo(id_tiempo)
                            ON DELETE NO ACTION
                            ON UPDATE NO ACTION,
    tipo_transaccion    VARCHAR(50)    NOT NULL,
    monto_transaccion   DECIMAL(18,2)  NOT NULL,
    numero_cuenta       BIGINT NOT NULL,
    fecha_carga         DATETIME       NULL DEFAULT (GETDATE()),  
    batch_id            VARCHAR(50)    NULL                           
)
GO

CREATE TABLE fact.ReporteRiesgo (
    id_reporte              BIGINT PRIMARY KEY,
    id_cliente              INT FOREIGN KEY REFERENCES dim.Cliente(id_cliente)
                                ON DELETE NO ACTION
                                ON UPDATE NO ACTION,
    id_tiempo               INT FOREIGN KEY REFERENCES dim.Tiempo(id_tiempo)
                                ON DELETE NO ACTION
                                ON UPDATE NO ACTION,
    reporte_central_riesgo  VARCHAR(100)   NULL,
    monto_reporte           DECIMAL(18,2)  NULL,
    tiempo_mora             VARCHAR(50)    NULL,
    fecha_carga             DATETIME       NOT NULL DEFAULT (GETDATE()), 
    batch_id                VARCHAR(50)    NULL                           
)
GO

 ---By Juan Castillo Amaya
