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
![Diagrama del modelo](Parte1/diagrama.png)
### Justificación del modelo dimensional
Elegí una constelación de hechos (galaxy schema): dos tablas de hechos (fact.Transacciones y fact.ReporteRiesgo) que comparten dimensiones conformadas (dim.Cliente, dim.Tiempo), con dim.Ciudad normalizada en copo de nieve respecto a dim.Cliente.

La razón es que el caso de negocio integra dos procesos con grano distinto, transacciones (una fila por movimiento) y riesgo crediticio (una fila por reporte de central de riesgo por periodo). Forzarlos en una sola tabla de hechos generaría duplicación de filas al hacer join. Al compartir dim.Cliente y dim.Tiempo como dimensiones conformadas, un analista puede cruzar ambos procesos sin reconciliar modelos separados, esto le da  una vista 360° del cliente.