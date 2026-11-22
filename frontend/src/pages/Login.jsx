import { useState } from "react";
import "./Login.css";
import { loginCliente,registroCliente, loginEmpleado } from "../services/authService";

export default function Login({ onLoginSuccess }) {
  const [rol, setRol] = useState(null);
  const [modoCliente, setModoCliente] = useState("login");

  const [correoLogin, setCorreoLogin] = useState("");
  const [claveClienteLogin, setClaveClienteLogin] = useState("");

  const [nombreRegistro, setNombreRegistro] = useState("");
  const [correoRegistro, setCorreoRegistro] = useState("");
  const [claveRegistro, setClaveRegistro] = useState("");

  const [codigoEmpleado, setCodigoEmpleado] = useState("");
  const [claveEmpleado, setClaveEmpleado] = useState("");

  const [mensaje, setMensaje] = useState("");
  const [cargando, setCargando] = useState(false);

  const resetearMensaje = () => setMensaje("");

  const seleccionarRol = (nuevoRol) => {
    setRol(nuevoRol);
    setModoCliente("login");
    resetearMensaje();
  };

  const volverAlInicio = () => {
    setRol(null);
    resetearMensaje();
  };

  const manejarLoginCliente = async (e) => {
    e.preventDefault();
    resetearMensaje();
    setCargando(true);

    try{
    const data = await loginCliente(correoLogin.trim(),claveClienteLogin);
    setMensaje(`Bienvenido, ${data.primer_nombre ?? data.correo}`);
    if(onLoginSuccess) onLoginSuccess(data)
    } catch(err){
      setMensaje(err.message || "Error de conexión con el servidor")
    }finally{
      setCargando(false)
    }

  };

  const manejarRegistroCliente = async (e) => {
    e.preventDefault();
    resetearMensaje();
    setCargando(true);

    const partes = nombreRegistro.trim().split(/\s+/).filter(Boolean);
    const primer_nombre = partes[0] || "Cliente";
    const primer_apellido = partes.slice(1).join(" ") || "General";
    
    try{
      const data = await registroCliente(correoRegistro.trim(),claveRegistro);
      setMensaje(`Cuenta creada para ${data.correo}. Ya puedes iniciar sesión.`);
      setNombreRegistro("");
      setCorreoRegistro("");
      setClaveRegistro("");
      setModoCliente("login");
    } catch(err){
      setMensaje(err.message || "No se pudo crear la cuenta");
    }finally{
      setCargando(false);
    }
  };

  const manejarLoginEmpleado = async (e) => {
    e.preventDefault();
    resetearMensaje();
    setCargando(true);
    try {
      const data = await loginEmpleado(codigoEmpleado.trim(),claveEmpleado);
      setMensaje(`Bienvenido, ${data.primer_nombre ?? data.codigo_empleado}`);
      if(onLoginSuccess) onLoginSuccess(data)
    } catch(err){
      setMensaje(err.message || "Erro con la conexion al servidor")
    } finally{
      setCargando(false);
    }
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

                <button type="submit" className="btn-primario" disabled={cargando}>
                  {cargando ? "Ingresando..." : "Entrar como Cliente"}
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
                    placeholder="Mínimo 8 caracteres"
                    minLength={8}
                    value={claveRegistro}
                    onChange={(e) => setClaveRegistro(e.target.value)}
                    required
                  />
                </div>

                <button type="submit" className="btn-primario" disabled={cargando}>
                  {cargando ? "Registrando..." : "Registrar Cuenta de Cliente"}
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
                  placeholder="Ej. EMP001"
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

              <button type="submit" className="btn-primario" disabled={cargando}>
                {cargando ? "Ingresando..." : "Entrar como Empleado"}
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