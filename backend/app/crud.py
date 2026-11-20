from sqlalchemy.orm import Session

from models import Persona
from schemas import UserData

def get_correo(db: Session, correo: str):
    return db.query(Persona).filter(Persona.correo = correo).first()

def get_contrasena(db: Session, contrasena: str):
    return db.query(Persona).filter(Persona.contrasena_hash = contrasena).first()