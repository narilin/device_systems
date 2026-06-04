from fastapi import FastAPI
from app.routes.user_routes import router as user_router


app = FastAPI(
    title="device_systems API",
    description=(
        "API REST para la gestión de usuarios del sistema **device_systems**.\n\n"
        "Permite crear, consultar, actualizar y eliminar usuarios con validaciones "
        "de roles, correos únicos y manejo de errores HTTP.\n\n"
      
    ),
    version="2.0.0",
    contact={
        "name": "Soporte device_systems"
    },
    license_info={
        "name": "MIT"
    }
)

app.include_router(user_router)



@app.get("/", tags=["Root"], summary="Bienvenida")
def inicio():
    return {
        "mensaje": "Bienvenido a la API device_systems v2.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }