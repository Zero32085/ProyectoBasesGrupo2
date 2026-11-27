from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
#Agregue esto para traer los paises
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


from app.schemas.schemas import CompraOut, ProductoOut, SucursalOut, SucursalResumenOut, CompraCreate, CompraDetalleRespuestaOut


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











@app.get("/compras", response_model=list[CompraOut])
def listar_compras(db: Session = Depends(get_db)):
    # Devuelve el listado de compras registradas
    return crud.obtener_compras(db)

@app.get("/productos", response_model=list[ProductoOut])
def listar_productos(db: Session = Depends(get_db)):
    # Retorna la lista de productos para los selects del sistema
    return crud.obtener_productos(db)

@app.get("/sucursales", response_model=list[SucursalOut])
def listar_sucursales(db: Session = Depends(get_db)):
    # Retorna la lista de productos para los selects del sistema
    return crud.obtener_sucursales(db)

@app.post("/compras", response_model=CompraOut, status_code=status.HTTP_201_CREATED)
def registrar_compra(datos: CompraCreate, db: Session = Depends(get_db)):
    # Guarda compra, detalles, lote e inventario en una transacción
    return crud.crear_compra(db, datos)

@app.get("/compras/{id_compra}/detalle", response_model=CompraDetalleRespuestaOut)
def ver_detalle_compra(id_compra: int, db: Session = Depends(get_db)):
    # Devuelve los datos de la compra y sus detalles/lotes para el modal
    return crud.obtener_compra_con_detalles(db, id_compra)