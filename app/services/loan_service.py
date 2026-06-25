from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from typing import Optional, List
from app.models.loan_model import Loan
from app.models.device_model import Device
from app.models.user_model import User
from app.schemas.loan_schema import LoanCreate


def obtener_prestamo_por_id(db: Session, loan_id: int) -> Loan:
    """Busca un préstamo por ID. Lanza 404 si no existe."""
    prestamo = db.query(Loan).filter(Loan.id == loan_id).first()
    if not prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    return prestamo


def listar_prestamos(
    db: Session,
    status: Optional[str] = None,
    user_id: Optional[int] = None,
    device_id: Optional[int] = None,
    device_type: Optional[str] = None
) -> List[Loan]:
    """Retorna préstamos con filtros opcionales."""
    query = db.query(Loan).join(User).join(Device)

    if status:
        query = query.filter(Loan.status == status)

    if user_id:
        query = query.filter(Loan.user_id == user_id)

    if device_id:
        query = query.filter(Loan.device_id == device_id)

    if device_type:
        query = query.filter(Device.device_type == device_type)

    return query.all()


def crear_prestamo(db: Session, loan: LoanCreate) -> Loan:
    """
    Crea un nuevo préstamo.
    Valida: usuario existe, dispositivo existe, dispositivo disponible.
    Efecto: marca el dispositivo como no disponible.
    """
    usuario = db.query(User).filter(User.id == loan.user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    dispositivo = db.query(Device).filter(Device.id == loan.device_id).first()
    if not dispositivo:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")

    if not dispositivo.is_available:
        raise HTTPException(status_code=409, detail="El dispositivo no está disponible")

    nuevo_prestamo = Loan(
        user_id=loan.user_id,
        device_id=loan.device_id,
        status="active",
        loan_date=datetime.utcnow()
    )
    db.add(nuevo_prestamo)

    dispositivo.is_available = False

    db.commit()
    db.refresh(nuevo_prestamo)
    return nuevo_prestamo


def devolver_prestamo(db: Session, loan_id: int) -> Loan:
    """
    Marca un préstamo como devuelto.
    Valida: préstamo existe, no está ya devuelto.
    Efecto: marca el dispositivo como disponible de nuevo.
    """
    prestamo = obtener_prestamo_por_id(db, loan_id)

    if prestamo.status == "returned":
        raise HTTPException(status_code=409, detail="Este préstamo ya fue devuelto")

    prestamo.status = "returned"
    prestamo.return_date = datetime.utcnow()

    dispositivo = db.query(Device).filter(Device.id == prestamo.device_id).first()
    if dispositivo:
        dispositivo.is_available = True

    db.commit()
    db.refresh(prestamo)
    return prestamo


def listar_prestamos_detallados(db: Session) -> List[Loan]:
    """
    Retorna todos los préstamos con la información del usuario
    y del dispositivo cargada (para el LoanDetailResponse).
    """
    return db.query(Loan).join(User).join(Device).all()

def listar_prestamos_de_usuario(db: Session, user_id: int) -> List[Loan]:
    """Retorna los préstamos asociados a un usuario específico."""
    usuario = db.query(User).filter(User.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db.query(Loan).filter(Loan.user_id == user_id).all()


def listar_prestamos_de_dispositivo(db: Session, device_id: int) -> List[Loan]:
    """Retorna el historial de préstamos de un dispositivo específico."""
    dispositivo = db.query(Device).filter(Device.id == device_id).first()
    if not dispositivo:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return db.query(Loan).filter(Loan.device_id == device_id).all()