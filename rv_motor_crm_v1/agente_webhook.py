import os
import csv
from datetime import datetime
from flask import Flask, request, Response
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from twilio.rest import Client as TwilioClient

app = Flask(__name__)

# ==========================================
# 1. Configuración de Credenciales de Seguridad
# ==========================================
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")

client = None
twilio_client = None

if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)
if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
    twilio_client = TwilioClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# ==========================================
# 2. Esquema Estricto Pydantic
# ==========================================
class ClasificacionLead(BaseModel):
    interes_ia: str = Field(
        description="Categoría de clasificación obligatoria: 'Lead Caliente', 'Cliente Potencial', 'Cliente que Solo Pregunta', o 'Lead Frío'."
    )
    motivo_semantico: str = Field(
        description="Explicación breve de la clasificación de acuerdo con el mensaje analizado."
    )
    respuesta_automatica: str = Field(
        description="Respuesta humana, persuasiva y empática en español orientada a la conversión o resolución de dudas."
    )

CSV_FILE_PATH = "mensajes_clasificados_ia.csv"

# ==========================================
# 3. Lógica Financiera de ROI
# ==========================================
def calcular_metricas_financieras(categoria: str):
    cat_clean = categoria.strip().lower()
    if "caliente" in cat_clean:
        return 2500.0, 1566.0, "Alta"
    elif "potencial" in cat_clean:
        return 1200.0, 750.0, "Media"
    elif "pregunta" in cat_clean:
        return 0.0, -100.0, "Baja"
    else:
        return 0.0, -100.0, "Nula"

# ==========================================
# 4. Registro de Datos Seguro en CSV
# ==========================================
def registrar_mensaje_en_csv(telefono, mensaje, categoria, motivo, ingreso, roi, prioridad, respuesta_ia):
    file_exists = os.path.isfile(CSV_FILE_PATH)
    telefono_anonimo = f"WhatsApp: +502XXXX{telefono[-4:]}" if len(str(telefono)) >= 4 else "WhatsApp: Oculto"

    try:
        with open(CSV_FILE_PATH, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=",")
            if not file_exists:
                writer.writerow([
                    "Fecha_Hora", "Telefono_Anonimizado", "Mensaje",
                    "Interes_IA", "Motivo_Semantico", "Ingreso_Estimado",
                    "ROI", "Prioridad", "Respuesta_Automatica"
                ])
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                telefono_anonimo,
                mensaje.replace("\n", " "),
                categoria,
                motivo,
                f"{ingreso:.2f}",
                f"{roi}%",
                prioridad,
                respuesta_ia.replace("\n", " ")
            ])
    except Exception as e:
        print(f"[ERROR] Error al registrar datos en el CSV: {e}")

# ==========================================
# 5. Endpoint del Webhook (POST)
# ==========================================
@app.route("/webhook", methods=["POST"])
def webhook():
    sender_phone = request.values.get("From", "Unknown")
    incoming_msg = request.values.get("Body", "").strip()

    categoria_final = "Lead Frío"
    motivo_final = "Bypass por error del sistema de IA"
    respuesta_final = "Hola, en este momento experimentamos alta demanda. Un asesor humano de R&V Motor se comunicará contigo pronto."

    if client and incoming_msg:
        try:
            system_prompt = """
            Actúas como el Agente de IA experto de la concesionaria de motocicletas "R&V Motor".
            Analiza el contexto del mensaje enviado por el cliente en menos de 3 segundos y clasifícalo en una de estas categorías obligatorias:
            1. 'Lead Caliente': Intención clara e inmediata de compra.
            2. 'Cliente Potencial': Interés real pero con planes a futuro.
            3. 'Cliente que Solo Pregunta': Soporte o información general operativa.
            4. 'Lead Frío': Negativa, descartes o textos sin sentido.
            """

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=incoming_msg,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    response_mime_type="application/json",
                    response_schema=ClasificacionLead,
                    temperature=0.2
                )
            )

            analisis = response.parsed
            categoria_final = analisis.interes_ia
            motivo_final = analisis.motivo_semantico
            respuesta_final = analisis.respuesta_automatica

        except Exception as e:
            print(f"[LOG] Error de llamada API Gemini: {e}")

    ingreso, roi, prioridad = calcular_metricas_financieras(categoria_final)
    registrar_mensaje_en_csv(sender_phone, incoming_msg, categoria_final, motivo_final, ingreso, roi, prioridad, respuesta_final)

    if twilio_client and sender_phone != "Unknown":
        try:
            twilio_client.messages.create(
                body=str(respuesta_final),
                from_=request.values.get("To", "whatsapp:+14155238886"),
                to=sender_phone
            )
        except Exception as e:
            print(f"[LOG] Error de envío de Twilio: {e}")

    resp = Response("<Response></Response>", mimetype="text/xml")
    resp.headers["ngrok-skip-browser-warning"] = "true"
    return resp

if __name__ == "__main__":
    app.run(port=5000, debug=True)
