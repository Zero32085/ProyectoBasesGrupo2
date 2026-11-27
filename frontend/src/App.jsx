import {useState} from "react";
import TiendaClientes from "./pages/TiendaClientes";
import Login from "./pages/Login";
import PanelAdmin from "./pages/PanelAdmin";
import BotonLogin from "./components/BotonLogin";

export default function App() {

  const [usuarioActivo, setUsuarioActivo] = useState(null);
  const [vista,setVista] = useState("tienda")

  const manejarLoginExitoso = (datosUsuario) =>{
  
    setUsuarioActivo(datosUsuario);
    if(datosUsuario.rol === "cliente"){
      setVista("tienda");
    }else if(datosUsuario.rol_empleado.toLowerCase() === "administrador"){
      setVista("admin");
    }
  };
  
  const abrirLogin = () =>{
    setVista("login")
  }
  
  const cerrarSesion = () =>{
    setUsuarioActivo(null);
    setVista("tienda");
  };

  if(vista === "login"){
      return <Login onLoginSuccess={manejarLoginExitoso}/>
  }


if(vista === "admin" && usuarioActivo?.rol_empleado.toLowerCase() === "administrador"){
    return(
        <PanelAdmin onCerrarSesion={cerrarSesion}/>
    );
}

return(
    <TiendaClientes
        usuarioActivo={usuarioActivo}
        onAbrirLogin={abrirLogin}
        onCerrarSesion={cerrarSesion}
    />
  );
}