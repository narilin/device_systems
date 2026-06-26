from sqlalchemy.orm import Session
from app.dependencies.database_dependency import get_db
from app.schemas.auth_schema import UserRegister, UserLogin, Token
from app.schemas.user_schema import UserResponse
from app.auth import auth_service
from app.dependencies.auth_dependency import get_current_user
from app.models.user_model import User
from fastapi import APIRouter, Depends, Request
from app.middlewares.rate_limit import limiter

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
    summary="Registrar usuario",
    description="Crea un nuevo usuario con contraseña segura (hasheada). Valida correo único y reglas de contraseña.",
    response_description="Usuario registrado exitosamente"
)
@limiter.limit("3/minute")
def register(
    request: Request,
    datos: UserRegister,
    db: Session = Depends(get_db)
):
    return auth_service.registrar_usuario(db, datos)

@router.post(
    "/login",
    response_model=Token,
    summary="Iniciar sesión",
    description="Valida credenciales y retorna un token JWT de acceso.",
    response_description="Token de acceso generado"
)
@limiter.limit("5/minute")
def login(
    request: Request,
    datos: UserLogin,
    db: Session = Depends(get_db)
):
    token = auth_service.autenticar_usuario(db, datos)
    return Token(access_token=token, token_type="bearer")

@router.get(
    "/me",
    response_model=UserResponse,
    summary="Usuario autenticado",
    description="Retorna los datos del usuario actualmente autenticado, según el token enviado.",
    response_description="Datos del usuario autenticado"
)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user