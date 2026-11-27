import {useState} from "react";
import TiendaClientes from "./pages/TiendaClientes";
import Login from "./pages/Login";
import PanelAdmin from "./pages/PanelAdmin";

export default function App() {
  const [usuarioActivo, setUsuarioActivo] = useState(null);

  const manejarLoginExitoso = (datosUsuario) =>{
    setUsuarioActivo(datosUsuario);
  };

  const cerrarSesion = () =>{
    setUsuarioActivo(null);
  };

  if(!usuarioActivo){
    return <Login onLoginSuccess={manejarLoginExitoso}/>;
  }

  if(usuarioActivo.rol == "cliente"){
    return(
      <TiendaClientes
      usuatio = {usuarioActivo}
      onCerrarSesion = {cerrarSesion}
      />
    );
  }

if(usuarioActivo.rol === "empleado"){
    return(
        <PanelAdmin onCerrarSesion={cerrarSesion}/>
    );
}
  return (
    <div
        style={{
            padding: "2rem",
            color: "#f8fafc",
            backgroundColor: "#0f172a",
            minHeight: "100vh",
        }}
    >
        <h2>Panel de Empleado</h2>
        <p>Código: {usuarioActivo.codigo}</p>

        <button type="button" onClick={cerrarSesion}>
            Cerrar sesión
        </button>
    </div>
);
}