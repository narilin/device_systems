## Evidencias de Pruebas y Funcionamiento (Swagger UI)

A continuación se presentan las capturas de pantalla tomadas desde la documentación interactiva de Swagger UI (`http://127.0.0.1:8000/docs`) que certifican el correcto funcionamiento de la API REST.

### 1. Interfaz Principal de Swagger UI
Muestra la estructura global de los endpoints del recurso `users` y la metadata de la aplicación.

![Documentación de Swagger UI](imagenes/api_home.png)

---

### 2. Evidencia de Pruebas: GET /users
Prueba exitosa que retorna la lista de usuarios precargados en la base de datos simulada en memoria, incluyendo las cabeceras HTTP personalizadas `X-App-Name` y `X-API-Version`.

![Prueba Endpoint GET](imagenes/pruebas_get.png)

---

### 3. Evidencia de Pruebas: POST /users
Prueba de creación de un nuevo usuario enviando el cuerpo JSON correspondiente y recibiendo la respuesta con el código de estado `201 Created`.

![Prueba Endpoint POST](imagenes/pruebas_post.png)

---

### 4. Evidencia de Validaciones y Manejo de Errores
Captura que demuestra el funcionamiento de las restricciones de **Pydantic v2**:
* Intento de registro con un correo electrónico duplicado (Retorna error `400 Bad Request`).
* Validación del campo `role` con valores no permitidos o nombres de longitud menor a 3 caracteres (Retorna error `422 Unprocessable Entity`).

![Pruebas de Validación de Errores](imagenes/validacion_error.png)

## Codigo 200 ![alt text](imagenes/image.png)
## Codigo 201 ![alt text](imagenes/image-1.png)
## Codigo 404 ![alt text](imagenes/image-2.png)
## Codigo 400 ![alt text](imagenes/image-3.png)
## Codiogo 422 ![alt text](imagenes/image-4.png)

---

## Instalación

```bash
pip install -r requirements.txt
```

---

## Ejecución

```bash
uvicorn app.main:app --reload
```

Accede a la documentación en:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

---

## Endpoints

| Operación           | Método | Ruta             | Código esperado |
|---------------------|--------|------------------|-----------------|
| Listar usuarios     | GET    | /users           | 200 OK          |
| Consultar usuario   | GET    | /users/{user_id} | 200 OK          |
| Crear usuario       | POST   | /users           | 201 Created     |
| Actualizar completo | PUT    | /users/{user_id} | 200 OK          |
| Actualizar parcial  | PATCH  | /users/{user_id} | 200 OK          |
| Eliminar usuario    | DELETE | /users/{user_id} | 204 No Content  |

---

## Códigos de error

| Situación                     | Código |
|-------------------------------|--------|
| Usuario no encontrado         | 404    |
| Correo duplicado              | 400    |
| Rol no permitido              | 400    |
| PATCH sin datos               | 400    |
| Datos inválidos (Pydantic)    | 422    |
| Sin autenticación (X-API-Key) | 401    |

---

## Dependency Injection (`Depends`)

El proyecto usa `Depends()` para reutilizar lógica en múltiples endpoints:

- `get_user_or_404` → busca usuario por ID o lanza 404
- `validar_correo_unico` → verifica que el correo no esté en uso
- `validar_rol_permitido` → verifica que el rol sea válido
- `get_api_config` → retorna configuración general de la API
- `simular_autenticacion` → valida cabecera `X-API-Key`

---

## Roles permitidos

- `admin`
- `support`
- `user`

![Base de datos](imagenes/basededatos.png)

## Diferencia entre modelo SQLAlchemy y schema Pydantic

El **modelo SQLAlchemy** define cómo se guarda la información en la base de datos,
mientras que el **schema Pydantic** define qué datos recibe y devuelve la API,
validando que sean correctos antes de procesarlos.

---

## ¿Por qué usar base de datos en lugar de listas?

Con listas, los datos se pierden al reiniciar el servidor.
Con SQLite los datos se guardan en el archivo `device_systems.db`
y persisten aunque el servidor se apague.


## Imagenes [Proyecto-Final-v1] GA1-220501096-01-AA1-EV10

Prueba 1: Ejecutar migraciones con Alembic
![alt text](/imagenes/imagen1.png)
![alt text](/imagenes/imagen2.png)

Prueba 2: Crear usuario
![alt text](/imagenes/imagen3.png)

Prueba 3: Crear dispositivo
![alt text](/imagenes/imagen4.png)

Prueba 4: Crear préstamo
![alt text](/imagenes/imagen5.png)

Prueba 5: Intentar prestar un dispositivo no disponible
![alt text](/imagenes/imagen6.png)

Prueba 6: Listar préstamos con información de usuario y dispositivo
![alt text](/imagenes/imagen7.png)

Prueba 7: Filtrar préstamos por estado
![alt text](/imagenes/imagen8.png)

Prueba 8: Filtrar préstamos por tipo de dispositivo
![alt text](/imagenes/imagen9.png)

Prueba 9: Consultar préstamos de un usuario
![alt text](/imagenes/imagen10.png)

Prueba 10: Devolver un dispositivo
![alt text](/imagenes/imagen11.png)

Prueba 11: Validar que el dispositivo vuelva a estar disponible
![alt text](/imagenes/imagen12.png)

Prueba 12: Consultar historial de préstamos del dispositivo
![alt text](/imagenes/imagen13.png)


## [Proyecto-Final-v2] GA1-220501096-01-AA1-EV11

Registro de usuario.
![alt text](/imagenes/imagen14.png)
Registro con contraseña débil.
![alt text](/imagenes/imagen15.png)
Registro con email duplicado.
![alt text](/imagen/imagen16.png)
Login correcto.
![alt text](/imagen/imagen17.png)
Login con contraseña incorrecta.
![alt text](/imagen/imagen18.png)
Consulta de /auth/me.
![alt text](/imagen/imagen20.png)
Acceso a ruta protegida sin token.
![alt text](/imagen/imagen21.png)
Acceso con token inválido.
Acceso con usuario sin permisos.
Creación de dispositivo con rol permitido.
Eliminación de dispositivo con rol no permitido.
Configuración CORS.
Cabeceras generadas por middleware.
Activación de rate limiting.
Verificación de Swagger/OpenAPI.
![alt text](/imagen/imagen19.png)
