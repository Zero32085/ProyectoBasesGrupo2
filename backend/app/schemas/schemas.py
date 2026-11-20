# 
from pydantic import BaseModel, EmailStr

class OutBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class LoginClienteData(BaseModel):
    correo: EmailStr
    password: str

class LoginEmpleadoData(BaseModel):
    codigo_empleado: str
    password: str

class UserOut(BaseModel):
    id_User: int
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

class PersonaOut(OutBase):
    id_persona: int
    dni: str | None
    primer_nombre: str | None
    segundo_nombre: str | None
    primer_apellido: str | None
    segundo_apellido: str | None
    correo: str | None
    fecha_nacimiento: date | None
    estado: int
    telefono: str | None

class ClienteCreate(BaseModel):
    id_persona: int
    id_direccion: int
    rtn: str | None = Field(default=None, max_length=14)
    razon_social: str | None = Field(default=None, max_length=200)

class ClienteUpdate(BaseModel):
    id_direccion: int | None = None
    rtn: str | None = Field(default=None, max_length=14)
    razon_social: str | None = Field(default=None, max_length=200)

class ClienteOut(OutBase):
    id_cliente: int
    id_persona: int
    id_direccion: int
    rtn: str | None
    razon_social: str | None

class RolEmpleadoCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    descripcion: str | None = Field(default=None, max_length=500)
    estado: Estado = 1

class RolEmpleadoOut(OutBase):
    id_rol_empleado: int
    nombre: str
    descripcion: str | None
    estado: int

class TurnoEmpleadoCreate(BaseModel):
    tipo_turno: str = Field(min_length=1, max_length=20)
    hora_inicio: time
    hora_finalizacion: time
    descripcion: str | None = Field(default=None, max_length=100)

class TurnoEmpleadoOut(OutBase):
    id_turno_empleado: int
    tipo_turno: str
    hora_inicio: time
    hora_finalizacion: time
    descripcion: str | None