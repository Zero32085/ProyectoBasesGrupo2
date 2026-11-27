import { useEffect, useState } from "react";
import { getProductos } from "../services/productosService";
import { getCategorias } from "../services/categoriasService";
import { getInventarios } from "../services/inventarioService";
import ProductoCard from "../components/ProductoCard";
import CarritoSidebar from "../components/CarritoSidebar";
import NavBar from "../components/NavBar";
import SelectorCategorias from "../components/SelectorCategorias";
import "./styles/TiendaClientes.css";
import { guardarDireccionCliente } from "../services/direccionesService";

export default function TiendaCliente({ usuarioActivo, onAbrirLogin, onCerrarSesion }) {
  const [productos, setProductos] = useState([]);
  const [categorias, setCategorias] = useState([
    { id_categoria: 0, nombre: "Todas" },
  ]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState(null);

  const [busqueda, setBusqueda] = useState("");
  const [categoriaActiva, setCategoriaActiva] = useState(0);
  const [carrito, setCarrito] = useState([]);

  useEffect(() => {
    const cargarCatalogo = async () => {
      try {
        setCargando(true);
        setError(null);

        const [dataProductos, dataCategorias, dataInventarios] = await Promise.all([
          getProductos(),
          getCategorias(),
          getInventarios(),
        ]);

        const stockPorProducto = new Map();
        for (const inv of Array.isArray(dataInventarios) ? dataInventarios : []) {
          const idProd = inv.Id_Producto ?? inv.id_producto;
          const stock = Number(inv.stock_actual ?? 0);
          if (idProd != null) {
            stockPorProducto.set(idProd, (stockPorProducto.get(idProd) ?? 0) + stock);
          }
        }

        const productosAdaptados = (Array.isArray(dataProductos) ? dataProductos : [])
          .filter((prod) => prod.estado !== false && prod.estado !== 0)
          .map((prod) => {
            const idProd = prod.Id_Producto ?? prod.id_producto;
            return {
              id_producto: idProd,
              id_categoria: prod.Id_Categoria ?? prod.id_categoria,
              cod_barra: prod.cod_barra ?? "",
              nombre: prod.nombre ?? "",
              descripcion: prod.descripcion ?? "",
              precio: Number(prod.precio ?? 0),
              porcentaje_isv: Number(prod.porcentaje_isv ?? 0),
              stock_actual: stockPorProducto.has(idProd)
                ? stockPorProducto.get(idProd)
                : 0,
              imagen: prod.imagen || "🛒",
            };
          });

        const categoriasAdaptadas = (Array.isArray(dataCategorias) ? dataCategorias : [])
          .filter((cat) => cat.estado !== false && cat.estado !== 0)
          .map((cat) => ({
            id_categoria: cat.Id_Categoria ?? cat.id_categoria,
            nombre: cat.nombre,
          }));

        setProductos(productosAdaptados);
        setCategorias([
          { id_categoria: 0, nombre: "Todas" },
          ...categoriasAdaptadas,
        ]);
      } catch (err) {
        setError(err.message || "No se pudieron cargar los datos de la tienda");
      } finally {
        setCargando(false);
      }
    };

    cargarCatalogo();
  }, []);

  const productosFiltrados = productos.filter((prod) => {
    const coincideTexto =
      prod.nombre.toLowerCase().includes(busqueda.toLowerCase()) ||
      String(prod.cod_barra).toLowerCase().includes(busqueda.toLowerCase());
    const coincideCat =
      categoriaActiva === 0 || prod.id_categoria === categoriaActiva;
    return coincideTexto && coincideCat;
  });

  const agregarAlCarrito = (producto) => {
    setCarrito((prev) => {
      const existe = prev.find(
        (item) => item.id_producto === producto.id_producto);

      const maxStock =
        producto.stock_actual != null ? Number(producto.stock_actual): Infinity;
      
        if (maxStock <= 0) return prev;

        if (existe) {
          if(existe.cantidad >=maxStock) return prev;
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
        .map((item) => {
          if (item.id_producto !== idProducto) return item;
          const maxStock =
            item.stock_actual != null ? Number(item.stock_actual) : Infinity;
          const nuevaCantidad = item.cantidad + delta;
          if (delta > 0 && nuevaCantidad > maxStock) return item;
          return { ...item, cantidad: nuevaCantidad };
        })
        .filter((item) => item.cantidad > 0)
    );
  };

  const eliminarDelCarrito = (idProducto) => {
    setCarrito((prev) => prev.filter((item) => item.id_producto !== idProducto));
  };

  const handleGuardarDireccion = async (payloadDireccion) => {
    const idPersona = usuarioActivo?.Id_Persona ?? usuarioActivo?.id_persona;

    if (!usuarioActivo || !idPersona) {
      onAbrirLogin?.();
      throw new Error("Debes iniciar sesión con tu cuenta de cliente para guardar tu dirección.");
    }

    return await guardarDireccionCliente(idPersona, payloadDireccion);
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
          <SelectorCategorias
            categorias={categorias}
            categoriaActiva={categoriaActiva}
            onSeleccionar={setCategoriaActiva}
          />

          {cargando && <p>Cargando productos...</p>}
          {error && <p>{error}</p>}

          {!cargando && !error && (
            <div className="productos-grid">
              {productosFiltrados.map((prod) => (
                <ProductoCard
                  key={prod.id_producto}
                  producto={prod}
                  onAgregar={agregarAlCarrito}
                />
              ))}
            </div>
          )}
        </main>

        <CarritoSidebar
          carrito={carrito}
          onCambiarCantidad={cambiarCantidad}
          onEliminar={eliminarDelCarrito}
          onVaciar={() => setCarrito([])}
          usuarioActivo={usuarioActivo}
          onAbrirLogin={onAbrirLogin}
          onGuardarDireccion={handleGuardarDireccion}
        />
      </div>
    </div>
  );
}