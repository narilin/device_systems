from fastapi import APIRouter, Depends, Response
from typing import List, Optional
from sqlalchemy.orm import Session
from app.schemas.device_schema import DeviceCreate, DeviceUpdate, DeviceResponse
from app.dependencies.database_dependency import get_db
from app.services import device_service
from app.services import loan_service
from app.schemas.loan_schema import LoanResponse

router = APIRouter(prefix="/devices", tags=["Devices"])


@router.get(
    "/",
    response_model=List[DeviceResponse],
    summary="Listar dispositivos",
    description="Retorna todos los dispositivos. Permite filtrar por `device_type`, `is_available`, `brand` y `search` (búsqueda por nombre).",
    response_description="Lista de dispositivos"
)
def get_devices(
    db: Session = Depends(get_db),
    device_type: Optional[str] = None,
    is_available: Optional[bool] = None,
    brand: Optional[str] = None,
    search: Optional[str] = None
):
    return device_service.listar_dispositivos(
        db,
        device_type=device_type,
        is_available=is_available,
        brand=brand,
        search=search
    )


@router.get(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Consultar dispositivo por ID",
    description="Retorna la información de un dispositivo específico por su ID.",
    response_description="Datos del dispositivo"
)
def get_device_by_id(device_id: int, db: Session = Depends(get_db)):
    return device_service.obtener_dispositivo_por_id(db, device_id)


@router.post(
    "/",
    response_model=DeviceResponse,
    status_code=201,
    summary="Crear dispositivo",
    description="Registra un nuevo dispositivo. Valida número de serie duplicado.",
    response_description="Dispositivo creado exitosamente"
)
def create_device(device: DeviceCreate, db: Session = Depends(get_db)):
    return device_service.crear_dispositivo(db, device)


@router.put(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Actualizar dispositivo",
    description="Actualiza los campos enviados de un dispositivo existente.",
    response_description="Dispositivo actualizado"
)
def update_device(device_id: int, device: DeviceUpdate, db: Session = Depends(get_db)):
    return device_service.actualizar_dispositivo(db, device_id, device)


@router.patch(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Actualizar dispositivo parcialmente",
    description="Modifica solo los campos enviados.",
    response_description="Dispositivo actualizado parcialmente"
)
def partial_update_device(device_id: int, device: DeviceUpdate, db: Session = Depends(get_db)):
    return device_service.actualizar_dispositivo(db, device_id, device)


@router.delete(
    "/{device_id}",
    status_code=204,
    summary="Eliminar dispositivo",
    description="Elimina un dispositivo existente por su ID.",
    response_description="Dispositivo eliminado (sin contenido)"
)
def delete_device(device_id: int, db: Session = Depends(get_db)):
    device_service.eliminar_dispositivo(db, device_id)
    return Response(status_code=204)

@router.get(
    "/{device_id}/loans",
    response_model=List[LoanResponse],
    summary="Historial de préstamos de un dispositivo",
    description="Retorna todos los préstamos asociados a un dispositivo específico.",
    response_description="Lista de préstamos del dispositivo"
)
def get_device_loans(device_id: int, db: Session = Depends(get_db)):
    return loan_service.listar_prestamos_de_dispositivo(db, device_id)