# Especificación: Sistema Inteligente de Orquestación Comercial y Analítica - R&V Motor

Esta especificación técnica detalla la arquitectura de la suite de IA para la concesionaria R&V Motor, integrando el prototipado experimental, el microservicio de producción en tiempo real, el entorno corporativo de simulación social y el panel analítico web interactivo.

## 1. Problema y usuario
* **Quién tiene el problema:** Pedro Núñez Martínez, líder comercial de la concesionaria de motocicletas R&V Motor, encargado de gestionar las solicitudes de clientes.
* **Cómo lo resuelve hoy:** De forma completamente manual. Los prospectos entran por WhatsApp o Meta, se leen uno por uno y se registran de forma asíncrona en un archivo histórico común.
* **Qué le molesta de cómo lo hace hoy:** Alto consumo de tiempo de respuesta (más de 15 minutos por mensaje), omisión involuntaria de datos críticos de venta, errores tipográficos al registrar clientes y falta de visibilidad del Retorno de Inversión (ROI) de marketing en tiempo real.
* **Qué parte resuelve la IA:** Clasifica la intención de compra del cliente de manera semántica en menos de 3 segundos, redacta una respuesta persuasiva inmediata para WhatsApp y alimenta de forma automatizada la base de datos analítica.
* **Qué parte se queda fuera:** El agendamiento final de citas presenciales en sucursal y el cierre de contratos financieros, los cuales se derivan de forma manual a un asesor humano.

## 2. Componentes de la Solución (Estructura del Repositorio)
El ecosistema digital de R&V Motor está compuesto por cuatro capas funcionales operando sobre el repositorio central de GitHub.

*Nota de Trazabilidad y Gobernanza:* El comportamiento operativo, las restricciones de codificación y las instrucciones de control para los agentes de desarrollo de software con IA se rigen y auditan bajo las reglas vinculantes detalladas en [AGENTS.md](AGENTS.md).

* **Capa de Prototipado e Investigación (agente_clasificador.ipynb):** Notebook de Jupyter utilizado para la experimentación previa, validación de la ingeniería de prompts y calibración del esquema Pydantic antes de pasar a producción.
* **Capa de Orquestación en Tiempo Real (agente_webhook.py / app.py):** Microservicio backend Flask acoplado a Ngrok y Twilio. Intercepta los mensajes, invoca a Gemini de forma estructurada y actualiza la persistencia histórica en `mensajes_clasificados_ia.csv`.
* **Entorno de Simulación de Canal (Cliente R&V Motors / logo_rv.png):** Red social simulada en un grupo de WhatsApp integrado por participantes controlados (Pedro y su esposa) expuestos a estímulos comerciales mediante artes gráficos de conversión directa enlazados a wa.me.
* **Capa de Visualización y BI (app_dashboard.py):** Dashboard público interactivo en Streamlit Cloud que procesa la persistencia de datos del archivo unificado para renderizar gráficos de Plotly y calcular KPIs financieros en tiempo real basados en los parámetros dinámicos de simulación financiera.

## 3. Entradas y salidas y Esquema de Datos

### Componente: Entorno de Simulación Social
* **Entrada:** Publicación de los artes corporativos de la Promoción #1 o #2 en el grupo simulado. El usuario hace clic en el enlace corto wa.me de la imagen.
* **Salida:** Redirección instantánea a la pasarela activa de Twilio para iniciar el flujo automatizado.

### Componente: Backend Webhook
* **Entrada:** Message de WhatsApp enviado desde el entorno simulado.
* **Salida:** Fila indexada con 9 columnas analíticas en `mensajes_clasificados_ia.csv` y envío del texto de respuesta persuasiva personalizada según el modelo de interés.

#### Esquema Oficial de la Base de Datos (`mensajes_clasificados_ia.csv`)
Para garantizar la consistencia, el webhook escribe estrictamente estas 9 columnas delimitadas por comas:
1. `fecha_hora`: Timestamp ISO 8601 del registro.
2. `telefono`: Número de teléfono del remitente anonimizado (`+57XXXXXX` o similar).
3. `mensaje_original`: El mensaje de texto plano enviado por el usuario.
4. `interes_ia`: Clasificación semántica de la IA ('Lead Caliente', 'Cliente Potencial', 'Cliente que Solo Pregunta', 'Lead Frío').
5. `motivo_semantico`: Justificación analítica del porqué la IA asignó dicha clasificación.
6. `respuesta_automatica`: Mensaje persuasivo generado por la IA para WhatsApp.
7. `canal`: Canal de origen (fijo 'WhatsApp_Twilio_Sandbox').
8. `promocion`: Identificador del estímulo publicitario interactuado ('Promocion_1', 'Promocion_2' o 'Ninguna').
9. `id_interaccion`: Hash alfanumérico único para auditoría e integridad de datos.

### Componente: Streamlit Dashboard
* **Entrada:** Archivo de datos históricos unificado `mensajes_clasificados_ia.csv` and parámetros dinámicos del Sidebar ingresados interactiva y manualmente por el evaluador (Costo de Campaña, Precio Promedio, % de Conversión).
* **Salida:** Gráficos de barras interactivos de conversión, líneas de tiempo, KPIs de Ingresos Estimados, Leads de Alto Valor, Ventas Estimadas y ROI proyectado recalculado de forma instantánea en memoria en base a los datos históricos.

## 4. La pieza de IA
* **Opción elegida:** API oficial de Google GenAI SDK (`google-genai==1.3.0`) invocando al modelo `gemini-3.8-flash-lite`.
* **Por qué:** Ofrece la menor latencia de inferencia para procesamiento en tiempo real (<3s), salida estructurada estricta mediante tipado Pydantic (`BaseModel`) y una capa gratuita robusta.

### Instrucciones del Sistema (system prompt):
```
Actúas como el Agente de IA experto de la concesionaria de motocicletas "R&V Motor".
Analiza el contexto del mensaje enviado por el cliente en menos de 3 segundos y clasifícalo en una de estas categorías obligatorias:
1. 'Lead Caliente': Intención clara e inmediata de compra.
2. 'Cliente Potencial': Interés real pero con planes a futuro.
3. 'Cliente que Solo Pregunta': Soporte o información general operativa.
4. 'Lead Frío': Negativa, descartes o textos sin sentido.

REGLA DE RESPUESTA AUTOMÁTICA: Genera una respuesta persuasiva, humana y empática en español, orientada a cerrar la venta o resolver el soporte.
```

## 5. Flujo del usuario y Datos
1. **Estímulo y Clic:** El cliente visualiza la promoción y presiona el link del Sandbox.
2. **Orquestación:** El webhook recibe el payload de Twilio, Gemini ejecuta la clasificación semántica en milisegundos, Pandas inyecta la clasificación en el CSV y Twilio devuelve la respuesta comercial de vuelta por WhatsApp.
3. **Visualización Ejecutiva:** El evaluador de maestría hace uso de Streamlit, define los parámetros financieros en la barra lateral, y observa los picos analíticos calculados dinámicamente a partir de los registros históricos.

## 6. Restricciones
* **Coste cero:** Uso de las capas gratuitas de Google AI Studio, Twilio Sandbox, Ngrok y Streamlit Cloud.
* **Ciberseguridad:** Inyección en caliente de credenciales críticas en las variables de entorno; prohibido hardcodear llaves dentro del código fuente.
* **Privacidad de datos:** Anonimización de números telefónicos reales en las vistas públicas de Streamlit.

## 7. Criterios de aceptación y Matriz de Trazabilidad
* **Caso de Éxito Comercial e Interactividad Dinámica:** Ante registros clasificados como 'Lead Caliente' en el archivo analítico, el Dashboard debe recalcular dinámicamente los KPIs financieros (Ingreso Estimado, ROI y Ventas Estimadas) aplicando las fórmulas financieras sobre los parámetros del Sidebar (Costo, Precio, % Conversión) seleccionados por el usuario, sin usar valores quemados en código.
* **Caso de Estabilidad Gráfica:** Al ejecutar `app_dashboard.py`, Streamlit debe renderizar las tablas y los componentes visuales de Plotly leyendo el CSV maestro unificado por comas sin mezclar columnas.
* **Caso de Tolerancia a Fallos:** Si el agente local pierde conexión o la API excede su cuota, el bloque try-except debe atrapar los errores HTTP mostrando logs informativos sin tumbar el microservicio ni corromper el CSV.

### Matriz de Trazabilidad (Objetivos vs. Componente de IA)
| Requerimiento del Negocio | Componente Técnico | Solución de IA (Gemini) |
|---|---|---|
| Clasificar Intención | Clasificación Semántica Estricta | Tipado Pydantic `ClasificacionLead` |
| Tiempo de Respuesta | Backend Async Flask | Modelo `gemini-3.8-flash-lite` (<3s Latencia) |
| Respuesta Inmediata | Webhook Twilio + WhatsApp | Respuesta estructurada generada in-situ |
| Visibilidad Financiera | Sliders del Dashboard Streamlit | Fórmulas de ROI dinámicas vinculadas al CSV |

## 8. Fuera de alcance (por ahora)
* Procesamiento de imágenes (Computer Vision) enviadas por clientes al chat para cotizar repuestos de motos.
* Pasarela de cobros transaccionales bancarios integrados dentro del mismo chat de WhatsApp.

## 9. Diseño Visual, Interfaz (UI/UX) e Identidad de Marca
Para garantizar una experiencia de usuario (UX) corporativa y profesional propia de un sistema de Business Intelligence académico, la interfaz sigue directrices de diseño estrictas:

* **Paleta de Colores (Estilo Deportivo R&V):** Uso prioritario del **Rojo Automotriz/Carmesí** (`#D32F2F` / `#FF4B4B`) como color de acento principal para reflejar velocidad y dinamismo de marca, contrastando con grises oscuros de fondo neutro y tipografía blanca limpia en los títulos.
* **Diseño del Layout (Estructura Espacial):** Uso de configuración de pantalla ancha (`layout="wide"`).
  * **Barra Lateral (Sidebar):** Reservada para la carga del logotipo de identidad de marca `logo_rv.png` mediante un contenedor relativo controlado y los deslizadores dinámicos de parámetros económicos.
  * **Cuerpo Principal:** Panel superior con tres contenedores de tarjetas métricas (KPIs) en negrita (Ventas Estimadas, Ingreso Estimado y ROI Proyectado) para visibilidad inmediata, seguido de gráficos interactivos de barras y líneas de tiempo usando Plotly.
* **Identidad e Imagen de Marca:** Integración mandatoria del logotipo corporativo local en formato PNG transparente para evitar bordes blancos discordantes y lograr una inmersión visual fluida con el fondo de la plataforma de Streamlit.

## 10. Despliegue
* **Ruta de Despliegue elegida:** Streamlit Community Cloud acoplada directamente al repositorio público de GitHub (`ProyectoModuloIA/rv_motor_crm_v1`), leyendo de forma dinámica la base de datos distribuida en formato homogéneo.
* **URL del proyecto en GitHub:** https://github.com/PedroNunezMartinez/ProyectoModuloIA/tree/main/rv_motor_crm_v1
* **URL del dashboard en producción:** https://rv-motor-crm.streamlit.app
