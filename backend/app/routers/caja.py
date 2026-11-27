from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import caja as crud_caja
from app.database import SessionLocal
from app.schemas.caja import (
    AperturaCajaData,
    AperturaContextoOut,
    ArqueoOut,
    CierreCajaData,
    SesionCajaOut,
)

router = APIRouter(prefix="/caja", tags=["Caja"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/apertura/contexto/{id_empleado}", response_model=AperturaContextoOut)
def contexto_apertura(id_empleado: int, db: Session = Depends(get_db)):
    """Datos que necesita la pantalla de apertura: cajero, turno, permisos y cajas libres."""
    contexto = crud_caja.obtener_contexto_apertura(db, id_empleado)
    if not contexto:
        raise HTTPException(status_code=404, detail="El empleado no existe")
    return contexto


@router.post("/abrir", response_model=SesionCajaOut, status_code=201)
def abrir_caja(data: AperturaCajaData, db: Session = Depends(get_db)):
    try:
        return crud_caja.abrir_caja(db, data)
    except crud_caja.ErrorCaja as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get("/arqueo/{id_sesion}", response_model=ArqueoOut)
def arqueo(id_sesion: int, db: Session = Depends(get_db)):
    """Resumen de ventas del turno por método de pago, sin cerrar la caja."""
    try:
        return crud_caja.obtener_arqueo(db, id_sesion)
    except crud_caja.ErrorCaja as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.post("/cerrar/{id_sesion}", response_model=ArqueoOut)
def cerrar_caja(id_sesion: int, data: CierreCajaData, db: Session = Depends(get_db)):
    """Cierra el turno: guarda esperado, contado y diferencia."""
    try:
        return crud_caja.cerrar_caja(db, id_sesion, data)
    except crud_caja.ErrorCaja as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
