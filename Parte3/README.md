# Prueba Técnica — Ingeniería de Datos (Banco de Bogota)





### Parte 1: Modelado y Arquitectura de Datos (Teórico - Diseño) Instrucciones:

# 📌 Parte 1: Modelado y Arquitectura de Datos (Teórico - Diseño)

## Instrucciones

1. **Dado el siguiente caso de negocio:**

   *Una entidad bancaria quiere analizar el comportamiento de sus clientes en productos financieros (cuentas de ahorro, tarjetas de crédito y créditos). Para ello, se requiere integrar datos de múltiples fuentes (transacciones, datos de clientes y riesgo crediticio) en un Data Warehouse implementado en GCP.*

2. **Preguntas a desarrollar:**
   - Diseña un modelo **dimensional (modelo estrella o copo de nieve)** para el caso presentado.
   - Justifica tu elección del modelo, destacando sus ventajas para el análisis en entornos de BI y reporting.
   - Propón una estrategia de particionamiento y clustering que permita optimizar las consultas en BigQuery.
   - Describe cómo garantizarías la calidad y la gobernanza de los datos a lo largo del pipeline.
   - Explica qué mecanismos implementarías para asegurar la trazabilidad y auditoría de los datos procesados.

---

## Criterios de Evaluación

a. Diseño de modelo lógico y físico adecuado  
b. Estrategias de optimización y escalabilidad  
c. Consideraciones de calidad, gobierno y seguridad

## Respuesta
![Diagrama del modelo](diagrama.png)
**Figura 1.** Diagrama del modelo


### Justificación del modelo dimensional
Elegí una constelación de hechos (galaxy schema): dos tablas de hechos (fact.Transacciones y fact.ReporteRiesgo) que comparten dimensiones conformadas (dim.Cliente, dim.Tiempo), con dim.Ciudad normalizada en copo de nieve respecto a dim.Cliente.

La razón es que el caso de negocio integra dos procesos con grano distinto, transacciones (una fila por movimiento) y riesgo crediticio (una fila por reporte de central de riesgo por periodo). Forzarlos en una sola tabla de hechos generaría duplicación de filas al hacer join. Al compartir dim.Cliente y dim.Tiempo como dimensiones conformadas, un analista puede cruzar ambos procesos sin reconciliar modelos separados, esto le da  una vista 360° del cliente.

**Ventajas para BI y reporting:**
- Menos joins que un snowflake completo, lo que se traduce en consultas más simples y rápidas en Power BI.
- Escalable: un tercer proceso de negocio (reclamos) se integra como una tercera tabla de hechos reutilizando las dimensiones existentes.
- dim.Cliente maneja SCD (Slowly Changing Dimension) tipo 2 (histórico de cambios), permitiendo análisis retrospectivos correctos — crítico para auditorías bancarias.


### Estrategia de particionamiento y clustering
| Estrategia                          | En BigQuery (nativo del caso)                                      | En Synapse (implementación real de esta prueba)                                                                 |
|-------------------------------------|--------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|
| Particionamiento                    | PARTITION BY DATE(fecha) sobre las tablas de hechos                | PARTITION (id_tiempo RANGE RIGHT FOR VALUES (...)) — partición mensual sobre fact.Transacciones y fact.ReporteRiesgo |
| Clustering                          | CLUSTER BY id_cliente — ordena físicamente filas dentro de cada partición | Ordered Clustered Columnstore Index: CLUSTERED COLUMNSTORE INDEX ORDER (id_cliente)                              |
| (sin equivalente en BigQuery)       | —                                                                  | Distribución HASH(id_cliente) en dimensión y hechos por igual, para lograr joins co-localizados sin movimiento de datos entre nodos — concepto propio de motores MPP |


![Figura 2. Diagrama arquitectura](arquitectura.png)

**Figura 2.** Diagrama arquitectura

**Trazabilidad y auditoría**
- Columnas de control en cada tabla de hechos: fecha_carga y batch_id (identificador único por ejecución del pipeline, que agrupa todas las filas cargadas en esa corrida —permite reprocesar o hacer rollback de un batch completo sin tocar el resto de la tabla).
- Historización con SCD tipo 2 en dim.Cliente: conserva el estado exacto del cliente en cada punto del tiempo, no solo el estado actual.
