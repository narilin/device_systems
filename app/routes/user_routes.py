from fastapi import APIRouter, Depends, Response, Request
from typing import List, Optional
from sqlalchemy.orm import Session

from app.schemas.user_schema import (
    UserCreate,
    UserUpdate,
    UserPatch,
    UserResponse
)
from app.schemas.loan_schema import LoanResponse

from app.dependencies.database_dependency import get_db
from app.dependencies.auth_dependency import get_current_user
from app.middlewares.rate_limit import limiter

from app.services import user_service, loan_service


router = APIRouter(prefix="/users", tags=["Users"])


# =========================
# UTILIDAD
# =========================
def agregar_cabeceras(response: Response) -> None:
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0.0"


# =========================
# GET ALL USERS
# =========================
@router.get(
    "/",
    response_model=List[UserResponse],
    summary="Listar usuarios",
    description="Retorna todos los usuarios. Permite filtros y ordenamiento.",
)
@limiter.limit("30/minute")
@router.get(
    "/",
    response_model=List[UserResponse],
    summary="Listar usuarios",
    description="Retorna todos los usuarios. Permite filtrar por `role`, `is_active` y ordenar por `name` o `created_at`.",
    response_description="Lista de usuarios"
)
@limiter.limit("30/minute")
def get_users(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
    order_by: Optional[str] = None
):
    agregar_cabeceras(response)
    return user_service.listar_usuarios(
        db=db,
        role=role,
        is_active=is_active,
        order_by=order_by
    )


# =========================
# GET USER BY ID
# =========================
@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Consultar usuario por ID"
)
def get_user_by_id(
    user_id: int,
    response: Response,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    agregar_cabeceras(response)
    return user_service.obtener_usuario_por_id(db, user_id)


# =========================
# CREATE USER
# =========================
@router.post(
    "/",
    response_model=UserResponse,
    status_code=201,
    summary="Crear usuario"
)
def create_user(
    user: UserCreate,
    response: Response,
    db: Session = Depends(get_db)
):
    agregar_cabeceras(response)
    return user_service.crear_usuario(db, user)


# =========================
# UPDATE USER (PUT)
# =========================
@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario completo"
)
def update_user(
    user_id: int,
    user: UserUpdate,
    response: Response,
    db: Session = Depends(get_db)
):
    agregar_cabeceras(response)
    return user_service.actualizar_usuario_completo(db, user_id, user)


# =========================
# PATCH USER
# =========================
@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario parcialmente"
)
def partial_update_user(
    user_id: int,
    user: UserPatch,
    response: Response,
    db: Session = Depends(get_db)
):
    agregar_cabeceras(response)
    return user_service.actualizar_usuario_parcial(db, user_id, user)


# =========================
# DELETE USER
# =========================
@router.delete(
    "/{user_id}",
    status_code=204,
    summary="Eliminar usuario"
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user_service.eliminar_usuario(db, user_id)
    return Response(status_code=204)


# =========================
# GET USER LOANS
# =========================
@router.get(
    "/{user_id}/loans",
    response_model=List[LoanResponse],
    summary="Préstamos de un usuario"
)
def get_user_loans(
    user_id: int,
    db: Session = Depends(get_db)
):
    return loan_service.listar_prestamos_de_usuario(db, user_id)