import {useState, useEffect} from "react";
import {
    crearProducto,
    actualizarProducto,
    getMarcas,
    getVistaProductos
} from "../services/productosService";
import {getCategorias} from "../services/categoriasService";

export default function Productos(){

    const [productos, setProductos] = useState([]);
    const [categorias, setCategorias] = useState([]);
    const [marcas, setMarcas] = useState([]);
    const [busqueda, setBusqueda] = useState("");
    const [error, setError] = useState("");
    const [mostrarFormulario, setMostrarFormulario] = useState(false);
    const [idProducto, setIdProducto] = useState(null);

    const datosIniciales = {
        Id_Sucursal: "",
        Id_Categoria: "",
        Id_Marca: "",
        cod_barra: "",
        nombre: "",
        descripcion: "",
        stock_minimo: "",
        stock_maximo: "",
        precio: "",
        costo: "",
        porcentaje_isv: "",
        estado: 1
    };

    const [formulario, setFormulario] = useState(datosIniciales);

    async function cargarProductos(){
        try{
            setProductos(await getVistaProductos());
            setCategorias(await getCategorias());
            setMarcas(await getMarcas());
        }catch(error){
            setError(error.message);
        }
    }

    useEffect(() => {
        cargarProductos();
    }, []);

    const productosFiltrados = productos.filter(
        producto => producto.nombre.toLowerCase()
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "")
            .includes(
                busqueda.toLowerCase()
                    .normalize("NFD")
                    .replace(/[\u0300-\u036f]/g, "")
            )
        || String(producto.cod_barra).includes(busqueda)
    );

    function nuevoProducto(){
        setIdProducto(null);
        setFormulario(datosIniciales);
        setError("");
        setMostrarFormulario(true);
    }

    function editarProducto(producto){
        setIdProducto(producto.id_producto);

        setFormulario({
            Id_Sucursal: producto.id_sucursal,
            Id_Categoria: producto.id_categoria,
            Id_Marca: producto.id_marca,
            cod_barra: producto.cod_barra,
            nombre: producto.nombre,
            descripcion: producto.descripcion,
            stock_minimo: producto.stock_minimo,
            stock_maximo: producto.stock_maximo,
            precio: producto.precio,
            costo: producto.costo,
            porcentaje_isv: producto.porcentaje_isv,
            estado: producto.estado
        });

        setError("");
        setMostrarFormulario(true);
    }

    function cambiarCampo(e){
        setFormulario({
            ...formulario,
            [e.target.name]: e.target.value
        });
    }

    async function guardarProducto(e){
        e.preventDefault();
        setError("");

        const datos = {
            ...formulario,
            Id_Sucursal: Number(formulario.Id_Sucursal),
            Id_Categoria: Number(formulario.Id_Categoria),
            Id_Marca: Number(formulario.Id_Marca),
            stock_minimo: Number(formulario.stock_minimo),
            stock_maximo: Number(formulario.stock_maximo),
            precio: Number(formulario.precio),
            costo: Number(formulario.costo),
            porcentaje_isv: Number(formulario.porcentaje_isv),
            estado: Number(formulario.estado)
        };

        try{
            if(idProducto === null){
                await crearProducto(datos);
            }else{
                await actualizarProducto(idProducto, datos);
            }

            setMostrarFormulario(false);
            await cargarProductos();

        }catch(error){
            setError(error.message);
        }
    }

    return(
        <div>
            <h2>Productos</h2>

            <div className="admin-buscador">
                <input
                    type="text"
                    placeholder="Buscar producto o código de barras..."
                    value={busqueda}
                    onChange={e => setBusqueda(e.target.value)}
                />
            </div>

            <button
                className="admin-btn-nuevo"
                onClick={nuevoProducto}
            >
                + Nuevo producto
            </button>

            {error && (
                <p className="admin-error">{error}</p>
            )}

            {mostrarFormulario && (
                <form
                    className="admin-formulario admin-formulario-amplio"
                    onSubmit={guardarProducto}
                >
                    <h3>
                        {idProducto === null
                            ? "Nuevo producto"
                            : "Editar producto"}
                    </h3>

                    <div className="admin-campos">

                        <div>
                            <label>Sucursal</label>
                            <input
                                type="number"
                                name="Id_Sucursal"
                                value={formulario.Id_Sucursal}
                                onChange={cambiarCampo}
                                min={1}
                                required
                            />
                        </div>

                        <div>
                            <label>Categoría</label>
                            <select
                                name="Id_Categoria"
                                value={formulario.Id_Categoria}
                                onChange={cambiarCampo}
                                required
                            >
                                <option value="">
                                    Seleccione una categoría
                                </option>

                                {categorias.filter(c =>
                                    c.estado === 1 ||
                                    c.Id_Categoria === Number(formulario.Id_Categoria)
                                ).map(categoria => (
                                    <option
                                        key={categoria.Id_Categoria}
                                        value={categoria.Id_Categoria}
                                    >
                                        {categoria.nombre}
                                    </option>
                                ))}
                            </select>
                        </div>

                        <div>
                            <label>Marca</label>
                            <select
                                name="Id_Marca"
                                value={formulario.Id_Marca}
                                onChange={cambiarCampo}
                                required
                            >
                                <option value="">
                                    Seleccione una marca
                                </option>

                                {marcas.filter(m =>
                                    m.estado === 1 ||
                                    m.Id_Marca === Number(formulario.Id_Marca)
                                ).map(marca => (
                                    <option
                                        key={marca.Id_Marca}
                                        value={marca.Id_Marca}
                                    >
                                        {marca.nombre}
                                    </option>
                                ))}
                            </select>
                        </div>

                        <div>
                            <label>Código de barras</label>
                            <input
                                type="text"
                                name="cod_barra"
                                value={formulario.cod_barra}
                                onChange={cambiarCampo}
                                maxLength={20}
                                required
                            />
                        </div>

                        <div>
                            <label>Nombre</label>
                            <input
                                type="text"
                                name="nombre"
                                value={formulario.nombre}
                                onChange={cambiarCampo}
                                maxLength={100}
                                required
                            />
                        </div>

                        <div>
                            <label>Descripción</label>
                            <input
                                type="text"
                                name="descripcion"
                                value={formulario.descripcion}
                                onChange={cambiarCampo}
                                maxLength={500}
                            />
                        </div>

                        <div>
                            <label>Stock mínimo</label>
                            <input
                                type="number"
                                name="stock_minimo"
                                value={formulario.stock_minimo}
                                onChange={cambiarCampo}
                                min={0}
                                step="0.01"
                                required
                            />
                        </div>

                        <div>
                            <label>Stock máximo</label>
                            <input
                                type="number"
                                name="stock_maximo"
                                value={formulario.stock_maximo}
                                onChange={cambiarCampo}
                                min={formulario.stock_minimo || 0}
                                step="0.01"
                                required
                            />
                        </div>

                        <div>
                            <label>Precio</label>
                            <input
                                type="number"
                                name="precio"
                                value={formulario.precio}
                                onChange={cambiarCampo}
                                min={0}
                                step="0.01"
                                required
                            />
                        </div>

                        <div>
                            <label>Costo</label>
                            <input
                                type="number"
                                name="costo"
                                value={formulario.costo}
                                onChange={cambiarCampo}
                                min={0}
                                step="0.01"
                                required
                            />
                        </div>

                        <div>
                            <label>Porcentaje ISV (decimal)</label>
                            <input
                                type="number"
                                name="porcentaje_isv"
                                value={formulario.porcentaje_isv}
                                onChange={cambiarCampo}
                                placeholder="Ejemplo: 0.15"
                                min={0}
                                max={1}
                                step="0.01"
                                required
                            />
                        </div>

                        <div>
                            <label>Estado</label>
                            <select
                                name="estado"
                                value={formulario.estado}
                                onChange={cambiarCampo}
                            >
                                <option value={1}>Activo</option>
                                <option value={0}>Inactivo</option>
                            </select>
                        </div>

                    </div>

                    <div className="admin-formulario-botones">
                        <button
                            type="submit"
                            className="admin-btn-nuevo"
                        >
                            Guardar
                        </button>

                        <button
                            type="button"
                            className="admin-btn-cancelar"
                            onClick={() => {
                                setMostrarFormulario(false);
                                setError("");
                            }}
                        >
                            Cancelar
                        </button>
                    </div>
                </form>
            )}

            <div className="admin-tabla-contenedor">
                <table className="admin-tabla">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Código de barras</th>
                            <th>Nombre</th>
                            <th>Categoría</th>
                            <th>Marca</th>
                            <th>Precio</th>
                            <th>Costo</th>
                            <th>Estado</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>

                    <tbody>
                        {productosFiltrados.map(producto => (
                            <tr key={producto.id_producto}>
                                <td>{producto.id_producto}</td>
                                <td>{producto.cod_barra}</td>
                                <td>{producto.nombre}</td>
                                <td>{producto.categoria}</td>
                                <td>{producto.marca}</td>

                                <td>
                                    L. {Number(producto.precio).toFixed(2)}
                                </td>

                                <td>
                                    L. {Number(producto.costo).toFixed(2)}
                                </td>

                                <td>
                                    {producto.estado === 1
                                        ? "Activo"
                                        : "Inactivo"}
                                </td>

                                <td>
                                    <button
                                        className="admin-btn-editar"
                                        onClick={() => editarProducto(producto)}
                                    >
                                        Editar
                                    </button>
                                </td>
                            </tr>
                        ))}

                        {productosFiltrados.length === 0 && (
                            <tr>
                                <td colSpan={9}>
                                    No se encontraron productos.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
}