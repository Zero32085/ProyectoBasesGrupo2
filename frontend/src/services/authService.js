const API_URL = "http://127.0.0.1:8000";

async function peticionPost(ruta, body){
    const res = await fetch(`${API_URL}${ruta}`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(body)
    });

    const data = await res.json();

    if(!res.ok){
        throw new Error(data.detail || "Ocurio un error en la solicitud");
    }
    return data;
}

function loginCliente(correo, password){
    return peticionPost("/auth/cliente/login",{correo, password});
}

function registroCliente(
    primerNombre,
    segundoNombre=null,
    primerApellido,
    segundoApellido=null,
    correo,
    password,
    fechaNacimiento=null,
    telefono=null){
    return peticionPost("/auth/cliente/registro",
        {primerNombre,
            segundoNombre,
            primerApellido,
            segundoApellido,
            correo,
            password,
            fechaNacimiento,
            telefono});
}

function loginEmpleado(codigo_empleado, password){
    return peticionPost("/auth/empleado/login",{codigo_empleado,password});
}

export{loginCliente, registroCliente, loginEmpleado}