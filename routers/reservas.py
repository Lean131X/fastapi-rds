from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from db import SessionDep
from models import Reserva, ReservaCreate, ReservaUpdate, Usuario

reservas = APIRouter(prefix="/reservas", tags=["reservas"])


@reservas.post("/", response_model=Reserva, summary="Crear una reserva")
def crear_reserva(reserva_data: ReservaCreate, session: SessionDep):
    # reviso que el usuario exista antes de guardar la reserva
    usuario = session.get(Usuario, reserva_data.usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario no fue encontrado"
        )

    reserva_nueva = Reserva(
        usuario_id=reserva_data.usuario_id,
        fecha=reserva_data.fecha,
        descripcion=reserva_data.descripcion,
        estado=reserva_data.estado,
    )
    session.add(reserva_nueva)
    session.commit()
    session.refresh(reserva_nueva)
    return reserva_nueva


@reservas.get("/", response_model=list[Reserva], summary="Listar todas las reservas")
def listar_reservas(session: SessionDep):
    return session.exec(select(Reserva)).all()


@reservas.get("/{reserva_id}", response_model=Reserva, summary="Obtener una reserva por id")
def obtener_reserva(reserva_id: int, session: SessionDep):
    reserva = session.get(Reserva, reserva_id)
    if not reserva:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La reserva no fue encontrada"
        )
    return reserva


@reservas.patch("/{reserva_id}", response_model=Reserva, summary="Actualizar una reserva")
def actualizar_reserva(reserva_id: int, reserva_data: ReservaUpdate, session: SessionDep):
    reserva = session.get(Reserva, reserva_id)
    if not reserva:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La reserva no fue encontrada"
        )

    datos = reserva_data.model_dump(exclude_unset=True)
    reserva.sqlmodel_update(datos)
    session.add(reserva)
    session.commit()
    session.refresh(reserva)
    return reserva


@reservas.delete("/{reserva_id}", summary="Eliminar una reserva")
def eliminar_reserva(reserva_id: int, session: SessionDep):
    reserva = session.get(Reserva, reserva_id)
    if not reserva:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La reserva no fue encontrada"
        )

    session.delete(reserva)
    session.commit()
    return {"mensaje": "Reserva eliminada"}
