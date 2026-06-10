from app.database.connection import SessionLocal


def get_db():
    """
    Dependencia que entrega una sesión de base de datos.
    Se cierra automáticamente al terminar cada request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()