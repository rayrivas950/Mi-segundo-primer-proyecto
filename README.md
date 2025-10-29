# Backend de Contactos

Este proyecto es una aplicación full-stack diseñada para gestionar una lista de contactos. Incluye un backend robusto construido con Flask y un frontend interactivo desarrollado con React.

## Características

*   **Autenticación de Usuarios:** Registro, inicio de sesión y cierre de sesión seguro mediante JSON Web Tokens (JWT).
*   **Gestión de Contactos (CRUD):**
    *   **Crear:** Añadir nuevos contactos con nombre, URL de imagen, notas, y múltiples números de teléfono y correos electrónicos.
    *   **Ver:** Visualizar la lista de contactos del usuario, incluyendo detalles como teléfonos, emails y fecha de creación.
    *   **Actualizar:** Editar la información de contactos existentes.
    *   **Eliminar:** Borrar contactos de la lista.
*   **Validaciones Robustas:** Validación de datos en el backend (Flask-Marshmallow) y en el frontend para asegurar la integridad de la información.
*   **Búsqueda de Contactos:** Función de búsqueda para filtrar contactos por nombre, teléfono o email.
*   **Interfaz de Usuario Intuitiva:** Diseño de tarjetas para contactos con expansión interactiva a un modal para edición y eliminación.

## Tecnologías Utilizadas

### Backend

*   **Python:** Lenguaje de programación principal.
*   **Flask:** Microframework web para la API REST.
*   **Flask-SQLAlchemy:** ORM para interactuar con la base de datos PostgreSQL.
*   **Flask-Migrate (Alembic):** Para gestionar las migraciones de la base de datos.
*   **Flask-Marshmallow:** Para serialización/deserialización y validación de datos.
*   **PyJWT:** Para la gestión de JSON Web Tokens.
*   **Flask-Limiter:** Para control de tasa de peticiones (rate limiting).
*   **Flask-CORS:** Para habilitar Cross-Origin Resource Sharing.
*   **python-dotenv:** Para la gestión de variables de entorno.

### Frontend

*   **React:** Librería de JavaScript para construir la interfaz de usuario.
*   **Axios:** Cliente HTTP para realizar peticiones a la API del backend.
*   **React Router DOM:** Para la navegación entre diferentes vistas de la aplicación.
*   **HTML/CSS:** Para la estructura y estilos de la interfaz.

## Configuración del Entorno de Desarrollo

Sigue estos pasos para configurar y ejecutar el proyecto en tu máquina local:

### 1. Clonar el Repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd backend
```

### 2. Configuración del Backend

1.  **Crear Entorno Virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  **Instalar Dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configurar Base de Datos:**
    *   Asegúrate de tener una base de datos PostgreSQL instalada y ejecutándose.
    *   Crea un archivo `.env` en la raíz del directorio `backend` con el siguiente contenido (reemplaza los valores con los de tu base de datos):
        ```
        DATABASE_URL=postgresql://user:password@host:port/database_name
        SECRET_KEY=supersecretkey # Cambia esto por una clave secreta segura
        ```

4.  **Ejecutar Migraciones de Base de Datos:**
    ```bash
    export FLASK_APP=app.py
    flask db upgrade
    ```

5.  **Iniciar el Servidor Flask:**
    ```bash
    export FLASK_APP=app.py
    flask run
    ```
    El backend estará disponible en `http://127.0.0.1:5000`.

### 3. Configuración del Frontend

1.  **Navegar al Directorio del Frontend:**
    ```bash
    cd frontend
    ```

2.  **Instalar Dependencias:**
    ```bash
    npm install
    ```

3.  **Iniciar la Aplicación React:**
    ```bash
    npm start
    ```
    El frontend se abrirá en tu navegador en `http://localhost:3000` (o un puerto similar).

## Endpoints de la API (Resumen)

*   `POST /auth/register`: Registro de nuevos usuarios.
*   `POST /auth/login`: Inicio de sesión y obtención de JWT.
*   `POST /contactos/`: Crear un nuevo contacto.
*   `GET /contactos/`: Obtener todos los contactos del usuario (con búsqueda opcional).
*   `PUT /contactos/<id>`: Actualizar un contacto existente.
*   `DELETE /contactos/<id>`: Eliminar un contacto.

## Próximas Mejoras Posibles

*   **Mejoras de UI/UX:** Refinar estilos, hacer la interfaz completamente responsiva para diferentes tamaños de pantalla.
*   **Subida de Imágenes:** Implementar la subida de archivos de imagen a un servicio de almacenamiento en la nube (ej. Amazon S3, Cloudinary) en lugar de solo URLs.
*   **Animaciones Avanzadas:** Integrar animaciones Lottie o más complejas para una experiencia de usuario más atractiva.
*   **Paginación:** Implementar paginación para la lista de contactos si el número es muy grande.
*   **Pruebas:** Añadir un conjunto de pruebas unitarias y de integración para ambos lados de la aplicación.
*   **Documentación de API:** Generar documentación automática para los endpoints del backend (ej. con Flask-RESTX).
*   **Despliegue:** Preparar scripts e instrucciones para el despliegue en entornos de producción.