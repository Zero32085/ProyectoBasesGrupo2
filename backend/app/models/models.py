from sqlalchemy import Column, Date, ForeignKey, String, Integer, Numeric, Time
from sqlalchemy.orm import relationship

# Esto es temporal, hasta que se cree la conexion de database.py
from app.database import Base

class Pais(Base):
	__tablename__ = 'Paises'

	Id_Pais = Column(Integer, primary_key=True, nullable=False)
	nombre = Column(String(50), nullable=False)
	codigo_iso = Column(String(2), nullable=False, default="HN", server_default="HN")
	moneda = Column(String(100), nullable=False, default="Lempira", server_default="Lempira")
	estado = Column(Integer, nullable=False, default=1, server_default="1")

class Departamento(Base):
	__tablename__ = 'Departamentos'

	Id_Departamento = Column(Integer, primary_key=True, nullable=False)
	Id_Pais = Column(Integer, ForeignKey("Paises.Id_Pais"), nullable=False)
	nombre = Column(String(50), nullable=False)
	estado = Column(Integer, nullable=False, default=1, server_default="1")
	pais = relationship("Pais")

class Ciudad(Base):
	__tablename__ = 'Ciudades'

	Id_Ciudad = Column(Integer, primary_key=True, nullable=False)
	Id_Departamento = Column(Integer, ForeignKey("Departamentos.Id_Departamento"), nullable=False)
	nombre = Column(String(50), nullable=False)
	estado = Column(Integer, nullable=False, default=1, server_default="1")
	departamento = relationship("Departamento")


class Direccion(Base):
	__tablename__ = 'Direcciones'

	Id_Direccion = Column(Integer, primary_key=True, nullable=False)
	Id_Ciudad = Column(Integer, ForeignKey("Ciudades.Id_Ciudad"), nullable=False)
	colonia = Column(String(50), nullable=False)
    calle = Column(String(50), nullable=True)
    referencia = Column(String(200), nullable=False)
    nombre_destinatario = Column(String(50), nullable=True)
    ciudad = relationship("Ciudad")


class Sucursal(Base):
	__tablename__ = 'Sucursales'

	Id_Sucursal = Column(Integer, primary_key=True, nullable=False)
    Id_Direccion = Column(Integer, ForeignKey("Direcciones.Id_Direccion"), nullable=False)
    nombre_sucursal = Column(String(50), nullable=False)
    telefono = Column(String(20), nullable=False)
    estado = Column(Integer, nullable=False, default=1, server_default="1")
    direccion = relationship("Direccion")


class Proveedor(Base):
	__tablename__ = 'Proveedores'

	Id_Proveedor = Column(Integer, primary_key=True, nullable=False)
    Id_Direccion = Column(Integer, ForeignKey("Direcciones.Id_Direccion"), nullable=False)
    nombre_o_razonSocial = Column(String(100), nullable=False)
    rtn = Column(String(14), unique=True, nullable=False)
    nombre_contacto = Column(String(50), nullable=False)
    correo = Column(String(50), nullable=True)
    fecha_Registro = Column(DateTime, nullable=False, server_default=func.now())
    estado = Column(Integer, nullable=False, default=1, server_default="1")
    direccion = relationship("Direccion")


class TelefonoProveedor(Base):
	__tablename__ = 'Telefonos_Proveedores'

	Id_TelefonoProveedor = Column(Integer, primary_key=True, nullable=False)
    Id_Proveedor = Column(Integer, ForeignKey("Proveedores.Id_Proveedor"), nullable=False)
    telefono = Column(String(20), nullable=False)
    estado = Column(Integer, nullable=False, default=1, server_default="1")
    proveedor = relationship("Proveedor")


class Categoria(Base):
    __tablename__ = 'Categorias'

    Id_Categoria = Column(Integer, primary_key=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(500), nullable=False)
    estado = Column(Integer, nullable=False, default=1, server_default="1")


class Marca(Base):
    __tablename__ = 'Marcas'

    Id_Marca = Column(Integer, primary_key=True, nullable=False)
    nombre = Column(String(50), nullable=False)
    pais_origen = Column(String(50), nullable=True)
    estado = Column(Integer, nullable=False, default=1, server_default="1")


class Producto(Base):
    __tablename__ = 'Productos'
    __table_args__ = (
        CheckConstraint("stock_minimo >= 0", name="ck_productos_stock_minimo"),
        CheckConstraint("stock_maximo >= 0", name="ck_productos_stock_maximo"),
        CheckConstraint("precio >= 0", name="ck_productos_precio"),
        CheckConstraint("costo >= 0", name="ck_productos_costo"),
        #CheckConstraint("porcentaje_isv >= 0", name="ck_productos_porcentaje_isv"),
    )

    Id_Producto = Column(Integer, primary_key=True, nullable=False)
    Id_Sucursal = Column(Integer, ForeignKey("Sucursales.Id_Sucursal"), nullable=False)
    Id_Categoria = Column(Integer, ForeignKey("Categorias.Id_Categoria"), nullable=False)
	Id_Marca = Column(Integer, ForeignKey("Marcas.Id_Marca"), nullable=False)
    cod_barra = Column(String(20), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(500), nullable=True)
    stock_minimo = Column(Numeric(8, 2), nullable=False, default=10, server_default="10")
    stock_maximo = Column(Numeric(8, 2), nullable=True)
    precio = Column(Numeric(8, 2), nullable=False)
    costo = Column(Numeric(8, 2), nullable=False)
    porcentaje_isv = Column(Numeric(8, 2), nullable=False)
    estado = Column(Integer, nullable=False, default=1, server_default="1")
    categoria = relationship("Categoria")
    sucursal = relationship("Sucursal")
    marca = relationship("Marca")


class Compra(Base):
	__tablename__ = 'Compra'

	Id_Compra = Column(Integer, primary_key=True, nullable=False)
    Id_Proveedor = Column(Integer, ForeignKey("Proveedores.Id_Proveedor"), nullable=False)
    Id_Sucursal = Column(Integer, ForeignKey("Sucursales.Id_Sucursal"), nullable=False)
    fecha_compra = Column(DateTime, nullable=False, server_default=func.now())
    numero_factura = Column(String(19), nullable=False)
    subtotal = Column(Numeric(12, 2), nullable=False)
    impuesto = Column(Numeric(12, 2), nullable=False)
    total = Column(Numeric(12, 2), nullable=False)
    estado = Column(Integer, nullable=False, default=1, server_default="1")
    proveedor = relationship("Proveedor")
    sucursal = relationship("Sucursal")


class DetalleCompra(Base):
	__tablename__ = 'Detalle_Compras'

	Id_Detalle_Compras = Column(Integer, primary_key=True, nullable=False)
    Id_Compra = Column(Integer, ForeignKey("Compras.Id_Compra"), nullable=False)
    Id_Producto = Column(Integer, ForeignKey("Productos.Id_Producto"), nullable=False)
    cantidad = Column(Numeric(8, 2), nullable=False)
    precio_unitario = Column(Numeric(8, 2), nullable=False)
    descuento = Column(Numeric(8, 2), nullable=True)
    subtotal_linea = Column(Numeric(12, 2), nullable=False)
    compra = relationship("Compra")
    producto = relationship("Producto")

class LoteVencimiento(Base):
	__tablename__ = 'Lotes_Vencimiento'
	__table_args__ = (
        CheckConstraint("fecha_vencimiento > fecha_fabricacion", name="ck_Lote_fecha_vencimiento"),
	)

	Id_LoteVencimiento = Column(Integer, primary_key=True, nullable=False)
    Id_DetalleCompra = Column(Integer, ForeignKey("DetalleCompra.Id_Detalle_Compras"), nullable=False)
    lote_codigo = Column(String(50), nullable=False)
    fecha_fabricacion = Column(Date, nullable=False)
    fecha_vencimiento = Column(Date, nullable=False)
    detalle_compra = relationship("DetalleCompra")


class Inventario(Base):
	__tablename__ = 'Inventarios'
	__table_args__ = (
        CheckConstraint("stock_actual >= 0", name="ck_inventarios_stock_actual"),
    )

	Id_Inventario = Column(Integer, primary_key=True, nullable=False)
    Id_Producto = Column(Integer, ForeignKey("Productos.Id_Producto"), nullable=False)
    Id_Sucursal = Column(Integer, ForeignKey("Sucursales.Id_Sucursal"), nullable=False)
    id_lote_encimiento = Column(Integer, ForeignKey("LoteVencimiento.Id_LoteVencimiento"), nullable=False)
    stock_actual = Column(Numeric(8, 2), nullable=False)
    producto = relationship("Producto")
    sucursal = relationship("Sucursal")
    lote = relationship("LoteVencimiento")


class Persona(Base):
	__tablename__ = 'Personas'

	Id_Persona = Column(Integer, primary_key=True, nullable=False)
	dni = Column(String(13), unique=True, nullable=True)
	primer_nombre = Column(String(80), nullable=True)
	segundo_nombre = Column(String(80), nullable=True)
	primer_apellido = Column(String(80), nullable=True)
	segundo_apellido = Column(String(80), nullable=True)
	correo = Column(String(100), unique=True, nullable=True)
	contrasena_hash = Column(String(60), nullable=True)
	fecha_nacimiento = Column(Date, nullable=True)
	estado = Column(Integer, nullable=False, default=1, server_default="1")
	telefono = Column(String(20), nullable=True)


class Cliente(Base):
	__tablename__ = 'Clientes'

	Id_Cliente = Column(Integer, primary_key=True, nullable=False)
	Id_Persona = Column(Integer, ForeignKey("Personas.Id_Persona"), nullable=False)
	rtn = Column(String(14), unique=True, nullable=True)
	Id_Direccion = Column(Integer, ForeignKey("Direcciones.Id_Direccion"), nullable=False)
	razon_social = Column(String(200), nullable=True)
	persona = relationship("Persona")
    direccion = relationship("Direccion")


class RolEmpleado(Base):
	__tablename__ = 'Roles_Empleados'
	
	Id_RolEmpleado = Column(Integer, primary_key=True, nullable=False)
	nombre = Column(String(100), nullable=False)
	descripcion = Column(String(500), nullable=True)
	estado = Column(Integer, nullable=False, default=1, server_default="1")


class TurnoEmpleado(Base):
	__tablename__ = 'Turnos_Empleados'

	Id_TurnoEmpleado = Column(Integer, primary_key=True, index=True, nullable=False)
	tipo_turno = Column(String(20), nullable=False)
	hora_inicio = Column(Time, nullable=False)
	hora_finalizacion = Column(Time, nullable=False)
	descripcion = Column(String(100), nullable=True)


class Empleado(Base):
	__tablename__ = 'Empleados'
	__table_args__ = (
        CheckConstraint("salario_base > 0", name="ck_empleados_salario_base"), #La coma es util, no borrar
        )

	Id_Empleado = Column(Integer, primary_key=True, index=True, nullable=False)
	codigo_empleado = Column(String(10), unique=True, nullable=False)
	Id_Persona = Column(Integer, ForeignKey("Personas.Id_Persona"), nullable=False)
	salario_base = Column(Numeric(10,2), nullable=False)
	fecha_contratacion = Column(Date, nullable=False)
	Id_RolEmpleado = Column(Integer, ForeignKey("Roles_Empleados.Id_RolEmpleado"), nullable=False)
	Id_TurnoEmpleado = Column(Integer, ForeignKey("Turnos_Empleados.Id_TurnoEmpleado"), nullable=False)
	Id_Sucursal = Column(Integer, ForeignKey("Sucursales.Id_Sucursal"), nullable=False)
	persona = relationship("Persona")
	turno_empleado = relationship("TurnoEmpleado")
	rol_empleado = relationship("RolEmpleado")
	sucursal = relationship("Sucursal")


class DosificacionCAI(Base):
	__tablename__ = 'Dosificaciones_CAI'

	Id_Dosificacion = Column(Integer, primary_key=True, nullable=False)
    Id_Sucursal = Column(Integer, ForeignKey("Sucursales.Id_Sucursal"), nullable=False)
    cai = Column(String(37), nullable=False)
    fecha_limite_emision = Column(Date, nullable=False)
    rango_inicial = Column(String(19), nullable=False)
    rango_final = Column(String(19), nullable=False)
    correlativo_actual = Column(Integer, nullable=False)
    estado = Column(Integer, nullable=False)
    sucursal = relationship("Sucursal")


class Factura(Base):
	__tablename__ = 'Facturas'
	__table_args__ = (
        CheckConstraint("subtotal_exento >= 0", name="ck_facturas_subtotal_exento"),
        CheckConstraint("subtotal_gravado_15 >= 0", name="ck_facturas_subtotal_gravado_15"),
        CheckConstraint("subtotal_gravado_18 >= 0", name="ck_facturas_subtotal_gravado_18"),
        CheckConstraint("isv_15 >= 0", name="ck_facturas_isv_15"),
        CheckConstraint("isv_18 >= 0", name="ck_facturas_isv_18"),
        CheckConstraint("impuesto_total >= 0", name="ck_facturas_impuesto_total"),
        CheckConstraint("descuento_total >= 0", name="ck_facturas_descuento_total"),
        CheckConstraint("total_pagar >= 0", name="ck_facturas_total_pagar"),
    )

    Id_Factura = Column(Integer, primary_key=True, nullable=False)
    Id_Sucursal = Column(Integer, ForeignKey("Sucursales.Id_Sucursal"), nullable=False)
    Id_Cliente = Column(Integer, ForeignKey("Clientes.Id_Cliente"), nullable=False, default=1, server_default="1")
    Id_Empleado = Column(Integer, ForeignKey("Empleados.Id_Empleado"), nullable=False)
    Id_Dosificacion = Column(Integer, ForeignKey("DosificacionesCAI.Id_Dosificacion"), nullable=False)
    numero_factura = Column(String(19), unique=True, nullable=False)
    cai = Column(String(37), nullable=False)
    fecha_emision = Column(DateTime, nullable=False, server_default=func.now())
    subtotal_exento = Column(Numeric(8, 2), nullable=False)
    subtotal_gravado_15 = Column(Numeric(8, 2), nullable=False)
    subtotal_gravado_18 = Column(Numeric(8, 2), nullable=False)
    isv_15 = Column(Numeric(5, 2), nullable=False)
    isv_18 = Column(Numeric(5, 2), nullable=False)
    impuesto_total = Column(Numeric(8, 2), nullable=False)
    descuento_total = Column(Numeric(8, 2), nullable=False)
    total_pagar = Column(Numeric(8, 2), nullable=False)
    numero_orden_compra_exenta = Column(String(30), nullable=True)
    numero_constancia_registro_exonerado = Column(String(30), nullable=True)
    estado = Column(Integer, nullable=False, default=1, server_default="1")
    sucursal = relationship("Sucursal")
    cliente = relationship("Cliente")
    empleado = relationship("Empleado")
    dosificacion = relationship("DosificacionCAI")


class DetalleFactura(Base):
	__tablename__ = 'Detalle_Facturas'
	__table_args__ = (
        CheckConstraint("cantidad > 0", name="ck_detalle_fact_cantidad"),
        CheckConstraint("precio_unitario >= 0", name="ck_detalle_fact_precio"),
        CheckConstraint("descuento_linea >= 0", name="ck_detalle_fact_descuento"),
        CheckConstraint("impuesto_linea >= 0", name="ck_detalle_fact_impuesto"),
        CheckConstraint("subtotal_linea >= 0", name="ck_detalle_fact_subtotal"),
    )

    Id_Detalle = Column(Integer, primary_key=True, nullable=False)
    Id_Factura = Column(Integer, ForeignKey("Facturas.Id_Factura"), nullable=False)
    Id_Producto = Column(Integer, ForeignKey("Productos.Id_Producto"), nullable=False)
    cantidad = Column(Numeric(6, 2), nullable=False)
    precio_unitario = Column(Numeric(8, 2), nullable=False)
    descuento_linea = Column(Numeric(8, 2), nullable=False, default=0, server_default="0.00")
    impuesto_linea = Column(Numeric(8, 2), nullable=False)
    subtotal_linea = Column(Numeric(8, 2), nullable=False)
    factura = relationship("Factura")
    producto = relationship("Producto")


class MetodoPago(Base):


class Tarjeta(Base):


class PagoFactura(Base):


class Oferta(Base):
    __tablename__ = 'Ofertas'
    __table_args__ = (
        CheckConstraint("descripcion BETWEEN 0 AND 1", name="ck_descripcion_ofertas"),
        CheckConstraint("fecha_fin > fecha_inicio", name="ck_ofertas_fechas"),
        CheckConstraint("estado BETWEEN 0 AND 1", name="ck_ofertas_estado"),
    )

    Id_Oferta = Column(Integer, primary_key=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Numeric(8, 2), nullable=False)
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_fin = Column(DateTime, nullable=False)
    estado = Column(Integer, nullable=False, default=1, server_default="1")


class ProductoOferta(Base):
	__tablename__ = 'ProductosOfertas'

	Id_ProductosOfertas = Column(Integer, primary_key=True, nullable=False)
    Id_Productos = Column(Integer, ForeignKey("Productos.Id_Producto"), nullable=False)
    Id_Oferta = Column(Integer, ForeignKey("Ofertas.Id_Oferta"), nullable=False)

    producto = relationship("Producto")
    oferta = relationship("Oferta")


class Caja(Base):
	__tablename__ = 'Cajas'

	Id_Caja = Column(Integer, primary_key=True, nullable=False)
    Id_Sucursal = Column(Integer, ForeignKey("Sucursales.Id_Sucursal"), nullable=False)
    numero_caja = Column(String(20), nullable=False)
    descripcion = Column(String(100), nullable=True)
    estado = Column(Integer, nullable=False, default=1, server_default="1")
    sucursal = relationship("Sucursal")


class SesionCaja(Base):
	__tablename__ = 'Sesiones_Cajas'
    __table_args__ = (
        CheckConstraint("monto_inicial >= 0", name="ck_secciones_monto_inicial"),
        CheckConstraint("monto_esperado >= 0", name="ck_secciones_monto_esperado"),
        CheckConstraint("diferencia >= 0", name="ck_secciones_diferencia"),
    )

    Id_Seccion = Column(Integer, primary_key=True, nullable=False)
    Id_Caja = Column(Integer, ForeignKey("Cajas.Id_Caja"), nullable=False)
    Id_Empleado = Column(Integer, ForeignKey("Empleados.Id_Empleado"), nullable=False)
    fecha_apertura = Column(DateTime, nullable=False, server_default=func.now())
    monto_inicial = Column(Numeric(10, 2), nullable=False, default=0, server_default="0")
    fecha_cierre = Column(DateTime, nullable=True)
    monto_esperado = Column(Numeric(10, 2), nullable=True, default=0, server_default="0")
    diferencia = Column(Numeric(10, 2), nullable=True, default=0, server_default="0")
    estado = Column(Integer, nullable=False, default=1, server_default="1")
    caja = relationship("Caja")
    empleado = relationship("Empleado")


class RepartidorExterno(Base):
	__tablename__ = 'RepartidorExterno'

	Id_RepartidorExterno = Column(Integer, primary_key=True, nullable=False)
    Id_Persona = Column(Integer, ForeignKey("Personas.Id_Persona"), nullable=False)
    empresa_delivery = Column(String(200), nullable=False)
    tipo_vehiculo = Column(String(50), nullable=True)
    persona = relationship("Persona")


class PedidoADomicilio(Base):


