# Contact Management Backend

This is the backend for a contact management web application, built with Flask, PostgreSQL, and JWT authentication.

## Features

*   User authentication (register, login)
*   Contact management (create, read, update, delete)
*   Search contacts by name, phone, or email
*   Contacts are associated with users

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd backend
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure environment variables:**
    Create a `.env` file in the root directory with the following content, replacing placeholders with your actual values:
    ```
    SECRET_KEY=your_very_strong_and_random_secret_key_here
    DB_HOST=localhost
    DB_NAME=contactosdb
    DB_USER=your_db_user
    DB_PASS=your_db_password
    ```
    **Note:** Replace `your_very_strong_and_random_secret_key_here` with a strong, randomly generated key.

5.  **Database Setup:**
    The application will automatically create the necessary tables when it starts. Ensure your PostgreSQL server is running and accessible with the credentials provided in `.env`.

## Running the Application

```bash
source venv/bin/activate
FLASK_APP=app.py flask run
```

The API will be available at `http://127.0.0.1:5000`.

## API Endpoints

### Authentication

*   **`POST /auth/register`**: Register a new user.
    *   Request Body: `{"username": "your_username", "password": "your_password"}`
*   **`POST /auth/login`**: Log in and get a JWT token.
    *   Request Body: `{"username": "your_username", "password": "your_password"}`
    *   Response: `{"token": "your_jwt_token"}`

### Contacts

All contact endpoints require a valid JWT token in the `Authorization` header (e.g., `Authorization: Bearer <your_jwt_token>`).

*   **`POST /contactos/`**: Create a new contact.
    *   Request Body: `{"nombre": "Contact Name", "telefonos": ["123-456-7890"], "emails": ["email@example.com"]}`
*   **`GET /contactos/`**: Get all contacts for the authenticated user.
    *   Optional Query Parameter: `?search=keyword` (searches by name, phone, or email)
*   **`PUT /contactos/<id>`**: Update an existing contact.
    *   Request Body: `{"nombre": "New Name", "telefonos": ["new-phone"], "emails": ["new-email"]}`
*   **`DELETE /contactos/<id>`**: Delete a contact.

---

# Backend de Gestión de Contactos

Este es el backend para una aplicación web de gestión de contactos, construida con Flask, PostgreSQL y autenticación JWT.

## Características

*   Autenticación de usuarios (registro, inicio de sesión)
*   Gestión de contactos (crear, leer, actualizar, eliminar)
*   Búsqueda de contactos por nombre, teléfono o correo electrónico
*   Los contactos están asociados a los usuarios

## Configuración

1.  **Clonar el repositorio:**
    ```bash
    git clone <url_del_repositorio>
    cd backend
    ```
2.  **Crear y activar un entorno virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
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
    La aplicación creará automáticamente las tablas necesarias cuando se inicie. Asegúrate de que tu servidor PostgreSQL esté funcionando y sea accesible con las credenciales proporcionadas en `.env`.

## Ejecutar la Aplicación

```bash
source venv/bin/activate
FLASK_APP=app.py flask run
```

La API estará disponible en `http://127.0.0.1:5000`.

## Endpoints de la API

### Autenticación

*   **`POST /auth/register`**: Registrar un nuevo usuario.
    *   Cuerpo de la solicitud: `{"username": "tu_nombre_de_usuario", "password": "tu_contraseña"}`
*   **`POST /auth/login`**: Iniciar sesión y obtener un token JWT.
    *   Cuerpo de la solicitud: `{"username": "tu_nombre_de_usuario", "password": "tu_contraseña"}`
    *   Respuesta: `{"token": "tu_token_jwt"}`

### Contactos

Todos los endpoints de contactos requieren un token JWT válido en el encabezado `Authorization` (por ejemplo, `Authorization: Bearer <tu_token_jwt>`).

*   **`POST /contactos/`**: Crear un nuevo contacto.
    *   Cuerpo de la solicitud: `{"nombre": "Nombre del Contacto", "telefonos": ["123-456-7890"], "emails": ["correo@ejemplo.com"]}`
*   **`GET /contactos/`**: Obtener todos los contactos del usuario autenticado.
    *   Parámetro de consulta opcional: `?search=palabra_clave` (busca por nombre, teléfono o correo electrónico)
*   **`PUT /contactos/<id>`**: Actualizar un contacto existente.
    *   Cuerpo de la solicitud: `{"nombre": "Nuevo Nombre", "telefonos": ["nuevo-telefono"], "emails": ["nuevo-correo"]}`
*   **`DELETE /contactos/<id>`**: Eliminar un contacto.