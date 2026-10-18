# Módulo de Catálogo: Libros y Ejemplares

Módulo de administración del inventario bibliográfico del sistema de biblioteca (Laboratorio de Bases de Datos). Permite gestionar libros y ejemplares físicos, buscar en el catálogo y consultar la disponibilidad.

**Tecnologías:** Python 3, Flask, MySQL 8 (`mysql-connector-python`), plantillas Jinja2.

## Funcionalidades

**Libros (CRUD)**
- Registrar, consultar, editar y eliminar libros.
- Campos: ISBN, título, autores, editorial, año, categorías y descripción.
- Los autores se escriben separados por coma; si no existen, se crean automáticamente.
- Guardar un libro con sus autores y categorías se hace en una sola transacción.
- Un libro **no se puede eliminar** si tiene ejemplares o préstamos asociados.

**Ejemplares (CRUD)**
- Registrar, consultar, editar y eliminar ejemplares físicos.
- Campos: código de barras, ubicación (sala/estante) y estado (`DISPONIBLE`, `PRESTADO`, `PERDIDO`).
- El estado `PRESTADO` lo gestiona el módulo de préstamos, por lo que no se puede asignar ni modificar manualmente desde este módulo.
- Un ejemplar prestado, o con historial de préstamos, no se puede eliminar (se marca como `PERDIDO`).

**Búsqueda y disponibilidad**
- Búsqueda por título, autor, ISBN o categoría.
- Filtro "solo disponibles".
- Cada resultado muestra los ejemplares disponibles frente al total (por ejemplo, "1 de 3").

## Reglas de negocio e integridad

- Un libro puede tener varios autores y varias categorías (tablas `libro_autor` y `libro_categoria`).
- La disponibilidad no se almacena: se calcula contando los ejemplares en estado `DISPONIBLE`.
- El ISBN y el código de barras son únicos; los errores se muestran con mensajes claros.
- El año debe estar entre 1400 y 2100 y el estado debe ser válido (restricciones `CHECK` de la base de datos).
- Al eliminar un libro, sus vínculos con autores y categorías se eliminan por `ON DELETE CASCADE`.

## Estructura

```
catalogo/
├── app.py            # Punto de entrada de Flask
├── catalogo.py       # Blueprint: rutas, búsqueda y lógica de libros/ejemplares
├── db.py             # Conexión a MySQL
├── requirements.txt
└── templates/        # Vistas HTML (lista, detalle, formularios)
```

El módulo está definido como un `Blueprint` de Flask, así que se integra con los demás módulos del proyecto registrándolo en la aplicación principal:

```python
from catalogo import bp as catalogo_bp
app.register_blueprint(catalogo_bp)
```

## Requisitos

- Python 3.9 o superior
- MySQL 8.0.16 o superior (necesario para las restricciones `CHECK`)
- MySQL Workbench (opcional, para cargar el script)

## Instalación y ejecución

1. **Cargar la base de datos.** En MySQL Workbench: abrir la conexión, ir a *File → Open SQL Script…*, seleccionar `Lab1.sql` y ejecutarlo completo con el icono del rayo. Esto crea `biblioteca_db` con datos de ejemplo (volver a ejecutarlo la reinicia).

2. **Crear el entorno virtual e instalar dependencias.**

   Windows:
   ```
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
   Mac/Linux:
   ```
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configurar la conexión.** Por defecto se usa `root`, contraseña vacía, `localhost:3306` y la base `biblioteca_db`. Para cambiarlo, define variables de entorno (no subas contraseñas al repositorio):

   | Variable | Valor por defecto |
   |---|---|
   | `DB_HOST` | `localhost` |
   | `DB_PORT` | `3306` |
   | `DB_USER` | `root` |
   | `DB_PASSWORD` | *(vacío)* |
   | `DB_NAME` | `biblioteca_db` |

   Ejemplo en PowerShell: `$env:DB_PASSWORD="tu_contraseña"`
   Ejemplo en Mac/Linux: `export DB_PASSWORD=tu_contraseña`

4. **Iniciar la aplicación.**
   ```
   python app.py
   ```
   Abrir **http://127.0.0.1:5000** en el navegador. Debe usarse `http://` (no `https://`), porque el servidor de desarrollo de Flask no usa HTTPS.

## Rutas y endpoints

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/libros` | Listado y búsqueda (`?q=...&campo=titulo\|autor\|isbn\|categoria&solo_disp=1`) |
| GET/POST | `/libros/nuevo` | Registrar libro |
| GET | `/libros/<id>` | Detalle del libro y sus ejemplares |
| GET/POST | `/libros/<id>/editar` | Editar libro |
| POST | `/libros/<id>/eliminar` | Eliminar libro |
| GET/POST | `/libros/<id>/ejemplares/nuevo` | Registrar ejemplar |
| GET/POST | `/ejemplares/<id>/editar` | Editar ejemplar |
| POST | `/ejemplares/<id>/eliminar` | Eliminar ejemplar |
| GET | `/api/libros` | Búsqueda en JSON (mismos parámetros que `/libros`) |
| GET | `/api/libros/<id>/disponibilidad` | Cantidad de ejemplares por estado (JSON) |
