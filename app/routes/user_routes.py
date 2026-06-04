from fastapi import APIRouter, HTTPException, Response, Depends
from typing import List, Optional
from app.schemas.user_schema import UserCreate, UserUpdate, UserPartialUpdate, UserResponse
from app.dependencies.user_dependencies import get_user_or_404
from app.services import user_service

router = APIRouter(prefix="/users", tags=["Users"])


def agregar_cabeceras(response: Response) -> None:
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0.0"


@router.get(
    "/",
    response_model=List[UserResponse],
    summary="Listar usuarios",
    description="Retorna todos los usuarios registrados. Permite filtrar por `role` y/o `is_active`.",
    response_description="Lista de usuarios encontrados"
)
def get_users(
    response: Response,
    role: Optional[str] = None,
    is_active: Optional[bool] = None
):
    agregar_cabeceras(response)
    return user_service.obtener_todos_los_usuarios(role=role, is_active=is_active)

@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Consultar usuario por ID",
    description="Retorna la información de un usuario específico buscado por su ID.",
    response_description="Datos del usuario encontrado"
)
def get_user_by_id(
    response: Response,
    usuario: dict = Depends(get_user_or_404)
):
    agregar_cabeceras(response)
    return usuario


@router.post(
    "/",
    response_model=UserResponse,
    status_code=201,
    summary="Crear usuario",
    description="Crea un nuevo usuario. Valida correo duplicado, ID duplicado y rol permitido.",
    response_description="Usuario creado exitosamente"
)
def create_user(user: UserCreate, response: Response):
    agregar_cabeceras(response)
    return user_service.crear_usuario(user)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario completo",
    description="Reemplaza **todos** los campos de un usuario existente. Todos los campos son obligatorios.",
    response_description="Usuario actualizado exitosamente"
)
def update_user(
    user_id: int,
    user: UserUpdate,
    response: Response,
    _usuario: dict = Depends(get_user_or_404)
):
    agregar_cabeceras(response)
    return user_service.actualizar_usuario_completo(user_id, user)


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario parcialmente",
    description="Modifica **solo los campos enviados** de un usuario. Si no se envía ningún campo, retorna 400.",
    response_description="Usuario actualizado parcialmente"
)
def partial_update_user(
    user_id: int,
    user: UserPartialUpdate,
    response: Response,
    _usuario: dict = Depends(get_user_or_404)
):
    agregar_cabeceras(response)
    return user_service.actualizar_usuario_parcial(user_id, user)


@router.delete(
    "/{user_id}",
    status_code=204,
    summary="Eliminar usuario",
    description="Elimina un usuario existente por su ID. Retorna 204 sin contenido si fue exitoso.",
    response_description="Usuario eliminado (sin contenido)"
)
def delete_user(
    user_id: int,
    _usuario: dict = Depends(get_user_or_404)
):
    user_service.eliminar_usuario(user_id)
    return Response(status_code=204)