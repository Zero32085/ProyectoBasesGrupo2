from datetime import date, time
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class OutBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class LoginClienteData(BaseModel):
    correo: EmailStr
    password: str


class LoginEmpleadoData(BaseModel):
    codigo_empleado: str
    password: str


class RegistroClientesData(BaseModel):
    primer_nombre: str = Field(min_length=1, max_length=80)
    segundo_nombre: str | None = Field(default=None, max_length=80)
    primer_apellido: str = Field(min_length=1, max_length=80)
    segundo_apellido: str | None = Field(default=None, max_length=80)
    correo: EmailStr
    password: str = Field(min_length=8, max_length=72)
    telefono: str | None = Field(default=None, max_length=20)
    dni: str | None = Field(default=None, max_length=13)
    rtn: str | None = Field(default=None, max_length=14)
    razon_social: str | None = Field(default=None, max_length=200)
    Id_Direccion: int | None = None


class AuthResponse(OutBase):
    Id_Persona: int
    primer_nombre: str | None = None
    primer_apellido: str | None = None
    correo: str | None = None
    rol: str


class UserOut(BaseModel):
    Id_Persona: int
    primer_nombre: str
    primer_apellido: str


class PersonaCreate(BaseModel):
    dni: str | None = Field(default=None, max_length=13)
    primer_nombre: str = Field(min_length=1, max_length=80)
    segundo_nombre: str | None = Field(default=None, max_length=80)
    primer_apellido: str = Field(min_length=1, max_length=80)
    segundo_apellido: str | None = Field(default=None, max_length=80)
    correo: EmailStr
    password: str = Field(min_length=8, max_length=72)
    fecha_nacimiento: date | None = None
    telefono: str | None = Field(default=None, max_length=20)


class PersonaUpdate(BaseModel):
    dni: str | None = Field(default=None, max_length=13)
    primer_nombre: str | None = Field(default=None, min_length=1, max_length=80)
    segundo_nombre: str | None = Field(default=None, max_length=80)
    primer_apellido: str | None = Field(default=None, min_length=1, max_length=80)
    segundo_apellido: str | None = Field(default=None, max_length=80)
    correo: EmailStr | None = None
    fecha_nacimiento: date | None = None
    telefono: str | None = Field(default=None, max_length=20)
    estado: int | None = Field(default=None, ge=0, le=1)


class PersonaOut(OutBase):
    Id_Persona: int
    dni: str | None = None
    primer_nombre: str | None = None
    segundo_nombre: str | None = None
    primer_apellido: str | None = None
    segundo_apellido: str | None = None
    correo: str | None = None
    fecha_nacimiento: date | None = None
    estado: int
    telefono: str | None = None


class ClienteCreate(BaseModel):
    Id_Persona: int
    Id_Direccion: int
    rtn: str | None = Field(default=None, max_length=14)
    razon_social: str | None = Field(default=None, max_length=200)


class ClienteUpdate(BaseModel):
    Id_Direccion: int | None = None
    rtn: str | None = Field(default=None, max_length=14)
    razon_social: str | None = Field(default=None, max_length=200)


class ClienteOut(OutBase):
    Id_Cliente: int
    Id_Persona: int
    Id_Direccion: int
    rtn: str | None = None
    razon_social: str | None = None


class RolEmpleadoCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    descripcion: str | None = Field(default=None, max_length=500)
    estado: int = Field(default=1, ge=0, le=1)


class RolEmpleadoOut(OutBase):
    Id_RolEmpleado: int
    nombre: str
    descripcion: str | None = None
    estado: int


class TurnoEmpleadoCreate(BaseModel):
    tipo_turno: str = Field(min_length=1, max_length=20)
    hora_inicio: time
    hora_finalizacion: time
    descripcion: str | None = Field(default=None, max_length=100)


class TurnoEmpleadoOut(OutBase):
    Id_TurnoEmpleado: int
    tipo_turno: str
    hora_inicio: time
    hora_finalizacion: time
    descripcion: str | None = None