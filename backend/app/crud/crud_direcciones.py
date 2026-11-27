from sqlalchemy.orm import Session
from app.models.models import Ciudad, Cliente, Direccion
from app.schemas.schema_direcciones import DireccionCreate


def get_cliente_por_persona(db: Session, id_persona: int) -> Cliente | None:
    return db.query(Cliente).filter(Cliente.Id_Persona == id_persona).first()


def get_ciudad_por_id(db: Session, id_ciudad: int) -> Ciudad | None:
    return db.query(Ciudad).filter(Ciudad.Id_Ciudad == id_ciudad).first()


def asignar_direccion_cliente(
    db: Session,
    id_persona: int,
    data: DireccionCreate,
) -> dict | None:
    cliente = get_cliente_por_persona(db, id_persona)
    if not cliente:
        return None

    ciudad = get_ciudad_por_id(db, data.Id_Ciudad)
    if not ciudad:
        raise ValueError("La ciudad seleccionada no existe")

    try:
        nueva_direccion = Direccion(
            Id_Ciudad=data.Id_Ciudad,
            colonia=data.colonia.strip(),
            calle=data.calle.strip() if data.calle and data.calle.strip() else None,
            referencia=data.referencia.strip(),
            nombre_destinatario=(
                data.nombre_destinatario.strip()
                if data.nombre_destinatario and data.nombre_destinatario.strip()
                else None
            ),
        )
        db.add(nueva_direccion)
        db.flush()

        cliente.Id_Direccion = nueva_direccion.Id_Direccion
        db.commit()
        db.refresh(nueva_direccion)
        db.refresh(cliente)

        return {
            "Id_Cliente": cliente.Id_Cliente,
            "Id_Persona": cliente.Id_Persona,
            "Id_Direccion": nueva_direccion.Id_Direccion,
            "direccion": nueva_direccion,
        }
    except Exception:
        db.rollback()
        raise