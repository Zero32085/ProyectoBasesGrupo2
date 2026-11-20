import { useState } from "react";
import { CATEGORIAS_MOCK, PRODUCTOS_MOCK } from "../services/mockProductos";
import ProductoCard from "../components/ProductoCard";
import CarritoSidebar from "../components/CarritoSidebar";
import "./TiendaClientes.css";

export default function TiendaCliente() {
  const [busqueda, setBusqueda] = useState("");
  const [categoriaActiva, setCategoriaActiva] = useState(0);
  const [carrito, setCarrito] = useState([]);

  const productosFiltrados = PRODUCTOS_MOCK.filter((prod) => {
    const coincideTexto =
      prod.nombre.toLowerCase().includes(busqueda.toLowerCase()) ||
      prod.cod_barra.includes(busqueda);
    const coincideCat =
      categoriaActiva === 0 || prod.id_categoria === categoriaActiva;
    return coincideTexto && coincideCat;
  });

  const agregarAlCarrito = (producto) => {
    setCarrito((prev) => {
      const existe = prev.find((item) => item.id_producto === producto.id_producto);
      if (existe) {
        return prev.map((item) =>
          item.id_producto === producto.id_producto
            ? { ...item, cantidad: item.cantidad + 1 }
            : item
        );
      }
      return [...prev, { ...producto, cantidad: 1 }];
    });
  };

  const cambiarCantidad = (idProducto, delta) => {
    setCarrito((prev) =>
      prev
        .map((item) =>
          item.id_producto === idProducto
            ? { ...item, cantidad: item.cantidad + delta }
            : item
        )
        .filter((item) => item.cantidad > 0)
    );
  };

  const eliminarDelCarrito = (idProducto) => {
    setCarrito((prev) => prev.filter((item) => item.id_producto !== idProducto));
  };

  return (
    <div className="tienda-layout">
      {/* Barra superior */}
      <header className="tienda-header">
        <div className="logo">🛍️ SuperMarket</div>
        <input
          type="text"
          className="buscador-input"
          placeholder="Buscar producto o código de barras..."
          value={busqueda}
          onChange={(e) => setBusqueda(e.target.value)}
        />
        <div className="rol-badge">Vista: Cliente</div>
      </header>

      {/* Contenedor principal responsivo */}
      <div className="tienda-contenido">
        <main className="catalogo-seccion">
          {/* Píldoras de Categorías */}
          <div className="categorias-bar">
            {CATEGORIAS_MOCK.map((cat) => (
              <button
                key={cat.id_categoria}
                className={`cat-pill ${categoriaActiva === cat.id_categoria ? "activa" : ""}`}
                onClick={() => setCategoriaActiva(cat.id_categoria)}
              >
                {cat.nombre}
              </button>
            ))}
          </div>

          {/* Grilla de Productos */}
          <div className="productos-grid">
            {productosFiltrados.map((prod) => (
              <ProductoCard
                key={prod.id_producto}
                producto={prod}
                onAgregar={agregarAlCarrito}
              />
            ))}
          </div>
        </main>

        {/* Carrito */}
        <CarritoSidebar
          carrito={carrito}
          onCambiarCantidad={cambiarCantidad}
          onEliminar={eliminarDelCarrito}
          onVaciar={() => setCarrito([])}
        />
      </div>
    </div>
  );
}