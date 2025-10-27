# Backend de Gestión de Contactos

Este es el backend para una aplicación web de gestión de contactos, construido con Flask, PostgreSQL y autenticación JWT.

## Características

*   Autenticación de usuarios (registro, inicio de sesión, cierre de sesión, refresco de tokens)
*   Gestión de contactos (crear, leer, actualizar, eliminar)
*   Búsqueda de contactos por nombre, teléfono o correo electrónico
*   Los contactos están asociados a los usuarios
*   **Limitación de Tasas:** Implementada en los endpoints de autenticación para prevenir ataques de fuerza bruta.
*   **Validación de Datos:** Validación de entrada y serialización de salida usando Marshmallow.

## Configuración

**Requiere Python 3.9 o superior**

1.  **Clonar el repositorio:**
    ```bash
    git clone <url_del_repositorio>
    cd backend
    ```
2.  **Crear y activar un entorno virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    # Para desactivar:
    # deactivate
    ```
3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configurar variables de entorno:**
    Crea un archivo `.env` en el directorio raíz con el siguiente contenido, reemplazando los marcadores de posición con tus valores reales:
    ```
    SECRET_KEY=tu_clave_secreta_muy_fuerte_y_aleatoria_aqui
    DB_HOST=localhost
    DB_NAME=contactosdb
    DB_USER=tu_usuario_db
    DB_PASS=tu_contraseña_db
    ```
    **Nota:** Reemplaza `tu_clave_secreta_muy_fuerte_y_aleatoria_aqui` con una clave fuerte y generada aleatoriamente.

5.  **Configuración de la Base de Datos:**
    Asegúrate de que tu servidor PostgreSQL esté funcionando.
    Aplica las migraciones para configurar el esquema de la base de datos:
    ```bash
    FLASK_APP=app.py flask db upgrade
    ```

6.  **Configuración de Redis:**
    Para la funcionalidad de limitación de tasas, se requiere un servidor Redis. Asegúrate de que Redis esté funcionando y sea accesible en `localhost:6379`.

## Ejecutar la Aplicación

```bash
source venv/bin/activate
FLASK_APP=app.py flask run
```

La API estará disponible en `http://127.0.0.1:5000`.

**Importante:** Para despliegues en producción, asegúrate de que tu aplicación se sirva a través de HTTPS para proteger los datos sensibles en tránsito.

## Pruebas

Para ejecutar las pruebas automatizadas:

```bash
source venv/bin/activate
export PYTHONPATH=$(pwd) # O la ruta absoluta a la raíz de tu proyecto
pytest
```

## Endpoints de la API

### Autenticación

*   **"POST /auth/register"**: Registrar un nuevo usuario.
    *   Cuerpo de la solicitud: `{"username": "tu_nombre_de_usuario", "password": "tu_contraseña"}`
    *   Respuesta: `{"message": "Usuario creado"}` o `{"errors": {"username": ["La validación de longitud falló"]}}` en caso de error.
*   **"POST /auth/login"**: Iniciar sesión y obtener tokens de acceso y refresco.
    *   Cuerpo de la solicitud: `{"username": "tu_nombre_de_usuario", "password": "tu_contraseña"}`
    *   Respuesta: `{"access_token": "tu_token_de_acceso", "refresh_token": "tu_token_de_refresco"}`.
*   **"POST /auth/logout"**: Invalidar el token de acceso actual.
    *   Requiere: Encabezado `Authorization: Bearer <token_de_acceso>` válido.
    *   Respuesta: `{"message": "Sesión cerrada exitosamente"}`.
*   **"POST /auth/refresh"**: Intercambiar un token de refresco válido por nuevos tokens de acceso y refresco.
    *   Cuerpo de la solicitud: `{"refresh_token": "tu_token_de_refresco"}`
    *   Respuesta: `{"access_token": "nuevo_token_de_acceso", "refresh_token": "nuevo_token_de_refresco"}`.

### Contactos

Todos los endpoints de contactos requieren un **token de acceso** válido en el encabezado `Authorization` (por ejemplo, `Authorization: Bearer <tu_token_de_acceso>`).

*   **"POST /contactos/"**: Crear un nuevo contacto.
    *   Cuerpo de la solicitud: `{"nombre": "Nombre del Contacto", "telefonos": [{"telefono": "123-456-7890"}], "emails": [{"email": "correo@ejemplo.com"}]}`
    *   Respuesta: `{"id": 1, "nombre": "Nombre del Contacto", ...}` (objeto de contacto serializado).
*   **"GET /contactos/"**: Obtener todos los contactos del usuario autenticado.
    *   Parámetro de consulta opcional: `?search=palabra_clave` (busca por nombre, teléfono o correo electrónico)
    *   Respuesta: `[...]` (lista de objetos de contacto serializados).
*   **"PUT /contactos/<id>"**: Actualizar un contacto existente.
    *   Cuerpo de la solicitud: `{"nombre": "Nuevo Nombre", "telefonos": [{"telefono": "nuevo-telefono"}], "emails": [{"email": "nuevo-correo"}]}` (se permiten actualizaciones parciales).
    *   Respuesta: `{"id": 1, "nombre": "Nuevo Nombre", ...}` (objeto de contacto actualizado serializado).
*   **"DELETE /contactos/<id>"**: Eliminar un contacto.
    *   Respuesta: `{"message": "Contacto eliminado"}`.
