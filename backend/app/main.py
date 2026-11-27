from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text


from app.crud import( 
    crud,
    crud_categorias,
    crud_ofertas, 
    crud_productos, 
    crud_marcas, 
    crud_inventarios, 
    crud_producto_oferta,
    crud_direcciones
    )
from app.database import SessionLocal, engine
from app.routers import caja  
from app.models.models import Base
from app.schemas.schemas import (
    AuthResponse,
    LoginClienteData,
    LoginEmpleadoData,
    RegistroClientesData,
    CategoriaCreate,
    CategoriaUpdate,
    CategoriaOut,
    OfertaCreate,
    OfertaUpdate,
    OfertaOut,
    ProductoCreate,
    ProductoUpdate,
    ProductoOut,
    MarcaCreate,
    MarcaUpdate,
    MarcaOut,
    InventarioCreate,
    InventarioUpdate,
    InventarioOut,
    ProductoOfertaCreate,
    ProductoOfertaUpdate,
    ProductoOfertaOut
)
from app.schemas.schema_direcciones import DireccionCreate, DireccionOut

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
    resultado = crud.autenticar_empleado(db, data.codigo_empleado, data.password)
    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Código de empleado o contraseña incorrectos",
        )
    persona = resultado["persona"]
    return AuthResponse(
        Id_Persona=persona.Id_Persona,
        primer_nombre=persona.primer_nombre,
        primer_apellido=persona.primer_apellido,
        correo=persona.correo,
        rol="empleado",
        Id_Empleado=resultado["empleado"].Id_Empleado,
        rol_empleado=resultado["rol_empleado"],
        codigo_empleado=resultado["codigo_empleado"],
    )

#categorias
@app.get("/categorias", response_model=list[CategoriaOut])
def listar_categorias(db: Session = Depends(get_db)):
    return crud_categorias.get_categoria(db)

@app.get ("/categorias/{id}", response_model=CategoriaOut)
def listar_categorias_id(id:int,db:Session = Depends (get_db)):
    cat = crud_categorias.get_categoria_id(db,id)

    if not cat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La categoria no existe"
        )

    return cat

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

#ofertas
@app.get("/ofertas", response_model=list[OfertaOut])
def listar_ofertas(db: Session = Depends(get_db)):
    return crud_ofertas.get_ofertas(db)

@app.get ("/ofertas/{id}", response_model=OfertaOut)
def listar_ofertas_id(id:int,db:Session = Depends (get_db)):
    oferta = crud_ofertas.get_ofertas_id(db,id)

    if not oferta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La oferta no existe"
        )
    return oferta


@app.post("/ofertas/registro", response_model=OfertaOut)
def crear_Oferta(data: OfertaCreate, db:Session = Depends(get_db)):
    oferta = crud_ofertas.crear_ofertas(db, data)
    
    if not oferta:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La Oferta ya existe"
        )

    return OfertaOut(
        Id_Oferta=oferta.Id_Oferta,
        nombre=oferta.nombre,
        porcentaje_descuento= oferta.porcentaje_descuento,
        fecha_inicio= oferta.fecha_inicio,
        fecha_fin= oferta.fecha_fin,
        estado= oferta.estado
    )

@app.put("/ofertas/{id}", response_model=OfertaOut)
def actualizar_Oferta (id:int, data: OfertaUpdate, db:Session=Depends(get_db)):
    oferta = crud_ofertas.actualizar_oferta(db,id,data)

    if not oferta:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La Oferta no existe o el nuevo nombre ya esta registrado"
        )
    
    return OfertaOut(
        Id_Oferta=oferta.Id_Oferta,
        nombre=oferta.nombre,
        porcentaje_descuento= oferta.porcentaje_descuento,
        fecha_inicio= oferta.fecha_inicio,
        fecha_fin= oferta.fecha_fin,
        estado= oferta.estado
    )

#productos
@app.get("/productos", response_model=list[ProductoOut])
def listar_productos(db: Session = Depends(get_db)):
    return crud_productos.get_producto(db)


@app.get("/productos/vista")
def listar_vista_productos(db: Session = Depends(get_db)):
    return db.execute(text("""
        SELECT *
        FROM vw_productos
        ORDER BY estado DESC, id_producto ASC
    """)).mappings().all()

#productos

@app.get("/productos/{id}", response_model=ProductoOut)
def listar_productos_id(id: int, db: Session = Depends(get_db)):
    producto = crud_productos.get_producto_id(db, id)

    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El producto no existe"
        )

    return producto

@app.post("/productos/registro", response_model=ProductoOut)
def crear_producto(data: ProductoCreate, db:Session = Depends(get_db)):
    producto = crud_productos.crear_producto(db, data)
    
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El producto ya existe"
        )

    return ProductoOut(
        Id_Producto=producto.Id_Producto,
        Id_Sucursal=producto.Id_Sucursal,
        Id_Categoria=producto.Id_Categoria,
        Id_Marca=producto.Id_Marca,
        cod_barra = producto.cod_barra,
        nombre=producto.nombre,
        descripcion=producto.descripcion,
        stock_minimo=producto.stock_minimo,
        stock_maximo= producto.stock_maximo,
        precio=producto.precio,
        costo=producto.costo,
        porcentaje_isv=producto.porcentaje_isv,
        estado=producto.estado
    )

@app.put("/productos/{id}", response_model=ProductoOut)
def actualizar_producto (id:int, data: ProductoUpdate, db:Session=Depends(get_db)):
    producto = crud_productos.actualizar_producto(db,id,data)

    if not producto:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El producto no existe o el nuevo nombre ya esta registrado"
        )
    
    return ProductoOut(
        Id_Producto=producto.Id_Producto,
        Id_Sucursal=producto.Id_Sucursal,
        Id_Categoria=producto.Id_Categoria,
        Id_Marca=producto.Id_Marca,
        cod_barra = producto.cod_barra,
        nombre=producto.nombre,
        descripcion=producto.descripcion,
        stock_minimo=producto.stock_minimo,
        stock_maximo= producto.stock_maximo,
        precio=producto.precio,
        costo=producto.costo,
        porcentaje_isv=producto.porcentaje_isv,
        estado=producto.estado
    )

#marcas
@app.get("/marcas", response_model=list[MarcaOut])
def listar_marcas(db: Session = Depends(get_db)):
    return crud_marcas.get_marcas(db)

@app.get("/marcas/{id}", response_model=MarcaOut)
def listar_marcas_id(id: int, db: Session = Depends(get_db)):
    marca = crud_marcas.get_marcas_id(db, id)

    if not marca:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La marca no existe"
        )

    return marca

@app.post("/marcas/registro", response_model=MarcaOut)
def crear_marca(data: MarcaCreate, db: Session = Depends(get_db)):
    marca = crud_marcas.crear_marcas(db, data)

    if not marca:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La marca ya existe"
        )

    return MarcaOut(
        Id_Marca=marca.Id_Marca,
        nombre=marca.nombre,
        pais_origen=marca.pais_origen,
        estado=marca.estado
    )


@app.put("/marcas/{id}", response_model=MarcaOut)
def actualizar_marca(id: int, data: MarcaUpdate, db: Session = Depends(get_db)):
    marca = crud_marcas.actualizar_Marcas(db, id, data)

    if not marca:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La marca no existe o el nuevo nombre ya esta registrado"
        )

    return MarcaOut(
        Id_Marca=marca.Id_Marca,
        nombre=marca.nombre,
        pais_origen=marca.pais_origen,
        estado=marca.estado
    )

#Inventarios
@app.get("/inventarios", response_model=list[InventarioOut])
def listar_inventarios(db: Session = Depends(get_db)):
    return crud_inventarios.get_inventarios(db)

@app.get("/inventarios/vista")
def listar_vista_inventarios(db: Session = Depends(get_db)):
    return db.execute(text("""
        SELECT *
        FROM vw_inventarios
        ORDER BY id_inventario ASC
    """)).mappings().all()

@app.get("/inventarios/{id}", response_model=InventarioOut)
def listar_inventarios_id(id: int, db: Session = Depends(get_db)):
    inventario = crud_inventarios.get_inventarios_id(db, id)

    if not inventario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El inventario no existe"
        )

    return inventario

@app.post("/inventarios/registro", response_model=InventarioOut)
def crear_inventario(data: InventarioCreate, db: Session = Depends(get_db)):
    inventario = crud_inventarios.crear_inventarios(db, data)

    if not inventario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El inventario ya existe"
        )

    return InventarioOut(
        Id_Inventario=inventario.Id_Inventario,
        Id_Producto=inventario.Id_Producto,
        Id_Sucursal=inventario.Id_Sucursal,
        Id_lote_vencimiento=inventario.Id_lote_vencimiento,
        stock_actual=inventario.stock_actual
    )

@app.put("/inventarios/{id}", response_model=InventarioOut)
def actualizar_inventario(id: int, data: InventarioUpdate, db: Session = Depends(get_db)):
    inventario = crud_inventarios.actualizar_inventarios(db, id, data)

    if not inventario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El inventario no existe"
        )

    return InventarioOut(
        Id_Inventario=inventario.Id_Inventario,
        Id_Producto=inventario.Id_Producto,
        Id_Sucursal=inventario.Id_Sucursal,
        Id_lote_vencimiento=inventario.Id_lote_vencimiento,
        stock_actual=inventario.stock_actual
    )


#ProductoOferta

@app.get("/productosofertas", response_model=list[ProductoOfertaOut])
def listar_productos_ofertas(db: Session = Depends(get_db)):
    return crud_producto_oferta.get_productos_ofertas(db)

@app.get("/productosofertas/{id}", response_model=ProductoOfertaOut)
def listar_productos_ofertas_id(id: int, db: Session = Depends(get_db)):
    producto_oferta = crud_producto_oferta.get_productos_ofertas_id(db, id)

    if not producto_oferta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El producto oferta no existe"
        )

    return producto_oferta


@app.post("/productosofertas/registro", response_model=ProductoOfertaOut)
def crear_producto_oferta(data: ProductoOfertaCreate, db: Session = Depends(get_db)):
    producto_oferta = crud_producto_oferta.crear_producto_oferta(db, data)

    if not producto_oferta:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La asignacion ya existe o el producto u oferta no existe"
        )

    return ProductoOfertaOut(
        Id_ProductosOfertas=producto_oferta.Id_ProductosOfertas,
        Id_Productos=producto_oferta.Id_Productos,
        Id_Oferta=producto_oferta.Id_Oferta
    )

@app.put("/productosofertas/{id}", response_model=ProductoOfertaOut)
def actualizar_producto_oferta(id: int, data: ProductoOfertaUpdate, db: Session = Depends(get_db)):
    producto_oferta = crud_producto_oferta.actualizar_producto_oferta(db, id, data)

    if not producto_oferta:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La asignacion no existe, esta duplicada o el producto u oferta no existe"
        )

    return ProductoOfertaOut(
        Id_ProductosOfertas=producto_oferta.Id_ProductosOfertas,
        Id_Productos=producto_oferta.Id_Productos,
        Id_Oferta=producto_oferta.Id_Oferta
    )

# Direcciones de clientes
@app.post("/clientes/direccion", status_code=status.HTTP_200_OK)
def guardar_direccion_cliente(
    id_persona: int,
    data: DireccionCreate,
    db: Session = Depends(get_db),
):
    if not id_persona:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Debes iniciar sesión para guardar una dirección de envío",
        )

    try:
        resultado = crud_direcciones.asignar_direccion_cliente(
            db=db,
            id_persona=id_persona,
            data=data,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró un cliente asociado al usuario",
        )

    dir_obj = resultado["direccion"]
    return {
        "Id_Cliente": resultado["Id_Cliente"],
        "Id_Persona": resultado["Id_Persona"],
        "Id_Direccion": resultado["Id_Direccion"],
        "direccion": DireccionOut.model_validate(dir_obj),
    }