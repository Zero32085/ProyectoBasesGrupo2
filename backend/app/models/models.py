from sqlalchemy import Column, Date, ForeignKey, String, Integer, Numeric, Time
from sqlalchemy.orm import relationship

# Esto es temporal, hasta que se cree la conexion de database.py
from app.database import Base

class Persona(Base):
	__tablename__ = 'Personas'

	Id_Persona = Column(Integer, primary_key=True, nullable=False)
	dni = Column(String(13), unique=True, nullable=True)
	primer_nombre = Column(String(80), nullable=True)
	segundo_nombre = Column(String(80), nullable=True)
	primer_apellido = Column(String(80), nullable=True)
	segundo_apellido = Column(String(80), nullable=True)
	correo = Column(String(100), unique=True, nullable=True)
	contrasena_hash = Column(String(60), nullable=True)
	fecha_nacimiento = Column(Date, nullable=True)
	estado = Column(Integer, nullable=False, default=1, server_default="1")
	telefono = Column(String(20), nullable=True)

class RolEmpleado(Base):
	__tablename__ = 'Roles_Empleados'
	
	Id_RolEmpleado = Column(Integer, primary_key=True, nullable=False)
	nombre = Column(String(100), nullable=False)
	descripcion = Column(String(500), nullable=True)
	estado = Column(Integer, nullable=False, default=1, server_default="1")


class TurnoEmpleado(Base):
	__tablename__ = 'Turnos_Empleados'

	Id_TurnoEmpleado = Column(Integer, primary_key=True, index=True, nullable=False)
	tipo_turno = Column(String(20), nullable=False)
	hora_inicio = Column(Time, nullable=False)
	hora_finalizacion = Column(Time, nullable=False)
	descripcion = Column(String(100), nullable=True)

	empleado = relationship("Empleado", back_populates="turno_empleado")


class Empleado(Base):
	__tablename__ = 'Empleados'

	Id_Empleado = Column(Integer, primary_key=True, index=True, nullable=False)
	codigo_empleado = Column(String(10), unique=True, nullable=False)
	Id_persona = Column(Integer, ForeignKey("Personas.Id_Persona"), nullable=False)
	salario_base = Column(Numeric(10,2), nullable=False)
	fecha_contratacion = Column(Date, nullable=False)
	Id_RolEmpleado = Column(Integer, ForeignKey("Roles_Empleados.Id_RolEmpleado"), nullable=False)
	Id_TurnoEmpleado = Column(Integer, ForeignKey("Turnos_Empleados.Id_TurnoEmpleado"), nullable=False)
	#Id_Sucursal = Column(Integer, ForeignKey("Sucursales.Id_Sucursal"), nullable=False)

	turno_empleado = relationship("TurnoEmpleado", back_populates="empleado")

	
class Cliente(Base):
	__tablename__ = 'Clientes'

	Id_Cliente = Column(Integer, primary_key=True, nullable=False)
	Id_Persona = Column(Integer, ForeignKey("Personas.Id_Persona"), nullable=False)
	rtn = Column(String(14), unique=True, nullable=True)
	Id_Direccion = Column(Integer, ForeignKey("Direcciones.Id_Direccion"), nullable=False)
	razon_social = Column(String(200), nullable=True)

	persona = relationship("Persona")
	#persona = relationship("Persona", back_populates="clientes")
    #direccion = relationship("Direccion")



