const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function guardarDireccionCliente(idPersona, payloadDireccion) {
    if (!idPersona) {
        throw new Error("Debes iniciar sesión para guardar una dirección de envío.");
    }

    const params = new URLSearchParams({
        id_persona: String(idPersona),
    });

    const body = {
        Id_Ciudad: Number(payloadDireccion.Id_Ciudad ?? 1),
        colonia: payloadDireccion.colonia?.trim(),
        referencia: payloadDireccion.referencia?.trim(),
    };

    if (payloadDireccion.calle && payloadDireccion.calle.trim()) {
        body.calle = payloadDireccion.calle.trim();
    }

    if (payloadDireccion.nombre_destinatario && payloadDireccion.nombre_destinatario.trim()) {
        body.nombre_destinatario = payloadDireccion.nombre_destinatario.trim();
    }

    const respuesta = await fetch(`${API_URL}/clientes/direccion?${params.toString()}`, {
        method: "POST",
        headers: {
        "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
    });

    if (!respuesta.ok) {
        const errorData = await respuesta.json().catch(() => ({}));
        let mensajeError = "No se pudo guardar la dirección de envío.";

        if (typeof errorData.detail === "string") {
        mensajeError = errorData.detail;
        } else if (Array.isArray(errorData.detail) && errorData.detail.length > 0) {
        // Errores de validación 422 de FastAPI/Pydantic
        mensajeError = errorData.detail
            .map((err) => err.msg || "Dato inválido")
            .join(", ");
        }

        throw new Error(mensajeError);
    }

    return respuesta.json();
}