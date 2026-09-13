# Prueba Técnica — Ingeniería de Datos (Banco de Bogota)






# 📌 Parte 1: Modelado y Arquitectura de Datos (Teórico - Diseño)

## Instrucciones

1. **Dado el siguiente caso de negocio:**

   *Una entidad bancaria quiere analizar el comportamiento de sus clientes en productos financieros (cuentas de ahorro, tarjetas de crédito y créditos). Para ello, se requiere integrar datos de múltiples fuentes (transacciones, datos de clientes y riesgo crediticio) en un Data Warehouse implementado en GCP.*
   - Diseña un modelo dimensional (modelo estrella o copo de nieve) para el caso presentado.
   - Justifica tu elección del modelo, destacando sus ventajas para el análisis en entornos de BI y reporting.
   - Propón una estrategia de particionamiento y clustering que permita optimizar las consultas en BigQuery.
   - Describe cómo garantizarías la calidad y la gobernanza de los datos a lo largo del pipeline.
   - Explica qué mecanismos implementarías para asegurar la trazabilidad y auditoría de los datos procesados.

## Estructura del repositorio

```
parte1/
├── README.md
├── diagrama.png
├── arquitectura.png
├── P1Arquitectura.drawio
├── 01_sqlserver_crear_basedatos.sql
├── 02_sqlserver_crear_esquemas.sql
├── 03_sqlserver_crear_tablas.sql
└── 04_synapse_modelo_completo.sql
```


# 📌 Parte 2: Construcción de Pipeline ETL/ELT (Práctico - Implementación)

## Instrucciones


1. **Se proporciona un dataset de ejemplo en formato CSV o JSON con datos de transacciones bancarias**
   - Cargar los datos en un Data Lake
   - Aplicar reglas de limpieza, transformación y control de calidad a los datos
   - Cargar los datos finales en el modelo dimensional.
   - Asegurar que el proceso sea escalable y eficiente.

## Estructura del repositorio

```
parte2/
├── dataflow/              
├── dataset/              
├── linkedService/         
├── pipeline/             
├── CargaCompleta.png
├── SynapsePruebaCarga.png
├── ETL.py                 # Intento no desplegado (se prueba offline, pero se puede cargar a servicios de databricks)
├── datos_transacciones.csv
├── publish_config.json
└── README.md
```
# 📌 Parte 3: Explotación y Acceso a los Datos (Práctico - Análisis)

## Instrucciones
1. **Desarrolla una consulta en el DWH que identifique a los clientes más rentables, basándose en su historial transaccional**
   - Explica cómo se podría utilizar esta información para la democratización de datos en la organización, facilitando su consumo por parte de analistas y otras áreas de negocio.

## Estructura del repositorio

```
parte3/
├── README.md
├── Consulta.png
├── SQLServerQuery.sql
└── SQLQuerySynapse.sql
```

# 📌 Parte 4: Procesamiento On-Premise con DataStage y Control-M (Python-Ya que no tengo la s licencias)

## Instrucciones
1. **Tomar un archivo plano (clientes_input.txt) con 7 columnas separadas por | y fechas en formatos mixtos.**
   - Estandarizar todas las fechas a YYYY-MM-DD.
   - Cambiar el delimitador de | a , (pipe a coma)
   - Generar el archivo de salida transformado.
   - Orquestar el movimiento del archivo transformado del directorio A al directorio B.
   - Calendarización obligatoria: configurar la ejecución de lunes a viernes a las 08:00 (zona horaria America/Bogota), con manejo de reintentos y alertas ante fallos.




