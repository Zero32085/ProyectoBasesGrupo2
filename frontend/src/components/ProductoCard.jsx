export default function ProductoCard({ producto, onAgregar }) {
  return (
    <div className="producto-card">
      <div className="producto-img">{producto.imagen}</div>
      <div className="producto-info">
        <span className="producto-codigo">Cód: {producto.cod_barra}</span>
        <h3>{producto.nombre}</h3>
        <p className="producto-desc">{producto.descripcion}</p>
        <div className="producto-footer">
          <div>
            <span className="producto-precio">L. {producto.precio.toFixed(2)}</span>
            {producto.porcentaje_isv > 0 && (
              <span className="badge-isv">+{producto.porcentaje_isv}% ISV</span>
            )}
          </div>
          <button
            className="btn-agregar"
            onClick={() => onAgregar(producto)}
            disabled={producto.stock_actual != null && Number(producto.stock_actual) <= 0}
          >
            + Agregar
          </button>
        </div>
      </div>
    </div>
  );
}