-- Active: 1794772925326@@127.0.0.1@5432@Supermercado
--Proyecto Sistema de Supermercado


--CREACION DE TABLAS

CREATE TABLE Paises(
    Id_Pais SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    codigo_iso VARCHAR(3) NOT NULL DEFAULT 'HN',
    moneda VARCHAR(10) NOT NULL DEFAULT 'Lempira',
    estado INT NOT NULL DEFAULT 1 
);

CREATE TABLE Departamentos(
    Id_Departamento SERIAL PRIMARY KEY,
    Id_Pais INT NOT NULL REFERENCES Paises(Id_Pais),
    nombre VARCHAR(50) NOT NULL,
    estado INT NOT NULL DEFAULT 1
);

CREATE TABLE Ciudades(
    Id_Ciudad SERIAL PRIMARY KEY,
    Id_Departamento INT NOT NULL REFERENCES Departamentos(Id_Departamento),
    nombre VARCHAR(50) NOT NULL,
    estado INT NOT NULL DEFAULT 1
);

CREATE TABLE Direcciones(
    Id_Direccion SERIAL PRIMARY KEY,
    Id_Ciudad INT NOT NULL REFERENCES Ciudades(Id_Ciudad),
    colonia VARCHAR(50) NOT NULL,
    sector VARCHAR(50),
    calle VARCHAR(50),
    numero_casa VARCHAR(10)
);

CREATE TABLE Sucursales(
    Id_Sucursal SERIAL PRIMARY KEY,
    Id_Direccion INT NOT NULL REFERENCES Direcciones(Id_Direccion),
    nombre_sucursal VARCHAR(50) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    estado INT NOT NULL DEFAULT 1
);

CREATE TABLE Proveedores(
    Id_Proveedor SERIAL PRIMARY KEY,
    Id_Direccion INT NOT NULL REFERENCES Direcciones(Id_Direccion),
    nombre_o_razonSocial VARCHAR(50) NOT NULL,
    rtn VARCHAR(14) NOT NULL UNIQUE,
    nombre_contacto VARCHAR(50) NOT NULL,
    correo VARCHAR(50),
    fecha_Registro DATE NOT NULL,
    estado INT NOT NULL DEFAULT 1
);

CREATE TABLE Telefonos_Proveedores(
    Id_TelefonoProveedor SERIAL PRIMARY KEY,
    Id_Proveedor INT NOT NULL REFERENCES Proveedores(Id_Proveedor),
    telefono VARCHAR(20) NOT NULL,
    estado INT NOT NULL DEFAULT 1
);

CREATE TABLE Categorias(
    Id_Categoria SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(500),
    estado INT NOT NULL DEFAULT 1
);

CREATE TABLE Productos(
    Id_Producto SERIAL PRIMARY KEY,
    Id_Categoria INT NOT NULL REFERENCES Categorias(Id_Categoria),
    cod_barra VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(500),
    precio DECIMAL(8,2) NOT NULL CHECK (precio >= 0),
    costo DECIMAL(8,2) NOT NULL CHECK (costo >= 0),
    porcentaje_isv DECIMAL(5,2) NOT NULL CHECK (porcentaje_isv >= 0),
    estado INT NOT NULL DEFAULT 1
);

CREATE TABLE Compras(
    Id_Compra SERIAL PRIMARY KEY,
    Id_Proveedor INT NOT NULL REFERENCES Proveedores(Id_Proveedor),
    Id_Sucursal INT NOT NULL REFERENCES Sucursales(Id_Sucursal),
    fecha_compra TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    numero_factura VARCHAR(19) NOT NULL,
    subtotal DECIMAL(12,2) NOT NULL CHECK (subtotal >= 0),
    impuesto DECIMAL(12,2) NOT NULL CHECK (impuesto >= 0),
    total DECIMAL(12,2) NOT NULL CHECK (total >= 0),
    estado INT NOT NULL DEFAULT 1
);

CREATE TABLE Detalle_Compras(
    Id_Detalle_Compras SERIAL PRIMARY KEY,
    Id_Compra INT NOT NULL REFERENCES Compras(Id_Compra),
    Id_Producto INT NOT NULL REFERENCES Productos(Id_Producto),
    cantidad DECIMAL(8,2) NOT NULL CHECK (cantidad > 0),
    precio_unitario DECIMAL(8,2) NOT NULL CHECK (precio_unitario >= 0),
    descuento DECIMAL(8,2) NULL CHECK (descuento >= 0),
    subtotal_linea  DECIMAL(12,2) NOT NULL CHECK (subtotal_linea >= 0)
);

CREATE TABLE Lotes_Vencimiento(
    Id_LoteVencimiento SERIAL PRIMARY KEY,
    Id_DetalleCompra INT NOT NULL REFERENCES Detalle_Compras(Id_Detalle_Compras),
    lote_codigo VARCHAR(50) NOT NULL,
    fecha_fabricacion DATE NOT NULL,
    fecha_vencimiento DATE NOT NULL
);

CREATE TABLE Clientes(
    Id_Cliente SERIAL PRIMARY KEY,
    dni VARCHAR(13) UNIQUE,
    rtn VARCHAR(14) UNIQUE,
    primer_nombre VARCHAR(80) DEFAULT 'Consumidor Final',
    segundo_nombre VARCHAR(80),
    primer_apellido VARCHAR(80),
    segundo_apellido VARCHAR(80),
    correo VARCHAR(100),
    fecha_nacimiento DATE,
    estado INT NOT NULL DEFAULT 1,
    telefono VARCHAR(20) 
);

CREATE TABLE RolesEmpleados(
    Id_RolEmpleado SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(500),
    estado INT NOT NULL DEFAULT 1
);

CREATE TABLE TurnosEmpleados(
    Id_TurnoEmpleado SERIAL PRIMARY KEY,
    tipo_turno VARCHAR(20) NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_finalizacion TIME NOT NULL,
    descripcion VARCHAR(100)
);

CREATE TABLE Empleados(
    Id_Empleado SERIAL PRIMARY KEY,
    dni VARCHAR(13) NOT NULL UNIQUE,
    codigo_empleado VARCHAR(10) NOT NULL UNIQUE,
    primer_nombre VARCHAR(80) NOT NULL,
    segundo_nombre VARCHAR(80),
    primer_apellido VARCHAR(80) NOT NULL,
    segundo_apellido VARCHAR(80),
    correo VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE,
    estado INT NOT NULL DEFAULT 1,
    telefono VARCHAR(20) NOT NULL,
    fecha_contratacion DATE NOT NULL,
    Id_RolEmpleado INT NOT NULL REFERENCES RolesEmpleados(Id_RolEmpleado),
    Id_TurnoEmpleado INT NOT NULL REFERENCES TurnosEmpleados(Id_TurnoEmpleado),
    Id_Sucursal INT NOT NULL REFERENCES Sucursales(Id_Sucursal)
);

CREATE TABLE Productos_Sucursales(
    Id_ProductoSucursal SERIAL PRIMARY KEY,
    Id_Producto INT NOT NULL REFERENCES Productos(Id_Producto),
    Id_Sucursal INT NOT NULL REFERENCES Sucursales(Id_Sucursal),
    stock_minimo DECIMAL(8,2) NOT NULL DEFAULT 10 CHECK (stock_minimo >= 0),
    stock_maximo DECIMAL(8,2) CHECK (stock_maximo >= 0)
);

CREATE TABLE Inventarios(
    Id_Inventario SERIAL PRIMARY KEY,
    Id_Producto INT NOT NULL REFERENCES Productos(Id_Producto),
    Id_Sucursal INT NOT NULL REFERENCES Sucursales(Id_Sucursal),
    Id_LoteVencimiento INT NOT NULL REFERENCES Lotes_Vencimiento(Id_LoteVencimiento),
    stock_actual DECIMAL(8,2) NOT NULL CHECK (stock_actual >= 0)
);

CREATE TABLE Dosificaciones_CAI(
    Id_Dosificacion SERIAL PRIMARY KEY,
    cai VARCHAR(37) UNIQUE NOT NULL,
    fecha_limite_emision DATE NOT NULL,
    rango_inicial VARCHAR(19) NOT NULL,
    rango_final VARCHAR(19) NOT NULL,
    correlativo_actual INT NOT NULL CHECK (correlativo_actual >= 0),
    estado INT NOT NULL DEFAULT 1,
    Id_Sucursal INT NOT NULL REFERENCES Sucursales(Id_Sucursal)
);

CREATE TABLE Metodos_Pago(
    Id_Metodo_Pago SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion VARCHAR(200) NULL,
    estado INT NOT NULL
);

CREATE TABLE Facturas(
    Id_Factura SERIAL PRIMARY KEY,
    numero_factura VARCHAR(19) UNIQUE NOT NULL,
    cai VARCHAR(37) NOT NULL,
    fecha_emision TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    subtotal_exento DECIMAL(8,2) NOT NULL CHECK (subtotal_exento >= 0),
    subtotal_gravado_15 DECIMAL(8,2) NOT NULL CHECK (subtotal_gravado_15 >= 0),
    subtotal_gravado_18 DECIMAL(8,2) NOT NULL CHECK (subtotal_gravado_18 >= 0),
    isv_15 DECIMAL(5,2) NOT NULL CHECK (isv_15 >= 0),
    isv_18 DECIMAL(5,2) NOT NULL CHECK (isv_18 >= 0),
    impuesto_total DECIMAL(8,2) NOT NULL CHECK (impuesto_total >= 0),
    descuento_total DECIMAL(8,2) NOT NULL CHECK (descuento_total >= 0),
    total_pagar DECIMAL(8,2) NOT NULL CHECK (total_pagar >= 0),
    estado INT NOT NULL DEFAULT 1,
    Id_Sucursal INT NOT NULL REFERENCES Sucursales(Id_Sucursal),
    Id_Cliente INT NOT NULL REFERENCES Clientes(Id_Cliente),
    Id_Empleado INT NOT NULL REFERENCES Empleados(Id_Empleado),
    Id_Dosificacion INT NOT NULL REFERENCES Dosificaciones_CAI(Id_Dosificacion),
    Id_Metodo_Pago INT NOT NULL REFERENCES Metodos_Pago(Id_Metodo_Pago)
);

CREATE TABLE Detalle_Facturas(
    Id_Detalle SERIAL PRIMARY KEY,
    Id_Factura INT NOT NULL REFERENCES Facturas(Id_Factura),
    Id_Producto INT NOT NULL REFERENCES Productos(Id_Producto),
    cantidad DECIMAL(6,2) NOT NULL CHECK (cantidad > 0),
    precio_unitario DECIMAL(8,2) NOT NULL CHECK (precio_unitario >= 0),
    descuento_linea DECIMAL(8,2) NOT NULL CHECK (descuento_linea >= 0),
    impuesto_linea DECIMAL(8,2) NOT NULL CHECK (impuesto_linea >= 0),
    subtotal_linea DECIMAL(8,2) NOT NULL CHECK (subtotal_linea >= 0)
);