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

function getInventarios(){
    return peticion("/inventarios", "GET");
}

function crearInventario(inventario){
    return peticion("/inventarios/registro", "POST", inventario);
}

function actualizarInventario(id, inventario){
    return peticion(`/inventarios/${id}`, "PUT", inventario);
}

function getVistaInventarios(){
    return peticion("/inventarios/vista", "GET");
}

export {
    getInventarios,
    crearInventario,
    actualizarInventario,
    getVistaInventarios
};