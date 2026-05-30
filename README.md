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