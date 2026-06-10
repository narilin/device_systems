from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from fastapi import HTTPException
from typing import Optional, List
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate, UserPatch


ROLES_PERMITIDOS = {"admin", "support", "user"}


def listar_usuarios(
    db: Session,
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
    order_by: Optional[str] = None
) -> List[User]:
    """Retorna todos los usuarios con filtros y orden opcionales."""
    query = db.query(User)

    if role:
        if role not in ROLES_PERMITIDOS:
            raise HTTPException(status_code=400, detail=f"Rol no permitido. Válidos: {', '.join(ROLES_PERMITIDOS)}")
        query = query.filter(User.role == role)

    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    if order_by == "name":
        query = query.order_by(asc(User.name))
    elif order_by == "created_at":
        query = query.order_by(desc(User.created_at))

    return query.all()


def obtener_usuario_por_id(db: Session, user_id: int) -> User:
    """Busca un usuario por ID. Lanza 404 si no existe."""
    usuario = db.query(User).filter(User.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


def obtener_usuario_por_email(db: Session, email: str) -> Optional[User]:
    """Busca un usuario por email."""
    return db.query(User).filter(User.email == email).first()


def crear_usuario(db: Session, user: UserCreate) -> User:
    """Crea un nuevo usuario. Valida correo duplicado."""
    if obtener_usuario_por_email(db, user.email):
        raise HTTPException(status_code=400, detail="El correo ya se encuentra registrado")

    nuevo_usuario = User(**user.model_dump())
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


def actualizar_usuario_completo(db: Session, user_id: int, user: UserUpdate) -> User:
    """Reemplaza completamente los datos de un usuario (PUT)."""
    usuario = obtener_usuario_por_id(db, user_id)

    existente = obtener_usuario_por_email(db, user.email)
    if existente and existente.id != user_id:
        raise HTTPException(status_code=400, detail="El correo ya está en uso por otro usuario")

    for campo, valor in user.model_dump().items():
        setattr(usuario, campo, valor)

    db.commit()
    db.refresh(usuario)
    return usuario


def actualizar_usuario_parcial(db: Session, user_id: int, user: UserPatch) -> User:
    usuario = obtener_usuario_por_id(db, user_id)

    datos = user.model_dump(exclude_none=True)
    if not datos:
        raise HTTPException(status_code=400, detail="Debe enviar al menos un campo para actualizar")


    if "email" in datos:
        existente = obtener_usuario_por_email(db, datos["email"])
        if existente and existente.id != user_id:
            raise HTTPException(status_code=400, detail="El correo ya está en uso por otro usuario")

    for campo, valor in datos.items():
        setattr(usuario, campo, valor)

    db.commit()
    db.refresh(usuario)
    return usuario


def eliminar_usuario(db: Session, user_id: int) -> None:
    """Elimina un usuario por ID. Lanza 404 si no existe."""
    usuario = obtener_usuario_por_id(db, user_id)
    db.delete(usuario)
    db.commit()