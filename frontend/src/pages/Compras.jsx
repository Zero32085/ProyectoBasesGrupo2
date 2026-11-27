import { useEffect, useMemo, useState } from "react";
import "../pages/Compras.css";

const API_URL = "http://127.0.0.1:8000";
const TASA_ISV = 0.15;

// Extrae un arreglo de forma segura sin importar si el API devuelve [...] o { data/items: [...] }
function normalizarLista(data) {
  if (Array.isArray(data)) return data;
  if (Array.isArray(data?.items)) return data.items;
  if (Array.isArray(data?.data)) return data.data;
  return [];
}

// Intenta consultar una o más rutas y devuelve la lista si responde OK
async function fetchCatalogo(rutas) {
  for (const ruta of rutas) {
    try {
      const res = await fetch(`${API_URL}${ruta}`);
      if (res.ok) {
        const data = await res.json();
        return normalizarLista(data);
      }
    } catch (err) {
      console.error(`Error consultando ${ruta}:`, err);
    }
  }
  return [];
}

export default function Compras() {
  // Estado para listar compras en la tabla
  const [compras, setCompras] = useState([]);
  const [cargando, setCargando] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");
  const [mensajeOk, setMensajeOk] = useState("");
  const [guardando, setGuardando] = useState(false);

  // Control del modal de nueva compra
  const [modalAbierto, setModalAbierto] = useState(false);
  const [errorModal, setErrorModal] = useState("");

  // Catálogos para selects dentro del modal
  const [proveedores, setProveedores] = useState([]);
  const [sucursales, setSucursales] = useState([]);
  const [productos, setProductos] = useState([]);

  // Card 1: Datos de Compras
  const [idProveedor, setIdProveedor] = useState("");
  const [idSucursal, setIdSucursal] = useState("");
  const [numeroFactura, setNumeroFactura] = useState("");
  const [estado, setEstado] = useState(1);

  // Card 2: Datos de Detalle Compra + Lote
  const [idProducto, setIdProducto] = useState("");
  const [cantidad, setCantidad] = useState("");
  const [precioUnitario, setPrecioUnitario] = useState("");
  const [descuento, setDescuento] = useState("0");
  const [loteCodigo, setLoteCodigo] = useState("");
  const [fechaFabricacion, setFechaFabricacion] = useState("");
  const [fechaVencimiento, setFechaVencimiento] = useState("");

  // Card 3: Lista temporal de detalles agregados
  const [detalles, setDetalles] = useState([]);

  // Modo de consulta cuando se abre desde "Ver detalle"
    const [modoSoloLectura, setModoSoloLectura] = useState(false);
    const [compraConsultadaId, setCompraConsultadaId] = useState(null);

  // Carga inicial de compras desde el backend
  useEffect(() => {
    let activo = true;

    async function fetchCompras() {
      setCargando(true);
      setErrorMsg("");
      try {
        const res = await fetch(`${API_URL}/compras`);
        if (!res.ok) {
          throw new Error(`Error ${res.status} al cargar las compras`);
        }
        const data = await res.json();
        if (activo) {
          setCompras(normalizarLista(data));
        }
      } catch (err) {
        if (activo) {
          console.error(err);
          setErrorMsg(err.message || "No se pudo conectar con el servidor");
        }
      } finally {
        if (activo) {
          setCargando(false);
        }
      }
    }

    fetchCompras();

    return () => {
      activo = false;
    };
  }, []);

  // Carga proveedores, sucursales y productos al abrir el modal
  async function cargarCatalogos() {
    const [dataProv, dataSuc, dataProd] = await Promise.all([
      fetchCatalogo(["/proveedores", "/proveedor"]),
      fetchCatalogo(["/sucursales", "/sucursal"]),
      fetchCatalogo(["/productos", "/producto"]),
    ]);

    setProveedores(dataProv);
    setSucursales(dataSuc);
    setProductos(dataProd);
  }

    function limpiarModal() {
    setIdProveedor("");
    setIdSucursal("");
    setNumeroFactura("");
    setEstado(1);
    setIdProducto("");
    setCantidad("");
    setPrecioUnitario("");
    setDescuento("0");
    setLoteCodigo("");
    setFechaFabricacion("");
    setFechaVencimiento("");
    setDetalles([]);
    setErrorModal("");
    setModoSoloLectura(false);
    setCompraConsultadaId(null);
    }

    // Abre el modal en modo registro nuevo
    function handleClickAgregarCompra() {
    limpiarModal();
    setMensajeOk("");
    cargarCatalogos();
    setModalAbierto(true);
    }

    // Consulta el detalle de una compra y carga los datos en los cards del modal
async function handleVerDetalleCompra(compra) {
  const idCompra = compra.Id_Compra ?? compra.id_compra;
  if (!idCompra) return;

  limpiarModal();
  setMensajeOk("");
  setModoSoloLectura(true);
  setCompraConsultadaId(idCompra);
  await cargarCatalogos();

  try {
    const res = await fetch(`${API_URL}/compras/${idCompra}/detalle`);
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail || `Error ${res.status} al cargar el detalle`);
    }

    // Card 1: datos de cabecera de la compra
    setIdProveedor(String(data.Id_Proveedor ?? ""));
    setIdSucursal(String(data.Id_Sucursal ?? ""));
    setNumeroFactura(data.numero_factura ?? "");
    setEstado(Number(data.estado ?? 1));

    // Card 3: filas de detalle + lote cargadas desde el backend
    const filasCargadas = (data.detalles || []).map((item, idx) => ({
      tempId: item.Id_Detalle_Compras ?? `${idCompra}-${idx}`,
      Id_Producto: item.Id_Producto,
      nombre_producto: item.nombre_producto ?? `Producto #${item.Id_Producto}`,
      cantidad: Number(item.cantidad ?? 0),
      precio_unitario: Number(item.precio_unitario ?? 0),
      descuento: Number(item.descuento ?? 0),
      subtotal_linea: Number(item.subtotal_linea ?? 0),
      lote_codigo: item.lote_codigo ?? "—",
      fecha_fabricacion: item.fecha_fabricacion ?? null,
      fecha_vencimiento: item.fecha_vencimiento ?? "—",
    }));

    setDetalles(filasCargadas);
    setModalAbierto(true);
  } catch (err) {
    console.error(err);
    setErrorMsg(err.message || "No se pudo cargar el detalle de la compra");
  }
}

  function handleCerrarModal() {
    limpiarModal();
    setModalAbierto(false);
  }

  // Agrega una línea de detalle + lote a la tabla temporal (Card 3)
  function handleAgregarDetalle(e) {
    e.preventDefault();
    setErrorModal("");

    const prod = productos.find(
      (p) => String(p.Id_Producto ?? p.id_producto) === String(idProducto)
    );
    const cantNum = parseFloat(cantidad);
    const precioNum = parseFloat(precioUnitario);
    const descNum = parseFloat(descuento) || 0;

    if (!prod) {
      setErrorModal("Selecciona un producto.");
      return;
    }
    if (isNaN(cantNum) || cantNum <= 0) {
      setErrorModal("La cantidad debe ser mayor a 0.");
      return;
    }
    if (isNaN(precioNum) || precioNum < 0) {
      setErrorModal("Ingresa un precio unitario válido.");
      return;
    }
    if (descNum < 0 || descNum > cantNum * precioNum) {
      setErrorModal("El descuento no es válido.");
      return;
    }
    if (!loteCodigo.trim()) {
      setErrorModal("Ingresa el código de lote.");
      return;
    }
    if (!fechaVencimiento) {
      setErrorModal("Ingresa la fecha de vencimiento.");
      return;
    }
    if (fechaFabricacion && fechaVencimiento < fechaFabricacion) {
      setErrorModal("La fecha de vencimiento no puede ser menor a la de fabricación.");
      return;
    }

    const subtotalLinea = Number((cantNum * precioNum - descNum).toFixed(2));

    const nuevoDetalle = {
      tempId: `${Date.now()}-${Math.random().toString(36).slice(2, 7)}`,
      Id_Producto: Number(idProducto),
      nombre_producto:
        prod.nombre ?? prod.nombre_producto ?? `Producto #${idProducto}`,
      cantidad: cantNum,
      precio_unitario: precioNum,
      descuento: descNum,
      subtotal_linea: subtotalLinea,
      lote_codigo: loteCodigo.trim(),
      fecha_fabricacion: fechaFabricacion || null,
      fecha_vencimiento: fechaVencimiento,
    };

    setDetalles((prev) => [...prev, nuevoDetalle]);

    // Limpia campos de detalle/lote para seguir agregando
    setIdProducto("");
    setCantidad("");
    setPrecioUnitario("");
    setDescuento("0");
    setLoteCodigo("");
    setFechaFabricacion("");
    setFechaVencimiento("");
  }

  // Elimina un detalle de la tabla temporal antes de guardar
  function handleEliminarDetalle(tempId) {
    setDetalles((prev) => prev.filter((item) => item.tempId !== tempId));
  }

  // Totales calculados a partir de los detalles agregados
  const totales = useMemo(() => {
    const subtotal = detalles.reduce((acc, item) => acc + item.subtotal_linea, 0);
    const impuesto = Number((subtotal * TASA_ISV).toFixed(2));
    const total = Number((subtotal + impuesto).toFixed(2));
    return {
      subtotal: Number(subtotal.toFixed(2)),
      impuesto,
      total,
    };
  }, [detalles]);

  // Recarga la tabla principal de compras
  async function recargarCompras() {
    setCargando(true);
    setErrorMsg("");
    try {
      const res = await fetch(`${API_URL}/compras`);
      if (!res.ok) {
        throw new Error(`Error ${res.status} al cargar las compras`);
      }
      const data = await res.json();
      setCompras(normalizarLista(data));
    } catch (err) {
      console.error(err);
      setErrorMsg(err.message || "No se pudo conectar con el servidor");
    } finally {
      setCargando(false);
    }
  }

  // Envía la compra completa (cabecera + detalles/lotes) al backend
  async function handleConfirmarCompra() {
    setErrorModal("");

    if (!idProveedor) {
      setErrorModal("Selecciona un proveedor en el Card 1.");
      return;
    }
    if (!idSucursal) {
      setErrorModal("Selecciona una sucursal en el Card 1.");
      return;
    }
    if (!numeroFactura.trim()) {
      setErrorModal("Ingresa el número de factura en el Card 1.");
      return;
    }
    if (detalles.length === 0) {
      setErrorModal("Agrega al menos un producto en el detalle antes de guardar.");
      return;
    }

    const payload = {
      Id_Proveedor: Number(idProveedor),
      Id_Sucursal: Number(idSucursal),
      numero_factura: numeroFactura.trim(),
      estado: Number(estado),
      detalles: detalles.map((d) => ({
        Id_Producto: d.Id_Producto,
        cantidad: d.cantidad,
        precio_unitario: d.precio_unitario,
        descuento: d.descuento,
        lote_codigo: d.lote_codigo,
        fecha_fabricacion: d.fecha_fabricacion,
        fecha_vencimiento: d.fecha_vencimiento,
      })),
    };

    setGuardando(true);
    try {
      const res = await fetch(`${API_URL}/compras`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || `Error ${res.status} al guardar la compra`);
      }

      setMensajeOk("Compra registrada, lote creado e inventario actualizado.");
      setModalAbierto(false);
      limpiarModal();
      await recargarCompras();
    } catch (err) {
      console.error(err);
      setErrorModal(err.message || "No se pudo guardar la compra");
    } finally {
      setGuardando(false);
    }
  }

  return (
    <div className="compras-wrapper">
      <div className="compras-stack">
        {/* Card 1: Título y botón para agregar compra */}
        <div className="compras-card">
          <div className="compras-header-acciones">
            <div className="compras-header">
              <h1>Compras</h1>
              <p>Consulta las compras registradas o inicia una nueva compra</p>
            </div>
            <button
              type="button"
              className="btn-agregar-compra"
              onClick={handleClickAgregarCompra}
            >
              + Agregar Compra
            </button>
          </div>
          {mensajeOk && (
            <div className="msg-modal-ok" style={{ marginTop: "1rem" }}>
              {mensajeOk}
            </div>
          )}
        </div>

        {/* Card 2: Tabla con todas las compras */}
        <div className="compras-card">
          <div className="compras-header" style={{ marginBottom: "1rem" }}>
            <h2>Compras Registradas</h2>
            <p>Listado de compras en el sistema</p>
          </div>

          <div className="tabla-compras-responsive">
            <table className="tabla-compras">
              <thead>
                <tr>
                  <th>N° Factura</th>
                  <th>Proveedor</th>
                  <th>Sucursal</th>
                  <th>Fecha Compra</th>
                  <th>Subtotal</th>
                  <th>Impuesto</th>
                  <th>Total</th>
                  <th>Estado</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {cargando ? (
                  <tr>
                    <td colSpan="8" className="tabla-compras-vacia">
                      Cargando compras...
                    </td>
                  </tr>
                ) : errorMsg ? (
                  <tr>
                    <td colSpan="8" className="tabla-compras-vacia">
                      {errorMsg}
                    </td>
                  </tr>
                ) : compras.length === 0 ? (
                  <tr>
                    <td colSpan="8" className="tabla-compras-vacia">
                      No hay compras registradas aún.
                    </td>
                  </tr>
                ) : (
                  compras.map((compra, idx) => (
                    <tr key={compra.Id_Compra ?? idx}>
                      <td>{compra.numero_factura}</td>
                      <td>
                        {compra.proveedor?.nombre_o_razonSocial ??
                          `Proveedor #${compra.Id_Proveedor}`}
                      </td>
                      <td>
                        {compra.sucursal?.nombre_sucursal ??
                          `Sucursal #${compra.Id_Sucursal}`}
                      </td>
                      <td>
                        {compra.fecha_compra
                          ? new Date(compra.fecha_compra).toLocaleString()
                          : "—"}
                      </td>
                      <td>{Number(compra.subtotal ?? 0).toFixed(2)}</td>
                      <td>{Number(compra.impuesto ?? 0).toFixed(2)}</td>
                      <td>
                        <strong>{Number(compra.total ?? 0).toFixed(2)}</strong>
                      </td>
                      <td>
                        <span
                          className={`badge-estado-compra ${
                            compra.estado === 1 ? "activa" : "inactiva"
                          }`}
                        >
                          {compra.estado === 1 ? "Activo" : "Inactivo"}
                        </span>
                      </td>
                      <td>
                        <button
                            type="button"
                            className="btn-ver-detalle"
                            onClick={() => handleVerDetalleCompra(compra)}
                        >
                            Ver detalle
                        </button>
                        </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Modal con los 3 cards para registrar una nueva compra */}
      {modalAbierto && (
        <div className="modal-compra-overlay" onClick={handleCerrarModal}>
          <div
            className="modal-compra-contenido"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Encabezado del modal */}
            <div className="modal-compra-topbar">
              <h2>Registrar Nueva Compra</h2>
              <button
                type="button"
                className="btn-cerrar-modal"
                onClick={handleCerrarModal}
              >
                Cerrar
              </button>
            </div>

            {/* Card 1: Datos de la tabla Compras */}
            <section className="card-modal-compra">
              <h3 className="card-modal-titulo">1. Datos de Compra</h3>
              <div className="grid-modal-compra">
                <div className="campo-modal-compra">
                  <label htmlFor="modal-proveedor">* Proveedor</label>
                  <select
                    id="modal-proveedor"
                    value={idProveedor}
                    onChange={(e) => setIdProveedor(e.target.value)}
                    disabled={modoSoloLectura}
                  >
                    <option value="">Seleccione un proveedor</option>
                    {proveedores.map((prov, idx) => {
                      const id = prov.Id_Proveedor ?? prov.id_proveedor ?? idx;
                      return (
                        <option key={id} value={id}>
                          {prov.nombre_o_razonSocial} ({prov.rtn})
                        </option>
                      );
                    })}
                  </select>
                </div>

                <div className="campo-modal-compra">
                  <label htmlFor="modal-sucursal">* Sucursal</label>
                  <select
                    id="modal-sucursal"
                    value={idSucursal}
                    onChange={(e) => setIdSucursal(e.target.value)}
                    disabled={modoSoloLectura}
                  >
                    <option value="">Seleccione una sucursal</option>
                    {sucursales.map((suc, idx) => {
                      const id = suc.Id_Sucursal ?? suc.id_sucursal ?? idx;
                      const nombreSuc =
                        suc.nombre_sucursal ?? suc.nombre ?? `Sucursal #${id}`;
                      return (
                        <option key={id} value={id}>
                          {nombreSuc}
                        </option>
                      );
                    })}
                  </select>
                </div>

                <div className="campo-modal-compra">
                  <label htmlFor="modal-factura">* Número de Factura</label>
                  <input
                    id="modal-factura"
                    type="text"
                    value={numeroFactura}
                    onChange={(e) => setNumeroFactura(e.target.value)}
                    placeholder="Ej: 000-001-01-00001234"
                  />
                </div>

                <div className="campo-modal-compra">
                  <label htmlFor="modal-estado">Estado</label>
                  <select
                    id="modal-estado"
                    value={estado}
                    onChange={(e) => setEstado(Number(e.target.value))}
                    disabled={modoSoloLectura}
                  >
                    <option value={1}>Activo</option>
                    <option value={0}>Inactivo</option>
                  </select>
                </div>
              </div>
            </section>

            {/* Card 2: Datos de Detalle Compra + Lote de Vencimiento */}
            <section className="card-modal-compra">
              <h3 className="card-modal-titulo">2. Detalle Compra y Lote</h3>
              <form onSubmit={handleAgregarDetalle} className="grid-modal-compra">
                <div className="campo-modal-compra">
                  <label htmlFor="modal-producto">* Producto</label>
                  <select
                    id="modal-producto"
                    value={idProducto}
                    onChange={(e) => setIdProducto(e.target.value)}
                    disabled={modoSoloLectura}
                  >
                    <option value="">Seleccione un producto</option>
                    {productos.map((prod, idx) => {
                      const id = prod.Id_Producto ?? prod.id_producto ?? idx;
                      const nombreProd =
                        prod.nombre ?? prod.nombre_producto ?? `Producto #${id}`;
                      return (
                        <option key={id} value={id}>
                          {nombreProd}
                        </option>
                      );
                    })}
                  </select>
                </div>

                <div className="campo-modal-compra">
                  <label htmlFor="modal-cantidad">* Cantidad</label>
                  <input
                    id="modal-cantidad"
                    type="number"
                    step="0.01"
                    min="0.01"
                    value={cantidad}
                    onChange={(e) => setCantidad(e.target.value)}
                    disabled={modoSoloLectura}
                    placeholder="0.00"
                  />
                </div>

                <div className="campo-modal-compra">
                  <label htmlFor="modal-precio">* Precio Unitario</label>
                  <input
                    id="modal-precio"
                    type="number"
                    step="0.01"
                    min="0"
                    value={precioUnitario}
                    onChange={(e) => setPrecioUnitario(e.target.value)}
                    disabled={modoSoloLectura}
                    placeholder="0.00"
                  />
                </div>

                <div className="campo-modal-compra">
                  <label htmlFor="modal-descuento">Descuento</label>
                  <input
                    id="modal-descuento"
                    type="number"
                    step="0.01"
                    min="0"
                    value={descuento}
                    onChange={(e) => setDescuento(e.target.value)}
                    disabled={modoSoloLectura}
                    placeholder="0.00"
                  />
                </div>

                <div className="campo-modal-compra">
                  <label htmlFor="modal-lote">* Código de Lote</label>
                  <input
                    id="modal-lote"
                    type="text"
                    value={loteCodigo}
                    onChange={(e) => setLoteCodigo(e.target.value)}
                    disabled={modoSoloLectura}
                    placeholder="Ej: LOTE-2026-01"
                  />
                </div>

                <div className="campo-modal-compra">
                  <label htmlFor="modal-fabricacion">Fecha Fabricación</label>
                  <input
                    id="modal-fabricacion"
                    type="date"
                    value={fechaFabricacion}
                    onChange={(e) => setFechaFabricacion(e.target.value)}
                    disabled={modoSoloLectura}
                  />
                </div>

                <div className="campo-modal-compra">
                  <label htmlFor="modal-vencimiento">* Fecha Vencimiento</label>
                  <input
                    id="modal-vencimiento"
                    type="date"
                    value={fechaVencimiento}
                    onChange={(e) => setFechaVencimiento(e.target.value)}
                    disabled={modoSoloLectura}
                  />
                </div>

                <div
                  className="campo-modal-compra"
                  style={{ justifyContent: "flex-end" }}
                >
                  <button type="submit" className="btn-agregar-compra">
                    + Agregar Detalle
                  </button>
                </div>
              </form>
            </section>

            {/* Card 3: Tabla de detalles agregados hasta el momento */}
            <section className="card-modal-compra">
              <h3 className="card-modal-titulo">3. Detalles Agregados</h3>

              <div className="tabla-compras-responsive">
                <table className="tabla-compras">
                  <thead>
                    <tr>
                      <th>Producto</th>
                      <th>Lote</th>
                      <th>Fabricación</th>
                      <th>Vencimiento</th>
                      <th>Cantidad</th>
                      <th>P. Unitario</th>
                      <th>Descuento</th>
                      <th>Subtotal</th>
                      <th>Acción</th>
                    </tr>
                  </thead>
                  <tbody>
                    {detalles.length === 0 ? (
                      <tr>
                        <td colSpan="9" className="tabla-compras-vacia">
                          No hay productos agregados al detalle todavía.
                        </td>
                      </tr>
                    ) : (
                      detalles.map((item) => (
                        <tr key={item.tempId}>
                          <td>{item.nombre_producto}</td>
                          <td>{item.lote_codigo}</td>
                          <td>{item.fecha_fabricacion || "—"}</td>
                          <td>{item.fecha_vencimiento}</td>
                          <td>{item.cantidad}</td>
                          <td>{item.precio_unitario.toFixed(2)}</td>
                          <td>{item.descuento.toFixed(2)}</td>
                          <td>
                            <strong>{item.subtotal_linea.toFixed(2)}</strong>
                          </td>
                          <td>
                            <button
                              type="button"
                              className="btn-eliminar-detalle"
                              onClick={() => handleEliminarDetalle(item.tempId)}
                              disabled={modoSoloLectura}
                            >
                              Eliminar
                            </button>
                          </td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>

              <div className="resumen-modal-compra">
                <div className="resumen-modal-fila">
                  <span>Subtotal:</span>
                  <span>{totales.subtotal.toFixed(2)}</span>
                </div>
                <div className="resumen-modal-fila">
                  <span>Impuesto ({Math.round(TASA_ISV * 100)}%):</span>
                  <span>{totales.impuesto.toFixed(2)}</span>
                </div>
                <div className="resumen-modal-fila total">
                  <span>Total:</span>
                  <span>{totales.total.toFixed(2)}</span>
                </div>
              </div>

              {errorModal && <div className="msg-modal-error">{errorModal}</div>}

              <div className="acciones-modal-footer">
                <button
                  type="button"
                  className="btn-secundario-modal"
                  onClick={handleCerrarModal}
                >
                  Cancelar
                </button>
                <button
                  type="button"
                  className="btn-agregar-compra"
                  onClick={handleConfirmarCompra}
                  disabled={modoSoloLectura}
                >
                  Guardar Compra
                </button>
              </div>
            </section>
          </div>
        </div>
      )}
    </div>
  );
}