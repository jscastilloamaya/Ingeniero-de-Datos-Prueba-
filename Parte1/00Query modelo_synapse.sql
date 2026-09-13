---Parte 1. Modelado y Arquitectura de Datos (Teórico - Diseño) Synapse

IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'dim') EXEC('CREATE SCHEMA dim');
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'fact') EXEC('CREATE SCHEMA fact');
GO


   ---1. DIMENSIONES PEQUEÑAS (replicadas)

CREATE TABLE dim.Ciudad (
    id_ciudad    INT NOT NULL,
    ciudad       VARCHAR(100) NOT NULL,
    CONSTRAINT PK_dim_Ciudad PRIMARY KEY NONCLUSTERED (id_ciudad) NOT ENFORCED
)
WITH (
    DISTRIBUTION = REPLICATE,
    CLUSTERED COLUMNSTORE INDEX
);
GO

CREATE TABLE dim.Producto (
    id_producto   INT NOT NULL,
    tipo_producto VARCHAR(50) NOT NULL,
    CONSTRAINT PK_dim_Producto PRIMARY KEY NONCLUSTERED (id_producto) NOT ENFORCED
)
WITH (
    DISTRIBUTION = REPLICATE,
    CLUSTERED COLUMNSTORE INDEX
);
GO

CREATE TABLE dim.Tiempo (
    id_tiempo   INT NOT NULL,
    fecha       DATE NOT NULL,
    anno        INT NOT NULL,
    mes         INT NOT NULL,
    dia         INT NOT NULL,
    trimestre   VARCHAR(2) NOT NULL,
    nombre_mes  VARCHAR(20) NOT NULL,
    dia_semana  VARCHAR(20) NOT NULL,
    CONSTRAINT PK_dim_Tiempo PRIMARY KEY NONCLUSTERED (id_tiempo) NOT ENFORCED
)
WITH (
    DISTRIBUTION = REPLICATE,
    CLUSTERED COLUMNSTORE INDEX
);
GO

 ---  2. DIMENSION MEDIANAMENTE GRANDE  Distribuida por HASH(id_cliente) para alinear con las tablas de hechos y permitir joins co-localizados (sin movimiento de datos)

CREATE TABLE dim.Cliente (
    id_cliente            INT NOT NULL,
    tipo_identificacion   VARCHAR(20) NOT NULL,
    numero_identificacion VARCHAR(20) NOT NULL,
    nombres               VARCHAR(200) NOT NULL,
    fecha_nacimiento      DATE NULL,
    direccion             VARCHAR(200) NULL,
    telefono              VARCHAR(20) NULL,
    correo                VARCHAR(150) NULL,
    id_ciudad             INT NULL,
    CONSTRAINT PK_dim_Cliente PRIMARY KEY NONCLUSTERED (id_cliente) NOT ENFORCED
)
WITH (
    DISTRIBUTION = HASH(id_cliente),
    CLUSTERED COLUMNSTORE INDEX
);
GO

--- 3. TABLAS DE HECHOS Distribuidas por HASH(id_cliente) (co-localizadas con dim.Cliente), particionadas por id_tiempo (mensual) y con Ordered CCI sobre   id_cliente -> equivalente al PARTITION BY + CLUSTER BY de BigQuery
   
CREATE TABLE fact.Transacciones (
    id_transaccion    BIGINT NOT NULL,
    id_cliente        INT NOT NULL,
    id_producto       INT NOT NULL,
    id_tiempo         INT NOT NULL,
    tipo_transaccion  VARCHAR(50) NOT NULL,
    monto_transaccion DECIMAL(18,2) NOT NULL,
    numero_cuenta     BIGINT NOT NULL,
    fecha_carga       DATETIME  NULL,
    batch_id          VARCHAR(50) NULL,
    CONSTRAINT PK_fact_Transacciones PRIMARY KEY NONCLUSTERED (id_transaccion, id_tiempo) NOT ENFORCED
)
WITH (
    DISTRIBUTION = HASH(id_cliente),
    CLUSTERED COLUMNSTORE INDEX ORDER (id_cliente),
    PARTITION (
        id_tiempo RANGE RIGHT FOR VALUES (
            20240101, 20240201, 20240301, 20240401, 20240501, 20240601,
            20240701, 20240801, 20240901, 20241001, 20241101, 20241201
        )
    )
);
GO

CREATE TABLE fact.ReporteRiesgo (
    id_reporte              BIGINT NOT NULL,
    id_cliente              INT NOT NULL,
    id_tiempo               INT NOT NULL,
    reporte_central_riesgo  VARCHAR(100) NULL,
    monto_reporte           DECIMAL(18,2) NULL,
    tiempo_mora             VARCHAR(50) NULL,
    fecha_carga             DATETIME NULL,
    batch_id                VARCHAR(50) NULL,
    CONSTRAINT PK_fact_ReporteRiesgo PRIMARY KEY NONCLUSTERED (id_reporte, id_tiempo) NOT ENFORCED
)
WITH (
    DISTRIBUTION = HASH(id_cliente),
    CLUSTERED COLUMNSTORE INDEX ORDER (id_cliente),
    PARTITION (
        id_tiempo RANGE RIGHT FOR VALUES (
            20240101, 20240201, 20240301, 20240401, 20240501, 20240601,
            20240701, 20240801, 20240901, 20241001, 20241101, 20241201
        )
    )
);
GO
