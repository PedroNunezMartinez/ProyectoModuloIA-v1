Version:1.0StartHTML:0000000312EndHTML:0000051386StartFragment:0000038705EndFragment:0000051346SourceURL:file:///C:/MAESTRIA%20EN%20OBS_BI_%20IA/OBS_MASTER%20EN%20MACHINE%20LEARNING%20E%20INTELIGENCIA%20ARTIFICIAL/MODULO_FUNDAMENTO%20DE%20PROGRAMACION/DESARROLLO%20DEL%20PROYECTO/Especificación.docx<style></style>

# Especificación: Sistema Inteligente de Orquestación Comercial y Analítica - R&V Motor

Esta especificación técnica detalla la arquitectura de la suite de IA para la concesionaria R&V Motor, integrando el prototipado experimental, el microservicio de producción en tiempo real, el entorno corporativo de simulación social y el panel analítico web.

## 1. Problema y usuario

* **Quién tiene el problema:** Pedro Núñez Martínez, líder comercial de la concesionaria de motocicletas R&V Motor, encargado degestionar las solicitudes de clientes.

* **Cómo lo resuelve hoy:** De forma completamente manual.Los prospectos entran por WhatsApp o Meta, se leen uno por uno y se registran de forma asíncrona en un archivo histórico común.

* **Qué le molesta de cómo lo hace hoy:** Alto consumo detiempo de respuesta (más de 15 minutos por mensaje), omisión involuntaria de datos críticos de venta, errores tipográficos al registrar clientes y falta devisibilidad del Retorno de Inversión (ROI) de marketing en tiempo real.

* **Qué parte resuelve la IA:** Clasifica la intención de compra del cliente de manera semántica en menos de 3 segundos, redacta unarespuesta persuasiva inmediata para WhatsApp y alimenta el flujo analíticofinanciero.

* **Qué parte se queda fuera:** El agendamiento final de citas presenciales en sucursal y el cierre de contratos financieros, los cuales se derivan de forma manual a un asesor humano.

## 2. Componentes de la Solución (Estructura del Repositorio)

El ecosistema digital de R&V Motor está compuesto por cuatro capas funcionales operando sobre el repositorio central de GitHub:

1. **Capa de Prototipado e Investigación(agente_clasificador.ipynb):** Notebook de Jupyter utilizado para la experimentación previa, validación de la ingeniería de prompts y calibración del esquema Pydantic antes de pasar a producción.

2. **Capa de Orquestación en Tiempo Real (agente_webhook.py/ app.py):** Microservicio backend Flask acoplado a Ngrok y Twilio. Intercepta los mensajes, invoca a Gemini 3.8 Flash de forma tipada y calcula las métricas financieras (Ingreso Estimado, ROI y Ventas Estimadas) de forma atómica en el archivo mensajes_clasificados_ia.csv.

3. **Entorno de Simulación de Canal (Cliente R&V Motors/ logo_rv.png):** Red social simulada en un grupo de WhatsApp integrado porparticipantes controlados (Pedro y su esposa) expuestos a estímulos comerciales mediante artes gráficos de conversión directa (Promoción #1 Yamaha FZ-S a US$2,999 y Promoción #2 Honda XR 190L a US$ 3,499) enlazados a wa.me/14155238886.

4. **Capa de Visualización y BI (**app_dashboard.py**):**Dashboard público interactivo en Streamlit Cloud que procesa la persistencia de datos para renderizar gráficos de Plotly en tiempo real ante el jurado.

## 3. Entradas y salidas

* **Componente: Entorno de Simulación Social**

  - Entrada:Publicación de los artes corporativos de la Promoción #1 o #2 en el gruposimulado. El usuario hace clic en el enlace corto wa.me de la imagen.

  - Salida:Redirección instantánea a la pasarela activa de Twilio para iniciar el flujo automatizado.

* **Componente: Backend Webhook**

  - Entrada: Mensajede WhatsApp enviado desde el entorno simulado (Ej: "Hola, me interesa lamoto R&V 200...").

  - Salida: Fila indexada con 9 columnas analíticas y envío del texto de respuesta persuasiva personalizada según el modelo de interés en menos de 3 segundos.( JSON tipado Pydantic que inyecta una fila con 9 columnas analíticas por cada interaccion por chat)

* **Componente: Streamlit Dashboard**

  - Entrada: Archivo persistente estructurado mensajes_clasificados_ia.csv sincronizado.

  - Salida: Gráficos de barras interactivos de conversión, líneas de tiempo y KPIs de ROI acumulado(Leads Calientes = $2500, Potenciales = $1200).

.

## 4. La pieza de IA

* **Opción elegida:** API oficial de Google GenAI SDK (google-genai==1.3.0) invocando al modelo gemini-3.8-flash.

* **Por qué:** Ofrece la menor latencia de inferencia del mercado para procesamiento en tiempo real (<3s), salida estructurada estricta mediante tipado Pydantic (BaseModel) y una capa gratuita robusta.

* **Instrucciones para el modelo (system prompt):**

  Actúas como el Agente de IA experto de la concesionaria de motocicletas "R&VMotor".

  Analiza el contexto del mensaje enviado por el cliente en menos de 3 segundos y clasifícalo en una de estas categorías obligatorias:

  1. 'Lead Caliente':Intención clara e inmediata de compra (precios específicos, cuotas,financiamiento, métodos de pago, quiere ir hoy mismo con el dinero).

  2. 'Cliente Potencial': Interés real pero con planes a futuro (agendar citas próximasemana, disponibilidad próximo mes, catálogos generales).

  3. 'Cliente que Solo Pregunta': Soporte o información general operativa sin venta directa (horarios,dirección física, repuestos, vacantes).

  4. 'Lead Frío':Negativa, descartes ("No gracias"), emoticones por error o textos sinsentido ajenos a motos.

  REGLA DE RESPUESTA AUTOMÁTICA: Genera una respuesta persuasiva, humana y empática en español,orientada a cerrar la venta o resolver el soporte.

## 5. Flujo del usuario y Datos

1. **Estímulo y Clic:** El cliente visualiza el arte gráficopromocional en la red social de prueba y presiona el link del Sandbox.

2. **Orquestación:** El webhook recibe el payload, Geminiejecuta la clasificación semántica en milisegundos, Pandas inyecta las métricasanalíticas de ROI en el histórico CSV local y Twilio devuelve el mensaje.

3. **Visualización Ejecutiva:** El líder comercial accede aStreamlit y observa los picos financieros de los impactos reales en vivo dePedro y su esposa (registros C051 a C055).

## 6. Restricciones

* **Coste cero:** Uso de las capas gratuitas de Google AIStudio, Twilio Sandbox, Ngrok y Streamlit Cloud de forma integrada.

* **Ciberseguridad:** Inyección en caliente de credenciales(GEMINI_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN) mediante CMD con 'set'; prohibido hardcodearlas en el código.

* **Privacidad de datos:** Anonimización de números telefónicos reales en las vistas públicas del panel web.

## 7. Criterios de aceptación

1. **Caso de Éxito Comercial:** Ante un mensaje de compra gatillado por los artes de las promociones #1 o #2, el sistema debe registrar el lead   como 'Lead Caliente', calcular un ingreso de $2500.00, un ROI del 1566% y disparar la respuesta automática.

2. **Caso de Estabilidad Gráfica:** Al ejecutara pp_dashboard.py, Streamlit debe renderizar las tablas y los componentes visuales de Plotly leyendo el CSV maestro unificado por comas sin mezclar columnas.

3. **Caso de Tolerancia a Fallos:** Si el agente local pierde conexión o la API excede su cuota, el bloque try-except debe atrapar los errores HTTP 429 o 503 mostrando logs informativos en consola sin tumbar el microservicio ni corromper el CSV histórico.

## 8. Fuera de alcance (por ahora)

* Procesamiento de imágenes (Computer Vision) enviadas por clientes al chat para cotizar repuestos de motos.

* Pasarela de cobros transaccionales bancarios integrados dentro del mismo chat de WhatsApp.

## 9. Despliegue

* **Ruta de Despliegue elegida:** Ruta A (StreamlitCommunity Cloud) acoplada directamente al repositorio público de GitHub(ProyectoModuloIA/rv_motor_crm), leyendo de forma dinámica la base de datos distribuida en formato homogéneo.
  -URL proyecto en GiHub: https://github.com/PedroNunezMartinez/ProyectoModuloIA/tree/main/rv_motor_crm
  -URL dashboard: [https://rv-motor-crm.streamlit.app](https://rv-motor-crm.streamlit.app/)

## 


