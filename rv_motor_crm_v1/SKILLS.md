# SKILLS.md · Catálogo de Capacidades y Lógica de Negocio - R&V Motor

Este archivo documenta las habilidades analíticas, funciones lógicas y capacidades técnicas estructuradas dentro de la suite de software de R&V Motor. Define la inteligencia operativa, fórmulas matemáticas y reglas de negocio que el sistema sabe computar.

## 1. Capacidades de Inteligencia Artificial (Natural Language Processing)
* **Clasificación Semántica Estricta:** Análisis psicológico y contextual en tiempo real del texto libre en español enviado por un usuario a través de WhatsApp, logrando categorizarlo bajo un esquema tipificado de 4 niveles comerciales: `Lead Caliente`, `Cliente Potencial`, `Cliente que Solo Pregunta` o `Lead Frío` usando el modelo `gemini-3.8-flash-lite`.
* **Generación Persuasiva Empática:** Redacción instantánea y síncrona de respuestas comerciales personalizadas que se adaptan al interés clasificado del prospecto, orientadas a la conversión y la retención inmediata, derivando el contacto al canal de cierre humano.
* **Garantía de Salida Estructurada (JSON):** Gobernanza estricta de la inferencia de la IA mediante un esquema Pydantic (`BaseModel`) para forzar una salida JSON limpia y libre de texto explicativo, lo cual previene errores de parseo en el backend Flask.

## 2. Capacidades de Fusión Analítica y Lógica Financiera Dinámica
El sistema posee la habilidad de traducir etiquetas semánticas cualitativas en variables cuantitativas continuas en memoria de forma instantánea, aplicando reglas financieras dinámicas alimentadas por la interacción del usuario en el frontend:

* **Cálculo Dinámico de Conversión e Ingresos:**
  A diferencia de modelos estáticos rígidos, la suite integra un motor de simulación financiera en `app_dashboard.py` que permite al usuario ajustar parámetros mediante deslizadores (sliders) en tiempo real:
  - **Leads de Alto Valor:** Identificación y agrupamiento de los prospectos más valiosos filtrando únicamente los registros que contengan en la columna `interes_ia` los estados `Lead Caliente` o `Cliente Potencial`.
  - **Ventas Estimadas:** Proyección entera del volumen de conversiones comerciales calculada bajo la fórmula:
    `Ventas Estimadas = ParteEntera((Leads de Alto Valor * Tasa de Conversión %) / 100)`
  - **Ingreso Estimado:** Simulación de entrada de capital calculada bajo la fórmula:
    `Ingreso Estimado = Ventas Estimadas * Precio Promedio de Motocicleta` *(donde el precio es parametrizado por el usuario en el sidebar)*.

* **Modelado del Retorno de Inversión (ROI) de Campaña:**
  Habilidad para computar en microsegundos el rendimiento económico neto de la inversión publicitaria relacionando el costo dinámico de campaña ingresado en el sidebar contra el ingreso estimado simulado, aplicando la ecuación:
  `ROI % = ((Ingreso Estimado - Costo de Campaña) / Costo de Campaña) * 100` *(siempre que Costo de Campaña > 0)*.

* **Métricas de Control Ejecutivo (Business Intelligence en Streamlit):**
  Procesamiento estadístico del DataFrame importado desde el CSV maestro por comas para inyectar KPIs en un contenedor horizontal simétrico de 4 columnas:
  ```python
  # Código lógico de cómputo en el Dashboard
  total_leads = len(df)
  leads_valorables = len(df[df["interes_ia"].isin(["Lead Caliente", "Cliente Potencial"])])
  ventas_estimadas = int((leads_valorables * tasa_conversion) / 100)
  ingreso_estimado = ventas_estimadas * valor_moto_promedio
  roi_calculado = ((ingreso_estimado - costo_campana) / costo_campana) * 100 if costo_campana > 0 else 0.0
  ```

## 3. Capacidades de Infraestructura y Redes
* **Orquestación Webhook de Entrada:** Habilidad para escuchar peticiones de tráfico de red asíncronas HTTP `POST` procedentes de Twilio Sandbox, procesar payloads URL-encoded, decodificar mensajes y consolidar de manera segura la persistencia en formato de comas en el archivo unificado `mensajes_clasificados_ia.csv`.
* **Evasión de Barreras de Inspección (Ngrok Bypass):** Capacidad técnica de inyectar dinámicamente cabeceras de elusión de seguridad (`ngrok-skip-browser-warning = true`) para garantizar la intercomunicación limpia del túnel de red sin intervención de clics manuales.
