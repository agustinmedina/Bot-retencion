from typing import Optional

RESPUESTAS = [
    {
        "triggers": ["cancelar", "baja", "darme de baja", "quiero irme", "abandonar", "no quiero seguir"],
        "respuesta": "Lamento escuchar eso. Valoramos mucho tu cuenta. ¿Podés contarme cuál es el motivo principal para cancelar?",
        "respuesta_pt": "Lamento ouvir isso. Valorizamos muito a sua conta. Você pode me contar qual é o principal motivo para cancelar?",
        "etiqueta": "intención_cancelación",
        "oferta": None,
        "retenido": False,
        "sentimiento": 0.2
    },
    {
        "triggers": ["precio", "caro", "costoso", "alto", "no puedo pagar", "tarifa", "cobran mucho"],
        "respuesta": "Entiendo que el costo es un factor clave. Para clientes con tu antigüedad tenemos opciones especiales: podemos ofrecerte un 10% de descuento permanente o un mes gratis para que evalúes el servicio sin compromiso. ¿Cuál te interesa?",
        "respuesta_pt": "Entendo que o custo é um fator chave. Para clientes com sua antiguidade temos opções especiais: podemos oferecer 10% de desconto permanente ou um mês grátis para avaliar o serviço sem compromisso. Qual te interessa?",
        "etiqueta": "queja_precio",
        "oferta": "10% de descuento",
        "retenido": True,
        "sentimiento": 0.5
    },
    {
        "triggers": ["competencia", "competidor", "otro proveedor", "mejor oferta", "otra empresa"],
        "respuesta": "Entiendo que recibiste una propuesta externa. Antes de decidir, podemos igualarte la oferta o darte una mejora de plan sin costo adicional por 3 meses. ¿Qué te ofrecieron?",
        "respuesta_pt": "Entendo que você recebeu uma proposta externa. Antes de decidir, podemos igualar a oferta ou dar uma melhoria de plano sem custo adicional por 3 meses. O que te ofereceram?",
        "etiqueta": "mención_competidor",
        "oferta": "Mejora de plan",
        "retenido": True,
        "sentimiento": 0.4
    },
    {
        "triggers": ["servicio", "falla", "inestable", "problema", "caída", "lento", "no funciona", "corte"],
        "respuesta": "Lamentamos los inconvenientes técnicos. Tu experiencia es nuestra prioridad. Para compensarte vamos a darte un mes gratis y asignarte atención prioritaria. ¿Cuándo empezaron los problemas?",
        "respuesta_pt": "Lamentamos os inconvenientes técnicos. Sua experiência é nossa prioridade. Para compensar vamos te dar um mês grátis e atribuir atendimento prioritário. Quando começaram os problemas?",
        "etiqueta": "problema_servicio",
        "oferta": "Mes gratis",
        "retenido": True,
        "sentimiento": 0.3
    },
    {
        "triggers": ["mudo", "mudando", "región", "otro lugar", "traslado", "me voy del campo"],
        "respuesta": "Entendemos que un traslado es un momento importante. Nuestro servicio cubre todas las provincias argentinas y Brasil. ¿A qué región te mudás? Podemos asignarte un asesor local.",
        "respuesta_pt": "Entendemos que uma mudança é um momento importante. Nosso serviço cobre todas as províncias argentinas e o Brasil. Para qual região você está se mudando? Podemos atribuir um consultor local.",
        "etiqueta": "neutral",
        "oferta": None,
        "retenido": False,
        "sentimiento": 0.5
    },
    {
        "triggers": ["soporte", "atención", "no me ayudaron", "mal trato", "espera", "no respondieron"],
        "respuesta": "Nos disculpamos por esa experiencia, no es el estándar que queremos dar. Vamos a asignarte un agente dedicado y aplicarte un 10% de descuento por las molestias. ¿Querés que lo procesemos ahora?",
        "respuesta_pt": "Pedimos desculpas por essa experiência, não é o padrão que queremos oferecer. Vamos atribuir um agente dedicado e aplicar 10% de desconto pelas inconveniências. Quer que processemos agora?",
        "etiqueta": "problema_servicio",
        "oferta": "10% de descuento",
        "retenido": True,
        "sentimiento": 0.4
    },
    {
        "triggers": ["acepto", "sí", "ok", "de acuerdo", "quiero el descuento", "aplicalo", "me quedo"],
        "respuesta": "¡Perfecto! Me alegra que podamos seguir trabajando juntos. Voy a procesar la oferta ahora mismo. En las próximas 24hs vas a recibir la confirmación por correo. ¿Hay algo más en lo que pueda ayudarte?",
        "respuesta_pt": "Perfeito! Fico feliz que possamos continuar trabalhando juntos. Vou processar a oferta agora mesmo. Nas próximas 24h você receberá a confirmação por e-mail. Há mais alguma coisa em que posso ajudar?",
        "etiqueta": "neutral",
        "oferta": None,
        "retenido": True,
        "sentimiento": 0.9
    },
    {
        "triggers": ["no", "igual", "de todas formas", "no me convence", "igual me voy", "nada"],
        "respuesta": "Respeto tu decisión. Si en algún momento querés reactivar o evaluar nuevas opciones, vamos a estar disponibles. ¿Te puedo pedir que nos cuentes brevemente qué podríamos mejorar?",
        "respuesta_pt": "Respeito sua decisão. Se em algum momento quiser reativar ou avaliar novas opções, estaremos disponíveis. Posso te pedir que nos conte brevemente o que poderíamos melhorar?",
        "etiqueta": "intención_cancelación",
        "oferta": None,
        "retenido": False,
        "sentimiento": 0.1
    },
]

FALLBACK = {
    "respuesta": "Gracias por compartirlo. ¿Podés contarme un poco más sobre lo que te llevó a esta decisión? Así busco la mejor solución para vos.",
    "respuesta_pt": "Obrigado por compartilhar. Você pode me contar um pouco mais sobre o que te levou a essa decisão? Assim busco a melhor solução para você.",
    "etiqueta": "neutral",
    "oferta": None,
    "retenido": False,
    "sentimiento": 0.5
}

def procesar_mensaje(texto: str) -> dict:
    t = texto.lower()
    for r in RESPUESTAS:
        if any(trigger in t for trigger in r["triggers"]):
            return r
    return FALLBACK

def generar_saludo(cliente: dict, historial: list) -> str:
    nombre = cliente.get("nombre_empresa", "cliente")
    plan = cliente.get("nombre_plan", "tu plan actual")
    meses = cliente.get("meses_antiguedad", 0)
    provincia = cliente.get("provincia", "")

    saludo = f"¡Hola! Soy el asistente de retención de AgroSaaS. "
    saludo += f"Estoy hablando con {nombre}"
    if provincia:
        saludo += f" de {provincia}"
    saludo += f", cliente con {meses} meses de antigüedad en el plan {plan}. "

    if historial:
        ultimo = historial[0]
        saludo += f"Veo que anteriormente tuviste un evento relacionado con '{ultimo.get('motivo_churn', '')}'. "

    saludo += "Noté que podrías estar pensando en cancelar tu suscripción. Estoy aquí para ayudarte. ¿Qué está pasando?"
    return saludo
