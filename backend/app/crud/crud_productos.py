from sqlalchemy.orm import Session
from app.models.models import Producto
from app.schemas.schemas import ProductoCreate, ProductoUpdate

#seleccionar todas los productos
def get_producto(db: Session) ->list[Producto] | None:
    return db.query(Producto).order_by(
        Producto.estado.desc(),
        Producto.Id_Producto.asc()
    ).all()

#seleccionar productos por id
def get_producto_id(db:Session, id:int) -> Producto | None:
    return db.query(Producto).filter(Producto.Id_Producto == id).first()

def get_producto_nombre(db: Session, nombre: str) -> Producto | None:
    return db.query(Producto).filter(Producto.nombre==nombre).first()


def crear_producto(db:Session, data: ProductoCreate) -> Producto | None:
    if get_producto_nombre(db, data.nombre):
        return None
    
    nuevo_producto = Producto(
        Id_Sucursal=data.Id_Sucursal,
        Id_Categoria=data.Id_Categoria,
        Id_Marca=data.Id_Marca,
        cod_barra = data.cod_barra,
        nombre=data.nombre,
        descripcion=data.descripcion,
        stock_minimo=data.stock_minimo,
        stock_maximo= data.stock_maximo,
        precio=data.precio,
        costo=data.costo,
        porcentaje_isv=data.porcentaje_isv,
        estado=data.estado
    )

    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)

    return nuevo_producto

def actualizar_producto (db:Session, id:int, data:ProductoUpdate) -> Producto | None:
    prod= get_producto_id(db, id)

    if prod is None:
        return None

    producto_existente = get_producto_nombre(db, data.nombre)

    if producto_existente and producto_existente.Id_Producto != id:
        return None

    prod.Id_Sucursal = data.Id_Sucursal
    prod.Id_Categoria = data.Id_Categoria
    prod.Id_Marca=data.Id_Marca
    prod.cod_barra = data.cod_barra
    prod.nombre=data.nombre
    prod.descripcion=data.descripcion
    prod.stock_minimo=data.stock_minimo
    prod.stock_maximo= data.stock_maximo
    prod.precio=data.precio
    prod.costo=data.costo
    prod.porcentaje_isv=data.porcentaje_isv
    prod.estado=data.estado

    db.commit()
    db.refresh(prod)

    return prod    



    




