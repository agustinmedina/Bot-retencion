import { Component, signal, effect } from '@angular/core';
import { CommonModule } from '@angular/common';

interface Coordenada_Cluster {
  id_sesion: string;
  x: number;
  y: number;
  categoria: string;
  sentimiento_promedio: number;
  texto_resumen: string;
}

interface Detalle_Palabra_SHAP {
  palabra: string;
  impacto: number;
}

interface Mensaje_Chat {
  id_mensaje: string;
  rol_remitente: string;
  contenido: string;
  hora_envio: string;
  etiqueta_intencion: string;
  palabras_clave_shap: Detalle_Palabra_SHAP[];
}

interface Detalle_Chat {
  id_sesion: string;
  nombre_empresa: string;
  provincia: string;
  tipo_contrato: string;
  cliente_retenido: boolean;
  puntaje_sentimiento: number;
  conversacion: Mensaje_Chat[];
}

interface Respuesta_Dashboard {
  total_clientes: number;
  tasa_abandono: number;
  tasa_retencion: number;
  conversaciones_analizadas: number;
  conversaciones_frustradas: number;
  sentimiento_promedio: number;
  motivos_churn: { [key: string]: number };
  retencion_por_oferta: { [key: string]: number };
}

interface Resultado_Regla {
  regla_generada: string;
  explicacion: string;
  registros_afectados: number;
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  // Signals para el Estado de la Aplicación
  protected readonly titulo = signal('AgroSaaS — Plataforma de Auditoría');
  protected readonly cargando = signal<boolean>(false);
  protected readonly error = signal<string | null>(null);

  // Signals de Control y Perfil (inspirados en el Mockup)
  protected readonly perfilSeleccionado = signal<'product' | 'analyst'>('product');
  protected readonly pestanaActiva = signal<'dashboard' | 'explorer'>('dashboard');
  protected readonly umbralConfianza = signal<number>(75);
  protected readonly borradorTicket = signal<string>('');

  protected readonly resumenDashboard = signal<Respuesta_Dashboard | null>(null);
  protected readonly listaClusters = signal<Coordenada_Cluster[]>([]);
  protected readonly chatSeleccionado = signal<Detalle_Chat | null>(null);
  
  protected readonly promptRegla = signal<string>('');
  protected readonly resultadoRegla = signal<Resultado_Regla | null>(null);
  protected readonly buscandoRegla = signal<boolean>(false);

  // Variable de control para simular la IP de la API
  private readonly URL_API = 'http://localhost:8000/api/v1';

  constructor() {
    this.inicializar_Plataforma();

    // Actualiza el borrador del ticket automáticamente al cambiar de chat
    effect(() => {
      const chat = this.chatSeleccionado();
      if (chat) {
        this.borradorTicket.set(`h2. Detalle del Quiebre
*Cliente:* ${chat.nombre_empresa}
*Intent:* ${chat.conversacion[0]?.etiqueta_intencion || 'N/A'}
*Sentimiento:* ${chat.puntaje_sentimiento} (Frustración Crítica)

h2. Recomendación de Diseño UX
El bot repite la restricción técnica sin proveer caminos de bonificación o mitigación, gatillando el abandono definitivo.`);
      } else {
        this.borradorTicket.set('');
      }
    });
  }

  // Carga inicial de datos
  private async inicializar_Plataforma() {
    this.cargando.set(true);
    this.error.set(null);
    try {
      await Promise.all([
        this.cargar_Dashboard(),
        this.cargar_Clusters()
      ]);
    } catch (e: any) {
      this.error.set('No se pudo establecer conexión con el servidor. Cargando datos simulados locales.');
    } finally {
      this.cargando.set(false);
    }
  }

  // Cargar métricas del dashboard
  private async cargar_Dashboard() {
    try {
      const res = await fetch(`${this.URL_API}/dashboard/resumen`);
      if (!res.ok) throw new Error();
      const datos = await res.json();
      this.resumenDashboard.set(datos);
    } catch {
      // Fallback a datos simulados si la API no responde
      this.resumenDashboard.set({
        total_clientes: 1200,
        tasa_abandono: 12.5,
        tasa_retencion: 68.2,
        conversaciones_analizadas: 340,
        conversaciones_frustradas: 108,
        sentimiento_promedio: 0.25,
        motivos_churn: {
          "Precio": 45,
          "Competidor": 30,
          "Insatisfacción": 15,
          "Actitud": 10
        },
        retencion_por_oferta: {
          "Descuento": 72.5,
          "Mes Gratis": 85.0,
          "Mejora Plan": 50.0
        }
      });
    }
  }

  // Cargar coordenadas de los clústeres
  private async cargar_Clusters() {
    try {
      const res = await fetch(`${this.URL_API}/analisis/clusters`);
      if (!res.ok) throw new Error();
      const datos = await res.json();
      this.listaClusters.set(datos);
    } catch {
      // Fallback a datos simulados si la API no responde
      this.listaClusters.set([
        {
          id_sesion: "sesion-1111", x: -1.25, y: 0.45,
          categoria: "Precio", sentimiento_promedio: -0.65,
          texto_resumen: "Quejas reiteradas sobre el aumento en el cargo mensual"
        },
        {
          id_sesion: "sesion-2222", x: -0.85, y: 1.20,
          categoria: "Competidor", sentimiento_promedio: -0.40,
          texto_resumen: "Menciones de migración a competidores por mejor oferta"
        },
        {
          id_sesion: "sesion-3333", x: 1.10, y: -0.50,
          categoria: "Insatisfacción", sentimiento_promedio: -0.75,
          texto_resumen: "Molestias con la velocidad de resolución en soporte"
        },
        {
          id_sesion: "sesion-4444", x: 0.50, y: 0.30,
          categoria: "Precio", sentimiento_promedio: 0.10,
          texto_resumen: "Dudas generales sobre tarifas resueltas con descuento"
        }
      ]);
    }
  }

  // Seleccionar y ver detalle de una conversación (SHAP)
  protected async seleccionar_Chat(id_sesion: string) {
    this.error.set(null);
    try {
      const res = await fetch(`${this.URL_API}/analisis/mensajes/${id_sesion}`);
      if (!res.ok) throw new Error();
      const datos = await res.json();
      this.chatSeleccionado.set(datos);
    } catch {
      // Fallback a datos simulados locales
      const mock_chats: { [key: string]: Detalle_Chat } = {
        "sesion-1111": {
          id_sesion: "sesion-1111",
          nombre_empresa: "Estancia Las Lilas",
          provincia: "Buenos Aires",
          tipo_contrato: "Mensual",
          cliente_retenido: false,
          puntaje_sentimiento: -0.65,
          conversacion: [
            {
              id_mensaje: "msg-101", rol_remitente: "cliente",
              contenido: "Hola, quiero cancelar la suscripción porque el precio es muy alto.",
              hora_envio: "2026-06-29T10:00:00", etiqueta_intencion: "intención_cancelación",
              palabras_clave_shap: [
                { palabra: "cancelar", impacto: -0.85 },
                { palabra: "precio", impacto: -0.75 },
                { palabra: "alto", impacto: -0.40 }
              ]
            },
            {
              id_mensaje: "msg-102", rol_remitente: "bot",
              contenido: "Hola. Entiendo tu preocupación. ¿Te gustaría un descuento del 20%?",
              hora_envio: "2026-06-29T10:00:05", etiqueta_intencion: "ofrecer_descuento",
              palabras_clave_shap: []
            },
            {
              id_mensaje: "msg-103", rol_remitente: "cliente",
              contenido: "No me sirve, prefiero dar de baja el servicio hoy mismo.",
              hora_envio: "2026-06-29T10:01:00", etiqueta_intencion: "intención_cancelación",
              palabras_clave_shap: [
                { palabra: "baja", impacto: -0.90 },
                { palabra: "servicio", impacto: -0.20 }
              ]
            }
          ]
        },
        "sesion-2222": {
          id_sesion: "sesion-2222",
          nombre_empresa: "AgroGanadera del Sur",
          provincia: "Córdoba",
          tipo_contrato: "Anual",
          cliente_retenido: true,
          puntaje_sentimiento: -0.20,
          conversacion: [
            {
              id_mensaje: "msg-201", rol_remitente: "cliente",
              contenido: "La competencia me ofrece lo mismo por la mitad de tarifa.",
              hora_envio: "2026-06-29T11:15:00", etiqueta_intencion: "mención_competidor",
              palabras_clave_shap: [
                { palabra: "competencia", impacto: -0.65 },
                { palabra: "mitad", impacto: -0.50 },
                { palabra: "tarifa", impacto: -0.30 }
              ]
            },
            {
              id_mensaje: "msg-202", rol_remitente: "bot",
              contenido: "Entiendo. Podemos darte 1 mes gratis para compensar.",
              hora_envio: "2026-06-29T11:15:10", etiqueta_intencion: "ofrecer_mes_gratis",
              palabras_clave_shap: []
            },
            {
              id_mensaje: "msg-203", rol_remitente: "cliente",
              contenido: "Bueno, acepto la oferta y seguimos con el plan.",
              hora_envio: "2026-06-29T11:16:00", etiqueta_intencion: "retention_interest",
              palabras_clave_shap: [
                { palabra: "acepto", impacto: 0.75 },
                { palabra: "oferta", impacto: 0.60 },
                { palabra: "seguimos", impacto: 0.45 }
              ]
            }
          ]
        }
      };
      
      const chat = mock_chats[id_sesion];
      if (chat) {
        this.chatSeleccionado.set(chat);
      } else {
        this.error.set('Conversación no encontrada en los datos locales simulados.');
      }
    }
  }

  // Traducir coordenadas a posición SVG en porcentaje
  protected obtener_Posicion_X(x: number): number {
    // Rango de entrada [-2.0, 2.0] mapeado a porcentaje [10%, 90%] para no tocar bordes
    return 50 + x * 20;
  }

  protected obtener_Posicion_Y(y: number): number {
    // Rango de entrada [-2.0, 2.0] mapeado a porcentaje [10%, 90%] e invertido
    return 50 - y * 20;
  }

  // Retornar clase CSS según la categoría
  protected obtener_Clase_Categoria(cat: string): string {
    switch (cat.toLowerCase()) {
      case 'precio': return 'precio';
      case 'competidor': return 'competidor';
      case 'insatisfacción':
      case 'insatisfaccion': return 'insatisfaccion';
      default: return 'soporte';
    }
  }

  // Enlazar input de texto del copiloto
  protected actualizar_Prompt(event: Event) {
    const input = event.target as HTMLInputElement;
    this.promptRegla.set(input.value);
  }

  // Invocar copiloto para generar regla programática
  protected async simular_Copiloto(event: Event) {
    event.preventDefault();
    if (!this.promptRegla().trim()) return;

    this.buscandoRegla.set(true);
    try {
      const res = await fetch(`${this.URL_API}/reglas/generar`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          id_cluster: this.chatSeleccionado()?.id_sesion || "sesion-general",
          instruccion_prompt: this.promptRegla()
        })
      });
      if (!res.ok) throw new Error();
      const datos = await res.json();
      this.resultadoRegla.set(datos);
    } catch {
      // Simulación local si falla la conexión
      setTimeout(() => {
        this.resultadoRegla.set({
          regla_generada: `CONTAINS('${this.promptRegla().toLowerCase()}') OR REGEX('\\b(cancelar|precio)\\b')`,
          explicacion: `Copiloto simulado: Regla generada basada en tu solicitud. Filtra los mensajes que contienen la palabra '${this.promptRegla()}' o sinónimos financieros en AgroSaaS.`,
          registros_afectados: Math.floor(Math.random() * 40) + 5
        });
        this.buscandoRegla.set(false);
      }, 1000);
      return;
    }
    this.buscandoRegla.set(false);
  }

  // --- ACCIONES HUMAN-IN-THE-LOOP ---

  protected parsear_Mensaje(m: Mensaje_Chat): { palabra: string, shap: Detalle_Palabra_SHAP | null }[] {
    const palabras = m.contenido.split(' ');
    return palabras.map(p => {
      // Limpiar puntuación para comparar con los términos de SHAP
      const limpia = p.toLowerCase().replace(/[.,\/#!$%\^&\*;:{}=\-_`~()?"¡¿]/g,"");
      const shap = m.palabras_clave_shap.find(s => s.palabra.toLowerCase() === limpia);
      return { palabra: p, shap: shap || null };
    });
  }

  protected aprobar_Chat() {
    alert(`Chat ${this.chatSeleccionado()?.id_sesion} validado y guardado correctamente en la base de datos central.`);
    this.chatSeleccionado.set(null);
  }

  protected exportar_Ticket_Bugs() {
    const chat = this.chatSeleccionado();
    if (!chat) return;

    const contenido_ticket = `# 🐛 Reporte de Discrepancia Algorítmica - AgroSaaS
## ID Sesión: ${chat.id_sesion}
* **Cliente:** ${chat.nombre_empresa}
* **Provincia:** ${chat.provincia}
* **Contrato:** ${chat.tipo_contrato}
* **Sentimiento Calculado:** ${chat.puntaje_sentimiento} (Discrepancia detectada)

### Conversación y Análisis SHAP:
${chat.conversacion.map(m => `
> **[${m.rol_remitente}]** (${m.etiqueta_intencion}): ${m.contenido}
> *Atribución SHAP:* ${m.palabras_clave_shap.map(s => `${s.palabra}: ${s.impacto}`).join(', ') || 'N/A'}
`).join('\n')}

---
**Generado por el Analista de Datos vía AgroSaaS Auditoría.**`;

    const blob = new Blob([contenido_ticket], { type: 'text/markdown' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `ticket_bug_${chat.id_sesion}.md`;
    a.click();
    window.URL.revokeObjectURL(url);
  }

  // --- MÉTODOS DE LA INTERFAZ MOCKUP INTEGRADOS ---

  protected setPerfil(perfil: 'product' | 'analyst') {
    this.perfilSeleccionado.set(perfil);
  }

  protected setTab(tab: 'dashboard' | 'explorer') {
    this.pestanaActiva.set(tab);
  }

  protected actualizar_Umbral(event: Event) {
    const input = event.target as HTMLInputElement;
    this.umbralConfianza.set(parseInt(input.value, 10));
  }

  protected actualizar_Borrador(event: Event) {
    const textarea = event.target as HTMLTextAreaElement;
    this.borradorTicket.set(textarea.value);
  }

  protected despachar_Mcp() {
    const ticket = this.borradorTicket();
    if (!ticket) return;
    alert(`[MCP Link] Despachando ticket al backlog de Jira:\n\n${ticket}`);
    this.chatSeleccionado.set(null);
  }
}
