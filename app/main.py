from fastapi import FastAPI
from app.database.connection import engine, Base
from app.routes.user_routes import router as user_router

# Crear tablas
import app.models.user_model  # noqa
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="device_systems API",
    description="API REST para la gestión de usuarios del sistema **device_systems**.",
    version="2.0.0",
    contact={"name": "Soporte device_systems", "email": "soporte@sena.edu.co"},
    license_info={"name": "MIT"}
)

app.include_router(user_router)

@app.get("/", tags=["Root"], summary="Bienvenida")
def inicio():
    return {
        "mensaje": "Bienvenido a la API device_systems v2.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }