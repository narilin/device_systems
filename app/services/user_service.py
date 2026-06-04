from fastapi import HTTPException
from typing import List, Dict, Any, Optional
from app.data.users_db import users_db
from app.schemas.user_schema import UserCreate, UserUpdate, UserPartialUpdate


ROLES_PERMITIDOS = {"admin", "support", "user"}


def obtener_todos_los_usuarios(
    role: Optional[str] = None,
    is_active: Optional[bool] = None
) -> List[Dict[str, Any]]:
    """Retorna la lista de usuarios, con filtros opcionales."""
    resultado = users_db

    if role:
        resultado = [u for u in resultado if u["role"] == role]

    if is_active is not None:
        resultado = [u for u in resultado if u["is_active"] == is_active]

    return resultado


def obtener_usuario_por_id(user_id: int) -> Dict[str, Any]:
    """Busca un usuario por ID. Lanza 404 si no existe."""
    usuario = next((u for u in users_db if u["id"] == user_id), None)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


def crear_usuario(user: UserCreate) -> Dict[str, Any]:
    """Crea un nuevo usuario. Valida ID y correo duplicados."""
    # Validar ID duplicado
    if any(u["id"] == user.id for u in users_db):
        raise HTTPException(status_code=400, detail="Ya existe un usuario con ese ID")

    if any(u["email"] == user.email for u in users_db):
        raise HTTPException(status_code=400, detail="El correo ya se encuentra registrado")

    nuevo_usuario = user.model_dump()
    users_db.append(nuevo_usuario)
    return nuevo_usuario


def actualizar_usuario_completo(user_id: int, user: UserUpdate) -> Dict[str, Any]:
    """Reemplaza completamente los datos de un usuario (PUT)."""
    usuario = obtener_usuario_por_id(user_id)

    if any(u["email"] == user.email and u["id"] != user_id for u in users_db):
        raise HTTPException(status_code=400, detail="El correo ya está en uso por otro usuario")

    usuario.update(user.model_dump())
    return usuario


def actualizar_usuario_parcial(user_id: int, user: UserPartialUpdate) -> Dict[str, Any]:
    """Actualiza solo los campos enviados (PATCH)."""
    usuario = obtener_usuario_por_id(user_id)

    datos = user.model_dump(exclude_none=True)
    if not datos:
        raise HTTPException(status_code=400, detail="Debe enviar al menos un campo para actualizar")

    # Validar correo duplicado si se está cambiando
    if "email" in datos:
        if any(u["email"] == datos["email"] and u["id"] != user_id for u in users_db):
            raise HTTPException(status_code=400, detail="El correo ya está en uso por otro usuario")

    usuario.update(datos)
    return usuario


def eliminar_usuario(user_id: int) -> None:
    """Elimina un usuario por ID. Lanza 404 si no existe."""
    usuario = obtener_usuario_por_id(user_id)
    users_db.remove(usuario)