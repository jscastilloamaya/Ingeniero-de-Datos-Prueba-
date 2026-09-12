---Parte 1. Modelado y Arquitectura de Datos (Teórico - Diseño)
USE bancoBogotaColombia;
GO

--Crear Esquemas (Schemas)
/*
Nota importante:
Inicialmente pensaba en crear los schemas por dominio de negocio: cliente, transacciones, productos y riesgo_crediticio.
Pero por facilidad y por como lo describe la guia, como modelo dimensiona lo dejo con hechos y dimensiones.
*/
CREATE SCHEMA dim;
GO

CREATE SCHEMA fact;
GO

 ---By Juan Castillo Amaya
