from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user_model import User
from app.schemas.auth_schema import UserRegister, UserLogin
from app.services.user_service import obtener_usuario_por_email
from app.auth.security import get_password_hash, verify_password, create_access_token


def registrar_usuario(db: Session, datos: UserRegister) -> User:
    """Registra un nuevo usuario con contraseña hasheada."""
    if obtener_usuario_por_email(db, datos.email):
        raise HTTPException(status_code=400, detail="El correo ya se encuentra registrado")

    nuevo_usuario = User(
        name=datos.name,
        email=datos.email,
        hashed_password=get_password_hash(datos.password),
        role=datos.role,
        is_active=True
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


def autenticar_usuario(db: Session, datos: UserLogin) -> str:
    """Valida credenciales y retorna un token JWT si son correctas."""
    usuario = obtener_usuario_por_email(db, datos.email)

    if not usuario or not verify_password(datos.password, usuario.hashed_password):
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")

    if not usuario.is_active:
        raise HTTPException(status_code=403, detail="Usuario inactivo")

    token = create_access_token(data={"sub": usuario.email, "role": usuario.role})
    return token