import { useEffect, useState } from "react";
import { abrirCaja, obtenerContextoApertura } from "../services/cajaService";
import "./style/AperturaCaja.css";

const formatoMoneda = (valor) =>
  new Intl.NumberFormat("es-HN", { style: "currency", currency: "HNL" }).format(
    Number(valor) || 0
  );

const formatoHora = (hhmmss) => (hhmmss ? hhmmss.slice(0, 5) : "");

const formatoFechaHora = (fecha) =>
  new Intl.DateTimeFormat("es-HN", { dateStyle: "full", timeStyle: "short" }).format(fecha);

export default function AperturaCaja({ usuario, onCajaAbierta, onCerrarSesion }) {
  const [contexto, setContexto] = useState(null);
  const [cargando, setCargando] = useState(true);
  const [errorCarga, setErrorCarga] = useState("");

  const [idCaja, setIdCaja] = useState("");
  const [fondo, setFondo] = useState("");
  const [confirmado, setConfirmado] = useState(false);
  const [enviando, setEnviando] = useState(false);
  const [errorEnvio, setErrorEnvio] = useState("");
  const [sesionNueva, setSesionNueva] = useState(null);

  const [ahora, setAhora] = useState(() => new Date());

  // Reloj de la cabecera
  useEffect(() => {
    const t = setInterval(() => setAhora(new Date()), 30000);
    return () => clearInterval(t);
  }, []);

  // Carga cajero, turno, permisos y cajas libres
  useEffect(() => {
    let cancelado = false;
    obtenerContextoApertura(usuario.Id_Empleado)
      .then((data) => !cancelado && setContexto(data))
      .catch((err) => !cancelado && setErrorCarga(err.message))
      .finally(() => !cancelado && setCargando(false));
    return () => {
      cancelado = true;
    };
  }, [usuario.Id_Empleado]);

  const fondoNumero = Number(fondo);
  const fondoValido =
    fondo !== "" &&
    Number.isFinite(fondoNumero) &&
    fondoNumero >= 0 &&
    /^\d+(\.\d{1,2})?$/.test(fondo);
  const puedeAbrir = Boolean(idCaja) && fondoValido && confirmado && !enviando;

  const manejarSubmit = async (e) => {
    e.preventDefault();
    if (!puedeAbrir) return;
    setErrorEnvio("");
    setEnviando(true);
    try {
      const sesion = await abrirCaja({
        Id_Empleado: usuario.Id_Empleado,
        Id_Caja: Number(idCaja),
        monto_inicial: fondo,
      });
      setSesionNueva(sesion);
    } catch (err) {
      setErrorEnvio(err.message);
    } finally {
      setEnviando(false);
    }
  };

  const encabezado = (
    <header className="apertura-header">
      <div>
        <h1>Apertura de caja</h1>
        <p>{formatoFechaHora(ahora)}</p>
      </div>
      <button type="button" className="btn-secundario" onClick={onCerrarSesion}>
        Cerrar sesión
      </button>
    </header>
  );

  if (cargando) {
    return (
      <div className="apertura-wrapper">
        <div className="apertura-contenedor">
          {encabezado}
          <p className="apertura-estado">Cargando información del turno…</p>
        </div>
      </div>
    );
  }

  if (errorCarga || !contexto) {
    return (
      <div className="apertura-wrapper">
        <div className="apertura-contenedor">
          {encabezado}
          <div className="apertura-alerta error" role="alert">
            No se pudo cargar la información: {errorCarga || "respuesta vacía"}. Verifica que el
            servidor esté encendido.
          </div>
        </div>
      </div>
    );
  }

  const { cajero, turno, permitido, motivo, sesion_abierta, cajas_disponibles } = contexto;

  // Pantalla de éxito
  if (sesionNueva) {
    return (
      <div className="apertura-wrapper">
        <div className="apertura-contenedor">
          {encabezado}
          <section className="apertura-card exito">
            <h2>✔ Caja abierta correctamente</h2>
            <dl className="apertura-datos">
              <div><dt>Caja</dt><dd>{sesionNueva.numero_caja}</dd></div>
              <div><dt>Cajero</dt><dd>{cajero.nombre_completo}</dd></div>
              <div><dt>Turno</dt><dd>{turno.tipo_turno}</dd></div>
              <div><dt>Fondo inicial</dt><dd>{formatoMoneda(sesionNueva.monto_inicial)}</dd></div>
              <div>
                <dt>Apertura</dt>
                <dd>{formatoFechaHora(new Date(sesionNueva.fecha_apertura))}</dd>
              </div>
            </dl>
            <button type="button" className="btn-primario" onClick={() => onCajaAbierta(sesionNueva)}>
              Continuar
            </button>
          </section>
        </div>
      </div>
    );
  }

  return (
    <div className="apertura-wrapper">
      <div className="apertura-contenedor">
        {encabezado}

        <div className="apertura-grid">
          <section className="apertura-card">
            <h2>Cajero</h2>
            <dl className="apertura-datos">
              <div><dt>Nombre</dt><dd>{cajero.nombre_completo}</dd></div>
              <div><dt>Código</dt><dd>{cajero.codigo_empleado}</dd></div>
              <div><dt>Rol</dt><dd>{cajero.rol}</dd></div>
              <div><dt>Sucursal</dt><dd>{cajero.sucursal.nombre}</dd></div>
            </dl>
          </section>

          <section className="apertura-card">
            <h2>Turno</h2>
            <dl className="apertura-datos">
              <div><dt>Turno</dt><dd>{turno.tipo_turno}</dd></div>
              <div>
                <dt>Horario</dt>
                <dd>{formatoHora(turno.hora_inicio)} – {formatoHora(turno.hora_finalizacion)}</dd>
              </div>
              {turno.descripcion && <div><dt>Descripción</dt><dd>{turno.descripcion}</dd></div>}
            </dl>
            <span className={`apertura-badge ${turno.dentro_de_horario ? "ok" : "aviso"}`}>
              {turno.dentro_de_horario ? "Dentro de tu horario" : "Fuera de tu horario"}
            </span>
          </section>
        </div>

        {!permitido && (
          <div className="apertura-alerta error" role="alert">
            {motivo} Roles autorizados: {contexto.roles_permitidos.join(", ")}.
          </div>
        )}

        {permitido && sesion_abierta && (
          <section className="apertura-card">
            <h2>Ya tienes una caja abierta</h2>
            <p>
              Caja <strong>{sesion_abierta.numero_caja}</strong>, abierta el{" "}
              {formatoFechaHora(new Date(sesion_abierta.fecha_apertura))} con un fondo de{" "}
              <strong>{formatoMoneda(sesion_abierta.monto_inicial)}</strong>.
            </p>
            <button type="button" className="btn-primario" onClick={() => onCajaAbierta(sesion_abierta)}>
              Continuar con mi caja
            </button>
          </section>
        )}

        {permitido && !sesion_abierta && (
          <form className="apertura-card" onSubmit={manejarSubmit} noValidate>
            <h2>Datos de apertura</h2>

            {!turno.dentro_de_horario && (
              <div className="apertura-alerta aviso">
                Estás abriendo caja fuera del horario de tu turno. Puedes continuar, pero verifica
                que sea correcto.
              </div>
            )}

            {cajas_disponibles.length === 0 ? (
              <div className="apertura-alerta aviso">
                No hay cajas disponibles en tu sucursal en este momento. Avisa a tu supervisor.
              </div>
            ) : (
              <>
                <div className="apertura-campo">
                  <label htmlFor="caja">Caja</label>
                  <select id="caja" value={idCaja} onChange={(e) => setIdCaja(e.target.value)}>
                    <option value="">Selecciona una caja…</option>
                    {cajas_disponibles.map((c) => (
                      <option key={c.Id_Caja} value={c.Id_Caja}>
                        {c.numero_caja}{c.descripcion ? ` — ${c.descripcion}` : ""}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="apertura-campo">
                  <label htmlFor="fondo">Fondo inicial (L.)</label>
                  <input
                    id="fondo"
                    type="number"
                    inputMode="decimal"
                    min="0"
                    step="0.01"
                    placeholder="0.00"
                    value={fondo}
                    onChange={(e) => setFondo(e.target.value)}
                  />
                  {fondo !== "" && !fondoValido && (
                    <small className="campo-error">
                      Ingresa un monto válido (0 o más, máximo 2 decimales).
                    </small>
                  )}
                  {fondoValido && (
                    <small className="campo-ayuda">Se registrará: {formatoMoneda(fondoNumero)}</small>
                  )}
                </div>

                <label className="apertura-check">
                  <input
                    type="checkbox"
                    checked={confirmado}
                    onChange={(e) => setConfirmado(e.target.checked)}
                  />
                  Confirmo que conté el efectivo y que el fondo inicial es correcto.
                </label>

                {errorEnvio && (
                  <div className="apertura-alerta error" role="alert">{errorEnvio}</div>
                )}

                <button type="submit" className="btn-primario" disabled={!puedeAbrir}>
                  {enviando ? "Abriendo…" : "Abrir caja"}
                </button>
              </>
            )}
          </form>
        )}
      </div>
    </div>
  );
}
