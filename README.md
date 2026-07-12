# GanadoChurn 🐄📊
### Análisis de churn, sentimiento e intención para un SaaS de gestión ganadera

![Status](https://img.shields.io/badge/status-completado-success)
![Stack](https://img.shields.io/badge/stack-Python%20%7C%20SQL%20%7C%20Power%20BI%20%7C%20FastAPI-blue)
![Domain](https://img.shields.io/badge/dominio-AgTech%20%7C%20Data%20Analytics-orange)


---

## Resumen

**GanadoChurn** analiza por qué los clientes de un SaaS de gestión ganadera cancelan su suscripción, en qué momento de la conversación con el bot de retención se pierde la oportunidad de retenerlos, y qué patrones de sentimiento e intención predicen el abandono.

El proyecto se originó como asignación de **No Country** (programa de simulación de proyectos reales de datos) sobre el dataset de churn de un SaaS de ganadería. A partir de ahí, desarrollé el análisis de sentimiento/intención y el dashboard que se documenta abajo.

---

## Problema

El equipo de producto medía tasas de resolución de tickets, pero no tenía visibilidad sobre:
- **Cuándo** dentro de la conversación el cliente se frustra al punto de cancelar.
- **Qué intenciones** no logra resolver el bot pese a que el cliente da pie a una oferta.
- Si existían **diferencias entre idiomas** (español/portugués) en el manejo de la conversación.

---

## Modelo de datos

6 entidades en **PostgreSQL / Supabase**:

| Tabla | Contenido |
|---|---|
| `clientes` | Provincia, tipo de productor, tipo de contrato, antigüedad |
| `suscripciones` | Plan, ciclo de facturación, estado |
| `eventos_churn` | Categoría y motivo de cancelación, si fue retenido, oferta usada |
| `sesiones_chat` | Duración, sentimiento, si el bot identificó el motivo |
| `mensajes_chat` | Mensaje a mensaje (bilingüe ES/PT), intención etiquetada por turno |
| `interacciones_soporte` | Canal, tema, tiempo y estado de resolución |

![Modelo de datos ERD](https://github.com/agustinmedina/Bot-retencion/blob/main/capturas/1.jpg)

---

## Dashboard — hallazgos por página

**1. Executive Summary** — 80 clientes, 37,5% churn rate, 26,7% retención lograda por el bot, sentimiento promedio 0,42. *Actitud del personal* e *insatisfacción* explican más del 60% del churn.

![Resumen ejecutivo](https://github.com/agustinmedina/Bot-retencion/blob/main/capturas/2.jpg)

**2. Chatbot Performance** — el bot identifica el motivo en 65-67% de los casos, pero eso no se traduce en retención: `retention_interest` y `queja_precio` tienen la peor tasa de retención pese a ser la señal más favorable. Muchas conversaciones ya arrancan con insatisfacción; las mejoras de plan retienen mejor que los mensajes personalizados.

![Performance del chatbot](https://github.com/agustinmedina/Bot-retencion/blob/main/capturas/3.jpg)

**3. Customer Profile & Churn** — los contratos mes a mes cancelan más que los anuales; *Analítica Pro* es el plan con más bajas absolutas. Cruzar contrato + plan con retención ayuda a priorizar, ya que no es lo mismo perder un cliente básico que uno premium.

![Perfil del cliente](https://github.com/agustinmedina/Bot-retencion/blob/main/capturas/4.jpg)

**4. Support Analytics** — 217 tickets, 77,9% de resolución, 5,15 días promedio. *Facturación* y *solicitud de función* concentran volumen y peor resolución. El % de tickets sin cerrar es candidato directo a explicar parte del churn de las páginas anteriores.

![Soporte](https://github.com/agustinmedina/Bot-retencion/blob/main/capturas/5.jpg)

---

## Recomendaciones

1. Adelantar la intervención del bot al tramo 20-40% de la conversación.
2. Reforzar el guion para `retention_interest` y `queja_precio`.
3. Auditar el flujo del bot en portugués.
4. Priorizar temas de soporte con peor resolución (facturación, solicitud de función).
5. Priorizar ofertas de mejora de plan sobre mensajes genéricos.
6. Cruzar soporte y chat: los tickets sin resolver probablemente explican parte del churn.

> **Nota metodológica:** muestra de 30 sesiones / 345 mensajes / 80 clientes. Patrones direccionales — validar sobre el corpus mensual completo antes de tocar producción.

---

## Desarrollo y arquitectura técnica

*(Detalle de implementación — el análisis de datos es el foco del proyecto; esta sección documenta cómo corre por debajo.)*

### Pipeline de datos

```
                                       PostgreSQL (Supabase)
                                                │
                        ┌───────────────────────┼───────────────────────┐
                        ▼                       ▼                       ▼
              FastAPI (Railway)        Notebook de análisis      Power BI / Dashboard
              Bot de retención         SQL + sentimiento/intención   6 páginas
```

### Arquitectura de servicios

Monorepo con tres servicios independientes, cada uno en su propio contenedor **Docker** desplegado en **Railway**:

| Servicio | Función |
|---|---|
| **Backend** | API que expone los datos de clientes, suscripciones, churn y soporte |
| **Frontend** | Interfaz web para visualizar clientes, suscripciones y métricas de retención |
| **Dashboard de análisis** | Panel con indicadores de churn, efectividad del bot y salud de cuentas |

### Stack técnico

- **Backend:** Python (FastAPI)
- **Frontend:** Angular
- **Base de datos:** PostgreSQL / Supabase
- **Infraestructura:** Docker, Railway
- **Análisis de datos:** pandas, SQL (window functions, CTEs), Power BI (DAX)

🔗 **Demo en vivo:** [frontganaderiadatos.up.railway.app](https://frontganaderiadatos.up.railway.app)

### Estructura del repositorio

```
ganadochurn/
├── data/churn_clientes_ganaderia_SaaS.xlsx
├── sql/schema.sql
├── bot_retencion/{main.py, requirements.txt}
├── notebooks/analisis_sentimiento_intencion.ipynb
├── dashboard/index.html
├── screenshots/01-...08-...png
└── README.md
```

### Cómo correrlo

```bash
git clone https://github.com/tu-usuario/ganadochurn.git
cd ganadochurn/bot_retencion
pip install -r requirements.txt
uvicorn main:app --reload
```

`.env` necesario: `SUPABASE_URL`, `SUPABASE_KEY`, `DATABASE_URL`

### Despliegue

Cada uno de los tres servicios se despliega de forma independiente en Railway a partir de su propio `Dockerfile`.

```bash
# Ejemplo genérico por servicio
docker build -t nombre-servicio ./ruta-del-servicio
docker run -p PUERTO:PUERTO nombre-servicio
```

> Ver la configuración específica de variables de entorno y puertos en cada subcarpeta de servicio del repositorio.

---

## Roadmap

- [ ] Escalar el análisis al corpus mensual completo (2M+ mensajes)
- [ ] Migrar transformaciones a dbt
- [ ] Automatizar el dashboard con n8n
- [ ] Entrenar un clasificador de intención supervisado

---

## Autor

**Agustín Medina Soto** — Ingeniería Agronómica (UNNE) en transición hacia Data Analytics, en la intersección entre agro y datos.

📧 agustincorrientescapital@gmail.com · 🌐 [Portfolio](https://agustinmedina.github.io/) · 💼 [LinkedIn](https://www.linkedin.com/in/agustin-medina-soto-a1a2a7132/)

---

## Licencia

Proyecto educativo/portfolio. El dataset fue provisto en un ejercicio de simulación de No Country y no representa datos reales de clientes.

