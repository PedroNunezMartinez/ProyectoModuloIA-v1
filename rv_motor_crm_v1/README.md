# 🏍️ R&V Motor - Sistema CRM & Chatbot Automático con IA

Este proyecto corresponde al entregable final del **Módulo de Programación con Inteligencia Artificial** de la Maestría en IA. Consiste en un prototipo real y funcional (MVP) de un CRM inteligente capaz de procesar mensajes entrantes de clientes, simular interacciones de campañas de marketing de motocicletas, clasificar el nivel de interés de los leads y visualizar las métricas en un Dashboard analítico en tiempo real.

---

## 🎯 Descripción y Funcionamiento del Proyecto

El sistema está diseñado para automatizar la atención al cliente y medir el impacto financiero de las campañas publicitarias de la concesionaria **R&V Motor**:

1. **Simulación e Interacción de Campañas:** El sistema permite registrar promociones de motocicletas específicas. Para evaluar el impacto y medir la rentabilidad real de la campaña de marketing, se inyectan interacciones de clientes en lenguaje natural.
2. **Entrada de Mensajes (Omnicanalidad Prototipada):** En la fase de pruebas del MVP, las interacciones se gestionan mediante dos vías:
   * Un script automatizado en **Google Colab** que inyecta un lote de 50 leads de prueba con comportamientos mixtos.
   * Una conexión controlada en vivo empleando un dispositivo móvil real (el teléfono de la esposa del desarrollador) a través de un entorno seguro como **Twilio Sandbox para WhatsApp**.
3. **Procesamiento Analítico (Agente LLM):** Cada mensaje entrante es interceptado y enviado al modelo de lenguaje. El agente analiza psicológicamente el texto del usuario para comprender su nivel de urgencia e intención de compra, y redacta una respuesta comercial óptima.
4. **Persistencia e Interfaz de Control:** Las clasificaciones y variables analizadas por la IA se guardan en una base de datos estructurada. Estos datos alimentan dinámicamente un Dashboard en **Streamlit** que calcula de forma automática el Retorno de Inversión (ROI) y muestra gráficamente la salud del embudo de ventas.

### 📊 Criterios de Clasificación de Leads
El Agente de IA evalúa la semántica de los mensajes y asigna estrictamente una de las siguientes categorías:
* **Lead Caliente:** Alta intención de compra inmediata. Clientes decididos que solicitan métodos de pago, datos de transferencia bancaria o disponibilidad para apartar/retirar un modelo de motocicleta el mismo día.
* **Cliente Potencial:** Interés real y genuino pero en fase de maduración. Usuarios que solicitan requisitos para planes de financiamiento, créditos de la casa, fichas técnicas o agendan citas para visitar el local físico.
* **Lead Frío:** Dudas muy vagas, saludos sin continuidad comercial o rechazo explícito por objeciones de costo ("está muy caro gracias", "solo miraba precios", "ok").
* **Irrelevante / Spam:** Mensajes erróneos o fuera del rubro comercial de la empresa.

---

## 📅 Plan de Ejecución General (4 Semanas)

El proyecto se desarrolla bajo una metodología ágil incremental basada en hitos semanales:
* **Semana 1 (Hito Actual):** Configuración de la infraestructura cloud, entorno aislado de carpetas en GitHub, definición de requerimientos y despliegue del cascarón visual.
* **Semana 2:** Programación del pipeline del Agente de IA y estructuración del prompt de clasificación en formato JSON estricto mediante Google Colab.
* **Semana 3:** Diseño e implementación del Dashboard analítico, gráficas dinámicas de Plotly y la calculadora de ROI en Streamlit.
* **Semana 4:** Evaluación científica del modelo (Métricas académicas y matriz de confusión) e integración final del chat interactivo en tiempo real para la demostración en vivo.

---
## 🤖 Ingeniería de Prompts & Arquitectura del Agente (Semana 2)

Para garantizar la estabilidad del pipeline analítico y forzar al modelo **Gemini 3.8 Flash** a responder en JSON estricto sin romper la estructura de las filas, se diseñó un prompt basado en asignación de rol, restricciones semánticas y control de formato de salida (`response_mime_type="application/json"`). 

El diseño lógico del prompt instruye al agente a evaluar las intenciones de compra y redactar respuestas comerciales automatizadas de forma síncrona. La evidencia técnica de este desarrollo, el manejo de errores (bloques `try-except`) y las pausas controladas para respetar los límites de la API gratuita se encuentran documentados de forma transparente en el cuaderno de desarrollo **`agente_clasificador.ipynb`**, el cual alimenta de manera directa el set de datos enriquecido **`mensajes_clasificados_ia.csv`**.

---

## ⚙️ Arquitectura Tecnológica (Hito Semana 1)

La infraestructura base ha sido aislada por completo dentro del directorio `rv_motor_crm/` para garantizar la replicabilidad del contenedor de producción sin alterar las prácticas regulares del aula:
* `app_dashboard.py`: Archivo principal de la interfaz visual construido sobre **Streamlit**.
* `requirements.txt`: Archivo de configuración que congela las dependencias analíticas y de IA requeridas.
* `README.md`: Documentación técnica del estado del arte del proyecto (este archivo).

### Librerías del Ecosistema
* **Streamlit (v1.35.0):** Framework para el desarrollo de la interfaz de usuario web.
* **Pandas (v2.2.2):** Biblioteca de manipulación de estructuras de datos.
* **Google Generative AI (v0.5.4):** SDK oficial para conectar con los modelos fundacionales de Gemini 3.8 Flash
* **Plotly (v5.22.0):** Biblioteca gráfica interactiva para analíticas de negocio.
* **Google GenAI SDK (v1.3.0):** Biblioteca moderna oficial para la invocación estructurada del modelo gemini-3.8-flash [1.1].
* **Twilio Python SDK:** Framework para la conexión y transmisión atómica del payload mediante webhooks seguros de WhatsApp [1.1].

---

## 🔒 Buenas Prácticas de Ciberseguridad Aplicadas

Siguiendo las directrices avanzadas de desarrollo seguro en IA, **este proyecto prohíbe estrictamente la exposición de API Keys en el código fuente**:
* **En desarrollo (Google Colab):** Las llaves se consumen mediante el gestor nativo de secrets (`from google.colab import userdata`).
* **En producción (Streamlit Cloud):** Las credenciales se inyectan dinámicamente utilizando el entorno cifrado de Streamlit Secrets (`st.secrets`).

---
🤖 Declaración Académica y Salvaguarda de Autoría (Uso Ético de IA)
En estricto cumplimiento con el marco de integridad académica de la Maestría en IA, se declara formalmente la metodología implementada en el uso de herramientas generativas:

* **Desarrollo y Laboratorio Independiente (Google Colab):** Las fases experimentales de calibración lógica, optimización de hiperparámetros de temperatura, pruebas del prompt de sistema y la inyección sintética del lote inicial de 50 leads se ejecutaron de manera autónoma en cuadernos de Google Colab bajo la estricta autoría intelectual del desarrollador [1.1].
* **Uso Controlado de IA como Copiloto Técnico:** Se emplearon asistentes de inteligencia artificial generativa exclusivamente como herramientas de apoyo para la optimización de código base (refactorización de bloques `try-except`), depuración de errores lógicos de indentación (`TabError`) y formateo estructural de los documentos Markdown de especificación técnica [1.1, 1.3].
* **Gobernanza del Proyecto:** El diseño conceptual del pipeline, la integración de la pasarela local con Flask/Twilio/Ngrok, las ecuaciones de fusión financiera para el cómputo en vivo del Retorno de Inversión (ROI) y la recolección física de evidencias comerciales reales en el Sandbox representan un esfuerzo de ingeniería original e independiente ideado en su totalidad por el autor [1.1, 1.2].
---

## 🚀 Escalabilidad Comercial Futura
La arquitectura de software propuesta desacopla totalmente el canal de mensajería del motor de IA. Esto garantizará que, tras concluir el módulo académico, el prototipo pueda escalarse e integrarse directamente a los canales de producción reales de la empresa: **WhatsApp Business API (Oficial)**, **Instagram Graph API**, **Facebook Messenger** y CRMs corporativos (como HubSpot o Zoho CRM) mediante Webhooks estables de alta disponibilidad.

---

## 🛠️ Instrucciones de Evaluación para el Docente

Para compilar y visualizar el estado actual del prototipo de la Semana 1 en Streamlit Cloud de forma independiente:
1. En el panel de control de Streamlit Cloud, cree una nueva aplicación conectada a este repositorio.
2. En el campo **"Main file path"**, asegúrese de apuntar a la ruta interna: `rv_motor_crm/app_dashboard.py`.
3. La aplicación se ejecutará de forma aislada, instalando su propio contenedor de dependencias sin alterar la práctica `app.py` ubicada en la raíz del repositorio.
