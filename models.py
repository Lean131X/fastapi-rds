from typing import Optional

from sqlmodel import Field, SQLModel


# USUARIO

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    email: str
    telefono: Optional[str] = None


class UsuarioCreate(SQLModel):
    nombre: str
    email: str
    telefono: Optional[str] = None


class UsuarioUpdate(SQLModel):
    # todo opcional para poder actualizar solo un campo
    nombre: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None


# RESERVA

class Reserva(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id")
    fecha: str
    descripcion: str
    estado: str = "pendiente"


class ReservaCreate(SQLModel):
    usuario_id: int
    fecha: str
    descripcion: str
    estado: str = "pendiente"


class ReservaUpdate(SQLModel):
    usuario_id: Optional[int] = None
    fecha: Optional[str] = None
    descripcion: Optional[str] = None
    estado: Optional[str] = None
