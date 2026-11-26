-- Active: 1795662717894@@127.0.0.1@5432@ProyectoSuper
--Proyecto Sistema de Supermercado


--CREACION DE TABLAS

CREATE TABLE Paises (
    Id_Pais SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    codigo_iso VARCHAR(2) NOT NULL DEFAULT 'HN',
    moneda VARCHAR(10) NOT NULL DEFAULT 'Lempira',
    estado INT NOT NULL DEFAULT 1
);
ALTER TABLE Paises
ALTER COLUMN moneda TYPE VARCHAR(50);

CREATE TABLE Departamentos (
    Id_Departamento SERIAL PRIMARY KEY,
    Id_Pais INT NOT NULL REFERENCES Paises(Id_Pais),
    nombre VARCHAR(50) NOT NULL,
    estado INT NOT NULL DEFAULT 1
);

CREATE TABLE Ciudades (
    Id_Ciudad SERIAL PRIMARY KEY,
    Id_Departamento INT NOT NULL REFERENCES Departamentos(Id_Departamento),
    nombre VARCHAR(50) NOT NULL,
    estado INT NOT NULL DEFAULT 1
);

CREATE TABLE Direcciones (
    Id_Direccion SERIAL PRIMARY KEY,
    Id_Ciudad INT NOT NULL REFERENCES Ciudades(Id_Ciudad),
    colonia VARCHAR(50) NOT NULL,
    calle VARCHAR(50) NULL,
    referencia VARCHAR(200) NOT NULL
);

CREATE TABLE Sucursales (
    Id_Sucursal SERIAL PRIMARY KEY,
    Id_Direccion INT NOT NULL REFERENCES Direcciones(Id_Direccion),
    nombre_sucursal VARCHAR(50) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    estado INT NOT NULL DEFAULT 1
);

CREATE TABLE Proveedores (
    Id_Proveedor SERIAL PRIMARY KEY,
    Id_Direccion INT NOT NULL REFERENCES Direcciones(Id_Direccion),
    nombre_o_razonSocial VARCHAR(100) NOT NULL,
    rtn VARCHAR(14) NOT NULL UNIQUE,
    nombre_contacto VARCHAR(50) NOT NULL,
    correo VARCHAR(50) NULL,
    fecha_Registro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    estado INT NOT NULL DEFAULT 1
);

CREATE TABLE Telefonos_Proveedores (
    Id_TelefonoProveedor SERIAL PRIMARY KEY,
    Id_Proveedor INT NOT NULL REFERENCES Proveedores(Id_Proveedor),
    telefono VARCHAR(20) NOT NULL,
    estado INT NOT NULL DEFAULT 1
);

CREATE TABLE Categorias (
    Id_Categoria SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(500) NULL,
    estado INT NOT NULL DEFAULT 1
);

CREATE TABLE Marcas (
    Id_Marca SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    pais_origen VARCHAR(50) NULL,
    estado INT NOT NULL DEFAULT 1
);

CREATE TABLE Productos (
    Id_Producto SERIAL PRIMARY KEY,
    Id_Sucursal INT NOT NULL REFERENCES Sucursales(Id_Sucursal),
    Id_Categoria INT NOT NULL REFERENCES Categorias(Id_Categoria),
    Id_Marca INT NOT NULL REFERENCES Marcas(Id_Marca),
    cod_barra VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(500) NULL,
    stock_minimo DECIMAL(8,2) NOT NULL DEFAULT 10 CHECK (stock_minimo >= 0),
    stock_maximo DECIMAL(8,2) NULL CHECK (stock_maximo >= 0),
    precio DECIMAL(8,2) NOT NULL CHECK (precio >= 0),
    costo DECIMAL(8,2) NOT NULL CHECK (costo >= 0),
    porcentaje_isv DECIMAL(5,2) NOT NULL,
    estado INT NOT NULL DEFAULT 1
);

CREATE TABLE Compras (
    Id_Compra SERIAL PRIMARY KEY,
    Id_Proveedor INT NOT NULL REFERENCES Proveedores(Id_Proveedor),
    Id_Sucursal INT NOT NULL REFERENCES Sucursales(Id_Sucursal),
    fecha_compra TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    numero_factura VARCHAR(19) NOT NULL,
    subtotal DECIMAL(12,2) NOT NULL,
    impuesto DECIMAL(12,2) NOT NULL,
    total DECIMAL(12,2) NOT NULL,
    estado INT NOT NULL DEFAULT 1
);

CREATE TABLE Detalle_Compras (
    Id_Detalle_Compras SERIAL PRIMARY KEY,
    Id_Compra INT NOT NULL REFERENCES Compras(Id_Compra),
    Id_Producto INT NOT NULL REFERENCES Productos(Id_Producto),
    cantidad DECIMAL(8,2) NOT NULL,
    precio_unitario DECIMAL(8,2) NOT NULL,
    descuento DECIMAL(8,2) NULL,
    subtotal_linea DECIMAL(12,2) NOT NULL
);

CREATE TABLE Lotes_Vencimiento (
    Id_LoteVencimiento SERIAL PRIMARY KEY,
    Id_DetalleCompra INT NOT NULL REFERENCES Detalle_Compras(Id_Detalle_Compras),
    lote_codigo VARCHAR(50) NOT NULL,
    fecha_fabricacion DATE NOT NULL,
    fecha_vencimiento DATE NOT NULL CHECK (fecha_vencimiento >= fecha_fabricacion)
);

CREATE TABLE Inventarios (
    Id_Inventario SERIAL PRIMARY KEY,
    Id_Producto INT NOT NULL REFERENCES Productos(Id_Producto),
    Id_Sucursal INT NOT NULL REFERENCES Sucursales(Id_Sucursal),
    id_lote_vencimiento INT NOT NULL REFERENCES Lotes_Vencimiento(Id_LoteVencimiento),
    stock_actual DECIMAL(8,2) NOT NULL CHECK (stock_actual >= 0)
);

CREATE TABLE Personas (
    Id_Persona SERIAL PRIMARY KEY,
    dni VARCHAR(13) UNIQUE NULL,
    primer_nombre VARCHAR(80) NULL,
    segundo_nombre VARCHAR(80) NULL,
    primer_apellido VARCHAR(80) NULL,
    segundo_apellido VARCHAR(80) NULL,
    correo VARCHAR(100) NULL,
    contrasena_hash VARCHAR(60) NULL,
    fecha_nacimiento DATE NULL,
    estado INT NOT NULL DEFAULT 1,
    telefono VARCHAR(20) NULL
);

CREATE TABLE Clientes (
    Id_Cliente SERIAL PRIMARY KEY,
    Id_Persona INT NOT NULL REFERENCES Personas(Id_Persona),
    rtn VARCHAR(14) UNIQUE NULL,
    Id_Direccion INT NOT NULL REFERENCES Direcciones(Id_Direccion),
    razon_social VARCHAR(200) NULL
);

CREATE TABLE Roles_Empleados (
    Id_RolEmpleado SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(500) NULL,
    estado INT NOT NULL DEFAULT 1
);

CREATE TABLE Turnos_Empleados (
    Id_TurnoEmpleado SERIAL PRIMARY KEY,
    tipo_turno VARCHAR(20) NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_finalizacion TIME NOT NULL,
    descripcion VARCHAR(100) NULL
);

CREATE TABLE Empleados (
    Id_Empleado SERIAL PRIMARY KEY,
    codigo_empleado VARCHAR(10) NOT NULL UNIQUE,
    Id_Persona INT NOT NULL REFERENCES Personas(Id_Persona),
    salario_base DECIMAL(10,2) NOT NULL CHECK (salario_base > 0),
    fecha_contratacion DATE NOT NULL,
    Id_RolEmpleado INT NOT NULL REFERENCES Roles_Empleados(Id_RolEmpleado),
    Id_TurnoEmpleado INT NOT NULL REFERENCES Turnos_Empleados(Id_TurnoEmpleado),
    Id_Sucursal INT NOT NULL REFERENCES Sucursales(Id_Sucursal)
);

CREATE TABLE Autorizaciones_SAR (
    id_autorizacion_sar SERIAL PRIMARY KEY,
    id_sucursal INT NOT NULL REFERENCES sucursales(id_Sucursal),
    cai VARCHAR(37) UNIQUE NOT NULL,
    fecha_limite_emision DATE NOT NULL,
    rango_inicial VARCHAR(19) NOT NULL,
    rango_final VARCHAR(19) NOT NULL,
    correlativo_actual INT NOT NULL,
    estado INT NOT NULL
);

CREATE TABLE Facturas (
    Id_Factura SERIAL PRIMARY KEY,
    Id_Sucursal INT NOT NULL REFERENCES Sucursales(Id_Sucursal),
    Id_Cliente INT NOT NULL DEFAULT 1 REFERENCES Clientes(Id_Cliente),
    Id_Empleado INT NOT NULL REFERENCES Empleados(Id_Empleado),
    Id_autorizacion_sar INT NOT NULL REFERENCES Autorizaciones_SAR(Id_autorizacion_sar),
    numero_factura VARCHAR(19) NOT NULL UNIQUE,
    cai VARCHAR(37) NOT NULL,
    fecha_emision TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    subtotal_exento DECIMAL(12,2) NOT NULL CHECK (subtotal_exento >= 0),
    subtotal_gravado_15 DECIMAL(12,2) NOT NULL CHECK (subtotal_gravado_15 >= 0),
    subtotal_gravado_18 DECIMAL(12,2) NOT NULL CHECK (subtotal_gravado_18 >= 0),
    isv_15 DECIMAL(12,2) NOT NULL CHECK (isv_15 >= 0),
    isv_18 DECIMAL(12,2) NOT NULL CHECK (isv_18 >= 0),
    impuesto_total DECIMAL(12,2) NOT NULL CHECK (impuesto_total >= 0),
    descuento_total DECIMAL(12,2) NOT NULL CHECK (descuento_total >= 0),
    total_pagar DECIMAL(12,2) NOT NULL CHECK (total_pagar >= 0),
    numero_orden_compra_exenta VARCHAR(30) NULL,
    numero_constancia_registro_exonerado VARCHAR(30) NULL,
    estado INT NOT NULL DEFAULT 1
);

CREATE TABLE Detalle_Facturas (
    Id_Detalle SERIAL PRIMARY KEY,
    Id_Factura INT NOT NULL REFERENCES Facturas(Id_Factura),
    Id_Producto INT NOT NULL REFERENCES Productos(Id_Producto),
    cantidad DECIMAL(6,2) NOT NULL CHECK (cantidad > 0),
    precio_unitario DECIMAL(8,2) NOT NULL CHECK (precio_unitario >= 0),
    descuento_linea DECIMAL(8,2) NOT NULL DEFAULT 0.00 CHECK (descuento_linea >= 0),
    impuesto_linea DECIMAL(8,2) NOT NULL CHECK (impuesto_linea >= 0),
    subtotal_linea DECIMAL(8,2) NOT NULL CHECK (subtotal_linea >= 0)
);

CREATE TABLE Metodos_Pagos (
    Id_Metodo_Pago SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion VARCHAR(200) NULL,
    estado INT NOT NULL
);

CREATE TABLE Tarjetas (
    Id_Tarjeta SERIAL PRIMARY KEY,
    Id_Cliente INT NOT NULL REFERENCES Clientes(Id_Cliente),
    nombre_titular VARCHAR(100) NOT NULL,
    final_tarjeta VARCHAR(4) NOT NULL,
    mes SMALLINT NOT NULL CHECK (mes BETWEEN 1 AND 12),
    anio SMALLINT NOT NULL CHECK (anio BETWEEN 2000 AND 2100),
    marca VARCHAR(20) NOT NULL,
    token_generado VARCHAR(255) NOT NULL,
    estado INT NOT NULL DEFAULT 1
);

CREATE TABLE Pagos_Facturas (
    Id_Pago SERIAL PRIMARY KEY,
    Id_Factura INT NOT NULL REFERENCES Facturas(Id_Factura),
    Id_Metodo_Pago INT NOT NULL REFERENCES Metodos_Pagos(Id_Metodo_Pago),
    Id_Tarjeta INT NULL REFERENCES Tarjetas(Id_Tarjeta),
    monto_pagado DECIMAL(8,2) NOT NULL CHECK (monto_pagado >= 0),
    referencia_transaccion VARCHAR(100) NULL,
    fecha_pago TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Ofertas (
    Id_Oferta SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(100) NOT NULL,
    porcentaje_descuento DECIMAL(8,2) NOT NULL CHECK (porcentaje_descuento BETWEEN 0 AND 1),
    fecha_inicio TIMESTAMP NOT NULL,
    fecha_fin TIMESTAMP NOT NULL CHECK (fecha_fin > fecha_inicio),
    estado INT NOT NULL DEFAULT 1 CHECK (estado BETWEEN 0 AND 1)
);

CREATE TABLE Productos_Ofertas (
    Id_ProductosOfertas SERIAL PRIMARY KEY,
    Id_Productos INT NOT NULL REFERENCES Productos(Id_Producto),
    Id_Oferta INT NOT NULL REFERENCES Ofertas(Id_Oferta)
);

CREATE TABLE Cajas (
    Id_Caja SERIAL PRIMARY KEY,
    Id_Sucursal INT NOT NULL REFERENCES Sucursales(Id_Sucursal),
    numero_caja VARCHAR(20) NOT NULL UNIQUE,
    descripcion VARCHAR(100) NULL,
    estado INT NOT NULL DEFAULT 1
);

CREATE TABLE Sesiones_Cajas (
    Id_Sesion SERIAL PRIMARY KEY,
    Id_Caja INT NOT NULL REFERENCES Cajas(Id_Caja),
    Id_Empleado INT NOT NULL REFERENCES Empleados(Id_Empleado),
    fecha_apertura TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    monto_inicial DECIMAL(10,2) NOT NULL DEFAULT 0 CHECK (monto_inicial >= 0),
    fecha_cierre TIMESTAMP NULL,
    monto_esperado DECIMAL(10,2) NULL DEFAULT 0 CHECK (monto_esperado >= 0),
    diferencia DECIMAL(10,2) NULL DEFAULT 0 CHECK (diferencia >= 0),
    estado INT NOT NULL DEFAULT 1
);

CREATE TABLE Repartidor_Externo (
    Id_RepartidorExterno SERIAL PRIMARY KEY,
    Id_Persona INT NOT NULL REFERENCES Personas(Id_Persona),
    empresa_Delivery VARCHAR(200) NOT NULL,
    tipo_vehiculo VARCHAR(50) NULL
);

CREATE TABLE Pedido_A_Domicilio (
    Id_PedidoADomicilio SERIAL PRIMARY KEY,
    Id_Repartidor INT NOT NULL REFERENCES Repartidor_Externo(Id_RepartidorExterno),
    Id_Factura INT NOT NULL UNIQUE REFERENCES Facturas(Id_Factura),
    nombre_destinatario VARCHAR(50) NOT NULL,
    tarifa DECIMAL(8,2) NOT NULL CHECK (tarifa > 0),
    hora_salida TIMESTAMP NULL,
    hora_entrega TIMESTAMP NULL,
    Id_Direccion INT NOT NULL REFERENCES Direcciones(Id_Direccion),
    estado_entrega INT NOT NULL
);

