from datetime import datetime, time

from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.models import (
    Caja,
    Empleado,
    Factura,
    MetodoPago,
    PagoFactura,
    SesionCaja,
)
from app.schemas.caja import (
    AperturaCajaData,
    AperturaContextoOut,
    ArqueoOut,
    CajaDisponible,
    CajeroInfo,
    CierreCajaData,
    SesionCajaOut,
    SucursalResumen,
    TurnoInfo,
    VentaMetodo,
)

ROLES_PERMITIDOS_APERTURA = ["Cajero", "Auxiliar de caja", "Supervisor de caja", "Gerente General"]

ESTADO_ABIERTA = 1
ESTADO_CERRADA = 0


class ErrorCaja(Exception):
    """Error de regla de negocio; el router lo convierte en HTTPException."""

    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


ErrorApertura = ErrorCaja 


def _nombre_completo(empleado: Empleado) -> str:
    p = empleado.persona
    partes = [p.primer_nombre, p.segundo_nombre, p.primer_apellido, p.segundo_apellido]
    return " ".join(x for x in partes if x) or empleado.codigo_empleado


def _dentro_de_horario(ahora: time, inicio: time, fin: time) -> bool:
    if inicio <= fin:
        return inicio <= ahora <= fin
    return ahora >= inicio or ahora <= fin  


def _sesion_abierta_de(db: Session, id_empleado: int) -> SesionCaja | None:
    return (
        db.query(SesionCaja)
        .filter(
            SesionCaja.Id_Empleado == id_empleado,
            SesionCaja.estado == ESTADO_ABIERTA,
            SesionCaja.fecha_cierre.is_(None),
        )
        .first()
    )


def _sesion_out(sesion: SesionCaja) -> SesionCajaOut:
    return SesionCajaOut(
        Id_Sesion=sesion.Id_Sesion,
        Id_Caja=sesion.Id_Caja,
        numero_caja=sesion.caja.numero_caja if sesion.caja else None,
        Id_Empleado=sesion.Id_Empleado,
        fecha_apertura=sesion.fecha_apertura,
        monto_inicial=sesion.monto_inicial,
        estado=sesion.estado,
    )


def _cajas_disponibles(db: Session, id_sucursal: int) -> list[Caja]:
    ocupadas = select(SesionCaja.Id_Caja).where(
        SesionCaja.estado == ESTADO_ABIERTA, SesionCaja.fecha_cierre.is_(None)
    )
    return (
        db.query(Caja)
        .filter(
            Caja.Id_Sucursal == id_sucursal,
            Caja.estado == 1,
            Caja.Id_Caja.not_in(ocupadas.scalar_subquery()),
        )
        .order_by(Caja.numero_caja)
        .all()
    )


def obtener_contexto_apertura(db: Session, id_empleado: int) -> AperturaContextoOut | None:
    empleado = db.get(Empleado, id_empleado)
    if not empleado:
        return None

    ahora = datetime.now()
    rol = empleado.rol_empleado.nombre
    turno = empleado.turno_empleado
    sucursal = empleado.sucursal

    permitido = rol in ROLES_PERMITIDOS_APERTURA
    motivo = None if permitido else (
        f"Tu rol ({rol}) no tiene permiso para abrir una caja."
    )

    abierta = _sesion_abierta_de(db, empleado.Id_Empleado)
    cajas = _cajas_disponibles(db, empleado.Id_Sucursal) if permitido and not abierta else []

    return AperturaContextoOut(
        cajero=CajeroInfo(
            Id_Empleado=empleado.Id_Empleado,
            codigo_empleado=empleado.codigo_empleado,
            nombre_completo=_nombre_completo(empleado),
            rol=rol,
            sucursal=SucursalResumen(
                Id_Sucursal=sucursal.Id_Sucursal, nombre=sucursal.nombre_sucursal
            ),
        ),
        turno=TurnoInfo(
            tipo_turno=turno.tipo_turno,
            hora_inicio=turno.hora_inicio,
            hora_finalizacion=turno.hora_finalizacion,
            descripcion=turno.descripcion,
            dentro_de_horario=_dentro_de_horario(
                ahora.time(), turno.hora_inicio, turno.hora_finalizacion
            ),
        ),
        permitido=permitido,
        motivo=motivo,
        roles_permitidos=ROLES_PERMITIDOS_APERTURA,
        sesion_abierta=_sesion_out(abierta) if abierta else None,
        cajas_disponibles=[CajaDisponible.model_validate(c) for c in cajas],
        fecha_servidor=ahora,
    )


def abrir_caja(db: Session, data: AperturaCajaData) -> SesionCajaOut:
    empleado = db.get(Empleado, data.Id_Empleado)
    if not empleado:
        raise ErrorApertura(404, "El empleado no existe")

    if empleado.rol_empleado.nombre not in ROLES_PERMITIDOS_APERTURA:
        raise ErrorApertura(403, "Tu rol no tiene permiso para abrir una caja")

    if _sesion_abierta_de(db, empleado.Id_Empleado):
        raise ErrorApertura(409, "Ya tienes una caja abierta. Debes cerrarla primero")

    caja = db.get(Caja, data.Id_Caja)
    if not caja or caja.estado != 1:
        raise ErrorApertura(404, "La caja no existe o está inactiva")

    if caja.Id_Sucursal != empleado.Id_Sucursal:
        raise ErrorApertura(403, "Esa caja pertenece a otra sucursal")

    ocupada = (
        db.query(SesionCaja)
        .filter(
            SesionCaja.Id_Caja == caja.Id_Caja,
            SesionCaja.estado == ESTADO_ABIERTA,
            SesionCaja.fecha_cierre.is_(None),
        )
        .first()
    )
    if ocupada:
        raise ErrorApertura(409, "Esa caja ya está abierta por otro cajero")

    sesion = SesionCaja(
        Id_Caja=caja.Id_Caja,
        Id_Empleado=empleado.Id_Empleado,
        monto_inicial=data.monto_inicial,
        estado=ESTADO_ABIERTA,
    )
    db.add(sesion)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ErrorApertura(409, "No se pudo abrir la caja: ya está en uso")
    db.refresh(sesion)
    return _sesion_out(sesion)



# Para el arqueo y los cierres de caja

def _es_efectivo(nombre_metodo: str) -> bool:
    return "efectivo" in nombre_metodo.lower()


def _ventas_por_metodo(db: Session, sesion: SesionCaja) -> list[VentaMetodo]:
    """Pagos cobrados por este cajero dentro de la ventana de tiempo de su sesión."""
    fin = sesion.fecha_cierre or datetime.now()
    filas = (
        db.query(
            MetodoPago.nombre,
            func.count(PagoFactura.Id_Pago),
            func.coalesce(func.sum(PagoFactura.monto_pagado), 0),
        )
        .join(PagoFactura, PagoFactura.Id_Metodo_Pago == MetodoPago.Id_Metodo_Pago)
        .join(Factura, Factura.Id_Factura == PagoFactura.Id_Factura)
        .filter(
            Factura.Id_Empleado == sesion.Id_Empleado,
            Factura.estado == 1,
            PagoFactura.fecha_pago >= sesion.fecha_apertura,
            PagoFactura.fecha_pago <= fin,
        )
        .group_by(MetodoPago.nombre)
        .order_by(MetodoPago.nombre)
        .all()
    )
    return [VentaMetodo(metodo=n, cantidad_pagos=c, total=Decimal(t)) for n, c, t in filas]


def _armar_arqueo(db: Session, sesion: SesionCaja, monto_contado: Decimal | None = None) -> ArqueoOut:
    ventas = _ventas_por_metodo(db, sesion)
    efectivo = sum((v.total for v in ventas if _es_efectivo(v.metodo)), Decimal("0"))
    tarjeta = sum((v.total for v in ventas if not _es_efectivo(v.metodo)), Decimal("0"))

    if sesion.estado == ESTADO_CERRADA:
        # muestran los valores que quedaron guardados
        esperado = Decimal(sesion.monto_esperado or 0)
        diferencia = Decimal(sesion.diferencia or 0)
        contado = esperado + diferencia
    else:
        esperado = Decimal(sesion.monto_inicial) + efectivo
        contado = monto_contado
        diferencia = (monto_contado - esperado) if monto_contado is not None else None

    return ArqueoOut(
        Id_Sesion=sesion.Id_Sesion,
        numero_caja=sesion.caja.numero_caja if sesion.caja else None,
        Id_Empleado=sesion.Id_Empleado,
        cajero=_nombre_completo(sesion.empleado),
        fecha_apertura=sesion.fecha_apertura,
        fecha_cierre=sesion.fecha_cierre,
        monto_inicial=sesion.monto_inicial,
        ventas_por_metodo=ventas,
        total_efectivo=efectivo,
        total_tarjeta=tarjeta,
        total_ventas=efectivo + tarjeta,
        monto_esperado=esperado,
        monto_contado=contado,
        diferencia=diferencia,
        estado=sesion.estado,
    )


def obtener_arqueo(db: Session, id_sesion: int) -> ArqueoOut:
    sesion = db.get(SesionCaja, id_sesion)
    if not sesion:
        raise ErrorCaja(404, "La sesión de caja no existe")
    return _armar_arqueo(db, sesion)


def cerrar_caja(db: Session, id_sesion: int, data: CierreCajaData) -> ArqueoOut:
    sesion = db.get(SesionCaja, id_sesion)
    if not sesion:
        raise ErrorCaja(404, "La sesión de caja no existe")
    if sesion.Id_Empleado != data.Id_Empleado:
        raise ErrorCaja(403, "Esta caja fue abierta por otro cajero")
    if sesion.estado != ESTADO_ABIERTA or sesion.fecha_cierre is not None:
        raise ErrorCaja(409, "Esta caja ya está cerrada")


    arqueo = _armar_arqueo(db, sesion, monto_contado=data.monto_contado)

    sesion.fecha_cierre = datetime.now()
    sesion.monto_esperado = arqueo.monto_esperado
    sesion.diferencia = arqueo.diferencia      
    sesion.estado = ESTADO_CERRADA
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ErrorCaja(
            409, "No se pudo cerrar la caja. Verifica que quitaste el CHECK de 'diferencia' en la BD"
        )
    db.refresh(sesion)
    return _armar_arqueo(db, sesion)
