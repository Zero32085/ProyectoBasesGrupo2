import {useState} from "react";
import Productos from "./Productos";
import Inventario from "./Inventario";
import Categorias from "./Categorias";
import "./PanelAdmin.css";

export default function PanelAdmin({onCerrarSesion}){

    const [pagina, setPagina] = useState("inicio");

    return(
        <div className="admin-panel">

            <aside className="admin-menu">
                <h1>Valora</h1>
                <p>Administrador</p>

                <nav>
                    <button onClick={() => setPagina("inicio")}>
                        Inicio
                    </button>

                    <button onClick={() => setPagina("productos")}>
                        Productos
                    </button>

                    <button onClick={() => setPagina("inventario")}>
                        Inventario
                    </button>

                    <button onClick={() => setPagina("categorias")}>
                        Categorías
                    </button>
                </nav>

                <button className="admin-salir" onClick={onCerrarSesion}>
                    Cerrar sesión
                </button>
            </aside>

            <main className="admin-contenido">

                {pagina === "inicio" && (
                    <>
                        <h2>Panel administrativo</h2>
                        <p>Bienvenido al sistema de Valora</p>

                        <div className="admin-tarjetas">

                            <button className="admin-tarjeta"
                                onClick={() => setPagina("productos")}>
                                <h3>Productos</h3>
                                <p>Administrar productos</p>
                            </button>

                            <button className="admin-tarjeta"
                                onClick={() => setPagina("inventario")}>
                                <h3>Inventario</h3>
                                <p>Consultar existencias</p>
                            </button>

                            <button className="admin-tarjeta"
                                onClick={() => setPagina("categorias")}>
                                <h3>Categorías</h3>
                                <p>Administrar categorías</p>
                            </button>

                        </div>
                    </>
                )}

                {pagina === "productos" && <Productos/>}

                {pagina === "inventario" && <Inventario/>}

                {pagina === "categorias" && <Categorias/>}

            </main>
        </div>
    );
}