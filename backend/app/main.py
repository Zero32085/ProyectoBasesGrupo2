from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.crud import crud, crud_categorias
from app.database import SessionLocal, engine
from app.models.models import Base
from app.schemas.schemas import (
    AuthResponse,
    LoginClienteData,
    LoginEmpleadoData,
    RegistroClientesData,
    CategoriaCreate,
    CategoriaUpdate,
    CategoriaOut
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

#categorias
@app.get("/categorias", response_model=list[CategoriaOut])
def listar_categorias(db: Session = Depends(get_db)):
    return crud_categorias.get_categoria(db)

@app.get ("/categorias/{id}", response_model=CategoriaOut)
def listar_categorias_nombre(id:int,db:Session = Depends (get_db)):
    return crud_categorias.get_categoria_id(db,id)

@app.post("/categorias/registro", response_model=CategoriaOut)
def crear_categoria(data: CategoriaCreate, db:Session = Depends(get_db)):
    categoria = crud_categorias.crear_categoria(db, data)
    
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La categoria ya existe"
        )

    return CategoriaOut(
        Id_Categoria=categoria.Id_Categoria,
        nombre= categoria.nombre,
        descripcion = categoria.descripcion,
        estado=categoria.estado
    )

@app.put("/categorias/{id}", response_model=CategoriaOut)
def actualizar_categoria (id:int, data: CategoriaUpdate, db:Session=Depends(get_db)):
    categoria = crud_categorias.actualizar_categoria(db,id,data)

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La categoria no existe o el nuevo nombre ya esta registrado"
        )
    
    return CategoriaOut(
        Id_Categoria=categoria.Id_Categoria,
        nombre= categoria.nombre,
        descripcion = categoria.descripcion,
        estado=categoria.estado
    )
