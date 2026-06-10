from fastapi import APIRouter, Depends, Response
from typing import List, Optional
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate, UserUpdate, UserPatch, UserResponse
from app.dependencies.database_dependency import get_db
from app.services import user_service

router = APIRouter(prefix="/users", tags=["Users"])



def agregar_cabeceras(response: Response) -> None:
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0.0"


#GET
@router.get(
    "/",
    response_model=List[UserResponse],
    summary="Listar usuarios",
    description="Retorna todos los usuarios. Permite filtrar por `role`, `is_active` y ordenar por `name` o `created_at`.",
    response_description="Lista de usuarios"
)
def get_users(
    response: Response,
    db: Session = Depends(get_db),
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
    order_by: Optional[str] = None
):
    agregar_cabeceras(response)
    return user_service.listar_usuarios(db, role=role, is_active=is_active, order_by=order_by)


#GET 
@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Consultar usuario por ID",
    description="Retorna la información de un usuario específico por su ID.",
    response_description="Datos del usuario"
)
def get_user_by_id(
    user_id: int,
    response: Response,
    db: Session = Depends(get_db)
):
    agregar_cabeceras(response)
    return user_service.obtener_usuario_por_id(db, user_id)


# POST
@router.post(
    "/",
    response_model=UserResponse,
    status_code=201,
    summary="Crear usuario",
    description="Crea un nuevo usuario. Valida correo duplicado y rol permitido.",
    response_description="Usuario creado exitosamente"
)
def create_user(
    user: UserCreate,
    response: Response,
    db: Session = Depends(get_db)
):
    agregar_cabeceras(response)
    return user_service.crear_usuario(db, user)


#PUT
@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario completo",
    description="Reemplaza **todos** los campos de un usuario. Todos los campos son obligatorios.",
    response_description="Usuario actualizado"
)
def update_user(
    user_id: int,
    user: UserUpdate,
    response: Response,
    db: Session = Depends(get_db)
):
    agregar_cabeceras(response)
    return user_service.actualizar_usuario_completo(db, user_id, user)


#PATCH
@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario parcialmente",
    description="Modifica **solo los campos enviados**. Si no se envía ningún campo retorna 400.",
    response_description="Usuario actualizado parcialmente"
)
def partial_update_user(
    user_id: int,
    user: UserPatch,
    response: Response,
    db: Session = Depends(get_db)
):
    agregar_cabeceras(response)
    return user_service.actualizar_usuario_parcial(db, user_id, user)


#DELETE 
@router.delete(
    "/{user_id}",
    status_code=204,
    summary="Eliminar usuario",
    description="Elimina un usuario existente por su ID.",
    response_description="Usuario eliminado (sin contenido)"
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user_service.eliminar_usuario(db, user_id)
    return Response(status_code=204)