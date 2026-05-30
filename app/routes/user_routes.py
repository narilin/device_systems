from fastapi import APIRouter, HTTPException, Response, Query
from typing import List, Optional
from app.schemas.user_schema import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

# Base de datos simulada en memoria
db_users = [
    {"id": 1, "name": "Kimberly", "email": "kimberly@sena.edu.co", "role": "admin", "is_active": True},
    {"id": 2, "name": "Cesar Cardona", "email": "cesar@sena.edu.co", "role": "user", "is_active": False}
]

# Agregar Cabeceras Personalizadas obligatorias por el profesor
def agregar_cabeceras(response: Response):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"

# --- ENDPOINTS GET ---

@router.get("/", response_model=List[UserResponse])
def get_users(
    response: Response,
    role: Optional[str] = None,
    is_active: Optional[bool] = None
):
    agregar_cabeceras(response)
    usuarios_filtrados = db_users

    # Filtro por Query Parameter: role
    if role:
        usuarios_filtrados = [u for u in usuarios_filtrados if u["role"] == role]
    
    # Filtro por Query Parameter: is_active
    if is_active is not None:
        usuarios_filtrados = [u for u in usuarios_filtrados if u["is_active"] == is_active]

    return usuarios_filtrados


@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, response: Response):
    agregar_cabeceras(response)
    usuario = next((u for u in db_users if u["id"] == user_id), None)
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

# --- ENDPOINT POST ---

@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, response: Response):
    agregar_cabeceras(response)
    
    # Validación: Evitar correos duplicados
    for u in db_users:
        if u["email"] == user.email:
            raise HTTPException(status_code=400, detail="El correo ya se encuentra registrado")
            
    nuevo_usuario = user.model_dump()
    db_users.append(nuevo_usuario)
    return nuevo_usuario