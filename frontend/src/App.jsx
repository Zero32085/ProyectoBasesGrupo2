import {useState} from "react";
import TiendaClientes from "./pages/TiendaClientes";
import Login from "./pages/Login";
import BotonLogin from "./components/BotonLogin";

export default function App() {

  const [usuarioActivo, setUsuarioActivo] = useState(null);
  const [vista,setVista] = useState("tienda")

  
  const manejarLoginExitoso = (datosUsuario) =>{
    setUsuarioActivo(datosUsuario);
    if(datosUsuario.rol === "cliente"){
      setVista("tienda");
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


  return(
    <TiendaClientes
    usuarioActivo = {usuarioActivo}
    onAbrirLogin = {abrirLogin}
    onCerrarSesion = {cerrarSesion}
    />
  );
}