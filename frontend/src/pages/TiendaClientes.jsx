import { useState } from "react";
import { CATEGORIAS_MOCK, PRODUCTOS_MOCK } from "../services/mockProductos";
import ProductoCard from "../components/ProductoCard";
import CarritoSidebar from "../components/CarritoSidebar";
import NavBar from "../components/NavBar";
import "./TiendaClientes.css";

export default function TiendaCliente({ usuarioActivo, onAbrirLogin, onCerrarSesion }) {
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

      <NavBar
        busqueda={busqueda}
        setBusqueda={setBusqueda}
        usuarioActivo={usuarioActivo}
        onAbrirLogin={onAbrirLogin}
        onCerrarSesion={onCerrarSesion}
      />

      <div className="tienda-contenido">
        <main className="catalogo-seccion">
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