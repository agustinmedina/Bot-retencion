# Bot de Retención — AgroSaaS 🐄

API REST con FastAPI que conecta un bot de retención de clientes ganaderos con la base de datos PostgreSQL en Supabase.

## Estructura

```
bot_retencion/
├── main.py          # FastAPI — endpoints
├── database.py      # Conexión a Supabase via REST API
├── bot_logic.py     # Lógica de respuestas fijas (ES + PT)
├── models.py        # Esquemas Pydantic
├── requirements.txt
├── .env             # Credenciales (NO subir a GitHub)
└── .env.example     # Plantilla de credenciales
```

## Requisitos

- Python 3.10 o superior (recomendado — evitar 3.14 por compatibilidad)
- Cuenta en [Supabase](https://supabase.com) con la base de datos cargada

## Instalación

```bash
# 1. Crear entorno virtual
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# 2. Instalar dependencias
pip install psycopg2-binary --only-binary=:all:
pip install fastapi uvicorn python-dotenv pydantic supabase --only-binary=:all:
```

## Configuración

Copiás el archivo `.env.example`, lo renombrás a `.env` y completás con tus credenciales de Supabase:

```
SUPABASE_URL=https://xxxxxxxxxxxx.supabase.co
SUPABASE_KEY=tu_publishable_key_aqui
```

Las credenciales las encontrás en:
**Supabase → Settings → API**

- **Project URL** → va en `SUPABASE_URL`
- **Publishable key** → va en `SUPABASE_KEY`

## Correr la API

```bash
uvicorn main:app --reload
```

La API queda disponible en: http://localhost:8000

Documentación automática (Swagger): http://localhost:8000/docs

## Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/clientes` | Lista clientes para el login |
| POST | `/login` | Login del cliente + apertura de sesión |
| POST | `/mensaje` | Enviar mensaje al bot |
| POST | `/cerrar-sesion` | Cerrar sesión de chat |

## Flujo de uso

```
1. GET  /clientes         → elegís un cliente de la base de datos
2. POST /login            → recibís saludo personalizado + id_sesion
3. POST /mensaje          → mandás mensajes, el bot responde y guarda en Supabase
4. POST /cerrar-sesion    → cerrás la sesión con resultado final
```

## Qué guarda el bot en Supabase

Cada conversación guarda automáticamente en:

- `mensajes_chat` → contenido del mensaje, idioma, etiqueta de intención, contenido en ES y PT
- `sesiones_chat` → motivo identificado por el bot, puntaje de sentimiento, si el cliente fue retenido

## Archivos a ignorar en GitHub

Crear un `.gitignore` con:

```
.env
venv/
__pycache__/
*.pyc
```
