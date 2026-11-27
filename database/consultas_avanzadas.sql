-- Active: 1794772925326@@127.0.0.1@5432@ProyectoSuper

ALTER TABLE Paises ALTER COLUMN moneda TYPE VARCHAR(100);

CREATE VIEW vw_productos AS
SELECT
    p.Id_Producto,
    p.Id_Categoria,
    p.Id_Marca,
    p.cod_barra,
    p.nombre,
    p.descripcion,
    c.nombre AS categoria,
    m.nombre AS marca,
    p.stock_minimo,
    p.stock_maximo,
    p.precio,
    p.costo,
    p.porcentaje_isv,
    p.estado
FROM Productos p
INNER JOIN Categorias c
    ON p.Id_Categoria = c.Id_Categoria
INNER JOIN Marcas m
    ON p.Id_Marca = m.Id_Marca;

CREATE VIEW vw_inventarios AS
SELECT
    i.Id_Inventario,
    i.Id_Producto,
    i.Id_Sucursal,
    i.Id_lote_vencimiento,
    p.nombre AS producto,
    s.nombre_sucursal AS sucursal,
    i.stock_actual
FROM Inventarios i
INNER JOIN Productos p
    ON i.Id_Producto = p.Id_Producto
INNER JOIN Sucursales s
    ON i.Id_Sucursal = s.Id_Sucursal;

-- MÓDULO 1

ALTER TABLE Sesiones_Cajas DROP CONSTRAINT IF EXISTS sesiones_cajas_diferencia_check;


-- Vista v_cierre_caja (resumen por cajero y turno)
CREATE OR REPLACE VIEW v_cierre_caja AS
SELECT
    s.Id_Sesion,
    c.numero_caja,
    e.codigo_empleado,
    p.primer_nombre || ' ' || p.primer_apellido AS cajero,
    t.tipo_turno AS turno,
    s.fecha_apertura,
    s.fecha_cierre,
    s.monto_inicial,
    COALESCE(SUM(pf.monto_pagado) FILTER (WHERE mp.nombre ILIKE '%efectivo%'), 0) AS ventas_efectivo,
    COALESCE(SUM(pf.monto_pagado) FILTER (WHERE mp.nombre NOT ILIKE '%efectivo%'), 0) AS ventas_tarjeta,
    s.monto_esperado,
    s.monto_esperado + s.diferencia AS monto_contado,
    s.diferencia,
    CASE WHEN s.estado = 1 THEN 'ABIERTA' ELSE 'CERRADA' END AS estado_sesion
FROM Sesiones_Cajas s
JOIN Cajas c ON c.Id_Caja = s.Id_Caja
JOIN Empleados e ON e.Id_Empleado = s.Id_Empleado
JOIN Personas p ON p.Id_Persona = e.Id_Persona
JOIN Turnos_Empleados t ON t.Id_TurnoEmpleado = e.Id_TurnoEmpleado
LEFT JOIN Facturas f ON f.Id_Empleado = s.Id_Empleado
                    AND f.estado = 1
                    AND f.fecha_emision >= s.fecha_apertura
                    AND f.fecha_emision <= COALESCE(s.fecha_cierre, NOW())
LEFT JOIN Pagos_Facturas pf ON pf.Id_Factura = f.Id_Factura
LEFT JOIN Metodos_Pagos mp  ON mp.Id_Metodo_Pago = pf.Id_Metodo_Pago
GROUP BY s.Id_Sesion, c.Id_Caja, e.Id_Empleado, p.Id_Persona, t.Id_TurnoEmpleado;
