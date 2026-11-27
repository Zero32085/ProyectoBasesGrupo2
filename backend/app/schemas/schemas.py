from datetime import date, time, datetime
from decimal import Decimal
from typing import Annotated, Optional
from pydantic import (
    BaseModel, ConfigDict, EmailStr, Field, model_validator,
)

Dinero = Annotated[Decimal, Field(max_digits=8, decimal_places=2, ge=0)]
DineroGrande = Annotated[Decimal, Field(max_digits=12, decimal_places=2, ge=0)]
Estado = Annotated[int, Field(ge=0, le=1)] 

class OutBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class LoginClienteData(BaseModel):
    correo: EmailStr
    password: str


class LoginEmpleadoData(BaseModel):
    codigo_empleado: str
    password: str


class RegistroClientesData(BaseModel):
    primer_nombre: str = Field(min_length=1, max_length=80)
    segundo_nombre: str | None = Field(default=None, max_length=80)
    primer_apellido: str = Field(min_length=1, max_length=80)
    segundo_apellido: str | None = Field(default=None, max_length=80)
    correo: EmailStr
    password: str = Field(min_length=8, max_length=72)
    telefono: str | None = Field(default=None, max_length=20)
    dni: str | None = Field(default=None, max_length=13)
    rtn: str | None = Field(default=None, max_length=14)
    razon_social: str | None = Field(default=None, max_length=200)
    Id_Direccion: int | None = None


class AuthResponse(OutBase):
    Id_Persona: int
    primer_nombre: str | None = None
    primer_apellido: str | None = None
    correo: str | None = None
    rol: str


class UserOut(BaseModel):
    Id_Persona: int
    primer_nombre: str
    primer_apellido: str


class PersonaCreate(BaseModel):
    dni: str | None = Field(default=None, max_length=13)
    primer_nombre: str = Field(min_length=1, max_length=80)
    segundo_nombre: str | None = Field(default=None, max_length=80)
    primer_apellido: str = Field(min_length=1, max_length=80)
    segundo_apellido: str | None = Field(default=None, max_length=80)
    correo: EmailStr
    password: str = Field(min_length=8, max_length=72)
    fecha_nacimiento: date | None = None
    telefono: str | None = Field(default=None, max_length=20)


class PersonaUpdate(BaseModel):
    dni: str | None = Field(default=None, max_length=13)
    primer_nombre: str | None = Field(default=None, min_length=1, max_length=80)
    segundo_nombre: str | None = Field(default=None, max_length=80)
    primer_apellido: str | None = Field(default=None, min_length=1, max_length=80)
    segundo_apellido: str | None = Field(default=None, max_length=80)
    correo: EmailStr | None = None
    fecha_nacimiento: date | None = None
    telefono: str | None = Field(default=None, max_length=20)
    estado: int | None = Field(default=None, ge=0, le=1)


class PersonaOut(OutBase):
    Id_Persona: int
    dni: str | None = None
    primer_nombre: str | None = None
    segundo_nombre: str | None = None
    primer_apellido: str | None = None
    segundo_apellido: str | None = None
    correo: str | None = None
    fecha_nacimiento: date | None = None
    estado: int
    telefono: str | None = None


class ClienteCreate(BaseModel):
    Id_Persona: int
    Id_Direccion: int
    rtn: str | None = Field(default=None, max_length=14)
    razon_social: str | None = Field(default=None, max_length=200)


class ClienteUpdate(BaseModel):
    Id_Direccion: int | None = None
    rtn: str | None = Field(default=None, max_length=14)
    razon_social: str | None = Field(default=None, max_length=200)


class ClienteOut(OutBase):
    Id_Cliente: int
    Id_Persona: int
    Id_Direccion: int
    rtn: str | None = None
    razon_social: str | None = None


class RolEmpleadoCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    descripcion: str | None = Field(default=None, max_length=500)
    estado: int = Field(default=1, ge=0, le=1)


class RolEmpleadoOut(OutBase):
    Id_RolEmpleado: int
    nombre: str
    descripcion: str | None = None
    estado: int


class TurnoEmpleadoCreate(BaseModel):
    tipo_turno: str = Field(min_length=1, max_length=20)
    hora_inicio: time
    hora_finalizacion: time
    descripcion: str | None = Field(default=None, max_length=100)


class TurnoEmpleadoOut(OutBase):
    Id_TurnoEmpleado: int
    tipo_turno: str
    hora_inicio: time
    hora_finalizacion: time
    descripcion: str | None = None

class PaisCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=50)
    codigo_iso: str = Field(default="HN", min_length=2, max_length=2)
    moneda: str = Field(default="Lempira", min_length=1, max_length=10)
    estado: Estado = 1

class PaisOut(OutBase):
    Id_Pais: int
    nombre: str
    codigo_iso: str
    moneda: str
    estado: int

class DepartamentoCreate(BaseModel):
    Id_Pais: int
    nombre: str = Field(min_length=1, max_length=50)
    estado: Estado = 1

class DepartamentoOut(OutBase):
    Id_Departamento: int
    Id_Pais: int
    nombre: str
    estado: int
    pais: PaisOut | None = None

class CiudadCreate(BaseModel):
    Id_Departamento: int
    nombre: str = Field(min_length=1, max_length=50)
    estado: Estado = 1

class CiudadOut(OutBase):
    Id_Ciudad: int
    Id_Departamento: int
    nombre: str
    estado: int
    departamento: DepartamentoOut | None = None

class DireccionCreate(BaseModel):
    Id_Ciudad: int
    colonia: str = Field(min_length=1, max_length=50)
    calle: str | None = Field(default=None, max_length=50)
    referencia: str = Field(min_length=1, max_length=200)
    nombre_destinatario: str | None = Field(default=None, max_length=50)

class DireccionOut(OutBase):
    Id_Direccion: int
    Id_Ciudad: int
    colonia: str
    calle: str | None
    referencia: str
    ciudad: CiudadOut | None = None

class SucursalCreate(BaseModel):
    Id_Direccion: int
    nombre: str = Field(min_length=1, max_length=50)
    telefono: str = Field(min_length=1, max_length=20)
    estado: Estado = 1

class SucursalOut(OutBase):
    Id_Sucursal: int
    Id_Direccion: int
    nombre_sucursal: str
    telefono: str
    estado: int

class SucursalResumenOut(OutBase):
    Id_Sucursal: int
    nombre_sucursal: str


class EmpleadoCreate(BaseModel):
    codigo_empleado: str = Field(min_length=1, max_length=10)
    Id_Persona: int
    salario_base: Decimal | None = Field(default=None, gt=0, max_digits=12, decimal_places=2)
    fecha_contratacion: date
    Id_RolEmpleado: int
    Id_TurnoEmpleado: int
    Id_Sucursal: int

class EmpleadoUpdate(BaseModel):
    salario_base: Decimal | None = Field(default=None, gt=0, max_digits=12, decimal_places=2)
    Id_RolEmpleado: int | None = None
    Id_TurnoEmpleado: int | None = None
    Id_Sucursal: int | None = None

class EmpleadoOut(OutBase):
    Id_Empleado: int
    codigo_empleado: str
    Id_Persona: int
    salario_base: Decimal | None
    fecha_contratacion: date
    Id_RolEmpleado: int
    Id_TurnoEmpleado: int
    Id_Sucursal: int

class RepartidorExternoCreate(BaseModel):
    Id_Persona: int
    empresa_delivery: str = Field(min_length=1, max_length=200)
    tipo_vehiculo: str | None = Field(default=None, max_length=50)

class RepartidorExternoOut(OutBase):
    Id_RepartidorExterno: int
    Id_Persona: int
    empresa_delivery: str
    tipo_vehiculo: str | None

class CajaCreate(BaseModel):
    Id_Sucursal: int
    numero_caja: str = Field(min_length=1, max_length=20)
    descripcion: str | None = Field(default=None, max_length=100)
    estado: Estado = 1

class CajaOut(OutBase):
    Id_Caja: int
    Id_Sucursal: int
    numero_caja: str
    descripcion: str | None
    estado: int

class SeccionCajaAbrir(BaseModel):
    Id_Caja: int
    Id_Empleado: int
    monto_inicial: Decimal = Field(default=Decimal("0"), ge=0, max_digits=10, decimal_places=2)

class SeccionCajaCerrar(BaseModel):
    monto_contado: Decimal = Field(ge=0, max_digits=10, decimal_places=2)

class SeccionCajaOut(OutBase):
    Id_Seccion: int
    Id_Caja: int
    Id_Empleado: int
    fecha_apertura: datetime
    monto_inicial: Decimal
    fecha_cierre: datetime | None
    monto_esperado: Decimal | None
    diferencia: Decimal | None
    estado: int

class CategoriaCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    descripcion: str = Field(min_length=1, max_length=500)
    estado: Estado = 1

class CategoriaOut(OutBase):
    Id_Categoria: int
    nombre: str
    descripcion: str
    estado: int

class MarcaCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=50)
    pais_origen: str | None = Field(default=None, max_length=50)
    estado: Estado = 1

class MarcaOut(OutBase):
    Id_Marca: int
    nombre: str
    pais_origen: str | None
    estado: int

class ProductoCreate(BaseModel):
    Id_Categoria: int
    Id_Sucursal: int
    cod_barra: str = Field(min_length=1, max_length=20)
    nombre: str = Field(min_length=1, max_length=100)
    descripcion: str | None = Field(default=None, max_length=500)
    Id_Marca: int
    stock_minimo: Dinero = Decimal("10")
    stock_maximo: Dinero | None = None
    precio: Dinero
    costo: Dinero
    porcentaje_isv: Dinero
    estado: Estado = 1

    #@model_validator(mode="after")
    #def validar_stock(self):
    #    if self.stock_maximo is not None and self.stock_maximo < self.stock_minimo:
    #        raise ValueError("stock_maximo no puede ser menor que stock_minimo")
    #    return self

class ProductoUpdate(BaseModel):
    Id_Categoria: int | None = None
    Id_Marca: int | None = None
    cod_barra: str | None = Field(default=None, min_length=1, max_length=20)
    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    descripcion: str | None = Field(default=None, max_length=500)
    stock_minimo: Dinero | None = None
    stock_maximo: Dinero | None = None
    precio: Dinero | None = None
    costo: Dinero | None = None
    porcentaje_isv: Dinero | None = None
    estado: Estado | None = None

class ProductoOut(OutBase):
    Id_Producto: int
    Id_Categoria: int
    Id_Sucursal: int
    cod_barra: str
    nombre: str
    descripcion: str | None
    Id_Marca: int
    stock_minimo: Decimal
    stock_maximo: Decimal | None
    precio: Decimal
    costo: Decimal
    porcentaje_isv: Decimal
    estado: int

class OfertaCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    porcentaje_descuento: Decimal = Field(ge=0, le=1, max_digits=8, decimal_places=2)  # 0.15 = 15%
    fecha_inicio: datetime
    fecha_fin: datetime
    estado: Estado = 1

    #@model_validator(mode="after")
    #def validar_fechas(self):
    #    if self.fecha_fin <= self.fecha_inicio:
    #        raise ValueError("fecha_fin debe ser posterior a fecha_inicio")
    #    return self

class OfertaOut(OutBase):
    Id_Oferta: int
    nombre: str
    porcentaje_descuento: Decimal
    fecha_inicio: datetime
    fecha_fin: datetime
    estado: int

class ProductoOfertaCreate(BaseModel):
    Id_Productos: int
    Id_Oferta: int

class ProductoOfertaOut(OutBase):
    Id_ProductosOfertas: int
    Id_Productos: int
    Id_Oferta: int


class ProveedorCreate(BaseModel):
    direccion : DireccionCreate
    nombre_o_razonSocial: str = Field(min_length=1, max_length=100)
    rtn: str = Field(min_length=1, max_length=14)
    nombre_contacto: str = Field(min_length=1, max_length=50)
    correo: EmailStr | None = None
    estado: Estado = 1
    telefonos: list[str]

class ProveedorUpdate(BaseModel):
    direccion : DireccionCreate
    nombre_o_razonSocial: str = Field(min_length=1, max_length=100)
    rtn: str = Field(min_length=1, max_length=14)
    nombre_contacto: str = Field(min_length=1, max_length=50)
    correo: EmailStr | None = None
    estado: Estado = 1
    telefonos: list[str]

class ProveedorOut(OutBase):
    Id_Proveedor: int
    Id_Direccion: int
    nombre_o_razonSocial: str
    rtn: str
    nombre_contacto: str
    correo: str | None
    fecha_Registro: datetime
    estado: int

class ProveedorResumenOut(OutBase):
    Id_Proveedor: int
    nombre_o_razonSocial: str
    rtn: str


class TelefonoProveedorCreate(BaseModel):
    Id_Proveedor: int
    telefono: str = Field(min_length=1, max_length=20)
    estado: Estado = 1

class TelefonoProveedorOut(OutBase):
    Id_TelefonoProveedor: int
    Id_Proveedor: int
    telefono: str
    estado: int

class ProveedorListadoOut(OutBase):
    Id_Proveedor: int
    Id_Direccion: int
    nombre_o_razonSocial: str
    rtn: str
    nombre_contacto: str
    correo: str | None
    fecha_Registro: datetime
    estado: int
    direccion : DireccionOut | None = None
    telefonos : list[TelefonoProveedorOut] = []

class DetalleCompraCreate(BaseModel):
# Datos del producto y su lote para cada línea de compra
    Id_Producto: int
    cantidad: Decimal = Field(..., gt=0)
    precio_unitario: Decimal = Field(..., ge=0)
    descuento: Decimal = Field(default=Decimal("0.00"), ge=0)
    lote_codigo: str = Field(..., min_length=1, max_length=60)
    fecha_fabricacion: Optional[date] = None
    fecha_vencimiento: date

class DetalleCompraOut(OutBase):
    Id_Detalle_Compras: int
    Id_Compra: int
    Id_Producto: int
    cantidad: Decimal
    precio_unitario: Decimal
    descuento: Decimal | None
    subtotal_linea: Decimal

class CompraCreate(BaseModel):
    Id_Proveedor: int
    Id_Sucursal: int
    numero_factura: str = Field(min_length=1, max_length=19)
    estado: int = 1
    detalles: list[DetalleCompraCreate] = Field(min_length=1)

class CompraOut(OutBase):
    Id_Compra: int
    Id_Proveedor: int
    Id_Sucursal: int
    fecha_compra: datetime
    numero_factura: str
    subtotal: Decimal
    impuesto: Decimal
    total: Decimal
    estado: int
    proveedor: ProveedorResumenOut | None = None
    sucursal: SucursalResumenOut | None = None

    model_config = ConfigDict(from_attributes=True)

class CompraDetalleOut(CompraOut):
    detalles: list[DetalleCompraOut] = []

class LoteVencimientoCreate(BaseModel):
    Id_DetalleCompra: int
    lote_codigo: str = Field(min_length=1, max_length=50)
    fecha_fabricacion: date
    fecha_vencimiento: date

    #@model_validator(mode="after")
    #def validar_fechas(self):
    #    if self.fecha_vencimiento <= self.fecha_fabricacion:
    #        raise ValueError("fecha_vencimiento debe ser posterior a fecha_fabricacion")
    #    return self

class LoteVencimientoOut(OutBase):
    Id_lote_vencimiento: int
    Id_DetalleCompra: int
    lote_codigo: str
    fecha_fabricacion: date
    fecha_vencimiento: date

class DetalleCompraItemOut(BaseModel):
    # Representa una fila del detalle + su lote asociado
    Id_Detalle_Compras: int
    Id_Producto: int
    nombre_producto: str
    cantidad: Decimal
    precio_unitario: Decimal
    descuento: Decimal
    subtotal_linea: Decimal
    lote_codigo: str
    fecha_fabricacion: Optional[date] = None
    fecha_vencimiento: date

    class Config:
        from_attributes = True


class CompraDetalleRespuestaOut(BaseModel):
    # Cabecera de la compra + lista de detalles con lote
    Id_Compra: int
    Id_Proveedor: int
    Id_Sucursal: int
    numero_factura: str
    subtotal: Decimal
    impuesto: Decimal
    total: Decimal
    estado: int
    detalles: list[DetalleCompraItemOut]

class InventarioCreate(BaseModel):
    Id_Producto: int
    Id_Sucursal: int
    Id_lote_vencimiento: int
    stock_actual: Dinero

class InventarioUpdate(BaseModel):
    stock_actual: Dinero

class InventarioOut(OutBase):
    Id_Inventario: int
    Id_Producto: int
    Id_Sucursal: int
    Id_lote_vencimiento: int
    stock_actual: Decimal

class AutorizacionesSARCreate(BaseModel):
    Id_Sucursal: int
    cai: str = Field(min_length=1, max_length=37)
    fecha_limite_emision: date
    rango_inicial: str = Field(min_length=1, max_length=19)
    rango_final: str = Field(min_length=1, max_length=19)
    correlativo_actual: int = Field(ge=0)
    estado: Estado = 1

class AutorizacionesSAROut(OutBase):
    Id_autorizacion_sar: int
    Id_Sucursal: int
    cai: str
    fecha_limite_emision: date
    rango_inicial: str
    rango_final: str
    correlativo_actual: int
    estado: int

class MetodoPagoCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=50)
    descripcion: str | None = Field(default=None, max_length=200)
    estado: Estado = 1

class MetodoPagoOut(OutBase):
    Id_Metodo_Pago: int
    nombre: str
    descripcion: str | None
    estado: int

class TarjetaCreate(BaseModel):
    Id_Cliente: int
    nombre_titular: str = Field(min_length=1, max_length=100)
    final_tarjeta: str = Field(pattern=r"^\d{4}$")
    mes: int = Field(ge=1, le=12)
    anio: int = Field(ge=2000, le=2100)
    marca: str = Field(min_length=1, max_length=20)
    token_generado: str = Field(min_length=1, max_length=255)

class TarjetaOut(OutBase):
    Id_Tarjeta: int
    Id_Cliente: int
    nombre_titular: str
    final_tarjeta: str
    mes: int
    anio: int
    marca: str
    estado: int

class DetalleFacturaCreate(BaseModel):
    Id_Producto: int
    cantidad: Decimal = Field(gt=0, max_digits=6, decimal_places=2)
    descuento_linea: Dinero = Decimal("0.00")

class DetalleFacturaOut(OutBase):
    Id_Detalle: int
    Id_Factura: int
    Id_Producto: int
    cantidad: Decimal
    precio_unitario: Decimal
    descuento_linea: Decimal
    impuesto_linea: Decimal
    subtotal_linea: Decimal

class PagoFacturaCreate(BaseModel):
    Id_Metodo_Pago: int
    Id_Tarjeta: int | None = None
    monto_pagado: Dinero
    referencia_transaccion: str | None = Field(default=None, max_length=100)

class PagoFacturaOut(OutBase):
    Id_Pago: int
    Id_Factura: int
    Id_Metodo_Pago: int
    Id_Tarjeta: int | None
    monto_pagado: Decimal
    referencia_transaccion: str | None
    fecha_pago: datetime

class FacturaCreate(BaseModel):
    Id_Sucursal: int
    Id_Cliente: int = 1  # 1 = consumidor final (default de tu tabla)
    Id_Empleado: int
    Id_autorizacion_sar: int
    numero_orden_compra_exenta: str | None = Field(default=None, max_length=30)
    numero_constancia_registro_exonerado: str | None = Field(default=None, max_length=30)
    detalles: list[DetalleFacturaCreate] = Field(min_length=1)
    pagos: list[PagoFacturaCreate] = Field(min_length=1)

class FacturaOut(OutBase):
    Id_Factura: int
    Id_Sucursal: int
    Id_Cliente: int
    Id_Empleado: int
    Id_autorizacion_sar: int
    numero_factura: str
    cai: str
    fecha_emision: datetime
    subtotal_exento: Decimal
    subtotal_gravado_15: Decimal
    subtotal_gravado_18: Decimal
    isv_15: Decimal
    isv_18: Decimal
    impuesto_total: Decimal
    descuento_total: Decimal
    total_pagar: Decimal
    numero_orden_compra_exenta: str | None
    numero_constancia_registro_exonerado: str | None
    estado: int

class FacturaDetalleOut(FacturaOut):
    detalles: list[DetalleFacturaOut] = []
    pagos: list[PagoFacturaOut] = []

class PedidoADomicilioCreate(BaseModel):
    Id_Repartidor: int
    Id_Factura: int
    nombre_destinatario: str = Field(min_length=1, max_length=50)
    tarifa: Decimal = Field(gt=0, max_digits=8, decimal_places=2)
    Id_Direccion: int

class PedidoADomicilioUpdate(BaseModel):
    hora_salida: datetime | None = None
    hora_entrega: datetime | None = None
    estado_entrega: Estado | None = None  # 1 entregado, 0 pendiente

class PedidoADomicilioOut(OutBase):
    Id_PedidoADomicilio: int
    Id_Repartidor: int
    Id_Factura: int
    nombre_destinatario: str
    tarifa: Decimal
    hora_salida: datetime | None
    hora_entrega: datetime | None
    Id_Direccion: int
    estado_entrega: int
