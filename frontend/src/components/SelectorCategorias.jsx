import { useEffect, useRef, useState } from "react";
import "./styles/SelectorCategorias.css";

export default function SelectorCategorias({
    categorias,
    categoriaActiva,
    onSeleccionar,
    }) {
    const [abierto, setAbierto] = useState(false);
    const contenedorRef = useRef(null);

    const categoriaSeleccionada =
        categorias.find((cat) => cat.id_categoria === categoriaActiva) ||
        categorias[0] || { id_categoria: 0, nombre: "Todas" };

    useEffect(() => {
        const manejarClickFuera = (e) => {
        if (contenedorRef.current && !contenedorRef.current.contains(e.target)) {
            setAbierto(false);
        }
        };

        const manejarEscape = (e) => {
        if (e.key === "Escape") setAbierto(false);
        };

        document.addEventListener("mousedown", manejarClickFuera);
        document.addEventListener("keydown", manejarEscape);
        return () => {
        document.removeEventListener("mousedown", manejarClickFuera);
        document.removeEventListener("keydown", manejarEscape);
        };
    }, []);

    const elegirCategoria = (idCategoria) => {
        onSeleccionar(idCategoria);
        setAbierto(false);
    };

    return (
        <div className="selector-categorias-bar" ref={contenedorRef}>
        <div className="dropdown-categorias">
            <button
            type="button"
            className={`dropdown-trigger ${categoriaActiva !== 0 ? "tiene-filtro" : ""}`}
            aria-expanded={abierto}
            onClick={() => setAbierto((prev) => !prev)}
            >
            <span className="dropdown-etiqueta">Categoría:</span>
            <strong className="dropdown-valor">{categoriaSeleccionada.nombre}</strong>
            <span className={`dropdown-flecha ${abierto ? "rotada" : ""}`}>▾</span>
            </button>

            {abierto && (
            <ul className="dropdown-menu-lista" role="listbox">
                {categorias.map((cat) => {
                const activa = cat.id_categoria === categoriaActiva;
                return (
                    <li key={cat.id_categoria}>
                    <button
                        type="button"
                        role="option"
                        aria-selected={activa}
                        className={`dropdown-opcion ${activa ? "activa" : ""}`}
                        onClick={() => elegirCategoria(cat.id_categoria)}
                    >
                        <span>{cat.nombre}</span>
                        {activa && <span className="opcion-check">✓</span>}
                    </button>
                    </li>
                );
                })}
            </ul>
            )}
        </div>

        {categoriaActiva !== 0 && (
            <button
            type="button"
            className="btn-limpiar-categoria"
            onClick={() => elegirCategoria(0)}
            >
            {categoriaSeleccionada.nombre} ×
            </button>
        )}
        </div>
    );
}