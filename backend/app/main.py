from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.schemas.schemas import (
PaisOut, 
DepartamentoOut, 
CiudadOut, 
DireccionOut,
ProveedorCreate,
ProveedorListadoOut,
ProveedorUpdate,
TelefonoProveedorOut,
ProveedorOut,
)


from app.crud import crud
from app.database import SessionLocal, engine
from app.models.models import Base

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

@app.get("/ubicaciones/paises", response_model=list[PaisOut])
def listar_paises(db: Session = Depends(get_db)):
    return crud.obtener_paises(db)

@app.get("/ubicaciones/departamentos/{id_pais}", response_model=list[DepartamentoOut])
def listar_departamentos(id_pais: int, db: Session = Depends(get_db)):
    return crud.obtener_departamentos_por_pais(db, id_pais=id_pais)

@app.get("/ubicaciones/ciudades/{id_departamento}", response_model=list[CiudadOut])
def listar_ciudades(id_departamento: int, db: Session = Depends(get_db)):
    return crud.obtener_ciudades_por_departamento(db, id_departamento=id_departamento)

@app.get("/ubicaciones/direcciones/{id_ciudad}", response_model=list[DireccionOut])
def listar_direcciones(id_ciudad: int, db: Session = Depends(get_db)):
    return crud.obtener_direcciones_por_ciudad(db, id_ciudad=id_ciudad)

@app.get("/ubicaciones/ciudades", response_model=list[CiudadOut])
def listar_ciudades(db: Session = Depends(get_db)):
    return crud.obtener_ciudades(db)

@app.post("/proveedores", response_model=ProveedorOut, status_code=status.HTTP_201_CREATED)
def crear_proveedor(data: ProveedorCreate, db: Session = Depends(get_db)):
    return crud.registrar_proveedor(db, data)

@app.get("/proveedores", response_model=list[ProveedorListadoOut])
def listar_proveedores(db: Session = Depends(get_db)):
    return crud.obtener_proveedores(db)

@app.put("/proveedores/{id_proveedor}", response_model=ProveedorOut)
def editar_proveedor(id_proveedor: int, data: ProveedorUpdate, db: Session = Depends(get_db)):
    return crud.actualizar_proveedor(db, id_proveedor=id_proveedor, data=data)

@app.delete("/proveedores/{id_proveedor}", status_code=status.HTTP_200_OK)
def borrar_proveedor(id_proveedor: int, db: Session = Depends(get_db)):
    return crud.eliminar_proveedor(db, id_proveedor=id_proveedor)
