from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app import crud
from app.database import SessionLocal, engine
from app.models.models import Base
from app.schemas.schemas import (
    AuthResponse,
    LoginClienteData,
    LoginEmpleadoData,
    RegistroClienteData,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"status":"ok"}

@app.post("/auth/cliente/login",response_model=AuthResponse)
def login_cliente(data: LoginClienteData, db: Session = Depends(get_db)):
    persona = crud.autenticar_cliente(db,data.correo,data.pasword)
    if not persona:
        raise HTTPException(
            status_code=status.HTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrecta"
        )
    return AuthResponse(
        id_persona=persona.Id_Persona,
        primer_nombre=persona.primer_nombre,
        primer_apellido=persona.primer_apellido,
        correo=persona.correo,
        rol="cliente",
    )

@app.post(
    "/auth/cliente/registro",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
)
def registro_cliente(data: RegistroClienteData, db: Session = Depends(get_db)):
    persona = crud.registrar_cliente(db, data)
    if not persona:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo ya está registrado",
        )
    return AuthResponse(
        id_persona=persona.Id_Persona,
        primer_nombre=persona.primer_nombre,
        primer_apellido=persona.primer_apellido,
        correo=persona.correo,
        rol="cliente",
    )


@app.post("/auth/empleado/login", response_model=AuthResponse)
def login_empleado(data: LoginEmpleadoData, db: Session = Depends(get_db)):
    persona = crud.autenticar_empleado(db, data.codigo_empleado, data.password)
    if not persona:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Código de empleado o contraseña incorrectos",
        )
    return AuthResponse(
        id_persona=persona.Id_Persona,
        primer_nombre=persona.primer_nombre,
        primer_apellido=persona.primer_apellido,
        correo=persona.correo,
        rol="empleado",
    )