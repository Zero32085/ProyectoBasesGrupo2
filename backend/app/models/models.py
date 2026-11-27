from sqlalchemy import (
    CheckConstraint,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    SmallInteger,
    String,
    Time,
    func,
)
from sqlalchemy.orm import relationship

from app.database import Base


class Pais(Base):
    __tablename__ = "paises"
    __table_args__ = (
        CheckConstraint("estado IN (0, 1)", name="ck_paises_estado"),
    )

    Id_Pais = Column("id_pais", Integer, primary_key=True, nullable=False)
    nombre = Column(String(50), nullable=False)
    codigo_iso = Column(String(2), nullable=False, default="HN", server_default="HN")
    moneda = Column(String(100), nullable=False, default="Lempira", server_default="Lempira")
    estado = Column(Integer, nullable=False, default=1, server_default="1")


class Departamento(Base):
    __tablename__ = "departamentos"
    __table_args__ = (
        CheckConstraint("estado IN (0, 1)", name="ck_departamentos_estado"),
    )

    Id_Departamento = Column("id_departamento", Integer, primary_key=True, nullable=False)
    Id_Pais = Column("id_pais", Integer, ForeignKey("paises.id_pais"), nullable=False)
    nombre = Column(String(50), nullable=False)
    estado = Column(Integer, nullable=False, default=1, server_default="1")
    pais = relationship("Pais")


class Ciudad(Base):
    __tablename__ = "ciudades"
    __table_args__ = (
        CheckConstraint("estado IN (0, 1)", name="ck_ciudades_estado"),
    )

    Id_Ciudad = Column("id_ciudad", Integer, primary_key=True, nullable=False)
    Id_Departamento = Column("id_departamento", Integer, ForeignKey("departamentos.id_departamento"), nullable=False)
    nombre = Column(String(50), nullable=False)
    estado = Column(Integer, nullable=False, default=1, server_default="1")
    departamento = relationship("Departamento")


class Direccion(Base):
    __tablename__ = "direcciones"

    Id_Direccion = Column("id_direccion", Integer, primary_key=True, nullable=False)
    Id_Ciudad = Column("id_ciudad", Integer, ForeignKey("ciudades.id_ciudad"), nullable=False)
    colonia = Column(String(50), nullable=False)
    calle = Column(String(50), nullable=True)
    referencia = Column(String(200), nullable=False)
    nombre_destinatario = Column(String(50), nullable=True)
    ciudad = relationship("Ciudad")


class Sucursal(Base):
    __tablename__ = "sucursales"
    __table_args__ = (
        CheckConstraint("estado IN (0, 1)", name="ck_sucursales_estado"),
    )

    Id_Sucursal = Column("id_sucursal", Integer, primary_key=True, nullable=False)
    Id_Direccion = Column("id_direccion", Integer, ForeignKey("direcciones.id_direccion"), nullable=False)
    nombre_sucursal = Column(String(50), nullable=False)
    telefono = Column(String(20), nullable=False)
    estado = Column(Integer, nullable=False, default=1, server_default="1")
    direccion = relationship("Direccion")


class Proveedor(Base):
    __tablename__ = "proveedores"
    __table_args__ = (
        CheckConstraint("estado IN (0, 1)", name="ck_proveedores_estado"),
    )

    Id_Proveedor = Column("id_proveedor", Integer, primary_key=True, nullable=False)
    Id_Direccion = Column("id_direccion", Integer, ForeignKey("direcciones.id_direccion"), nullable=False)
    nombre_o_razonSocial = Column("nombre_o_razonsocial", String(100), nullable=False)
    rtn = Column(String(14), unique=True, nullable=False)
    nombre_contacto = Column(String(50), nullable=False)
    correo = Column(String(50), nullable=True)
    fecha_Registro = Column("fecha_registro", DateTime, nullable=False, server_default=func.now())
    estado = Column(Integer, nullable=False, default=1, server_default="1")
    direccion = relationship("Direccion")


class TelefonoProveedor(Base):
    __tablename__ = "telefonos_proveedores"
    __table_args__ = (
        CheckConstraint("estado IN (0, 1)", name="ck_telefonos_proveedores_estado"),
    )

    Id_TelefonoProveedor = Column("id_telefonoproveedor", Integer, primary_key=True, nullable=False)
    Id_Proveedor = Column("id_proveedor", Integer, ForeignKey("proveedores.id_proveedor"), nullable=False)
    telefono = Column(String(20), nullable=False)
    estado = Column(Integer, nullable=False, default=1, server_default="1")
    proveedor = relationship("Proveedor")


class Categoria(Base):
    __tablename__ = "categorias"
    __table_args__ = (
        CheckConstraint("estado IN (0, 1)", name="ck_categorias_estado"),
    )

    Id_Categoria = Column("id_categoria", Integer, primary_key=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(500), nullable=False)
    estado = Column(Integer, nullable=False, default=1, server_default="1")


class Marca(Base):
    __tablename__ = "marcas"
    __table_args__ = (
        CheckConstraint("estado IN (0, 1)", name="ck_marcas_estado"),
    )

    Id_Marca = Column("id_marca", Integer, primary_key=True, nullable=False)
    nombre = Column(String(50), nullable=False)
    pais_origen = Column(String(50), nullable=True)
    estado = Column(Integer, nullable=False, default=1, server_default="1")


class Producto(Base):
    __tablename__ = "productos"
    __table_args__ = (
        CheckConstraint("stock_minimo >= 0", name="ck_productos_stock_minimo"),
        CheckConstraint("stock_maximo >= 0", name="ck_productos_stock_maximo"),
        CheckConstraint("precio >= 0", name="ck_productos_precio"),
        CheckConstraint("costo >= 0", name="ck_productos_costo"),
        CheckConstraint("estado IN (0, 1)", name="ck_productos_estado"),
    )

    Id_Producto = Column("id_producto", Integer, primary_key=True, nullable=False)
    Id_Sucursal = Column("id_sucursal", Integer, ForeignKey("sucursales.id_sucursal"), nullable=False)
    Id_Categoria = Column("id_categoria", Integer, ForeignKey("categorias.id_categoria"), nullable=False)
    Id_Marca = Column("id_marca", Integer, ForeignKey("marcas.id_marca"), nullable=False)
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
    __tablename__ = "compras"
    __table_args__ = (
        CheckConstraint("estado IN (0, 1)", name="ck_compras_estado"),
    )

    Id_Compra = Column("id_compra", Integer, primary_key=True, nullable=False)
    Id_Proveedor = Column("id_proveedor", Integer, ForeignKey("proveedores.id_proveedor"), nullable=False)
    Id_Sucursal = Column("id_sucursal", Integer, ForeignKey("sucursales.id_sucursal"), nullable=False)
    fecha_compra = Column(DateTime, nullable=False, server_default=func.now())
    numero_factura = Column(String(19), nullable=False)
    subtotal = Column(Numeric(12, 2), nullable=False)
    impuesto = Column(Numeric(12, 2), nullable=False)
    total = Column(Numeric(12, 2), nullable=False)
    estado = Column(Integer, nullable=False, default=1, server_default="1")
    proveedor = relationship("Proveedor")
    sucursal = relationship("Sucursal")


class DetalleCompra(Base):
    __tablename__ = "detalle_compras"

    Id_Detalle_Compras = Column("id_detalle_compras", Integer, primary_key=True, nullable=False)
    Id_Compra = Column("id_compra", Integer, ForeignKey("compras.id_compra"), nullable=False)
    Id_Producto = Column("id_producto", Integer, ForeignKey("productos.id_producto"), nullable=False)
    cantidad = Column(Numeric(8, 2), nullable=False)
    precio_unitario = Column(Numeric(8, 2), nullable=False)
    descuento = Column(Numeric(8, 2), nullable=True)
    subtotal_linea = Column(Numeric(12, 2), nullable=False)
    compra = relationship("Compra")
    producto = relationship("Producto")


class LoteVencimiento(Base):
    __tablename__ = "lotes_vencimiento"
    __table_args__ = (
        CheckConstraint("fecha_vencimiento > fecha_fabricacion", name="ck_Lote_fecha_vencimiento"),
    )

    Id_LoteVencimiento = Column("id_lotevencimiento", Integer, primary_key=True, nullable=False)
    Id_DetalleCompra = Column("id_detallecompra", Integer, ForeignKey("detalle_compras.id_detalle_compras"), nullable=False)
    lote_codigo = Column(String(50), nullable=False)
    fecha_fabricacion = Column(Date, nullable=False)
    fecha_vencimiento = Column(Date, nullable=False)
    detalle_compra = relationship("DetalleCompra")


class Inventario(Base):
    __tablename__ = "inventarios"
    __table_args__ = (
        CheckConstraint("stock_actual >= 0", name="ck_inventarios_stock_actual"),
    )

    Id_Inventario = Column("id_inventario", Integer, primary_key=True, nullable=False)
    Id_Producto = Column("id_producto", Integer, ForeignKey("productos.id_producto"), nullable=False)
    Id_Sucursal = Column("id_sucursal", Integer, ForeignKey("sucursales.id_sucursal"), nullable=False)
    Id_lote_vencimiento = Column("id_lote_vencimiento", Integer, ForeignKey("lotes_vencimiento.id_lotevencimiento"), nullable=False)   
    stock_actual = Column(Numeric(8, 2), nullable=False)
    producto = relationship("Producto")
    sucursal = relationship("Sucursal")
    lote = relationship("LoteVencimiento")


class Persona(Base):
    __tablename__ = "personas"
    __table_args__ = (
        CheckConstraint("estado IN (0, 1)", name="ck_personas_estado"),
    )

    Id_Persona = Column("id_persona", Integer, primary_key=True, nullable=False)
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
    __tablename__ = "clientes"

    Id_Cliente = Column("id_cliente", Integer, primary_key=True, nullable=False)
    Id_Persona = Column("id_persona", Integer, ForeignKey("personas.id_persona"), nullable=False)
    rtn = Column(String(14), unique=True, nullable=True)
    Id_Direccion = Column("id_direccion", Integer, ForeignKey("direcciones.id_direccion"), nullable=False)
    razon_social = Column(String(200), nullable=True)
    persona = relationship("Persona")
    direccion = relationship("Direccion")


class RolEmpleado(Base):
    __tablename__ = "roles_empleados"
    __table_args__ = (
        CheckConstraint("estado IN (0, 1)", name="ck_roles_empleados_estado"),
    )

    Id_RolEmpleado = Column("id_rolempleado", Integer, primary_key=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(500), nullable=True)
    estado = Column(Integer, nullable=False, default=1, server_default="1")


class TurnoEmpleado(Base):
    __tablename__ = "turnos_empleados"

    Id_TurnoEmpleado = Column("id_turnoempleado", Integer, primary_key=True, index=True, nullable=False)
    tipo_turno = Column(String(20), nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_finalizacion = Column(Time, nullable=False)
    descripcion = Column(String(100), nullable=True)


class Empleado(Base):
    __tablename__ = "empleados"
    __table_args__ = (
        CheckConstraint("salario_base > 0", name="ck_empleados_salario_base"),
    )

    Id_Empleado = Column("id_empleado", Integer, primary_key=True, index=True, nullable=False)
    codigo_empleado = Column(String(10), unique=True, nullable=False)
    Id_Persona = Column("id_persona", Integer, ForeignKey("personas.id_persona"), nullable=False)
    salario_base = Column(Numeric(10, 2), nullable=False)
    fecha_contratacion = Column(Date, nullable=False)
    Id_RolEmpleado = Column("id_rolempleado", Integer, ForeignKey("roles_empleados.id_rolempleado"), nullable=False)
    Id_TurnoEmpleado = Column("id_turnoempleado", Integer, ForeignKey("turnos_empleados.id_turnoempleado"), nullable=False)
    Id_Sucursal = Column("id_sucursal", Integer, ForeignKey("sucursales.id_sucursal"), nullable=False)
    persona = relationship("Persona")
    turno_empleado = relationship("TurnoEmpleado")
    rol_empleado = relationship("RolEmpleado")
    sucursal = relationship("Sucursal")


class AutorizacionesSAR(Base):
    __tablename__ = "autorizaciones_sar"
    __table_args__ = (
        CheckConstraint("estado IN (0, 1)", name="ck_autorizaciones_sar_estado"),
    )

    Id_autorizacion_sar = Column("id_autorizacion_sar", Integer, primary_key=True, nullable=False)
    Id_Sucursal = Column("id_sucursal", Integer, ForeignKey("sucursales.id_sucursal"), nullable=False)
    cai = Column(String(37), nullable=False)
    fecha_limite_emision = Column(Date, nullable=False)
    rango_inicial = Column(String(19), nullable=False)
    rango_final = Column(String(19), nullable=False)
    correlativo_actual = Column(Integer, nullable=False)
    estado = Column(Integer, nullable=False)
    sucursal = relationship("Sucursal")


class Factura(Base):
    __tablename__ = "facturas"
    __table_args__ = (
        CheckConstraint("subtotal_exento >= 0", name="ck_facturas_subtotal_exento"),
        CheckConstraint("subtotal_gravado_15 >= 0", name="ck_facturas_subtotal_gravado_15"),
        CheckConstraint("subtotal_gravado_18 >= 0", name="ck_facturas_subtotal_gravado_18"),
        CheckConstraint("isv_15 >= 0", name="ck_facturas_isv_15"),
        CheckConstraint("isv_18 >= 0", name="ck_facturas_isv_18"),
        CheckConstraint("impuesto_total >= 0", name="ck_facturas_impuesto_total"),
        CheckConstraint("descuento_total >= 0", name="ck_facturas_descuento_total"),
        CheckConstraint("total_pagar >= 0", name="ck_facturas_total_pagar"),
        CheckConstraint("estado IN (0, 1)", name="ck_facturas_estado"),
    )

    Id_Factura = Column("id_factura", Integer, primary_key=True, nullable=False)
    Id_Sucursal = Column("id_sucursal", Integer, ForeignKey("sucursales.id_sucursal"), nullable=False)
    Id_Cliente = Column("id_cliente", Integer, ForeignKey("clientes.id_cliente"), nullable=False, default=1, server_default="1")
    Id_Empleado = Column("id_empleado", Integer, ForeignKey("empleados.id_empleado"), nullable=False)
    Id_autorizacion_sar = Column("id_autorizacion_sar", Integer, ForeignKey("autorizaciones_sar.id_autorizacion_sar"), nullable=False)
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
    autorizacionesSAR = relationship("AutorizacionesSAR")


class DetalleFactura(Base):
    __tablename__ = "detalle_facturas"
    __table_args__ = (
        CheckConstraint("cantidad > 0", name="ck_detalle_fact_cantidad"),
        CheckConstraint("precio_unitario >= 0", name="ck_detalle_fact_precio"),
        CheckConstraint("descuento_linea >= 0", name="ck_detalle_fact_descuento"),
        CheckConstraint("impuesto_linea >= 0", name="ck_detalle_fact_impuesto"),
        CheckConstraint("subtotal_linea >= 0", name="ck_detalle_fact_subtotal"),
    )

    Id_Detalle = Column("id_detalle", Integer, primary_key=True, nullable=False)
    Id_Factura = Column("id_factura", Integer, ForeignKey("facturas.id_factura"), nullable=False)
    Id_Producto = Column("id_producto", Integer, ForeignKey("productos.id_producto"), nullable=False)
    cantidad = Column(Numeric(6, 2), nullable=False)
    precio_unitario = Column(Numeric(8, 2), nullable=False)
    descuento_linea = Column(Numeric(8, 2), nullable=False, default=0, server_default="0.00")
    impuesto_linea = Column(Numeric(8, 2), nullable=False)
    subtotal_linea = Column(Numeric(8, 2), nullable=False)
    factura = relationship("Factura")
    producto = relationship("Producto")


class MetodoPago(Base):
    __tablename__ = "metodos_pagos"
    __table_args__ = (
        CheckConstraint("estado IN (0, 1)", name="ck_metodos_pagos_estado"),
    )

    Id_Metodo_Pago = Column("id_metodo_pago", Integer, primary_key=True, nullable=False)
    nombre = Column(String(50), nullable=False)
    descripcion = Column(String(200), nullable=True)
    estado = Column(Integer, nullable=False)


class Tarjeta(Base):
    __tablename__ = "tarjetas"
    __table_args__ = (
        CheckConstraint("mes BETWEEN 1 AND 12", name="ck_tarjeta_mes"),
        CheckConstraint("anio BETWEEN 2000 AND 2100", name="ck_tarjeta_anio"),
        CheckConstraint("estado BETWEEN 0 AND 1", name="ck_tarjetas_estado"),
    )

    Id_Tarjeta = Column("id_tarjeta", Integer, primary_key=True, nullable=False)
    Id_Cliente = Column("id_cliente", Integer, ForeignKey("clientes.id_cliente"), nullable=False)
    nombre_titular = Column(String(100), nullable=False)
    final_tarjeta = Column(String(4), nullable=False)
    mes = Column(SmallInteger, nullable=False)
    anio = Column(SmallInteger, nullable=False)
    marca = Column(String(20), nullable=False)
    token_generado = Column(String(255), nullable=False)
    estado = Column(Integer, nullable=False, server_default="1")

    cliente = relationship("Cliente")


class PagoFactura(Base):
    __tablename__ = "pagos_facturas"
    __table_args__ = (
        CheckConstraint("monto_pagado >= 0", name="ck_monto_pagado"),
    )

    Id_Pago = Column("id_pago", Integer, primary_key=True, nullable=False)
    Id_Factura = Column("id_factura", Integer, ForeignKey("facturas.id_factura"), nullable=False)
    Id_Metodo_Pago = Column("id_metodo_pago", Integer, ForeignKey("metodos_pagos.id_metodo_pago"), nullable=False)
    Id_Tarjeta = Column("id_tarjeta", Integer, ForeignKey("tarjetas.id_tarjeta"), nullable=False)
    monto_pagado = Column(Numeric(8, 2), nullable=False)
    referencia_transaccion = Column(String(100), nullable=False)
    fecha_pago = Column(DateTime, nullable=False, default=func.now(), server_default=func.now())


class Oferta(Base):
    __tablename__ = "ofertas"
    __table_args__ = (
        CheckConstraint("porcentaje_descuento BETWEEN 0 AND 1", name="ck_porcentaje_descuento_ofertas"),
        CheckConstraint("fecha_fin > fecha_inicio", name="ck_ofertas_fechas"),
        CheckConstraint("estado IN (0, 1)", name="ck_ofertas_estado"),
    )

    Id_Oferta = Column("id_oferta", Integer, primary_key=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(300), nullable=True)
    porcentaje_descuento = Column(Numeric(8, 2), nullable=False)
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_fin = Column(DateTime, nullable=False)
    estado = Column(Integer, nullable=False, default=1, server_default="1")


class ProductoOferta(Base):
    __tablename__ = "productosofertas"

    Id_ProductosOfertas = Column("id_productosofertas", Integer, primary_key=True, nullable=False)
    Id_Productos = Column("id_productos", Integer, ForeignKey("productos.id_producto"), nullable=False)
    Id_Oferta = Column("id_oferta", Integer, ForeignKey("ofertas.id_oferta"), nullable=False)

    producto = relationship("Producto")
    oferta = relationship("Oferta")


class Caja(Base):
    __tablename__ = "cajas"
    __table_args__ = (
        CheckConstraint("estado IN (0, 1)", name="ck_cajas_estado"),
    )

    Id_Caja = Column("id_caja", Integer, primary_key=True, nullable=False)
    Id_Sucursal = Column("id_sucursal", Integer, ForeignKey("sucursales.id_sucursal"), nullable=False)
    numero_caja = Column(String(20), nullable=False)
    descripcion = Column(String(100), nullable=True)
    estado = Column(Integer, nullable=False, default=1, server_default="1")
    sucursal = relationship("Sucursal")


class SesionCaja(Base):
    __tablename__ = "sesiones_cajas"
    __table_args__ = (
        CheckConstraint("monto_inicial >= 0", name="ck_secciones_monto_inicial"),
        CheckConstraint("monto_esperado >= 0", name="ck_secciones_monto_esperado"),
        #CheckConstraint("diferencia >= 0", name="ck_secciones_diferencia"),
        CheckConstraint("estado IN (0, 1)", name="ck_sesiones_cajas_estado"),
    )

    Id_Sesion = Column("id_sesion", Integer, primary_key=True, nullable=False)
    Id_Caja = Column("id_caja", Integer, ForeignKey("cajas.id_caja"), nullable=False)
    Id_Empleado = Column("id_empleado", Integer, ForeignKey("empleados.id_empleado"), nullable=False)
    fecha_apertura = Column(DateTime, nullable=False, server_default=func.now())
    monto_inicial = Column(Numeric(10, 2), nullable=False, default=0, server_default="0")
    fecha_cierre = Column(DateTime, nullable=True)
    monto_esperado = Column(Numeric(10, 2), nullable=True, default=0, server_default="0")
    diferencia = Column(Numeric(10, 2), nullable=True, default=0, server_default="0")
    estado = Column(Integer, nullable=False, default=1, server_default="1")
    caja = relationship("Caja")
    empleado = relationship("Empleado")


class RepartidorExterno(Base):
    __tablename__ = "repartidorexterno"

    Id_RepartidorExterno = Column("id_repartidorexterno", Integer, primary_key=True, nullable=False)
    Id_Persona = Column("id_persona", Integer, ForeignKey("personas.id_persona"), nullable=False)
    empresa_delivery = Column(String(200), nullable=False)
    tipo_vehiculo = Column(String(50), nullable=True)
    persona = relationship("Persona")


class PedidoADomicilio(Base):
    __tablename__ = "pedido_a_domicilio"
    __table_args__ = (
        CheckConstraint("tarifa > 0", name="ck_tarifa"),
        CheckConstraint("estado_entrega IN (0, 1)", name="ck_estado_pedido"),
        CheckConstraint(
            "estado_entrega <> 1 OR (hora_salida IS NOT NULL AND hora_entrega IS NOT NULL AND hora_entrega >= hora_salida)",
            name="ck_pedido_domicilio_horas_completado",
        ),
    )

    Id_PedidoADomicilio = Column("id_pedidoadomicilio", Integer, primary_key=True, nullable=False)
    Id_Repartidor = Column("id_repartidor", Integer, ForeignKey("repartidorexterno.id_repartidorexterno"), nullable=False)
    Id_Factura = Column("id_factura", Integer, ForeignKey("facturas.id_factura"), nullable=False)
    nombre_destinatario = Column(String(50), nullable=False)
    tarifa = Column(Numeric(8, 2), nullable=False)
    hora_salida = Column(DateTime, nullable=True)
    hora_entrega = Column(DateTime, nullable=True)
    Id_Direccion = Column("id_direccion", Integer, ForeignKey("direcciones.id_direccion"), nullable=False)
    estado_entrega = Column(Integer, nullable=False)
