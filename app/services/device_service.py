from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Optional, List
from app.models.device_model import Device
from app.schemas.device_schema import DeviceCreate, DeviceUpdate


def listar_dispositivos(
    db: Session,
    device_type: Optional[str] = None,
    is_available: Optional[bool] = None,
    brand: Optional[str] = None,
    search: Optional[str] = None
) -> List[Device]:
    """Retorna dispositivos con filtros opcionales."""
    query = db.query(Device)

    if device_type:
        query = query.filter(Device.device_type == device_type)

    if is_available is not None:
        query = query.filter(Device.is_available == is_available)

    if brand:
        query = query.filter(Device.brand.ilike(f"%{brand}%"))

    if search:
        query = query.filter(Device.name.ilike(f"%{search}%"))

    return query.all()


def obtener_dispositivo_por_id(db: Session, device_id: int) -> Device:
    """Busca un dispositivo por ID. Lanza 404 si no existe."""
    dispositivo = db.query(Device).filter(Device.id == device_id).first()
    if not dispositivo:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return dispositivo


def obtener_dispositivo_por_serial(db: Session, serial_number: str) -> Optional[Device]:
    """Busca un dispositivo por número de serie."""
    return db.query(Device).filter(Device.serial_number == serial_number).first()


def crear_dispositivo(db: Session, device: DeviceCreate) -> Device:
    """Crea un nuevo dispositivo. Valida número de serie duplicado."""
    if obtener_dispositivo_por_serial(db, device.serial_number):
        raise HTTPException(status_code=400, detail="El número de serie ya está registrado")

    nuevo_dispositivo = Device(**device.model_dump())
    db.add(nuevo_dispositivo)
    db.commit()
    db.refresh(nuevo_dispositivo)
    return nuevo_dispositivo


def actualizar_dispositivo(db: Session, device_id: int, device: DeviceUpdate) -> Device:
    """Actualiza parcialmente un dispositivo."""
    dispositivo = obtener_dispositivo_por_id(db, device_id)

    datos = device.model_dump(exclude_none=True)
    if not datos:
        raise HTTPException(status_code=400, detail="Debe enviar al menos un campo para actualizar")

    for campo, valor in datos.items():
        setattr(dispositivo, campo, valor)

    db.commit()
    db.refresh(dispositivo)
    return dispositivo


def eliminar_dispositivo(db: Session, device_id: int) -> None:
    """Elimina un dispositivo por ID."""
    dispositivo = obtener_dispositivo_por_id(db, device_id)
    db.delete(dispositivo)
    db.commit()