from sqlalchemy.orm import Session
from app.models.models import ProductoOferta, Producto, Oferta
from app.schemas.schemas import ProductoOfertaCreate, ProductoOfertaUpdate


def get_productos_ofertas(db: Session) -> list[ProductoOferta]:
    return db.query(ProductoOferta).all()

def get_productos_ofertas_id(db: Session, id: int) -> ProductoOferta | None:
    return db.query(ProductoOferta).filter(ProductoOferta.Id_ProductosOfertas == id).first()

def get_producto_oferta_existente(db: Session, id_producto: int, id_oferta: int) -> ProductoOferta | None:
    return db.query(ProductoOferta).filter(
    ProductoOferta.Id_Productos == id_producto,
    ProductoOferta.Id_Oferta == id_oferta
    ).first()


def crear_producto_oferta(db: Session, data: ProductoOfertaCreate) -> ProductoOferta | None:    
    if not db.get(Producto, data.Id_Productos):
        return None
    
    if not db.get(Oferta, data.Id_Oferta):
       return None
    
    if get_producto_oferta_existente(db, data.Id_Productos, data.Id_Oferta):
        return None

    nuevo_producto_oferta = ProductoOferta(
        Id_Productos=data.Id_Productos,
        Id_Oferta=data.Id_Oferta
    )

    db.add(nuevo_producto_oferta)
    db.commit()
    db.refresh(nuevo_producto_oferta)
    return nuevo_producto_oferta

def actualizar_producto_oferta(db: Session, id: int, data: ProductoOfertaUpdate) -> ProductoOferta | None:
    prod = get_productos_ofertas_id(db, id)
    if prod is None:
        return None
    
    if not db.get(Producto, data.Id_Productos):
        return None
    
    if not db.get(Oferta, data.Id_Oferta):
        return None
    producto_oferta_existente = get_producto_oferta_existente(db, data.Id_Productos, data.Id_Oferta)

    if (producto_oferta_existente and producto_oferta_existente.Id_ProductosOfertas != id):
        return None
    
    prod.Id_Productos = data.Id_Productos
    prod.Id_Oferta = data.Id_Oferta
    db.commit()
    db.refresh(prod)
    return prod