from pydantic import BaseModel, EmailStr, Field
from typing import Literal

# Modelo para Recibir Datos (Lo que envía el cliente al hacer POST)
class UserCreate(BaseModel):
    id: int
    name: str = Field(..., min_length=3, description="El nombre debe tener mínimo 3 caracteres")
    email: EmailStr = Field(..., description="Debe ser un correo con formato válido")
    role: Literal["admin", "support", "user"] = Field(..., description="Roles permitidos")
    is_active: bool = True

# Modelo para Responder Datos (Response Model - Oculta datos sensibles si los hubiera)
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool

    class Config:
        from_attributes = True