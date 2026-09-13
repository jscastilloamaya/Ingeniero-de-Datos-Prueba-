---Parte 1. Modelado y Arquitectura de Datos (Teórico - Diseño)

---Crear Base de datos Banco de Bogota
CREATE DATABASE bancoBogotaColombia
ON
(
    NAME = bancoBogotaColombia_dat,
    FILENAME = 'C:\Master en SQL Server\bancoBogotaColombia_dat.mdf',
    SIZE = 10MB,
    MAXSIZE = 100MB,
    FILEGROWTH = 10MB
)
LOG ON
(
    NAME = bancoBogotaColombia_log,
    FILENAME = 'C:\Master en SQL Server\bancoBogotaColombia_log.ldf',
    SIZE = 10MB,
    MAXSIZE = 100MB,
    FILEGROWTH = 10MB
);

---By Juan Castillo Amaya

