const API_URL = "http://127.0.0.1:8000";

async function peticion(ruta, metodo, body){
    const res = await fetch(`${API_URL}${ruta}`, {
        method: metodo,
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(body)
    });

    const data = await res.json();

    if(!res.ok){
        throw new Error(
            typeof data.detail === "string"
                ? data.detail
                : "Ocurrió un error en la solicitud"
        );
    }

    return data;
}

function getProductos(){
    return peticion("/productos", "GET");
}

function crearProducto(producto){
    return peticion("/productos/registro", "POST", producto);
}

function actualizarProducto(id, producto){
    return peticion(`/productos/${id}`, "PUT", producto);
}

function getMarcas(){
    return peticion("/marcas", "GET");
}

function getVistaProductos(){
    return peticion("/productos/vista", "GET");
}

export {
    getProductos,
    crearProducto,
    actualizarProducto,
    getMarcas, 
    getVistaProductos
};
