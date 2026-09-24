# API de Usuarios y Reservas - FastAPI en EC2 con Amazon RDS
 
Actividad de la materia Arquitectura en la Nube para Tecnologias de la Informacion (UIDE).
API RESTful hecha con FastAPI y SQLModel, desplegada en una instancia EC2 de AWS,
con la base de datos PostgreSQL alojada en Amazon RDS.
 
## Arquitectura
 
```
Internet --8000--> EC2 (FastAPI + pm2)
                     |
                     +--5432--> RDS PostgreSQL (sin acceso publico)
```
 
La instancia RDS no tiene acceso publico. Su grupo de seguridad solo acepta
conexiones en el puerto 5432 provenientes del grupo de seguridad de la EC2,
siguiendo el principio de minimo privilegio.
 
## URL publica
 
- Documentacion (Swagger): http://52.73.115.143:8000/docs
- Verificacion de la conexion con RDS: http://52.73.115.143:8000/check_db
- Listado de usuarios: http://52.73.115.143:8000/usuarios/
- Listado de reservas: http://52.73.115.143:8000/reservas/
## Infraestructura en AWS
 
| Recurso | Detalle |
|---------|---------|
| Region | us-east-1 (Norte de Virginia) |
| EC2 | `fastapi-rds`, Ubuntu Server 26.04 LTS, t3.micro |
| IP publica EC2 | 52.73.115.143 |
| Security group EC2 | `fastapi-ec2-sg` — puertos 22 (SSH) y 8000 (API) |
| RDS | `fastapi-rds-db`, PostgreSQL 18.3, db.t4g.micro |
| Endpoint RDS | fastapi-rds-db.c6d4qcoouy3y.us-east-1.rds.amazonaws.com |
| Security group RDS | `fastapi-rds-sg` — puerto 5432 solo desde `fastapi-ec2-sg` |
| Acceso publico RDS | No |
| VPC | Ambos recursos en la misma VPC (`vpc-0b9db12198999dcab`) |
 
El endpoint `/check_db` ejecuta una consulta directa contra la base y devuelve el
host de RDS y la version de PostgreSQL, para comprobar que la API desplegada en
EC2 esta usando efectivamente la instancia RDS.
 
## Entidades
 
- **Usuario**: id, nombre, email, telefono
- **Reserva**: id, usuario_id, fecha, descripcion, estado
Un usuario puede tener varias reservas (relacion 1 a N). Al crear una reserva se
valida que el usuario exista, y no se puede eliminar un usuario que tenga
reservas asociadas.
 
## Endpoints
 
| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| GET | `/` | estado de la API |
| GET | `/check_db` | comprueba la conexion con RDS |
| POST | `/usuarios/` | crear usuario |
| GET | `/usuarios/` | listar usuarios |
| GET | `/usuarios/{id}` | obtener un usuario |
| PATCH | `/usuarios/{id}` | actualizar usuario |
| DELETE | `/usuarios/{id}` | eliminar usuario |
| POST | `/reservas/` | crear reserva |
| GET | `/reservas/` | listar reservas |
| GET | `/reservas/{id}` | obtener una reserva |
| PATCH | `/reservas/{id}` | actualizar reserva |
| DELETE | `/reservas/{id}` | eliminar reserva |
 
## Estructura del proyecto
 
```
fastapi-rds/
├── config.py          # lee las variables de entorno y arma la cadena de conexion
├── db.py              # engine, sesion y creacion de tablas
├── models.py          # modelos SQLModel de las dos entidades
├── routers/
│   ├── usuarios.py
│   └── reservas.py
├── main.py            # app FastAPI y registro de routers
├── requirements.txt
├── .env.example       # plantilla de variables de entorno
└── .gitignore
```
 
La separacion sigue la recomendacion del enunciado: modelos, rutas, configuracion
y conexion a la base de datos en modulos distintos.
 
## Variables de entorno
 
El archivo `.env` **no se sube al repositorio**. Para ejecutar el proyecto hay que
crear uno a partir de `.env.example`:
 
| Variable | Descripcion |
|----------|-------------|
| `DB_USER` | usuario maestro de la instancia RDS |
| `DB_PASSWORD` | contrasena del usuario maestro |
| `DB_HOST` | endpoint de la instancia RDS |
| `DB_PORT` | puerto de PostgreSQL (5432) |
| `DB_NAME` | nombre de la base de datos |
 
La cadena de conexion se arma en `config.py` a partir de esas variables. En ningun
momento aparece escrita en el codigo.
 
## Correr en local
 
```bash
git clone https://github.com/Lean131X/fastapi-rds.git
cd fastapi-rds
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env    # y editar con los valores reales
uvicorn main:app --reload
```
 
## Tecnologias
 
- Python 3
- FastAPI
- SQLModel (ORM)
- psycopg (driver de PostgreSQL)
- python-dotenv
- Amazon RDS (PostgreSQL)
- Amazon EC2 (Ubuntu) con pm2
 