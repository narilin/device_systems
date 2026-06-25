from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


class LoanCreate(BaseModel):
    user_id: int = Field(..., description="ID del usuario que solicita el préstamo")
    device_id: int = Field(..., description="ID del dispositivo a prestar")

    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": 1,
                "device_id": 3
            }
        }
    }


class LoanUpdate(BaseModel):
    status: Optional[Literal["active", "returned", "overdue"]] = None
    return_date: Optional[datetime] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "overdue"
            }
        }
    }


class LoanResponse(BaseModel):
    id: int
    user_id: int
    device_id: int
    loan_date: datetime
    return_date: Optional[datetime] = None
    status: str

    model_config = {"from_attributes": True}


# ── Esquemas anidados para LoanDetailResponse ──

class UserBasic(BaseModel):
    id: int
    name: str
    email: str

    model_config = {"from_attributes": True}


class DeviceBasic(BaseModel):
    id: int
    name: str
    serial_number: str
    device_type: str

    model_config = {"from_attributes": True}


class LoanDetailResponse(BaseModel):
    id: int
    status: str
    loan_date: datetime
    return_date: Optional[datetime] = None
    user: UserBasic
    device: DeviceBasic

    model_config = {"from_attributes": True}