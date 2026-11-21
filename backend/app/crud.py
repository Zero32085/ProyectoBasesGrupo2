import bcrypt
from sqlalchemy.orm import Session
from app.models.models import Cliente, Empleado, Persona
from app.schemas.schemas import LoginClienteData, LoginEmpleadoData, RegistroClienteData

def _hash_password(password: str)-> str:
    return bcrypt.hashpw(password.encode("UTF-8"), bcrypt.gensalt()).decode("utf-8")

def _verificar_password(password_plano: str, hash_guardado: str | None)-> bool:
    if not hash_guardado:
        return False

    if hash_guardado.startswith(("$2a$","$2b$","$2y$")):
        try:
            return bcrypt.checkpw(
                password_plano.encode("utf-8"),
                hash_guardado.encode("utf-8"),
            )
        except ValueError:
            return False
    return password_plano == hash_guardado

def get_persona_por_correo(db: Session, correo: str)-> Persona | None:
    return db.query(Persona).filter(Persona.correo == correo).first()

def autenticar_cliente(db: Session, correo: str, password: str)-> Persona | None:
    persona = get_persona_por_correo(db,correo)
    if not persona or not _verificar_password(password,persona.contrasena_hash):
        return None

    cliente = db.query(Cliente).filter(Cliente.Id_Persona == persona.Id_Persona).first()
    if not cliente:
        return None

    return persona


def autenticar_empleado(db: Session,codigo_empleado:str, password: str)-> Persona | None:
    empleado = (
        db.query(Empleado)
        .filter(Empleado.codigo_empleado == codigo_empleado)
        .frist()
    )

    if not empleado:
        return None

    persona = (
        db.query(Persona)
        .filter(Persona.Id_Persona == empleado.Id_persona)
        .first()
    )
    if not persona or not _verificar_password(password,persona.contrasena_hash):
        return None

    return persona


def registrar_cliente(db: Session,data: RegistroClienteData)->Persona | None:
    if get_persona_por_correo(db, data.correo):
        return None

    nueva_persona = Persona(
        primer_nombre=data.primer_nombre,
        segundo_nombre=data.segundo_nombre,
        primer_apellido=data.primer_apellido,
        segundo_apellido=data.segundo_apellido,
        correo=data.correo,
        contrasena_hash=_hash_password(data.password),
        telefono=data.telefono,
        dni=data.dni,
    )

    db.add(nueva_persona)
    db.flush()

    direccion_id = data.id_direccion if data.id_direccion is not None else 1

    nuevo_cliente = Cliente(
        Id_Persona=nueva_persona.Id_Persona,
        Id_Direccion=direccion_id,
        rtn=data.rtn,
        razon_social=data.razon_social,
    )
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nueva_persona)
    return nueva_persona

def get_contrasena(db: Session, contrasena: str):
    return db.query(Persona).filter(Persona.contrasena_hash == contrasena).first()

t