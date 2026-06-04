from fastapi import HTTPException, Header, Depends
from typing import Optional, Dict, Any
from app.data.users_db import users_db

ROLES_PERMITIDOS = {"admin", "support", "user"}


def get_user_or_404(user_id: int) -> Dict[str, Any]:
    """
    Dependencia reutilizable: busca un usuario por ID.
    Lanza HTTPException 404 si no existe.
    """
    usuario = next((u for u in users_db if u["id"] == user_id), None)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


def validar_correo_unico(email: str, exclude_id: Optional[int] = None) -> None:
    """
    Dependencia reutilizable: valida que el correo no esté en uso.
    Se puede excluir un ID para el caso de actualizaciones (PUT/PATCH).
    """
    for u in users_db:
        if u["email"] == email and u["id"] != exclude_id:
            raise HTTPException(status_code=400, detail="El correo ya se encuentra registrado")


def validar_rol_permitido(role: str) -> str:
    """
    Dependencia reutilizable: verifica que el rol sea uno de los permitidos.
    """
    if role not in ROLES_PERMITIDOS:
        raise HTTPException(
            status_code=400,
            detail=f"Rol no permitido. Los roles válidos son: {', '.join(ROLES_PERMITIDOS)}"
        )
    return role


def get_api_config() -> Dict[str, str]:
    """
    Dependencia reutilizable: retorna configuración general de la API.
    Útil para inyectar metadatos en respuestas o lógica.
    """
    return {
        "app_name": "device_systems",
        "version": "2.0.0",
        "environment": "development"
    }


def simular_autenticacion(x_api_key: Optional[str] = Header(default=None)) -> str:
    """
    Dependencia reutilizable: simula autenticación básica por cabecera.
    Espera la cabecera X-API-Key con valor 'device-secret-2025'.
    """
    if x_api_key != "device-secret-2025":
        raise HTTPException(
            status_code=401,
            detail="No autorizado. Debes enviar el header X-API-Key correcto."
        )
    return x_api_key