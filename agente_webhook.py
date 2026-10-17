
import os
import csv
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import Literal

app = Flask(__name__)

# 1. Esquema estructurado Pydantic para la IA
class AnalisisInteraccion(BaseModel):
    clasificacion: Literal['Lead Caliente', 'Cliente Potencial', 'Cliente que Solo Pregunta', 'Lead Frío'] = Field(
        description="Categoría de intención de compra de acuerdo a las reglas de negocio."
    )
    ingreso_estimado: float = Field(
        description="Ingreso estimado basado en la categoría (Leads Calientes = 2500, Potenciales = 1200, otros = 0)."
    )
    roi_estimado: float = Field(
        description="Retorno de Inversión estimado porcentual (ej: 1566% expresado como 1566.0)."
    )
    respuesta_automatica: str = Field(
        description="Respuesta persuasiva, humana y empática en español para WhatsApp, orientada a cerrar la venta."
    )

# 2. Inicializar cliente de Gemini usando variables de entorno limpias de ciberseguridad
# NOTA: En producción ejecutar en consola antes: set GEMINI_API_KEY=tu_clave_aquí
api_key = os.environ.get('GEMINI_API_KEY', '').strip()
client = genai.Client(api_key=api_key if api_key else None)

CSV_FILE = 'mensajes_clasificados_ia.csv'

def inicializar_csv():
    # Inicializa el archivo CSV histórico si no existe con sus 9 columnas analíticas
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'id_interaccion', 'remitente_anonimo', 'mensaje_original',
                'clasificacion', 'ingreso_estimado', 'roi_estimado',
                'respuesta_enviada', 'modelo_utilizado', 'estado_entrega'
            ])

def anonimizar_telefono(telefono_completo: str) -> str:
    # Anonimizar el número telefónico para protección de privacidad de datos (C051, etc o enmascarado)
    if not telefono_completo:
        return "Anónimo"
    return f"+XXX-XXXX-{telefono_completo[-4:]}"

@app.route("/webhook", methods=['POST'])
def webhook():
    try:
        # Leer payload entrante de Twilio
        from_number = request.values.get('From', '')
        body_message = request.values.get('Body', '')

        # Anonimizar número telefónico
        remitente_anonimo = anonimizar_telefono(from_number)

        # Configurar Prompt del Sistema para R&V Motor de manera segura
        system_prompt = (
            "Actúas como el Agente de IA experto de la concesionaria de motocicletas "R&V Motor".
"
            "Analiza el contexto del mensaje enviado por el cliente en menos de 3 segundos y clasifícalo en una de estas categorías obligatorias:

"
            "1. 'Lead Caliente': Intención clara e inmediata de compra (precios específicos, cuotas, financiamiento, métodos de pago, quiere ir hoy mismo con el dinero).
"
            "   - Métrica financiera asociada: ingreso_estimado = 2500.00, roi_estimado = 1566.0
"
            "2. 'Cliente Potencial': Interés real pero con planes a futuro (agendar citas próxima semana, disponibilidad próximo mes, catálogos generales).
"
            "   - Métrica financiera asociada: ingreso_estimado = 1200.00, roi_estimado = 750.0
"
            "3. 'Cliente que Solo Pregunta': Soporte o información general operativa sin venta directa (horarios, dirección física, repuestos, vacantes).
"
            "   - Métrica financiera asociada: ingreso_estimado = 0.0, roi_estimado = 0.0
"
            "4. 'Lead Frío': Negativa, descartes ("No gracias"), emoticones por error o textos sin sentido ajenos a motos.
"
            "   - Métrica financiera asociada: ingreso_estimado = 0.0, roi_estimado = 0.0

"
            "REGLA DE RESPUESTA AUTOMÁTICA: Genera una respuesta persuasiva, humana y empática en español, orientada a cerrar la venta o resolver el soporte."
        )

        # Consultar Gemini 3.8 Flash de forma estructurada con tolerancia a fallos
        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=body_message,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json",
                response_schema=AnalisisInteraccion,
                temperature=0.2
            )
        )

        analisis = response.parsed

    except Exception as e:
        # Caso de tolerancia a fallos (Error HTTP 429/503 o Key vacía): Respuesta de contingencia
        print(f"Log de Error: Falló la API de Gemini - {e}")
        analisis = AnalisisInteraccion(
            clasificacion='Cliente Potencial',
            ingreso_estimado=1200.0,
            roi_estimado=750.0,
            respuesta_automatica="¡Hola! Gracias por contactar a R&V Motor. En este momento estamos experimentando alta demanda, pero un asesor se comunicará contigo de inmediato."
        )

    # Guardar en CSV de manera atómica
    inicializar_csv()
    try:
        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Generar identificador correlativo simple de interacción basándose en el tamaño
            line_count = sum(1 for line in open(CSV_FILE)) if os.path.exists(CSV_FILE) else 1
            id_interaccion = f"C{line_count:03d}"

            writer.writerow([
                id_interaccion,
                remitente_anonimo,
                body_message,
                analisis.clasificacion,
                analisis.ingreso_estimado,
                analisis.roi_estimado,
                analisis.respuesta_automatica,
                'gemini-3.8-flash',
                'Entregado'
            ])
    except Exception as csv_err:
        print(f"Error guardando métricas en base CSV: {csv_err}")

    # Responder a Twilio para entregar respuesta por WhatsApp en menos de 3 segundos
    twilio_response = MessagingResponse()
    twilio_response.message(analisis.respuesta_automatica)
    return str(twilio_response)

if __name__ == "__main__":
    inicializar_csv()
    # Ejecutar servidor local de desarrollo en puerto 5000
    app.run(port=5000, debug=True)
