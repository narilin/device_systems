from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from slowapi.middleware import SlowAPIMiddleware


from app.middlewares.rate_limit import limiter
from app.middlewares.request_middleware import request_middleware

from app.routes.user_routes import router as user_router
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router
from app.auth.auth_routes import router as auth_router

from app.models import user_model, device_model, loan_model


app = FastAPI(
    title="device_systems API",
    description="API REST segura para gestión de usuarios, dispositivos y préstamos",
    version="3.0.0",
    contact={
        "name": "Soporte device_systems",
        "email": "soporte@sena.edu.co"
    },
    license_info={"name": "MIT"}
)

# Rate Limiting
app.state.limiter = limiter

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SlowAPI
app.add_middleware(SlowAPIMiddleware)

# Middleware personalizado
app.middleware("http")(request_middleware)

# Routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(device_router)
app.include_router(loan_router)


@app.get("/", tags=["Root"], summary="Bienvenida")
def inicio():
    return {
        "mensaje": "Bienvenido a la API device_systems v3.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }