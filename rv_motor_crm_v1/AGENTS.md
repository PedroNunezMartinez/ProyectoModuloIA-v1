# CRM AI Webhook Orchestrator & Dashboard (R&V Motor) - AGENTS.md

**ATENCIÓN AGENTE DE IA / COPILOT DE DESARROLLO:** Lee este archivo por completo antes de proponer cambios, escribir código o modificar los archivos del repositorio.

## Qué es este proyecto
Un ecosistema inteligente de orquestación comercial y Business Intelligence desarrollado para la concesionaria de motocicletas R&V Motor. Intercepta mensajes entrantes de WhatsApp en tiempo real, los clasifica semánticamente según la intención de compra en menos de 3 segundos usando Gemini, automatiza respuestas persuasivas y computa métricas financieras de Retorno de Inversión (ROI) dinámicas y proyectadas reflejadas en un panel web interactivo.

*Nota de Trazabilidad y Consistencia:* Antes de modificar cualquier funcionalidad, algoritmo, flujo de datos o interfaz de usuario, es de carácter obligatorio revisar, respetar y alinearse estrictamente al diseño técnico y diagramación plasmados en la [Especificación Técnica Oficial del Ecosistema (00_especificacion.md)](especificacion.md).

## Estructura Jerárquica del Repositorio
```
├── rv_motor_crm_v1/
│   ├── agente_clasificador.ipynb (Notebook experimental de Colab)
│   ├── agente_webhook.py (Orquestador Backend en Flask)
│   ├── app.py (Script auxiliar del microservicio)
│   ├── app_dashboard.py (Frontend e interfaz dinámica en Streamlit)
│   ├── logo_rv.png (Identidad visual e imagen corporativa transparente)
│   ├── mensajes_clasificados_ia.csv (Base de datos persistente por comas)
│   ├── requirements.txt (Congelamiento de librerías y SDKs)
│   ├── README.md (Documentación principal con salvaguarda)
│   ├── especificacion.md (Especificación técnica del ecosistema)
│   └── AGENTS.md (Reglas de control de prompts para agentes)
```

## Reglas de Desarrollo
1. **Ciberseguridad de Credenciales:** Las llaves de acceso (`GEMINI_API_KEY`, `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `GITHUB_TOKEN`) pertenecen a variables de entorno críticas. Queda TERMINANTEMENTE PROHIBIDO hardcodear llaves dentro del código fuente, subirlas a GitHub o exponerlas en comentarios.
2. **Interactividad Dinámica del Dashboard:** El archivo `app_dashboard.py` NUNCA debe simular o quemar valores estáticos fijos de ingresos o ROI para las categorías de clasificación. Las fórmulas matemáticas de KPIs (Ingreso Estimado, ROI, Ventas) de los Leads de Alto Valor deben calcularse enteramente de forma dinámica cruzando los datos del CSV con los valores de los sliders seleccionados en el sidebar por el usuario.
3. **Manejo del Logotipo Corporativo Local:** El script `app_dashboard.py` debe intentar cargar de manera relativa el logotipo corporativo usando `logo_rv.png` de manera local directa. Si no se encuentra, activará un fallback silencioso sin romper la inicialización.
4. **Capa Analítica y Persistencia:** El archivo de persistencia histórica es `mensajes_clasificados_ia.csv` y utiliza estrictamente una delimitación basada en COMAS (`,`) con la estructura de 9 columnas (`fecha_hora`, `telefono`, `mensaje_original`, `interes_ia`, `motivo_semantico`, `respuesta_automatica`, `canal`, `promocion`, `id_interaccion`).
5. **Bypass de Advertencia de Ngrok:** Toda respuesta HTTP generada por el webhook de Flask debe inyectar explícitamente en la cabecera el parámetro `resp.headers["ngrok-skip-browser-warning"] = "true"`.

## Casos de Prueba del Sistema Integrado

* **Caso Comercial de Éxito (Lead Caliente):** El sistema registra la fila en el CSV local como `Lead Caliente`, y el dashboard recalcula dinámicamente en tiempo real un Ingreso Estimado y ROI acorde a la fórmula: `(Leads Calientes * Tasa de Conversión% * Precio Promedio de Motocicleta)`. Twilio responde de vuelta con el mensaje persuasivo en menos de 3 segundos.
* **Caso Operativo (Cliente que Solo Pregunta):** Registro guardado en el CSV como `Cliente que Solo Pregunta`, con un impacto comercial neutro, mostrando la información de la sucursal.
* **Caso Fuera de Contexto (Lead Frío):** Clasificación semántica de `Lead Frío`, almacenamiento preventivo en la base de datos para auditoría de tráfico sin alterar el embudo estratégico.
* **Caso de Contingencia (Error de Red 429/503):** El microservicio intercepta el error en el bloque `except`, muestra el log de protección en consola y genera un bypass seguro que previene la caída del servidor y la corrupción de los datos analíticos.

## Qué NO Hacer
* **NO** borres, reescribas ni alteres la estructura del archivo analítico `mensajes_clasificados_ia.csv` sin validar que use la delimitación por comas.
* **NO** uses datos fijos o estáticos simulados en el código de Streamlit que contradigan o ignoren los parámetros de entrada de los sliders del sidebar.
* **NO** alteres la alineación de espacios de los bloques internos para evitar romper el script con un `IndentationError`.
