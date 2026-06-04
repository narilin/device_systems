from pydantic import BaseModel, EmailStr, Field
from typing import Literal, Optional


class UserCreate(BaseModel):
    id: int = Field(..., description="ID único del usuario")
    name: str = Field(..., min_length=3, description="El nombre debe tener mínimo 3 caracteres")
    email: EmailStr = Field(..., description="Debe ser un correo con formato válido")
    role: Literal["admin", "support", "user"] = Field(..., description="Roles permitidos: admin, support, user")
    is_active: bool = Field(default=True, description="Estado del usuario")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 3,
                "name": "Laura Gómez",
                "email": "laura@sena.edu.co",
                "role": "user",
                "is_active": True
            }
        }
    }


class UserUpdate(BaseModel):
    name: str = Field(..., min_length=3, description="El nombre debe tener mínimo 3 caracteres")
    email: EmailStr = Field(..., description="Debe ser un correo con formato válido")
    role: Literal["admin", "support", "user"] = Field(..., description="Roles permitidos: admin, support, user")
    is_active: bool = Field(..., description="Estado del usuario")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Laura Gómez Actualizada",
                "email": "laura.nueva@sena.edu.co",
                "role": "support",
                "is_active": False
            }
        }
    }


class UserPartialUpdate(BaseModel):
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


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool

    model_config = {"from_attributes": True}