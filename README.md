# Bot-retención — Plataforma de análisis de churn (Ganadería SaaS)

Monorepo con tres servicios desplegados en **Railway** mediante **Docker**, orientado a analizar y predecir la cancelación (*churn*) de clientes de una plataforma SaaS de ganadería, con un bot conversacional de retención integrado.

🔗 **Demo en vivo:** [frontganaderiadatos.up.railway.app](https://frontganaderiadatos.up.railway.app)

---

## 📋 Descripción

El sistema centraliza la información de clientes, suscripciones, eventos de cancelación e interacciones de soporte de una empresa SaaS agropecuaria (gestión de rodeos, analítica ganadera), con un enfoque particular en el **bot de retención**: un chat automatizado que interviene cuando un cliente inicia el proceso de baja, identifica el motivo y intenta ofrecer una alternativa antes de perderlo.

### Arquitectura

El proyecto está organizado como monorepo con tres servicios independientes:

| Servicio | Función |
|---|---|
| **Backend** | API que expone los datos de clientes, suscripciones, churn y soporte |
| **Frontend** | Interfaz web para visualizar clientes, suscripciones y métricas de retención |
| **Dashboard de análisis** | Panel con indicadores de churn, efectividad del bot y salud de cuentas |

Cada servicio corre en su propio contenedor **Docker**, desplegado como servicio independiente en **Railway**.

---

## 🗂️ Modelo de datos

La base de datos se organiza en 6 tablas principales:

### `clientes`
Datos de cada cuenta SaaS: empresa, provincia, tipo de productor (Cría, Tambo, Engorde a Corral, Ganadería de Carne, Mixto), tamaño de rodeo, tipo de contrato, método de pago, antigüedad y segmento demográfico.

### `suscripciones`
Plan contratado por cada cliente (Analítica Básica / Estándar / Pro, Empresarial), cargo mensual, ciclo de facturación, fechas de inicio/fin, estado de actividad y consumo de datos (GB promedio mensual, cargos por datos extra).

### `eventos_churn`
Registro de cada cancelación: fecha, categoría y motivo del churn, si el cliente fue retenido, fecha de retención y oferta utilizada para retenerlo.

### `sesiones_chat`
Sesiones del **bot de retención**: vínculo al evento de churn correspondiente, duración, cantidad de mensajes, motivo identificado automáticamente por el bot, si el cliente fue retenido en esa sesión y un puntaje de sentimiento.

### `mensajes_chat`
Mensajes individuales de cada sesión (bot / cliente), con contenido original, idioma detectado, traducciones (español / portugués) y etiqueta de intención.

### `interacciones_soporte`
Historial de contactos de soporte por canal (chat, email, etc.), tema, si fue resuelto y días de resolución.

**Relaciones principales:**
```
clientes 1─N suscripciones
clientes 1─N eventos_churn
clientes 1─N interacciones_soporte
eventos_churn 1─1 sesiones_chat
sesiones_chat 1─N mensajes_chat
```

---

## 🤖 Bot de retención

El componente central del proyecto: cuando un cliente da señales de cancelar (o cancela efectivamente), se dispara una sesión de chat automatizada que:

1. Conversa con el cliente para identificar el motivo real de la baja
2. Clasifica la intención del mensaje (`etiqueta_intencion`)
3. Evalúa el sentimiento de la conversación
4. Ofrece una alternativa de retención cuando corresponde (cambio de plan, descuento, etc.)
5. Registra si la retención fue exitosa

Los mensajes se procesan en múltiples idiomas (español/portugués), reflejando la operación de la plataforma en distintos países de la región.

---

## 🛠️ Stack técnico

- **Backend:** Python
- **Frontend:** Angular
- **Base de datos:** PostgreSQL / Supabase
- **Infraestructura:** Docker, Railway
- **Análisis de datos:** pandas, SQL (window functions, CTEs)

---

## 🚀 Despliegue

Cada uno de los tres servicios se despliega de forma independiente en Railway a partir de su propio `Dockerfile`.

```bash
# Ejemplo genérico por servicio
docker build -t nombre-servicio ./ruta-del-servicio
docker run -p PUERTO:PUERTO nombre-servicio
```

> Ver la configuración específica de variables de entorno y puertos en cada subcarpeta de servicio del repositorio.

---

## 📊 Casos de uso analítico

Este dataset permite responder preguntas como:

- ¿Qué motivo de churn es más frecuente por tipo de productor o provincia?
- ¿Qué tasa de éxito tiene el bot de retención según el motivo identificado?
- ¿Existe correlación entre consumo de GB, plan contratado y probabilidad de churn?
- ¿Cuántas interacciones de soporte previas anticipan una cancelación?

---

## 👤 Autor

**Agustín Medina Soto**
[GitHub](https://github.com/agustinmedina) · [LinkedIn](https://www.linkedin.com/in/agustin-medina-soto-a1a2a7132/) · [Portfolio](https://agustinmedina.github.io)
