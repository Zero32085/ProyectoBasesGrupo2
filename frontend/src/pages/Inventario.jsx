import {useState, useEffect} from "react";
import {
    crearInventario,
    actualizarInventario,
    getVistaInventarios
} from "../services/inventarioService";
import {getProductos} from "../services/productosService";

export default function Inventario(){

    const [inventarios, setInventarios] = useState([]);
    const [productos, setProductos] = useState([]);
    const [busqueda, setBusqueda] = useState("");
    const [error, setError] = useState("");
    const [mostrarFormulario, setMostrarFormulario] = useState(false);
    const [idInventario, setIdInventario] = useState(null);

    const datosIniciales = {
        Id_Producto: "",
        Id_Sucursal: "",
        Id_lote_vencimiento: "",
        stock_actual: ""
    };

    const [formulario, setFormulario] = useState(datosIniciales);

    async function cargarInventarios(){
        try{
            setInventarios(await getVistaInventarios());
            setProductos(await getProductos());
        }catch(error){
            setError(error.message);
        }
    }

    useEffect(() => {
        cargarInventarios();
    }, []);

    const inventariosFiltrados = inventarios.filter(
        inventario => (inventario.producto || "")
            .toLowerCase()
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "")
            .includes(
                busqueda.toLowerCase()
                    .normalize("NFD")
                    .replace(/[\u0300-\u036f]/g, "")
            )
    );

    function nuevoInventario(){
        setIdInventario(null);
        setFormulario(datosIniciales);
        setError("");
        setMostrarFormulario(true);
    }

    function editarInventario(inventario){
        setIdInventario(inventario.id_inventario);

        setFormulario({
            Id_Producto: inventario.id_producto,
            Id_Sucursal: inventario.id_sucursal,
            Id_lote_vencimiento: inventario.id_lote_vencimiento,
            stock_actual: inventario.stock_actual
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

    async function guardarInventario(e){
        e.preventDefault();
        setError("");

        try{
            if(idInventario === null){

                await crearInventario({
                    Id_Producto: Number(formulario.Id_Producto),
                    Id_Sucursal: Number(formulario.Id_Sucursal),
                    Id_lote_vencimiento: Number(formulario.Id_lote_vencimiento),
                    stock_actual: Number(formulario.stock_actual)
                });

            }else{

                await actualizarInventario(idInventario, {
                    stock_actual: Number(formulario.stock_actual)
                });

            }

            setMostrarFormulario(false);
            await cargarInventarios();

        }catch(error){
            setError(error.message);
        }
    }

    return(
        <div>
            <h2>Inventario</h2>

            <div className="admin-buscador">
                <input
                    type="text"
                    placeholder="Buscar producto..."
                    value={busqueda}
                    onChange={e => setBusqueda(e.target.value)}
                />
            </div>

            <button
                className="admin-btn-nuevo"
                onClick={nuevoInventario}
            >
                + Nuevo inventario
            </button>

            {error && (
                <p className="admin-error">{error}</p>
            )}

            {mostrarFormulario && (
                <form
                    className="admin-formulario"
                    onSubmit={guardarInventario}
                >
                    <h3>
                        {idInventario === null
                            ? "Nuevo inventario"
                            : "Editar inventario"}
                    </h3>

                    <label>Producto</label>
                    <select
                        name="Id_Producto"
                        value={formulario.Id_Producto}
                        onChange={cambiarCampo}
                        disabled={idInventario !== null}
                        required
                    >
                        <option value="">
                            Seleccione un producto
                        </option>

                        {productos.filter(p =>
                            p.estado === 1 ||
                            p.Id_Producto === Number(formulario.Id_Producto)
                        ).map(producto => (
                            <option
                                key={producto.Id_Producto}
                                value={producto.Id_Producto}
                            >
                                {producto.nombre}
                            </option>
                        ))}
                    </select>

                    <label>Sucursal</label>
                    <input
                        type="number"
                        name="Id_Sucursal"
                        value={formulario.Id_Sucursal}
                        onChange={cambiarCampo}
                        disabled={idInventario !== null}
                        min={1}
                        required
                    />

                    <label>Lote de vencimiento</label>
                    <input
                        type="number"
                        name="Id_lote_vencimiento"
                        value={formulario.Id_lote_vencimiento}
                        onChange={cambiarCampo}
                        disabled={idInventario !== null}
                        min={1}
                        required
                    />

                    <label>Stock actual</label>
                    <input
                        type="number"
                        name="stock_actual"
                        value={formulario.stock_actual}
                        onChange={cambiarCampo}
                        min={0}
                        step="0.01"
                        required
                    />

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
                            <th>Producto</th>
                            <th>Sucursal</th>
                            <th>Lote</th>
                            <th>Stock actual</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>

                    <tbody>
                        {inventariosFiltrados.map(inventario => (
                            <tr key={inventario.id_inventario}>
                                <td>{inventario.id_inventario}</td>
                                <td>{inventario.producto}</td>
                                <td>{inventario.sucursal}</td>
                                <td>{inventario.id_lote_vencimiento}</td>
                                <td>{inventario.stock_actual}</td>

                                <td>
                                    <button
                                        className="admin-btn-editar"
                                        onClick={() => editarInventario(inventario)}
                                    >
                                        Editar
                                    </button>
                                </td>
                            </tr>
                        ))}

                        {inventariosFiltrados.length === 0 && (
                            <tr>
                                <td colSpan={6}>
                                    No se encontraron registros.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
}