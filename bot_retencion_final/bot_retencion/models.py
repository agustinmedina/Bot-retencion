from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    id_cliente: str

class MensajeRequest(BaseModel):
    id_sesion: str
    id_cliente: str
    mensaje: str

class CerrarSesionRequest(BaseModel):
    id_sesion: str
    cliente_retenido: bool
    puntaje_sentimiento: float

class ClienteResponse(BaseModel):
    id_cliente: str
    nombre_empresa: str
    provincia: Optional[str]
    tipo_productor: Optional[str]
    nombre_plan: Optional[str]
    cargo_mensual: Optional[float]
    meses_antiguedad: Optional[int]

class MensajeResponse(BaseModel):
    respuesta: str
    etiqueta: str
    oferta: Optional[str]
    retenido: bool
    sentimiento: float
    id_mensaje_guardado: str
