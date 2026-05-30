from fastapi import FastAPI
from app.routes.user_routes import router as user_router

app = FastAPI(
    title="Device Systems API",
    description="API REST para la gestión de usuarios del sistema de equipos",
    version="1.0"
)

# Incluir las rutas modulares de usuarios
app.include_router(user_router)

@app.get("/")
def inicio():
    return {"mensaje": "Bienvenido a la API de device_systems. Ve a /docs para ver la documentación"}