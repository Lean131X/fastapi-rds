from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from config import DB_HOST, DB_NAME, DB_PORT
from db import SessionDep, create_all_tables
from routers.reservas import reservas
from routers.usuarios import usuarios

app = FastAPI(
    title="API de Usuarios y Reservas",
    description="Actividad de Arquitectura en la Nube - FastAPI en EC2 con base de datos en Amazon RDS",
    version="1.0.0",
    lifespan=create_all_tables,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuarios)
app.include_router(reservas)


@app.get("/", tags=["estado"], summary="Estado de la API")
def root():
    return {"mensaje": "API funcionando", "documentacion": "/docs"}


@app.get("/check_db", tags=["estado"], summary="Verifica la conexion con Amazon RDS")
def check_db(session: SessionDep):
    # consulta directa a la base para comprobar que la conexion esta viva
    version = session.execute(text("select version()")).scalar()
    base_actual = session.execute(text("select current_database()")).scalar()
    return {
        "conectado": True,
        "host_rds": DB_HOST,
        "puerto": DB_PORT,
        "base_de_datos": base_actual or DB_NAME,
        "version_postgres": version,
    }
