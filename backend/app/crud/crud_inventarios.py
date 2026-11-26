from sqlalchemy.orm import Session
from app.models.models import Inventario
from app.schemas.schemas import InventarioCreate, InventarioUpdate

def get_inventarios(db: Session) -> list[Inventario]:
    return db.query(Inventario).all()

def get_inventarios_id(db: Session, id: int) -> Inventario | None:
    return db.query(Inventario).filter(Inventario.Id_Inventario == id).first()

# Seleccionar inventario por producto, sucursal y lote
def get_inventario_existente(db: Session, id_producto: int, id_sucursal: int, id_lote: int) -> Inventario | None:
    return db.query(Inventario).filter(
        Inventario.Id_Producto == id_producto,
        Inventario.Id_Sucursal == id_sucursal,
        Inventario.Id_lote_vencimiento == id_lote
    ).first()

def crear_inventarios(db: Session, data: InventarioCreate) -> Inventario | None:
    if get_inventario_existente(db, data.Id_Producto, data.Id_Sucursal, data.Id_lote_vencimiento):
        return None

    nuevo_inventario = Inventario(
        Id_Producto=data.Id_Producto,
        Id_Sucursal=data.Id_Sucursal,
        Id_lote_vencimiento=data.Id_lote_vencimiento,
        stock_actual=data.stock_actual
    )

    db.add(nuevo_inventario)
    db.commit()
    db.refresh(nuevo_inventario)

    return nuevo_inventario

def actualizar_inventarios(db: Session, id: int, data: InventarioUpdate) -> Inventario | None:
    inv = get_inventarios_id(db, id)

    if inv is None:
        return None

    inv.stock_actual = data.stock_actual

    db.commit()
    db.refresh(inv)

    return inv