from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from decimal import Decimal, ROUND_HALF_UP
from datetime import timedelta
from app.models.models import Proveedor, TelefonoProveedor, Pais, Departamento, Ciudad, Direccion
from app.schemas.schemas import ProveedorCreate, ProveedorUpdate, ProveedorOut, TelefonoProveedorOut, TelefonoProveedorCreate, TelefonoProveedorOut, CiudadOut, DepartamentoOut, PaisOut
from app.schemas.schemas import CompraCreate

TASA_ISV = Decimal("0.15")

def obtener_paises(db: Session):
    return db.query(Pais).all()

def obtener_departamentos_por_pais(db: Session, id_pais: int):
    return db.query(Departamento).filter(Departamento.Id_Pais==id_pais).all()

def obtener_ciudades_por_departamento(db: Session, id_departamento: int):
    return db.query(Ciudad).filter(Ciudad.Id_Departamento == id_departamento).all()

def obtener_direcciones_por_ciudad(db: Session, id_ciudad: int):
    return db.query(Direccion).filter(Direccion.Id_Ciudad == id_ciudad).all()

def get_proveedor_por_nombre(db: Session, nombre_o_razonSocial: str)-> Proveedor | None:
    return db.query(Proveedor).filter(Proveedor.nombre_o_razonSocial == nombre_o_razonSocial).first()

def get_proveedor_por_rtn(db: Session, rtn: str)-> Proveedor | None:
    return db.query(Proveedor).filter(Proveedor.rtn == rtn).first()



def registrar_proveedor(db: Session, data: ProveedorCreate) -> Proveedor:
    
    if get_proveedor_por_rtn(db, data.rtn.strip()):
        raise HTTPException(
            status_code=400, detail="Ya existe un proveedor registrado con ese rtn"
            )
    ciudad = db.query(Ciudad).filter(Ciudad.Id_Ciudad == data.direccion.Id_Ciudad).first()
    if not ciudad:
        raise HTTPException(
            status_code=400, detail="La ciudad seleccionada no existe"
        )

    telefonos_limpios = [t.strip() for t in data.telefonos if t and t.strip()]
    if not telefonos_limpios:
        raise HTTPException(
            status_code=400, detail="Debe proporcionar al menos un numero de telefono valido"
        )

    try:

        calle_limpia = (
            data.direccion.calle.strip()
            if data.direccion.calle and data.direccion.calle.strip()
            else None
        )

        nueva_direccion = Direccion(
            Id_Ciudad = data.direccion.Id_Ciudad,
            colonia = data.direccion.colonia.strip(),
            calle = calle_limpia,
            referencia = data.direccion.referencia.strip(),
        )
        db.add(nueva_direccion)
        db.flush()
    
        nuevo_proveedor = Proveedor(
            nombre_o_razonSocial = data.nombre_o_razonSocial.strip(),
            rtn = data.rtn.strip(),
            nombre_contacto = data.nombre_contacto.strip(),
            correo = data.correo,
            estado = data.estado,
            Id_Direccion=nueva_direccion.Id_Direccion,
        )
        db.add(nuevo_proveedor)
        db.flush() #Genera nuevo_proveedor.Id_Proveedor sin hacer commit

        for num in telefonos_limpios:
            nuevo_telefono = TelefonoProveedor(
                Id_Proveedor=nuevo_proveedor.Id_Proveedor,
                telefono=num,
            )
            db.add(nuevo_telefono)


        db.commit()
        db.refresh(nuevo_proveedor)
        return nuevo_proveedor

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al registrar el proveedor: {str(e)}"
        )


def obtener_proveedores(db: Session):
    return (
        db.query(Proveedor)
        .options(
            joinedload(Proveedor.direccion)
            .joinedload(Direccion.ciudad)
            .joinedload(Ciudad.departamento)
            .joinedload(Departamento.pais),
            joinedload(Proveedor.telefonos)
        )
        .order_by(Proveedor.Id_Proveedor.desc())
        .all()
    )

def actualizar_proveedor(db: Session, id_proveedor: int, data: ProveedorUpdate) -> Proveedor:
    proveedor = db.query(Proveedor).filter(Proveedor.Id_Proveedor == id_proveedor).first()
    if not proveedor:
        raise HTTPException(
            status_code=404, detail="Proveedor no encontrado"
        )

    rtn_limpio = data.rtn.strip()
    duplicado = (
        db.query(Proveedor)
        .filter(Proveedor.rtn == rtn_limpio, Proveedor.Id_Proveedor != id_proveedor)
        .first()
    )
    if duplicado:
        raise HTTPException(
            status_code=400, detail="Ya existe otro proveedor registrado con ese rtn"
        )

    ciudad = db.query(Ciudad).filter(Ciudad.Id_Ciudad == data.direccion.Id_Ciudad).first()
    if not ciudad:
        raise HTTPException(
            status_code=400, detail="La ciudad seleccionada no existe"
        )

    telefonos_limpios = [t.strip() for t in data.telefonos if t and t.strip()]
    if not telefonos_limpios:
        raise HTTPException(
            status_code=400, detail="Debe proporcionar al menos un numero de telefono valido"
        )

    try:
        calle_limpia = (
            data.direccion.calle.strip()
            if data.direccion.calle and data.direccion.calle.strip()
            else None
        )

        if proveedor.direccion:
            proveedor.direccion.Id_Ciudad = data.direccion.Id_Ciudad
            proveedor.direccion.colonia = data.direccion.colonia.strip()
            proveedor.direccion.calle = calle_limpia
            proveedor.direccion.referencia = data.direccion.referencia.strip()
        else:
            nueva_direccion = Direccion(
                Id_Ciudad=data.direccion.Id_Ciudad,
                colonia=data.direccion.colonia.strip(),
                calle=calle_limpia,
                referencia=data.direccion.referencia.strip(),
            )
            db.add(nueva_direccion)
            db.flush()
            proveedor.Id_Direccion = nueva_direccion.Id_Direccion

        proveedor.nombre_o_razonSocial = data.nombre_o_razonSocial.strip()
        proveedor.rtn = rtn_limpio
        proveedor.nombre_contacto = data.nombre_contacto.strip()
        proveedor.correo = data.correo
        proveedor.estado = data.estado

        db.query(TelefonoProveedor).filter(
            TelefonoProveedor.Id_Proveedor == proveedor.Id_Proveedor
        ).delete()
        db.flush()

        for num in telefonos_limpios:
            db.add(
                TelefonoProveedor(
                    Id_Proveedor=proveedor.Id_Proveedor,
                    telefono=num,
                )
            )

        db.commit()
        db.refresh(proveedor)
        return proveedor

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar el proveedor: {str(e)}",
        )

def eliminar_proveedor(db: Session, id_proveedor: int) -> dict:
    proveedor = (
        db.query(Proveedor)
        .filter(Proveedor.Id_Proveedor == id_proveedor)
        .first()
    )
    if not proveedor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proveedor no encontrado",
        )

    id_direccion = proveedor.Id_Direccion

    try:
        db.query(TelefonoProveedor).filter(
            TelefonoProveedor.Id_Proveedor == id_proveedor
        ).delete(synchronize_session=False)

        db.delete(proveedor)
        db.flush()

        if id_direccion is not None:
            otro_proveedor_misma_dir = (
                db.query(Proveedor)
                .filter(Proveedor.Id_Direccion == id_direccion)
                .first()
            )
            if not otro_proveedor_misma_dir:
                direccion = (
                    db.query(Direccion)
                    .filter(Direccion.Id_Direccion == id_direccion)
                    .first()
                )
                if direccion:
                    db.delete(direccion)

        db.commit()
        return {"mensaje": "Proveedor eliminado correctamente", "id_proveedor": id_proveedor}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar el proveedor: {str(e)}",
        )