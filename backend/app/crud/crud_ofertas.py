from sqlalchemy.orm import Session
from app.models.models import Oferta
from app.schemas.schemas import OfertaCreate, OfertaUpdate

def get_ofertas(db: Session) ->list[Oferta] | None:
    return db.query(Oferta).all()

def get_ofertas_id(db:Session, id:int) -> Oferta | None:
    return db.query(Oferta).filter(Oferta.Id_Oferta == id).first()

def get_ofertas_nombre(db: Session, nombre: str) -> Oferta | None:
    return db.query(Oferta).filter(Oferta.nombre==nombre).first()

def crear_ofertas(db:Session, data: OfertaCreate) -> Oferta | None:
    if get_ofertas_nombre(db, data.nombre):
        return None
    
    nueva_oferta = Oferta(
        nombre=data.nombre,
        descripcion=data.descripcion,
        porcentaje_descuento= data.porcentaje_descuento,
        fecha_inicio= data.fecha_inicio,
        fecha_fin= data.fecha_fin,
        estado= data.estado
    )

    db.add(nueva_oferta)
    db.commit()
    db.refresh(nueva_oferta)

    return nueva_oferta

def actualizar_oferta (db:Session, id:int, data:OfertaUpdate) -> Oferta | None:
    oferta = get_ofertas_id(db, id)

    if oferta is None:
        return None

    oferta_existente = get_ofertas_nombre(db, data.nombre)

    if oferta_existente and oferta_existente.Id_Oferta != id:
        return None

    oferta.nombre=data.nombre
    oferta.descripcion = data.descripcion
    oferta.porcentaje_descuento= data.porcentaje_descuento
    oferta.fecha_inicio= data.fecha_inicio
    oferta.fecha_fin= data.fecha_fin
    oferta.estado= data.estado

    db.commit()
    db.refresh(oferta)

    return oferta