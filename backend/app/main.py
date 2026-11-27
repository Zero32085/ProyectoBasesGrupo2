from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.crud import crud
from app.database import SessionLocal, engine
from app.routers import caja
from app.models.models import Base
from app.schemas.schemas import (
    AuthResponse,
    LoginClienteData,
    LoginEmpleadoData,
    RegistroClientesData,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(caja.router)

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
    persona = crud.autenticar_cliente(db,data.correo,data.password)
    if not persona:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrecta"
        )
    return AuthResponse(
        Id_Persona=persona.Id_Persona,
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
def registro_cliente(data: RegistroClientesData, db: Session = Depends(get_db)):
    persona = crud.registrar_cliente(db, data)
    if not persona:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo ya está registrado",
        )
    return AuthResponse(
        Id_Persona=persona.Id_Persona,
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
        Id_Persona=persona.Id_Persona,
        primer_nombre=persona.primer_nombre,
        primer_apellido=persona.primer_apellido,
        correo=persona.correo,
        rol="empleado",
    )


#Con persona no me haci la comprobacion, solo con empleado
#@app.post("/auth/empleado/login", response_model=AuthResponse)
#def login_empleado(data: LoginEmpleadoData, db: Session = Depends(get_db)):
#    empleado = crud.autenticar_empleado(db, data.codigo_empleado, data.password)
#    if not empleado:
#        raise HTTPException(
#            status_code=status.HTTP_401_UNAUTHORIZED,
#            detail="Código de empleado o contraseña incorrectos",
#        )
#    persona = empleado.persona
#    return AuthResponse(
#        Id_Persona=persona.Id_Persona,
#        primer_nombre=persona.primer_nombre,
#        primer_apellido=persona.primer_apellido,
#        correo=persona.correo,
#        rol="empleado",
#        Id_Empleado=empleado.Id_Empleado,          # <-- el frontend lo necesita
#        codigo_empleado=empleado.codigo_empleado,
#    )
