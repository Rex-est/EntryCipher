# EntryCipher

Proyecto de Desarrollo Seguro de Software orientado a la gestión de entradas digitales con autenticación, control de sesiones y configuración segura de credenciales.

## Estructura del proyecto

```text
Backend/   API desarrollada con FastAPI
Frontend/  Interfaz web desarrollada con Angular
Database/  Recursos relacionados con la base de datos
```

## Configuración segura del backend

Antes de ejecutar el backend, crea un archivo local de variables de entorno:

```powershell
Copy-Item Backend\.env.example Backend\.env
```

Luego completa los valores reales en `Backend/.env`:

```env
DATABASE_URL=postgresql://USUARIO:CONTRASENA@HOST:5432/NOMBRE_BD
JWT_SECRET_KEY=clave_larga_y_segura
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
```

El archivo `.env` no debe subirse al repositorio, porque contiene configuraciones privadas como credenciales y claves JWT.

## Ejecución local

Desde la carpeta principal del proyecto:

```powershell
cd Backend
python -m pip install -r requirements.txt
uvicorn main:app --reload
```

La API se ejecutará en:

```text
http://127.0.0.1:8000
```

## Pruebas automatizadas

Desde la carpeta `Backend`:

```powershell
python -m pip install pytest
python -m pytest -q
```

## Controles de seguridad aplicados

- La clave JWT y la conexión a la base de datos se cargan mediante variables de entorno.
- Los secretos no se almacenan directamente en el código fuente.
- Los tokens JWT tienen una duración máxima de 15 minutos.
- Cada token incluye un identificador único de sesión (`jti`).
- Las pruebas usan configuraciones aisladas y una base SQLite local.
## Variables de entorno en Render

Antes de fusionar cambios que dependan de configuración sensible, se deben registrar las variables de entorno en el panel de Render para ambos servicios backend:

- `entrycipher-backend`
- `entrycipher-backend-dev`

Variables requeridas:

```text
DATABASE_URL
JWT_SECRET_KEY
JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES
