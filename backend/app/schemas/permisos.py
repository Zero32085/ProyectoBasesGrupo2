from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
ROLES_ADMIN_GERENCIA = {
    "administrador",
    "gerente general",
    "gerente de sucursal",
    "subgerente de sucursal",
}

ROLES_OPERACION_BASE = {
    "cajero",
    "auxiliar de caja",
    "supervisor de caja",
    "encargado de inventario",
    "bodeguero",
    "auxiliar de bodega",
    "encargado de compras",
    "reponedor",
    "encargado de ofertas",
    "atencion al cliente",
    "encargado de ventas en linea",
    "auditor interno",
    "contador",
    "encargado de recursos humanos",
    "encargado de seguridad",
    "encargado de limpieza",
}


def normalizar_rol(rol: str | None) -> str:
    return rol.strip().lower() if rol else ""


def tiene_acceso_administrativo(rol: str | None) -> bool:
    return normalizar_rol(rol) in ROLES_ADMIN_GERENCIA


def tiene_acceso_operativo(rol: str | None) -> bool:
    r = normalizar_rol(rol)
    return r in ROLES_OPERACION_BASE or r in ROLES_ADMIN_GERENCIA
