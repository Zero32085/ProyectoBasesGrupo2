import {useState} from "react";
import Login from "../pages/Login";
import "./styles/BotonLogin.css"

export default function BotonLogin({usuarioActivo,onAbrirLogin,onCerrarSesion}){
    if(!usuarioActivo){
        return (
        <button class="boton-login" type="button" onClick={onAbrirLogin}>
            Iniciar Sesion
        </button>
        );
    }

    return(
        <button class="boton-login" type="button" onClick={onCerrarSesion}>
            Cerrar Sesion
        </button>
    );
}
