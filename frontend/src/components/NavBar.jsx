import BotonLogin from "./BotonLogin";
import logo from "../assets/Logo.png"
import "./styles/NavBar.css"

export default function NavBar({
    busqueda,
    setBusqueda,
    usuarioActivo,
    onAbrirLogin,
    onCerrarSesion
}){
    return (
        <header className="tienda-header">
            <div className="logo">
                <img className="logo-img" src={logo}></img>
            </div>
                <input
                    type="text"
                    className="buscador-input"
                    placeholder="Buscar producto"
                    value={busqueda}
                    onChange={(e) => setBusqueda(e.target.value)}
                />
                <BotonLogin
                    usuarioActivo={usuarioActivo}
                    onAbrirLogin={onAbrirLogin}
                    onCerrarSesion={onCerrarSesion}
                />
            <div className="rol-badge">
                {usuarioActivo ? `Vista: ${usuarioActivo.rol}` : "Vista: Invitado"}
            </div>
        </header>
    );
}