from fastapi import FastAPI
from app.routes.user_routes import router as user_router
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router
from app.models import user_model, device_model, loan_model


app = FastAPI(
    title="device_systems API",
    description="API REST para la gestión de usuarios del sistema **device_systems**.",
    version="2.0.0",
    contact={"name": "Soporte device_systems", "email": "soporte@sena.edu.co"},
    license_info={"name": "MIT"}
)

app.include_router(user_router)
app.include_router(device_router)
app.include_router(loan_router)

@app.get("/", tags=["Root"], summary="Bienvenida")
def inicio():
    return {
        "mensaje": "Bienvenido a la API device_systems v2.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }