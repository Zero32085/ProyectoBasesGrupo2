import { useState } from "react";

export default function CarritoSidebar({
  carrito,
  onCambiarCantidad,
  onEliminar,
  onVaciar,
}) {
  const [esDomicilio, setEsDomicilio] = useState(false);
  const [direccion, setDireccion] = useState("");
  const TARIFA_ENVIO = 50.00;

  // Cálculos fiscales idénticos a tu tabla Facturas
  const subtotalExento = carrito
    .filter((item) => item.porcentaje_isv === 0)
    .reduce((acc, item) => acc + item.precio * item.cantidad, 0);

  const subtotalGravado15 = carrito
    .filter((item) => item.porcentaje_isv === 15)
    .reduce((acc, item) => acc + item.precio * item.cantidad, 0);

  const isv15 = subtotalGravado15 * 0.15;
  const costoEnvio = esDomicilio && carrito.length > 0 ? TARIFA_ENVIO : 0;
  const totalPagar = subtotalExento + subtotalGravado15 + isv15 + costoEnvio;

  const handleConfirmarPedido = (e) => {
    e.preventDefault();
    if (carrito.length === 0) return;

    // Aquí luego harás el POST a FastAPI (/facturas y /pedidos-domicilio)
    const payloadSimulado = {
      subtotal_exento: subtotalExento,
      subtotal_gravado_15: subtotalGravado15,
      isv_15: isv15,
      total_pagar: totalPagar,
      entrega_domicilio: esDomicilio ? { direccion, tarifa: TARIFA_ENVIO } : null,
      detalles: carrito.map((i) => ({
        id_producto: i.id_producto,
        cantidad: i.cantidad,
        precio_unitario: i.precio,
      })),
    };

    console.log("Payload listo para FastAPI:", payloadSimulado);
    alert(`¡Pedido confirmado por L. ${totalPagar.toFixed(2)}! Revisa la consola (F12) para ver el JSON.`);
    onVaciar();
  };

  return (
    <aside className="carrito-panel">
      <h2>🛒 Tu Carrito ({carrito.reduce((acc, i) => acc + i.cantidad, 0)})</h2>

      {carrito.length === 0 ? (
        <p className="carrito-vacio">Aún no has agregado productos.</p>
      ) : (
        <>
          <ul className="carrito-lista">
            {carrito.map((item) => (
              <li key={item.id_producto} className="carrito-item">
                <div className="item-datos">
                  <strong>{item.nombre}</strong>
                  <span>L. {(item.precio * item.cantidad).toFixed(2)}</span>
                </div>
                <div className="item-controles">
                  <button onClick={() => onCambiarCantidad(item.id_producto, -1)}>-</button>
                  <span>{item.cantidad}</span>
                  <button onClick={() => onCambiarCantidad(item.id_producto, 1)}>+</button>
                  <button className="btn-del" onClick={() => onEliminar(item.id_producto)}>
                    ✕
                  </button>
                </div>
              </li>
            ))}
          </ul>

          {/* Opción Pedido a Domicilio */}
          <div className="domicilio-box">
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={esDomicilio}
                onChange={(e) => setEsDomicilio(e.target.checked)}
              />
              Envío a domicilio (+ L. {TARIFA_ENVIO.toFixed(2)})
            </label>
            {esDomicilio && (
              <input
                type="text"
                className="input-direccion"
                placeholder="Colonia, calle y referencia..."
                value={direccion}
                onChange={(e) => setDireccion(e.target.value)}
                required
              />
            )}
          </div>

          {/* Desglose Fiscal */}
          <div className="resumen-totales">
            <div>
              <span>Subtotal Exento:</span>
              <span>L. {subtotalExento.toFixed(2)}</span>
            </div>
            <div>
              <span>Subtotal Gravado 15%:</span>
              <span>L. {subtotalGravado15.toFixed(2)}</span>
            </div>
            <div>
              <span>ISV (15%):</span>
              <span>L. {isv15.toFixed(2)}</span>
            </div>
            {esDomicilio && (
              <div>
                <span>Tarifa Envío:</span>
                <span>L. {costoEnvio.toFixed(2)}</span>
              </div>
            )}
            <div className="total-final">
              <strong>Total a Pagar:</strong>
              <strong>L. {totalPagar.toFixed(2)}</strong>
            </div>
          </div>

          <button className="btn-checkout" onClick={handleConfirmarPedido}>
            Confirmar Compra
          </button>
        </>
      )}
    </aside>
  );
}