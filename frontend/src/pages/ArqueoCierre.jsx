import { useEffect, useState } from "react";
import { cerrarCaja, obtenerArqueo } from "../services/cajaService";
import "./style/AperturaCaja.css";
import "./style/ArqueoCierre.css";

const moneda = (v) =>
  new Intl.NumberFormat("es-HN", { style: "currency", currency: "HNL" }).format(Number(v) || 0);

const fechaHora = (f) =>
  new Intl.DateTimeFormat("es-HN", { dateStyle: "medium", timeStyle: "short" }).format(new Date(f));

export default function ArqueoCierre({ usuario, sesionCaja, onCajaCerrada, onVolver }) {
  const [arqueo, setArqueo] = useState(null);
  const [cargando, setCargando] = useState(true);
  const [errorCarga, setErrorCarga] = useState("");

  const [contado, setContado] = useState("");
  const [confirmado, setConfirmado] = useState(false);
  const [enviando, setEnviando] = useState(false);
  const [errorEnvio, setErrorEnvio] = useState("");
  const [cierre, setCierre] = useState(null); // resultado del cierre

  useEffect(() => {
    let cancelado = false;
    obtenerArqueo(sesionCaja.Id_Sesion)
      .then((d) => !cancelado && setArqueo(d))
      .catch((e) => !cancelado && setErrorCarga(e.message))
      .finally(() => !cancelado && setCargando(false));
    return () => {
      cancelado = true;
    };
  }, [sesionCaja.Id_Sesion]);

  const contadoValido = contado !== "" && /^\d+(\.\d{1,2})?$/.test(contado);
  const diferenciaPreview =
    arqueo && contadoValido ? Number(contado) - Number(arqueo.monto_esperado) : null;
  const puedeCerrar = contadoValido && confirmado && !enviando;

  const manejarCierre = async (e) => {
    e.preventDefault();
    if (!puedeCerrar) return;
    setErrorEnvio("");
    setEnviando(true);
    try {
      const r = await cerrarCaja(sesionCaja.Id_Sesion, {
        Id_Empleado: usuario.Id_Empleado,
        monto_contado: contado,
      });
      setCierre(r);
    } catch (err) {
      setErrorEnvio(err.message);
    } finally {
      setEnviando(false);
    }
  };

  const encabezado = (
    <header className="apertura-header">
      <div>
        <h1>Arqueo y cierre de caja</h1>
        <p>Caja {sesionCaja.numero_caja}</p>
      </div>
      {!cierre && (
        <button type="button" className="btn-secundario" onClick={onVolver}>
          ← Volver al panel
        </button>
      )}
    </header>
  );

  if (cargando) {
    return (
      <div className="apertura-wrapper">
        <div className="apertura-contenedor">
          {encabezado}
          <p className="apertura-estado">Calculando arqueo…</p>
        </div>
      </div>
    );
  }

  if (errorCarga || !arqueo) {
    return (
      <div className="apertura-wrapper">
        <div className="apertura-contenedor">
          {encabezado}
          <div className="apertura-alerta error" role="alert">
            No se pudo cargar el arqueo: {errorCarga || "respuesta vacía"}
          </div>
        </div>
      </div>
    );
  }

  // Pantalla final: caja cerrada
  if (cierre) {
    const dif = Number(cierre.diferencia);
    const estado = dif === 0 ? "cuadra" : dif < 0 ? "faltante" : "sobrante";
    return (
      <div className="apertura-wrapper">
        <div className="apertura-contenedor">
          {encabezado}
          <section className="apertura-card exito">
            <h2>✔ Caja cerrada</h2>
            <dl className="apertura-datos">
              <div><dt>Esperado en caja</dt><dd>{moneda(cierre.monto_esperado)}</dd></div>
              <div><dt>Efectivo contado</dt><dd>{moneda(cierre.monto_contado)}</dd></div>
              <div>
                <dt>Diferencia</dt>
                <dd className={`dif-${estado}`}>
                  {moneda(cierre.diferencia)}{" "}
                  {estado === "cuadra" ? "(cuadra)" : estado === "faltante" ? "(faltante)" : "(sobrante)"}
                </dd>
              </div>
              <div><dt>Cierre</dt><dd>{fechaHora(cierre.fecha_cierre)}</dd></div>
            </dl>
            <button type="button" className="btn-primario" onClick={onCajaCerrada}>
              Finalizar
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

        <section className="apertura-card">
          <h2>Ventas del turno por método de pago</h2>
          <p className="arqueo-sub">
            {arqueo.cajero} · desde {fechaHora(arqueo.fecha_apertura)}
          </p>
          {arqueo.ventas_por_metodo.length === 0 ? (
            <p>Aún no hay ventas registradas en este turno.</p>
          ) : (
            <table className="arqueo-tabla">
              <thead>
                <tr><th>Método</th><th>Pagos</th><th>Total</th></tr>
              </thead>
              <tbody>
                {arqueo.ventas_por_metodo.map((v) => (
                  <tr key={v.metodo}>
                    <td>{v.metodo}</td>
                    <td>{v.cantidad_pagos}</td>
                    <td>{moneda(v.total)}</td>
                  </tr>
                ))}
              </tbody>
              <tfoot>
                <tr><td colSpan="2">Total ventas</td><td>{moneda(arqueo.total_ventas)}</td></tr>
              </tfoot>
            </table>
          )}

          <dl className="apertura-datos">
            <div><dt>Fondo inicial</dt><dd>{moneda(arqueo.monto_inicial)}</dd></div>
            <div><dt>Ventas en efectivo</dt><dd>{moneda(arqueo.total_efectivo)}</dd></div>
            <div><dt>Ventas con tarjeta</dt><dd>{moneda(arqueo.total_tarjeta)}</dd></div>
            <div><dt>Efectivo esperado en caja</dt><dd><strong>{moneda(arqueo.monto_esperado)}</strong></dd></div>
          </dl>
        </section>

        <form className="apertura-card" onSubmit={manejarCierre} noValidate>
          <h2>Cierre de caja</h2>

          <div className="apertura-campo">
            <label htmlFor="contado">Efectivo contado (L.)</label>
            <input
              id="contado"
              type="number"
              min="0"
              step="0.01"
              placeholder="0.00"
              value={contado}
              onChange={(e) => setContado(e.target.value)}
            />
            {contado !== "" && !contadoValido && (
              <small className="campo-error">Ingresa un monto válido (máximo 2 decimales).</small>
            )}
            {diferenciaPreview !== null && (
              <small className={diferenciaPreview === 0 ? "campo-ayuda" : "campo-error"}>
                {diferenciaPreview === 0
                  ? "La caja cuadra."
                  : `Diferencia: ${moneda(diferenciaPreview)} (${diferenciaPreview < 0 ? "faltante" : "sobrante"})`}
              </small>
            )}
          </div>

          <label className="apertura-check">
            <input
              type="checkbox"
              checked={confirmado}
              onChange={(e) => setConfirmado(e.target.checked)}
            />
            Confirmo el monto contado y que deseo cerrar mi turno de caja.
          </label>

          {errorEnvio && <div className="apertura-alerta error" role="alert">{errorEnvio}</div>}

          <button type="submit" className="btn-primario" disabled={!puedeCerrar}>
            {enviando ? "Cerrando…" : "Cerrar caja"}
          </button>
        </form>
      </div>
    </div>
  );
}
