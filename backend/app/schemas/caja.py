from datetime import datetime, time
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class _OutBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class SucursalResumen(BaseModel):
    Id_Sucursal: int
    nombre: str

class CajeroInfo(BaseModel):
    Id_Empleado: int
    codigo_empleado: str
    nombre_completo: str
    rol: str
    sucursal: SucursalResumen

class TurnoInfo(BaseModel):
    tipo_turno: str
    hora_inicio: time
    hora_finalizacion: time
    descripcion: str | None = None
    dentro_de_horario: bool

class CajaDisponible(_OutBase):
    Id_Caja: int
    numero_caja: str
    descripcion: str | None = None

class SesionCajaOut(BaseModel):
    Id_Sesion: int
    Id_Caja: int
    numero_caja: str | None = None
    Id_Empleado: int
    fecha_apertura: datetime
    monto_inicial: Decimal
    estado: int 

class AperturaContextoOut(BaseModel):
    cajero: CajeroInfo
    turno: TurnoInfo
    permitido: bool
    motivo: str | None = None
    roles_permitidos: list[str]
    sesion_abierta: SesionCajaOut | None = None
    cajas_disponibles: list[CajaDisponible]
    fecha_servidor: datetime

class AperturaCajaData(BaseModel):
    Id_Empleado: int
    Id_Caja: int
    monto_inicial: Decimal = Field(ge=0, max_digits=10, decimal_places=2)

# Para los arqueos y cierres de cajas
class CierreCajaData(BaseModel):
    Id_Empleado: int
    monto_contado: Decimal = Field(ge=0, max_digits=10, decimal_places=2)

class VentaMetodo(BaseModel):
    metodo: str
    cantidad_pagos: int
    total: Decimal

class ArqueoOut(BaseModel):
    Id_Sesion: int
    numero_caja: str | None = None
    Id_Empleado: int
    cajero: str
    fecha_apertura: datetime
    fecha_cierre: datetime | None = None
    monto_inicial: Decimal
    ventas_por_metodo: list[VentaMetodo]
    total_efectivo: Decimal
    total_tarjeta: Decimal
    total_ventas: Decimal
    monto_esperado: Decimal            
    monto_contado: Decimal | None = None
    diferencia: Decimal | None = None 
    estado: int                        
