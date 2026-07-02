from pydantic import BaseModel
from typing import List, Dict, Optional

class Coordenada_Cluster(BaseModel):
    id_sesion: str
    x: float
    y: float
    categoria: str
    sentimiento_promedio: float
    texto_resumen: str

class Detalle_Palabra_SHAP(BaseModel):
    palabra: str
    impacto: float  # Valor de contribución (positivo/negativo)

class Mensaje_Chat(BaseModel):
    id_mensaje: str
    rol_remitente: str  # 'bot' o 'cliente'
    contenido: str
    hora_envio: str
    etiqueta_intencion: str
    palabras_clave_shap: List[Detalle_Palabra_SHAP]

class Detalle_Chat(BaseModel):
    id_sesion: str
    nombre_empresa: str
    provincia: str
    tipo_contrato: str
    cliente_retenido: bool
    puntaje_sentimiento: float
    conversacion: List[Mensaje_Chat]

class Respuesta_Dashboard(BaseModel):
    total_clientes: int
    tasa_abandono: float
    tasa_retencion: float
    conversaciones_analizadas: int
    conversaciones_frustradas: int
    sentimiento_promedio: float
    motivos_churn: Dict[str, int]
    retencion_por_oferta: Dict[str, float]

class Prompt_Regla(BaseModel):
    id_cluster: str
    instruccion_prompt: str

class Resultado_Regla(BaseModel):
    regla_generada: str
    explicacion: str
    registros_afectados: int
