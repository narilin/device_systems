from fastapi import APIRouter, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from app.schemas.loan_schema import LoanCreate, LoanResponse, LoanDetailResponse
from app.dependencies.database_dependency import get_db
from app.services import loan_service

router = APIRouter(prefix="/loans", tags=["Loans"])


@router.get(
    "/",
    response_model=List[LoanResponse],
    summary="Listar préstamos",
    description="Retorna todos los préstamos registrados. Permite filtrar por `status`, `user_id`, `device_id` y `device_type`.",
    response_description="Lista de préstamos"
)
def get_loans(
    db: Session = Depends(get_db),
    status: Optional[str] = None,
    user_id: Optional[int] = None,
    device_id: Optional[int] = None,
    device_type: Optional[str] = None
):
    return loan_service.listar_prestamos(
        db,
        status=status,
        user_id=user_id,
        device_id=device_id,
        device_type=device_type
    )


@router.get(
    "/details",
    response_model=List[LoanDetailResponse],
    summary="Préstamos con información detallada",
    description="Retorna todos los préstamos incluyendo datos completos del usuario y del dispositivo asociado.",
    response_description="Lista de préstamos con información relacionada"
)
def get_loans_details(db: Session = Depends(get_db)):
    return loan_service.listar_prestamos_detallados(db)


@router.get(
    "/{loan_id}",
    response_model=LoanResponse,
    summary="Consultar préstamo por ID",
    description="Retorna la información de un préstamo específico.",
    response_description="Datos del préstamo"
)
def get_loan_by_id(loan_id: int, db: Session = Depends(get_db)):
    return loan_service.obtener_prestamo_por_id(db, loan_id)


@router.post(
    "/",
    response_model=LoanResponse,
    status_code=201,
    summary="Crear préstamo",
    description="Registra un nuevo préstamo. Valida que el usuario exista, el dispositivo exista y esté disponible.",
    response_description="Préstamo creado exitosamente"
)
def create_loan(loan: LoanCreate, db: Session = Depends(get_db)):
    return loan_service.crear_prestamo(db, loan)


@router.patch(
    "/{loan_id}/return",
    response_model=LoanResponse,
    summary="Devolver dispositivo",
    description="Marca un préstamo como devuelto y libera el dispositivo.",
    response_description="Préstamo devuelto exitosamente"
)
def return_loan(loan_id: int, db: Session = Depends(get_db)):
    return loan_service.devolver_prestamo(db, loan_id)