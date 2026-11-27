const API_URL = "http://127.0.0.1:8000";

async function manejarRespuesta(res) {
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    // FastAPI devuelve detail como texto o como lista cuando falla la validación
    const detalle = Array.isArray(data.detail)
      ? "Revisa los datos ingresados (el fondo inicial debe ser un monto válido)"
      : data.detail;
    throw new Error(detalle || "Ocurrió un error en la solicitud");
  }
  return data;
}

// Cajero, turno, permisos y cajas disponibles para la pantalla de apertura
export async function obtenerContextoApertura(idEmpleado) {
  const res = await fetch(`${API_URL}/caja/apertura/contexto/${idEmpleado}`);
  return manejarRespuesta(res);
}

export async function abrirCaja({ Id_Empleado, Id_Caja, monto_inicial }) {
  const res = await fetch(`${API_URL}/caja/abrir`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ Id_Empleado, Id_Caja, monto_inicial }),
  });
  return manejarRespuesta(res);
}

// Resumen de ventas del turno (no cierra la caja)
export async function obtenerArqueo(idSesion) {
  const res = await fetch(`${API_URL}/caja/arqueo/${idSesion}`);
  return manejarRespuesta(res);
}

// Cierra el turno con el efectivo contado
export async function cerrarCaja(idSesion, { Id_Empleado, monto_contado }) {
  const res = await fetch(`${API_URL}/caja/cerrar/${idSesion}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ Id_Empleado, monto_contado }),
  });
  return manejarRespuesta(res);
}
