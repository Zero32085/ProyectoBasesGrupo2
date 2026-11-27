const API_URL = "http://127.0.0.1:8000";

async function peticion(ruta, metodo, body){
    const res = await fetch(`${API_URL}${ruta}`, {
        method: metodo,
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(body)
    });

    const data = await res.json();

    if(!res.ok){
        throw new Error(data.detail || "Ocurio un error en la solicitud");
    }

    return data;
}

function getCategorias(){
    return peticion("/categorias", "GET");
}

function crearCategoria(categoria){
    return peticion("/categorias/registro", "POST", categoria);
}

function actualizarCategoria(id, categoria){
    return peticion(`/categorias/${id}`, "PUT", categoria);
}

export{getCategorias, crearCategoria, actualizarCategoria}