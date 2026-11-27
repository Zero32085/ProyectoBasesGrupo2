import bcrypt
from sqlalchemy.orm import Session
from app.models.models import Cliente, Empleado, Persona , RolEmpleado
from app.schemas.schemas import LoginClienteData, LoginEmpleadoData, RegistroClientesData

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


def autenticar_empleado(db: Session,codigo_empleado:str, password: str)-> dict | None:
    codigo_limpio = codigo_empleado.strip()
    empleado = (
        db.query(Empleado)
        .filter(Empleado.codigo_empleado == codigo_limpio)
        .first()
    )

    if not empleado:
        return None

    persona = (
        db.query(Persona)
        .filter(Persona.Id_Persona == empleado.Id_Persona)
        .first()
    )
    if not persona or not _verificar_password(password,persona.contrasena_hash):
        return None

    rol = (
        db.query(RolEmpleado)
        .filter(RolEmpleado.Id_RolEmpleado == empleado.Id_RolEmpleado)
        .first()
    )

    nombre_rol = rol.nombre.strip().lower() if rol and rol.nombre else None

    return {
        "persona":persona,
        "rol_empleado": nombre_rol,
        "empleado": empleado,
        "codigo_empleado": empleado.codigo_empleado,
    }


def registrar_cliente(db: Session,data: RegistroClientesData)->Persona | None:
    correo_limpio = data.correo.strip().lower()
    if get_persona_por_correo(db, correo_limpio):
        return None
    try:
        nueva_persona = Persona(
            primer_nombre=data.primer_nombre,
            segundo_nombre=data.segundo_nombre,
            primer_apellido=data.primer_apellido,
            segundo_apellido=data.segundo_apellido,
            dni=data.dni,
            correo=correo_limpio,
            contrasena_hash=_hash_password(data.password),
            fecha_nacimiento= data.fecha_nacimiento,
            telefono=data.telefono
        )

        db.add(nueva_persona)
        db.flush()

        direccion_id = data.Id_Direccion if data.Id_Direccion is not None else 21

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
    except Exception:
        db.rollback()
        raise

def get_contrasena(db: Session, contrasena: str):
    return db.query(Persona).filter(Persona.contrasena_hash == contrasena).first()
