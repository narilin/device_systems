from pydantic import BaseModel, EmailStr, Field
from typing import Literal, Optional
from datetime import datetime


# Modelo para crear usuario (POST)
class UserCreate(BaseModel):
    name: str = Field(..., min_length=3, description="El nombre debe tener mínimo 3 caracteres")
    email: EmailStr = Field(..., description="Debe ser un correo con formato válido")
    role: Literal["admin", "support", "user"] = Field(..., description="Roles permitidos: admin, support, user")
    is_active: bool = Field(default=True, description="Estado del usuario")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Laura Gómez",
                "email": "laura@sena.edu.co",
                "role": "user",
                "is_active": True
            }
        }
    }


# Modelo para actualización completa (PUT)
class UserUpdate(BaseModel):
    name: str = Field(..., min_length=3, description="El nombre debe tener mínimo 3 caracteres")
    email: EmailStr = Field(..., description="Debe ser un correo con formato válido")
    role: Literal["admin", "support", "user"] = Field(..., description="Roles permitidos: admin, support, user")
    is_active: bool = Field(..., description="Estado del usuario")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Laura Actualizada",
                "email": "laura.nueva@sena.edu.co",
                "role": "support",
                "is_active": False
            }
        }
    }


# Modelo para actualización parcial (PATCH)
class UserPatch(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3, description="Nombre del usuario")
    email: Optional[EmailStr] = Field(default=None, description="Correo electrónico")
    role: Optional[Literal["admin", "support", "user"]] = Field(default=None, description="Rol del usuario")
    is_active: Optional[bool] = Field(default=None, description="Estado del usuario")

    model_config = {
        "json_schema_extra": {
            "example": {
                "role": "support"
            }
        }
    }


# Modelo de respuesta
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}