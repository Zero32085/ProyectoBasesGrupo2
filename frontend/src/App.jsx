import {useState} from "react";
import TiendaClientes from "./pages/TiendaClientes";
import Login from "./pages/Login";
import PanelAdmin from "./pages/PanelAdmin";
import AperturaCaja from "./pages/AperturaCaja";
import ArqueoCierre from "./pages/ArqueoCierre";
import PanelEmpleado from "./pages/PanelEmpleado";

import BotonLogin from "./components/BotonLogin";

export default function App() {

  const [usuarioActivo, setUsuarioActivo] = useState(null);
  const [vista,setVista] = useState("tienda")
  const [sesionCaja, setSesionCaja] = useState(null);
  const [mostrandoApertura, setMostrandoApertura] = useState(false);
  

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
    setSesionCaja(null);
    setMostrandoApertura(false);
    setVista("tienda");
  };

  if(!usuarioActivo && vista === "login"){
      return <Login onLoginSuccess={manejarLoginExitoso}/>
  }


if(vista === "admin" && usuarioActivo?.rol_empleado.toLowerCase() === "administrador"){
    return(
        <PanelAdmin onCerrarSesion={cerrarSesion}/>
    );
}

if (!usuarioActivo || usuarioActivo.rol === "cliente") {
    return (
      <TiendaClientes
        usuarioActivo={usuarioActivo}
        onAbrirLogin={abrirLogin}
        onCerrarSesion={cerrarSesion}
      />
    );
  }

if (!sesionCaja) {
  return (
      <AperturaCaja
        usuario={usuarioActivo}
        onCajaAbierta={setSesionCaja}
        onCerrarSesion={cerrarSesion}
      />
    );
  }

  if (mostrandoApertura) {
      return (
          <AperturaCaja
              usuario={usuarioActivo}
              onCajaAbierta={(datosCaja) => {
                  setSesionCaja(datosCaja);
                  setMostrandoApertura(false);
              }}
              onCerrarSesion={cerrarSesion}
          />
      );
  }

  if (mostrandoArqueo) {
    return (
      <ArqueoCierre
        usuario={usuarioActivo}
        sesionCaja={sesionCaja}
        onVolver={() => setMostrandoArqueo(false)}
        onCajaCerrada={() => {
          setSesionCaja(null);        // vuelve a la pantalla de apertura
          setMostrandoArqueo(false);
        }}
      />
    );
  }

  return (
      <PanelEmpleado
        usuario={usuarioActivo}
        sesionCaja={sesionCaja}
        onArqueoCierre={() => setMostrandoArqueo(true)}
        onCerrarSesion={cerrarSesion}
      />
    );

}
