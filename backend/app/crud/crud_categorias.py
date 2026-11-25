from sqlalchemy.orm import Session
from app.models.models import Categoria
from app.schemas.schemas import CategoriaCreate, CategoriaUpdate

#seleccionar todas las categorias
def get_categoria(db: Session) ->Categoria | None:
    return db.query(Categoria).all()

#seleccionar categoria por id
def get_categoria_id(db:Session, id:int) -> Categoria | None:
    return db.query(Categoria).filter(Categoria.Id_Categoria == id).first()

def get_categoria_nombre(db: Session, nombre: str) -> Categoria | None:
    return db.query(Categoria).filter(Categoria.nombre==nombre).first()


def crear_categoria(db:Session, data: CategoriaCreate) -> Categoria | None:
    if get_categoria_nombre(db, data.nombre):
        return None
    
    nueva_categoria = Categoria(
        nombre = data.nombre,
        descripcion = data.descripcion,
        estado = data.estado
    )

    db.add(nueva_categoria)
    db.commit()
    db.refresh(nueva_categoria)

    return nueva_categoria

def actualizar_categoria (db:Session, id:int, data:CategoriaUpdate) -> Categoria | None:
    cat = get_categoria_id(db, id)

    if cat is None:
        return None

    categoria_existente = get_categoria_nombre(db, data.nombre)

    if categoria_existente and categoria_existente.Id_Categoria != id:
        return None

    cat.nombre=data.nombre
    cat.descripcion = data.descripcion
    cat.estado = data.estado

    db.commit()
    db.refresh(cat)

    return cat
    



    



