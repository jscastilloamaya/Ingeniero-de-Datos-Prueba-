---Parte 1. Modelado y Arquitectura de Datos (Teórico - Diseño)

---Crear Base de datos Banco de Bogota
CREATE DATABASE bancoBogotaColombia
ON
(
    NAME = bancoBogotaColombia_dat,
    FILENAME = 'C:\Users\jcast\Desktop\Pruebas Tecnicas\Banco de Bogota\Ingeniero de datos\Parte 1\bancoBogotaColombia_dat.mdf',
    SIZE = 10MB,
    MAXSIZE = 100MB,
    FILEGROWTH = 10MB
)
LOG ON
(
    NAME = bancoBogotaColombia_log,
    FILENAME = 'C:\Users\jcast\Desktop\Pruebas Tecnicas\Banco de Bogota\Ingeniero de datos\Parte 1\bancoBogotaColombia_log.ldf',
    SIZE = 10MB,
    MAXSIZE = 100MB,
    FILEGROWTH = 10MB
);

---By Juan Castillo Amaya

