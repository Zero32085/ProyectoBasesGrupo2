import {useState, useEffect} from "react";
import {
    getCategorias,
    crearCategoria,
    actualizarCategoria
} from "../services/categoriasService";

export default function Categorias(){

    const [categorias, setCategorias] = useState([]);
    const [busqueda, setBusqueda] = useState("");
    const [error, setError] = useState("");
    const [mostrarFormulario, setMostrarFormulario] = useState(false);
    const [idCategoria, setIdCategoria] = useState(null);

    const [formulario, setFormulario] = useState({
        nombre: "",
        descripcion: "",
        estado: 1
    });

    async function cargarCategorias(){
        try{
            const data = await getCategorias();
            setCategorias(data);
        }catch(error){
            setError(error.message);
        }
    }

    useEffect(() => {
        cargarCategorias();
    }, []);

    const categoriasFiltradas = categorias.filter(
        categoria => categoria.nombre.toLowerCase()
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "")
            .includes(
                busqueda.toLowerCase()
                    .normalize("NFD")
                    .replace(/[\u0300-\u036f]/g, "")
            )
    );

    function nuevaCategoria(){
        setIdCategoria(null);

        setFormulario({
            nombre: "",
            descripcion: "",
            estado: 1
        });

        setError("");
        setMostrarFormulario(true);
    }

    function editarCategoria(categoria){
        setIdCategoria(categoria.Id_Categoria);

        setFormulario({
            nombre: categoria.nombre,
            descripcion: categoria.descripcion,
            estado: categoria.estado
        });

        setError("");
        setMostrarFormulario(true);
    }

    async function guardarCategoria(e){
        e.preventDefault();
        setError("");

        try{
            if(idCategoria === null){
                await crearCategoria(formulario);
            }else{
                await actualizarCategoria(idCategoria, formulario);
            }

            setMostrarFormulario(false);
            await cargarCategorias();

        }catch(error){
            setError(error.message);
        }
    }

    return(
        <div>
            <h2>Categorías</h2>

            <div className="admin-buscador">
                <input
                    type="text"
                    placeholder="Buscar categoría..."
                    value={busqueda}
                    onChange={e => setBusqueda(e.target.value)}
                />
            </div>

            <button
                className="admin-btn-nuevo"
                onClick={nuevaCategoria}
            >
                + Nueva categoría
            </button>

            {error && (
                <p className="admin-error">{error}</p>
            )}

            {mostrarFormulario && (
                <form
                    className="admin-formulario"
                    onSubmit={guardarCategoria}
                >
                    <h3>
                        {idCategoria === null
                            ? "Nueva categoría"
                            : "Editar categoría"}
                    </h3>

                    <label>Nombre</label>
                    <input
                        type="text"
                        value={formulario.nombre}
                        maxLength={100}
                        onChange={e => setFormulario({
                            ...formulario,
                            nombre: e.target.value
                        })}
                        required
                    />

                    <label>Descripción</label>
                    <textarea
                        value={formulario.descripcion}
                        maxLength={500}
                        onChange={e => setFormulario({
                            ...formulario,
                            descripcion: e.target.value
                        })}
                        required
                    />

                    <label>Estado</label>
                    <select
                        value={formulario.estado}
                        onChange={e => setFormulario({
                            ...formulario,
                            estado: Number(e.target.value)
                        })}
                    >
                        <option value={1}>Activo</option>
                        <option value={0}>Inactivo</option>
                    </select>

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

            <table className="admin-tabla">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nombre</th>
                        <th>Descripción</th>
                        <th>Estado</th>
                        <th>Acciones</th>
                    </tr>
                </thead>

                <tbody>
                    {categoriasFiltradas.map(categoria => (
                        <tr key={categoria.Id_Categoria}>
                            <td>{categoria.Id_Categoria}</td>
                            <td>{categoria.nombre}</td>
                            <td>{categoria.descripcion}</td>
                            <td>
                                {categoria.estado === 1
                                    ? "Activo"
                                    : "Inactivo"}
                            </td>
                            <td>
                                <button
                                    className="admin-btn-editar"
                                    onClick={() => editarCategoria(categoria)}
                                >
                                    Editar
                                </button>
                            </td>
                        </tr>
                    ))}

                    {categoriasFiltradas.length === 0 && (
                        <tr>
                            <td colSpan={5}>
                                No se encontraron categorías.
                            </td>
                        </tr>
                    )}
                </tbody>
            </table>
        </div>
    );
}