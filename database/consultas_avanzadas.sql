-- Active: 1795662717894@@127.0.0.1@5432@ProyectoSuper

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
