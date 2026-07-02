



PROBLEMA:

Problema
Build a sentiment and intent analysis system on the corpus of support conversations to identify when users become frustrated, which intentions are not being resolved, and what patterns predict escalation or abandonment.

Descripción
ConversaAI processes over 2 million messages per month. Currently, resolution rates are measured, but emotional tone and whether user intent is being accurately captured are not understood. This makes it difficult to improve workflows because there is no clear data on where they are failing.

Expectations
Text processing pipeline for conversations in Spanish and Portuguese. Sentiment classification model with evaluation metrics. Intent detection model. Insights dashboard with top unresolved intentions and moments of greatest frustration. Report with actionable recommendations for conversational workflows.

Users
ConversaAI product team that designs and improves conversational workflows. Data analyst who processes the corpus monthly.

Flows
Analyst loads the month's conversation corpus → the pipeline cleans and processes the texts → the models classify each message by sentiment and intent → the system aggregates the results → the dashboard displays the most relevant patterns → the product team identifies the flows with the most frustration → prioritizes improvements for the next sprint.




----------------


# 📊 Documentación Funcional – Dashboard de Churn y Efectividad del Chatbot

# Objetivo del proyecto

Desarrollar un dashboard interactivo que permita analizar las causas del abandono (Churn), evaluar la efectividad del chatbot de retención y brindar información accionable para reducir la pérdida de clientes.

El dashboard permitirá identificar qué factores influyen en el abandono, cómo interactúan los clientes con el chatbot y qué estrategias de retención generan mejores resultados.

---

# Problema de negocio

La empresa cuenta con un chatbot diseñado para detectar clientes con intención de cancelar su suscripción e intentar retenerlos mediante distintas estrategias (descuentos, mejora de plan, mes gratis, entre otras).

Actualmente existen registros de clientes, suscripciones, eventos de churn, conversaciones con el chatbot, mensajes intercambiados e interacciones con soporte.

Sin embargo, la empresa no posee una visión integrada que permita responder preguntas como:

- ¿Por qué abandonan los clientes?
- ¿Qué tan efectivo es el chatbot para evitar el churn?
- ¿Qué motivos de abandono son más frecuentes?
- ¿Qué ofertas funcionan mejor?
- ¿Existe relación entre el sentimiento del cliente y la retención?
- ¿Cómo influye el soporte en el abandono?

El objetivo es centralizar esta información mediante un dashboard de Business Intelligence.

---

# Preguntas de negocio

- ¿Cuál es la tasa de abandono de clientes?
- ¿Cuál es la tasa de retención lograda por el chatbot?
- ¿Cuáles son las principales causas de churn?
- ¿Qué porcentaje de clientes logra retener el chatbot?
- ¿Qué ofertas de retención tienen mayor éxito?
- ¿Qué tan preciso es el chatbot identificando la intención del cliente?
- ¿Qué sentimiento presentan los clientes durante la conversación?
- ¿Qué tipo de clientes presentan mayor riesgo de abandono?
- ¿Existe relación entre soporte, sentimiento y churn?
- ¿Qué segmentos de clientes presentan mayor probabilidad de cancelar?

---

# KPIs

## Churn

### Tasa de abandono (Churn Rate)

**Descripción**

Porcentaje de clientes que abandonaron el servicio.

**Fórmula**

Clientes con churn / Total de clientes × 100

**Visualización**

Card

---

### Total de eventos de churn

**Descripción**

Cantidad total de abandonos registrados.

**Visualización**

Card

---

### Motivos de abandono

**Descripción**

Distribución de los motivos por los cuales los clientes cancelan.

**Visualización**

Barras horizontales

---

### Categorías de churn

**Descripción**

Agrupa los abandonos según la categoría principal.

- Precio
- Competidor
- Insatisfacción
- Actitud
- Otro

**Visualización**

Barras

---

## Retención del chatbot

### Tasa de retención del chatbot

**Descripción**

Porcentaje de clientes retenidos luego de interactuar con el chatbot.

**Fórmula**

Clientes retenidos / Total de conversaciones de retención ×100

**Visualización**

Card

---

### Clientes retenidos

Cantidad de clientes retenidos.

Visualización:

Card

---

### Clientes no retenidos

Cantidad de clientes que igualmente abandonaron.

Visualización:

Card

---

### Ofertas de retención más efectivas

Comparar:

- Mejora de plan
- Mes gratis
- Descuento

Visualización:

Barras

---

### Retención por categoría de churn

Ejemplo:

- Precio
- Competidor
- Insatisfacción

Visualización:

Columnas agrupadas

---

## Chatbot

### Conversaciones analizadas

Cantidad total de sesiones del chatbot.

Visualización:

Card

---

### Total de conversaciones frustradas

Conversaciones donde el cliente finalmente no fue retenido.

Visualización:

Card

---

### Bot Identification Rate

Porcentaje de conversaciones donde el chatbot identificó correctamente la intención del cliente.

Fórmula

motivo_identificado_bot = TRUE

/

Total sesiones

Visualización

Card

---

### Puntaje promedio de sentimiento

Promedio del puntaje de sentimiento obtenido durante las conversaciones.

Visualización

Card

---

### Sentimiento promedio por resultado

Comparar sentimiento de

- Clientes retenidos
- Clientes no retenidos

Visualización

Columnas

---

### Intenciones detectadas

Mostrar frecuencia de

- intención_cancelación
- problema_servicio
- queja_precio
- mención_competidor
- retention_interest

Visualización

Barras

---

### Mensajes promedio por conversación

Promedio de mensajes intercambiados por sesión.

Visualización

Card

---

## Clientes

### Clientes por tipo de contrato

Visualización

Barras

---

### Clientes por plan

Visualización

Barras

---

### Clientes por provincia

Visualización

Mapa o barras

---

### Clientes por segmento demográfico

Visualización

Donut

---

### Antigüedad promedio

Visualización

Card

---

## Soporte

### Tickets por canal

Visualización

Donut

---

### Temas más frecuentes

Visualización

Barras

---

### Tasa de resolución

Fórmula

Tickets resueltos / Total tickets ×100

Visualización

Card

---

### Tiempo promedio de resolución

Visualización

Card

---

# Páginas del Dashboard

## Página 1 — Resumen Ejecutivo

Indicadores:

- Total clientes
- Churn Rate
- Tasa de retención
- Conversaciones analizadas
- Conversaciones frustradas
- Sentimiento promedio

Gráficos:

- Motivos de churn
- Categorías de churn
- Retención por categoría

---

## Página 2 — Análisis del Chatbot

Indicadores:

- Bot Identification Rate
- Clientes retenidos
- Clientes no retenidos
- Mensajes promedio
- Sentimiento promedio

Gráficos:

- Intenciones detectadas
- Sentimiento vs Retención
- Ofertas de retención
- Mensajes por conversación

---

## Página 3 — Perfil del Cliente

Gráficos:

- Tipo de contrato
- Tipo de plan
- Provincia
- Segmento demográfico
- Antigüedad

---

## Página 4 — Soporte

Indicadores:

- Tasa de resolución
- Tiempo promedio

Gráficos:

- Tickets por canal
- Temas más frecuentes
- Tickets resueltos vs no resueltos

---

# Medidas DAX

## Clientes

Total Clientes

DISTINCTCOUNT(Clientes[id_cliente])

---

Clientes con Churn

DISTINCTCOUNT(eventos_churn[id_cliente])

---

Churn Rate

DIVIDE([Clientes con Churn],[Total Clientes])

---

Clientes Retenidos

CALCULATE(

COUNTROWS(sesiones_chat),

sesiones_chat[cliente_retenido]="VERDADERO"

)

---

Clientes No Retenidos

CALCULATE(

COUNTROWS(sesiones_chat),

sesiones_chat[cliente_retenido]="FALSO"

)

---

Tasa de Retención

DIVIDE(

[Clientes Retenidos],

[Clientes Retenidos]+[Clientes No Retenidos]

)

---

Conversaciones Analizadas

COUNTROWS(sesiones_chat)

---

Conversaciones Frustradas

CALCULATE(

COUNTROWS(sesiones_chat),

sesiones_chat[cliente_retenido]="FALSO"

)

---

Sentimiento Promedio

AVERAGE(sesiones_chat[puntaje_sentimiento])

---

Mensajes Promedio

AVERAGE(sesiones_chat[total_mensajes])

---

Bot Identification Rate

DIVIDE(

CALCULATE(

COUNTROWS(sesiones_chat),

sesiones_chat[motivo_identificado_bot]="VERDADERO"

),

COUNTROWS(sesiones_chat)

)

---

Tiempo Promedio Resolución

AVERAGE(interacciones_soporte[días_resolución])

---

Tasa Resolución

DIVIDE(

CALCULATE(

COUNTROWS(interacciones_soporte),

interacciones_soporte[resuelto]="VERDADERO"

),

COUNTROWS(interacciones_soporte)

)


-----------------



primer mockup (html vanilla) :