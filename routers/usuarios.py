from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from db import SessionDep
from models import Reserva, Usuario, UsuarioCreate, UsuarioUpdate

usuarios = APIRouter(prefix="/usuarios", tags=["usuarios"])


@usuarios.post("/", response_model=Usuario, summary="Crear un usuario")
def crear_usuario(user_data: UsuarioCreate, session: SessionDep):
    usuario_nuevo = Usuario(
        nombre=user_data.nombre,
        email=user_data.email,
        telefono=user_data.telefono,
    )
    session.add(usuario_nuevo)
    session.commit()
    session.refresh(usuario_nuevo)
    return usuario_nuevo


@usuarios.get("/", response_model=list[Usuario], summary="Listar todos los usuarios")
def listar_usuarios(session: SessionDep):
    return session.exec(select(Usuario)).all()


@usuarios.get("/{usuario_id}", response_model=Usuario, summary="Obtener un usuario por id")
def obtener_usuario(usuario_id: int, session: SessionDep):
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario no fue encontrado"
        )
    return usuario


@usuarios.patch("/{usuario_id}", response_model=Usuario, summary="Actualizar un usuario")
def actualizar_usuario(usuario_id: int, user_data: UsuarioUpdate, session: SessionDep):
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario no fue encontrado"
        )

    datos = user_data.model_dump(exclude_unset=True)
    usuario.sqlmodel_update(datos)
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario


@usuarios.delete("/{usuario_id}", summary="Eliminar un usuario")
def eliminar_usuario(usuario_id: int, session: SessionDep):
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario no fue encontrado"
        )

    # si tiene reservas no se puede borrar por la llave foranea
    reservas_del_usuario = session.exec(
        select(Reserva).where(Reserva.usuario_id == usuario_id)
    ).all()
    if reservas_del_usuario:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar, el usuario tiene reservas asociadas"
        )

    session.delete(usuario)
    session.commit()
    return {"mensaje": "Usuario eliminado"}
