from sqlalchemy.orm import Session
from app.models.models import Marca
from app.schemas.schemas import MarcaCreate, MarcaUpdate

def get_marcas(db: Session) ->list[Marca] | None:
    return db.query(Marca).all()

#seleccionar Marca por id
def get_marcas_id(db:Session, id:int) -> Marca | None:
    return db.query(Marca).filter(Marca.Id_Marca == id).first()

def get_marcas_nombre(db: Session, nombre: str) -> Marca | None:
    return db.query(Marca).filter(Marca.nombre==nombre).first()


def crear_marcas(db:Session, data: MarcaCreate) -> Marca | None:
    if get_marcas_nombre(db, data.nombre):
        return None
    
    nueva_marca = Marca(
        nombre = data.nombre,
        pais_origen = data.pais_origen,
        estado = data.estado
    )

    db.add(nueva_marca)
    db.commit()
    db.refresh(nueva_marca)

    return nueva_marca

def actualizar_Marcas (db:Session, id:int, data:MarcaUpdate) -> Marca | None:
    mar = get_marcas_id(db, id)

    if mar is None:
        return None

    marcas_existente = get_marcas_nombre(db, data.nombre)

    if marcas_existente and marcas_existente.Id_Marca != id:
        return None

    mar.nombre=data.nombre
    mar.pais_origen = data.pais_origen
    mar.estado = data.estado

    db.commit()
    db.refresh(mar)

    return mar
