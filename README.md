# Configuraciones necesarias para montar el proyecto

## 1. Pasos previos (Base de Datos y VS Code)
1. Crear la base de datos en **PostgreSQL** (por ejemplo, `proyectosuper`).
2. Instalar la extensión **PostgreSQL** en **VS Code**.
3. Abrir el panel de PostgreSQL en la barra lateral de VS Code, hacer clic en **Add Connection** (`+`) y conectarse usando las mismas credenciales locales que pondrás en tu `.env` (`localhost`, puerto `5432`, nombre de la BD, usuario y contraseña).

---

## 2. Configurar variables de entorno (`.env`)
1. Ubicarse en la carpeta `backend/` del proyecto.
2. Copiar el archivo `.env.example` y renombrarlo a `.env` (nunca subir el `.env` real al repositorio).
3. Completar el archivo `.env` con las credenciales de tu entorno local:

```env.example
DB_HOST=localhost
DB_PORT=5432
DB_NAME=proyectosuper
DB_USER=postgres
DB_PASSWORD=tu_password_local
```

---

## 3. Configuración del entorno virtual de Python (Backend)
1. Ubicarse en la carpeta `backend` del proyecto:
   ```bash
   cd backend
   ```
2. Crear y activar el entorno virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate      # En Linux / macOS
   .\venv\Scripts\Activate.ps1   # En Windows (PowerShell)
   ```
3. Instalar las dependencias necesarias desde `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
4. Levantar el servidor de desarrollo de FastAPI:
   ```bash
   uvicorn app.main:app --reload
   ```
   *(El backend quedará corriendo normalmente en `http://localhost:8000`).*

---

## 4. Configuración del entorno de React (Frontend)

### Opción A: Cuando el proyecto de React YA existe en el repositorio (lo habitual al hacer `git pull`)
1. Ubicarse en la carpeta `frontend`:
   ```bash
   cd frontend
   ```
2. Instalar las dependencias del proyecto:
   ```bash
   npm install
   ```
3. Levantar el servidor de desarrollo:
   ```bash
   npm run dev
   ```
   *(El frontend quedará corriendo normalmente en `http://localhost:5173`. Para detenerlo en la terminal, presionar `Ctrl + C`).*

### Opción B: Solo si se inicializa la carpeta `frontend` desde cero
1. Ubicarse en la carpeta `frontend` y ejecutar:
   ```bash
   npm create vite@latest .
   ```
2. Seleccionar en el asistente interactivo:
   * **Framework:** `React`
   * **Variant:** `JavaScript`
   * **Linter:** `ESLint`
   * **Install with npm and start now?:** `Yes` *(si eliges `No`, ejecuta manualmente `npm install` y luego `npm run dev`)*.

---

## 5. Flujo de trabajo con Git (Ramas por módulo)
1. Actualizar la rama principal antes de empezar a trabajar:
   ```bash
   git checkout main
   git pull origin main
   ```
2. Crear una rama nueva para tu módulo asignado:
   ```bash
   git checkout -b feat/nombre-del-modulo
   ```
3. Hacer pruebas en local y subir cambios únicamente a tu rama:
   ```bash
   git add .
   git commit -m "Descripción clara de los cambios"
   git push origin feat/nombre-del-modulo
   ```