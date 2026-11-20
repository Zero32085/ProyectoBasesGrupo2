import { useState } from "react";
import "./Login.css";

export default function Login({onLoginSuccess}){
//Esta parte define el rol de empleado o de cliente
const [rol,setRol] = useState(null);

//Estos son los estados para un cliente que va a hacer un login
const [modoCliente,setModoCliente] = useState("login");

const [correoLogin,setCorreoLogin] = useState("");

const [claveClienteLogin,setClaveClienteLogin] = useState("");


//Estos son los estados para un cliente que va a crear un nuevo registro

const [nombreRegistro, setNombreRegistro] = useState("");

const [correoRegistro, setCorreoRegistro] = useState("");

const [claveRegistro,setClaveRegistro] = useState("");

//Esta parte son los estados del login del empleado

const [codigoEmpleado, setCodigoEmpleado] = useState("");

const [claveEmpleado, setClaveEmpleado] = useState("");


//Mensajes de Retroalimentacion en la ventana del login
const [mensaje,setMensaje] = useState("");

const resetearMensaje = () => setMensaje("");


const seleccionarRol = (nuevoRol) => {
    setRol(nuevoRol);
    setModoCliente("login");
    resetearMensaje();
};

const volverAlInicio = () =>{
    setRol(null);
    resetearMensaje();
};

const manejarLoginCliente = (e) =>{
    e.preventDefault();
    const payload = {
        rol: "cliente",
        correo: correoLogin.trim(),
        contrasena: claveClienteLogin,
    };

    setMensaje(`Inicio de Sesion de Cliente preparado para ${payload.correo}`);
    if (onLoginSuccess) onLoginSuccess(payload);
};

const manejarRegistroCliente = (e) =>{
    e.preventDefault();
    const payload = {
        rol: "cliente",
        nombre: nombreRegistro.trim(),
        correo: correoRegistro.trim(),
        contrasena: claveRegistro,
    };

    setMensaje(`Cuenta Creada para ${payload.correo}. Ya puedes iniciar sesion`);

    setNombreRegistro("");
    setCorreoRegistro("");
    setClaveRegistro("");
    setModoCliente("login");
};

const manejarLoginEmpleado = (e) =>{
    e.preventDefault();
    const payload = {
        rol:"empleado",
        codigo: codigoEmpleado.trim(),
        contrasena: claveEmpleado,
    };
    setMensaje(`Acceso de empleado preparado para ${payload.codigo}`);
    if(onLoginSuccess) onLoginSuccess(payload);
};

return (
<div className="login-wrapper">
  <div className="login-card">
    {!rol && (
      <>
        <div className="login-header">
          <h1>SuperMarket</h1>
          <p>Selecciona cómo deseas ingresar al sistema</p>
        </div>

        <div className="rol-grid">
          <button
            type="button"
            className="rol-btn"
            onClick={() => seleccionarRol("cliente")}
          >
            <span className="rol-icono">🛒</span>
            <span>Soy Cliente</span>
          </button>

          <button
            type="button"
            className="rol-btn"
            onClick={() => seleccionarRol("empleado")}
          >
            <span className="rol-icono">🪪</span>
            <span>Soy Empleado</span>
          </button>
        </div>
      </>
    )}

    {rol === "cliente" && (
      <>
        <div className="login-header">
          <h1>Acceso Cliente</h1>
          <p>Ingresa con tu correo o crea una cuenta nueva</p>
        </div>

        <div className="modo-tabs">
          <button
            type="button"
            className={`tab-btn ${modoCliente === "login" ? "activo" : ""}`}
            onClick={() => {
              setModoCliente("login");
              resetearMensaje();
            }}
          >
            Iniciar Sesión
          </button>
          <button
            type="button"
            className={`tab-btn ${modoCliente === "registro" ? "activo" : ""}`}
            onClick={() => {
              setModoCliente("registro");
              resetearMensaje();
            }}
          >
            Crear Cuenta
          </button>
        </div>

        {modoCliente === "login" ? (
          <form onSubmit={manejarLoginCliente}>
            <div className="form-grupo">
              <label htmlFor="correo-cliente">Correo electrónico</label>
              <input
                id="correo-cliente"
                type="email"
                placeholder="cliente@correo.com"
                value={correoLogin}
                onChange={(e) => setCorreoLogin(e.target.value)}
                required
              />
            </div>

            <div className="form-grupo">
              <label htmlFor="clave-cliente">Contraseña</label>
              <input
                id="clave-cliente"
                type="password"
                placeholder="••••••••"
                value={claveClienteLogin}
                onChange={(e) => setClaveClienteLogin(e.target.value)}
                required
              />
            </div>

            <button type="submit" className="btn-primario">
              Entrar como Cliente
            </button>
          </form>
        ) : (
          <form onSubmit={manejarRegistroCliente}>
            <div className="form-grupo">
              <label htmlFor="nombre-registro">Nombre completo</label>
              <input
                id="nombre-registro"
                type="text"
                placeholder="Ej. María Pérez"
                value={nombreRegistro}
                onChange={(e) => setNombreRegistro(e.target.value)}
                required
              />
            </div>

            <div className="form-grupo">
              <label htmlFor="correo-registro">Correo electrónico</label>
              <input
                id="correo-registro"
                type="email"
                placeholder="maria@correo.com"
                value={correoRegistro}
                onChange={(e) => setCorreoRegistro(e.target.value)}
                required
              />
            </div>

            <div className="form-grupo">
              <label htmlFor="clave-registro">Contraseña</label>
              <input
                id="clave-registro"
                type="password"
                placeholder="Mínimo 6 caracteres"
                minLength={6}
                value={claveRegistro}
                onChange={(e) => setClaveRegistro(e.target.value)}
                required
              />
            </div>

            <button type="submit" className="btn-primario">
              Registrar Cuenta de Cliente
            </button>
          </form>
        )}

        <button type="button" className="btn-volver" onClick={volverAlInicio}>
          ← Cambiar rol (Cliente / Empleado)
        </button>
      </>
    )}

    {rol === "empleado" && (
      <>
        <div className="login-header">
          <h1>Acceso Empleado</h1>
          <p>Ingresa tu código de empleado y contraseña</p>
        </div>

        <form onSubmit={manejarLoginEmpleado}>
          <div className="form-grupo">
            <label htmlFor="codigo-empleado">Código de empleado</label>
            <input
              id="codigo-empleado"
              type="text"
              placeholder="Ej. EMP-001"
              value={codigoEmpleado}
              onChange={(e) => setCodigoEmpleado(e.target.value)}
              required
            />
          </div>

          <div className="form-grupo">
            <label htmlFor="clave-empleado">Contraseña</label>
            <input
              id="clave-empleado"
              type="password"
              placeholder="••••••••"
              value={claveEmpleado}
              onChange={(e) => setClaveEmpleado(e.target.value)}
              required
            />
          </div>

          <button type="submit" className="btn-primario">
            Entrar como Empleado
          </button>
        </form>

        <button type="button" className="btn-volver" onClick={volverAlInicio}>
          ← Cambiar rol (Cliente / Empleado)
        </button>
      </>
    )}

    {mensaje && <div className="mensaje-feedback">{mensaje}</div>}
  </div>
</div>
  );
}