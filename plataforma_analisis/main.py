from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from utils.logger import logger
from models import (
    Respuesta_Dashboard, Coordenada_Cluster, Detalle_Chat,
    Mensaje_Chat, Detalle_Palabra_SHAP, Prompt_Regla, Resultado_Regla
)

app = FastAPI(
    title="Plataforma de Análisis — AgroSaaS",
    description="API de análisis offline con clustering y explicabilidad SHAP para AgroSaaS",
    version="1.0.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MOCK DATA ---

mock_dashboard = Respuesta_Dashboard(
    total_clientes=1200,
    tasa_abandono=12.5,
    tasa_retencion=68.2,
    conversaciones_analizadas=340,
    conversaciones_frustradas=108,
    sentimiento_promedio=0.25,
    motivos_churn={
        "Precio": 45,
        "Competidor": 30,
        "Insatisfacción": 15,
        "Actitud": 10
    },
    retencion_por_oferta={
        "Descuento": 72.5,
        "Mes Gratis": 85.0,
        "Mejora Plan": 50.0
    }
)

mock_clusters = [
    Coordenada_Cluster(
        id_sesion="sesion-1111", x=-1.25, y=0.45,
        categoria="Precio", sentimiento_promedio=-0.65,
        texto_resumen="Quejas reiteradas sobre el aumento en el cargo mensual"
    ),
    Coordenada_Cluster(
        id_sesion="sesion-2222", x=-0.85, y=1.20,
        categoria="Competidor", sentimiento_promedio=-0.40,
        texto_resumen="Menciones de migración a competidores por mejor oferta"
    ),
    Coordenada_Cluster(
        id_sesion="sesion-3333", x=1.10, y=-0.50,
        categoria="Insatisfacción", sentimiento_promedio=-0.75,
        texto_resumen="Molestias con la velocidad de resolución en soporte"
    ),
    Coordenada_Cluster(
        id_sesion="sesion-4444", x=0.50, y=0.30,
        categoria="Precio", sentimiento_promedio=0.10,
        texto_resumen="Dudas generales sobre tarifas resueltas con descuento"
    )
]

mock_detalles_chat = {
    "sesion-1111": Detalle_Chat(
        id_sesion="sesion-1111",
        nombre_empresa="Estancia Las Lilas",
        provincia="Buenos Aires",
        tipo_contrato="Mensual",
        cliente_retenido=False,
        puntaje_sentimiento=-0.65,
        conversacion=[
            Mensaje_Chat(
                id_mensaje="msg-101", rol_remitente="cliente",
                contenido="Hola, quiero cancelar la suscripción porque el precio es muy alto.",
                hora_envio="2026-06-29T10:00:00", etiqueta_intencion="intención_cancelación",
                palabras_clave_shap=[
                    Detalle_Palabra_SHAP(palabra="cancelar", impacto=-0.85),
                    Detalle_Palabra_SHAP(palabra="precio", impacto=-0.75),
                    Detalle_Palabra_SHAP(palabra="alto", impacto=-0.40)
                ]
            ),
            Mensaje_Chat(
                id_mensaje="msg-102", rol_remitente="bot",
                contenido="Hola. Entiendo tu preocupación. ¿Te gustaría un descuento del 20%?",
                hora_envio="2026-06-29T10:00:05", etiqueta_intencion="ofrecer_descuento",
                palabras_clave_shap=[]
            ),
            Mensaje_Chat(
                id_mensaje="msg-103", rol_remitente="cliente",
                contenido="No me sirve, prefiero dar de baja el servicio hoy mismo.",
                hora_envio="2026-06-29T10:01:00", etiqueta_intencion="intención_cancelación",
                palabras_clave_shap=[
                    Detalle_Palabra_SHAP(palabra="baja", impacto=-0.90),
                    Detalle_Palabra_SHAP(palabra="servicio", impacto=-0.20)
                ]
            )
        ]
    ),
    "sesion-2222": Detalle_Chat(
        id_sesion="sesion-2222",
        nombre_empresa="AgroGanadera del Sur",
        provincia="Córdoba",
        tipo_contrato="Anual",
        cliente_retenido=True,
        puntaje_sentimiento=-0.20,
        conversacion=[
            Mensaje_Chat(
                id_mensaje="msg-201", rol_remitente="cliente",
                contenido="La competencia me ofrece lo mismo por la mitad de tarifa.",
                hora_envio="2026-06-29T11:15:00", etiqueta_intencion="mención_competidor",
                palabras_clave_shap=[
                    Detalle_Palabra_SHAP(palabra="competencia", impacto=-0.65),
                    Detalle_Palabra_SHAP(palabra="mitad", impacto=-0.50),
                    Detalle_Palabra_SHAP(palabra="tarifa", impacto=-0.30)
                ]
            ),
            Mensaje_Chat(
                id_mensaje="msg-202", rol_remitente="bot",
                contenido="Entiendo. Podemos darte 1 mes gratis para compensar.",
                hora_envio="2026-06-29T11:15:10", etiqueta_intencion="ofrecer_mes_gratis",
                palabras_clave_shap=[]
            ),
            Mensaje_Chat(
                id_mensaje="msg-203", rol_remitente="cliente",
                contenido="Bueno, acepto la oferta y seguimos con el plan.",
                hora_envio="2026-06-29T11:16:00", etiqueta_intencion="retention_interest",
                palabras_clave_shap=[
                    Detalle_Palabra_SHAP(palabra="acepto", impacto=0.75),
                    Detalle_Palabra_SHAP(palabra="oferta", impacto=0.60),
                    Detalle_Palabra_SHAP(palabra="seguimos", impacto=0.45)
                ]
            )
        ]
    )
}

# --- ENDPOINTS ---

@app.get("/api/v1/dashboard/resumen", response_model=Respuesta_Dashboard)
def obtener_Resumen_Dashboard():
    logger.info("obtener_Resumen_Dashboard iniciada")
    try:
        logger.debug(f"Retornando mock de dashboard: {mock_dashboard}")
        return mock_dashboard
    except Exception as e:
        logger.error(f"Error en obtener_Resumen_Dashboard: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno al obtener resumen")

@app.get("/api/v1/analisis/clusters", response_model=List[Coordenada_Cluster])
def obtener_Coordenadas_Clusters():
    logger.info("obtener_Coordenadas_Clusters iniciada")
    try:
        logger.debug(f"Retornando {len(mock_clusters)} puntos de clústeres")
        return mock_clusters
    except Exception as e:
        logger.error(f"Error en obtener_Coordenadas_Clusters: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno al obtener clústeres")

@app.get("/api/v1/analisis/mensajes/{id_sesion}", response_model=Detalle_Chat)
def obtener_Detalle_Mensajes(id_sesion: str):
    logger.info(f"obtener_Detalle_Mensajes iniciada para sesion: {id_sesion}")
    try:
        detalle = mock_detalles_chat.get(id_sesion)
        if not detalle:
            logger.warning(f"Sesión no encontrada: {id_sesion}")
            raise HTTPException(status_code=404, detail="Sesión analítica no encontrada")
        logger.debug(f"Retornando conversación de {detalle.nombre_empresa}")
        return detalle
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error en obtener_Detalle_Mensajes: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno al obtener conversación")

@app.post("/api/v1/reglas/generar", response_model=Resultado_Regla)
def generar_Regla_Programatica(req: Prompt_Regla):
    logger.info(f"generar_Regla_Programatica iniciada para clúster: {req.id_cluster}")
    try:
        # Simulación del Copiloto LLM que genera una regla
        regla = "CONTAINS('precio') OR CONTAINS('tarifa') OR CONTAINS('costo')"
        explicacion = f"Regla generada con Gemini basada en tu prompt '{req.instruccion_prompt}'. Busca términos asociados a insatisfacción financiera."
        impacto_simulado = 45 # número ficticio de chats que coinciden en el clúster

        logger.info("Regla programática generada exitosamente")
        return Resultado_Regla(
            regla_generada=regla,
            explicacion=explicacion,
            registros_afectados=impacto_simulado
        )
    except Exception as e:
        logger.error(f"Error en generar_Regla_Programatica: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al generar regla programática")

@app.get("/")
def raiz():
    return {"status": "ok", "app": "Plataforma de Analisis AgroSaaS"}
