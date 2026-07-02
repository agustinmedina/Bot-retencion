import os
from dotenv import load_dotenv
from supabase import create_client, Client
import uuid
from datetime import datetime

load_dotenv()

def get_client() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    return create_client(url, key)

def get_cliente(id_cliente: str):
    sb = get_client()
    res = sb.table("clientes").select(
        "id_cliente, nombre_empresa, provincia, tipo_productor, tamaño_rodeo, tipo_contrato, metodo_pago, meses_antiguedad, segmento_demografico"
    ).eq("id_cliente", id_cliente).single().execute()
    if not res.data:
        return None
    cliente = res.data

    sub = sb.table("suscripciones").select(
        "nombre_plan, cargo_mensual, esta_activo"
    ).eq("id_cliente", id_cliente).limit(1).execute()
    if sub.data:
        cliente.update(sub.data[0])
    return cliente

def get_historial_churn(id_cliente: str):
    sb = get_client()
    res = sb.table("eventos_churn").select(
        "categoria_churn, motivo_churn, fue_retenido, oferta_retencion, fecha_churn"
    ).eq("id_cliente", id_cliente).order("fecha_churn", desc=True).limit(3).execute()
    return res.data or []

def get_interacciones_soporte(id_cliente: str):
    sb = get_client()
    res = sb.table("interacciones_soporte").select(
        "canal, tema, resuelto, dias_resolucion"
    ).eq("id_cliente", id_cliente).order("fecha_interaccion", desc=True).limit(5).execute()
    return res.data or []

def crear_sesion_chat(id_cliente: str, id_churn: str = None):
    sb = get_client()
    id_sesion = str(uuid.uuid4())
    sb.table("sesiones_chat").insert({
        "id_sesion": id_sesion,
        "id_cliente": id_cliente,
        "id_churn": id_churn,
        "hora_inicio": datetime.now().isoformat(),
        "total_mensajes": 0,
        "cliente_retenido": False
    }).execute()
    return id_sesion

def guardar_mensaje(id_sesion: str, rol: str, contenido: str, idioma: str, etiqueta: str,
                    contenido_es: str = None, contenido_pt: str = None):
    sb = get_client()
    id_mensaje = str(uuid.uuid4())
    sb.table("mensajes_chat").insert({
        "id_mensaje": id_mensaje,
        "id_sesion": id_sesion,
        "rol_remitente": rol,
        "contenido": contenido,
        "idioma": idioma,
        "hora_envio": datetime.now().isoformat(),
        "etiqueta_intencion": etiqueta,
        "contenido_es": contenido_es if contenido_es else contenido,
        "contenido_pt": contenido_pt if contenido_pt else contenido
    }).execute()

    sesion = sb.table("sesiones_chat").select("total_mensajes").eq("id_sesion", id_sesion).single().execute()
    if sesion.data:
        nuevo_total = sesion.data["total_mensajes"] + 1
        sb.table("sesiones_chat").update({"total_mensajes": nuevo_total}).eq("id_sesion", id_sesion).execute()

    return id_mensaje

def actualizar_sesion_parcial(id_sesion: str, motivo: str, sentimiento: float):
    sb = get_client()
    sb.table("sesiones_chat").update({
        "motivo_identificado_bot": motivo,
        "puntaje_sentimiento": sentimiento
    }).eq("id_sesion", id_sesion).execute()

def cerrar_sesion(id_sesion: str, cliente_retenido: bool, puntaje_sentimiento: float):
    sb = get_client()
    sb.table("sesiones_chat").update({
        "hora_fin": datetime.now().isoformat(),
        "cliente_retenido": cliente_retenido,
        "puntaje_sentimiento": puntaje_sentimiento
    }).eq("id_sesion", id_sesion).execute()

def listar_clientes():
    sb = get_client()
    res = sb.table("clientes").select(
        "id_cliente, nombre_empresa, provincia, tipo_productor"
    ).order("nombre_empresa").limit(20).execute()
    return res.data or []
