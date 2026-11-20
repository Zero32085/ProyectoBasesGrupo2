import {useState} from "react";
import TiendaClientes from "./pages/TiendaClientes";
import Login from "./pages/Login";

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

  if(usuarioActivo.rol == "clientes"){
    return(
      <TiendaClientes
      usuatio = {usuarioActivo}
      onCerrarSesion = {cerrarSesion}
      />
    );
  }

  return (
    <di
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
    </di>
  )
}