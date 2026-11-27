export default function PanelEmpleado({
  usuario,
  sesionCaja,
  onAperturarCaja,
  onArqueoCierre,
  onCerrarSesion,
}) {
  return (
    <div style={{ padding: "2rem", minHeight: "100vh", backgroundColor: "#0f172a", color: "#f8fafc" }}>
      <h1>Panel de Empleado</h1>
      <h3>Bienvenido, {usuario.primer_nombre ?? usuario.codigo_empleado}</h3>
      <p>Código de empleado: {usuario.codigo_empleado}</p>
      <hr />

      {!sesionCaja ? (
        <div>
          <h2>Estado de caja</h2>
          <p>No tienes ninguna caja abierta.</p>
          <button type="button" onClick={onAperturarCaja}>Aperturar Caja</button>
        </div>
      ) : (
        <div>
          <h2>Caja abierta</h2>
          <p>Número de caja: {sesionCaja.numero_caja}</p>
          <p>Ya tienes una sesión de caja activa.</p>
          <button type="button" onClick={onArqueoCierre}>Arqueo y cierre de caja</button>
        </div>
      )}

      <div style={{ marginTop: "1rem" }}>
        <button type="button" onClick={onCerrarSesion}>Cerrar sesión</button>
      </div>
    </div>
  );
}
