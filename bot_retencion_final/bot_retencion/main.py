from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import LoginRequest, MensajeRequest, CerrarSesionRequest
from database import (
    get_cliente, get_historial_churn, get_interacciones_soporte,
    crear_sesion_chat, guardar_mensaje, cerrar_sesion, listar_clientes,
    actualizar_sesion_parcial
)
from bot_logic import procesar_mensaje, generar_saludo

app = FastAPI(
    title="Bot de Retención — AgroSaaS",
    description="API para el bot de retención de clientes ganaderos",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/clientes")
def listar():
    """Devuelve los primeros 20 clientes para seleccionar en el login."""
    try:
        clientes = listar_clientes()
        return {"clientes": clientes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/login")
def login(req: LoginRequest):
    """
    Recibe un id_cliente, consulta su perfil e historial,
    abre una nueva sesión de chat y devuelve el saludo personalizado.
    """
    cliente = get_cliente(req.id_cliente)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    historial = get_historial_churn(req.id_cliente)
    interacciones = get_interacciones_soporte(req.id_cliente)
    id_sesion = crear_sesion_chat(req.id_cliente)

    saludo = generar_saludo(dict(cliente), [dict(h) for h in historial])

    guardar_mensaje(
        id_sesion=id_sesion,
        rol="bot",
        contenido=saludo,
        idioma="Español",
        etiqueta="neutral",
        contenido_es=saludo,
        contenido_pt=saludo
    )

    return {
        "id_sesion": id_sesion,
        "cliente": dict(cliente),
        "historial_churn": [dict(h) for h in historial],
        "interacciones_recientes": [dict(i) for i in interacciones],
        "saludo": saludo
    }


@app.post("/mensaje")
def mensaje(req: MensajeRequest):
    """
    Recibe el mensaje del cliente, genera la respuesta del bot
    y guarda ambos mensajes en mensajes_chat con contenido_es y contenido_pt.
    """
    # Guardar mensaje del cliente
    guardar_mensaje(
        id_sesion=req.id_sesion,
        rol="cliente",
        contenido=req.mensaje,
        idioma="Español",
        etiqueta="intención_cancelación",
        contenido_es=req.mensaje,
        contenido_pt=req.mensaje
    )

    # Procesar respuesta del bot
    resultado = procesar_mensaje(req.mensaje)

    # Guardar respuesta del bot con ambos idiomas
    id_msg = guardar_mensaje(
        id_sesion=req.id_sesion,
        rol="bot",
        contenido=resultado["respuesta"],
        idioma="Español",
        etiqueta=resultado["etiqueta"],
        contenido_es=resultado["respuesta"],
        contenido_pt=resultado.get("respuesta_pt")
    )

    # Actualizar motivo y sentimiento en la sesión
    actualizar_sesion_parcial(
        id_sesion=req.id_sesion,
        motivo=resultado["etiqueta"],
        sentimiento=resultado["sentimiento"]
    )

    return {
        "respuesta": resultado["respuesta"],
        "respuesta_pt": resultado.get("respuesta_pt"),
        "etiqueta": resultado["etiqueta"],
        "oferta": resultado.get("oferta"),
        "retenido": resultado["retenido"],
        "sentimiento": resultado["sentimiento"],
        "id_mensaje_guardado": id_msg
    }


@app.post("/cerrar-sesion")
def cerrar(req: CerrarSesionRequest):
    """Actualiza hora_fin, cliente_retenido y puntaje_sentimiento de la sesión."""
    try:
        cerrar_sesion(req.id_sesion, req.cliente_retenido, req.puntaje_sentimiento)
        return {"mensaje": "Sesión cerrada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def root():
    return {"status": "ok", "app": "Bot de Retención AgroSaaS"}
