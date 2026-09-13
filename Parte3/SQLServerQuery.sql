-- Clientes mas rentables por 
SELECT TOP 10
    c.id_cliente,
    c.nombres,
    c.numero_identificacion,
    SUM(t.monto_transaccion)      AS monto_total_transaccionado,
    COUNT(*)                       AS numero_transacciones,
    COUNT(DISTINCT t.id_producto)  AS productos_utilizados,
    AVG(t.monto_transaccion)       AS ticket_promedio
FROM fact.Transacciones t
JOIN dim.Cliente c ON t.id_cliente = c.id_cliente
GROUP BY c.id_cliente, c.nombres, c.numero_identificacion
ORDER BY monto_total_transaccionado DESC;


---Clientes mas rentables excluyendo a los reportados
WITH RentabilidadPorCliente AS (
    SELECT
        c.id_cliente,
        c.nombres,
        c.numero_identificacion,
        SUM(t.monto_transaccion)      AS monto_total_transaccionado,
        COUNT(*)                       AS numero_transacciones,
        COUNT(DISTINCT t.id_producto)  AS productos_utilizados,
        AVG(t.monto_transaccion)       AS ticket_promedio
    FROM fact.Transacciones t
    JOIN dim.Cliente c ON t.id_cliente = c.id_cliente
    GROUP BY c.id_cliente, c.nombres, c.numero_identificacion
),
ClientesConRiesgo AS (
    SELECT DISTINCT id_cliente
    FROM fact.ReporteRiesgo
)
SELECT TOP 10
    r.id_cliente,
    r.nombres,
    r.numero_identificacion,
    r.monto_total_transaccionado,
    r.numero_transacciones,
    r.productos_utilizados,
    r.ticket_promedio
FROM RentabilidadPorCliente r
LEFT JOIN ClientesConRiesgo cr ON r.id_cliente = cr.id_cliente
WHERE cr.id_cliente IS NULL
ORDER BY r.monto_total_transaccionado DESC;