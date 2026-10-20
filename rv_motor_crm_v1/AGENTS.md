Version:1.0StartHTML:0000000105EndHTML:0000046899StartFragment:0000038501EndFragment:0000046859<style></style>
├── rv_motor_crm/  (Directorio Principal del MVP)
  │   ├── agente_clasificador.ipynb   (Notebook experimental de Colab)
  │   ├── agente_webhook.py           (Orquestador Backend en Flask)
  │   ├── app.py                      (Script auxiliar del microservicio)
  │   ├── app_dashboard.py            (Frontend e interfaz en Streamlit)
  │   ├── logo_rv.png                 (Identidad visual e imagen corporativa)
  │   ├── mensajes_clasificados_ia.csv (Base de datos persistente por comas)
  │   ├── requirements.txt            (Congelamiento de librerías y SDKs)
  │   ├── README.md                   (Documentación principal con salvaguarda)
  │   ├── especificacion.md           (Especificación técnica del ecosistema)
  │   ├── AGENTS.md                   (Reglas de control de prompts para agentes)
  │   └── pitch.md                    (Matriz de pruebas y pitch ejecutivo)
  ├── app.py                          (Práctica general de la raíz)


# AGENTS.md· CRM AI Webhook Orchestrator & Dashboard (R&V Motor)

> ATENCIÓN AGENTE DE IA: Lee este archivo por completoantes de proponer cambios, escribir código o modificar los archivos del repositorio. Para Claude Code, un archivo CLAUDE.md apunta directamente aquí.Para Gemini CLI, GEMINI.md hace lo mismo.

## Qué es este proyecto

Un ecosistema inteligente de orquestación comercial y Business Intelligence desarrollado para la concesionaria de motocicletas R&V Motor. Intercepta mensajes entrantes de WhatsApp en tiempo real, losclasifica semánticamente según la intención de compra en menos de 3 segundosusando Gemini, automatiza respuestas persuasivas y computa métricas financierasde Retorno de Inversión (ROI) reflejadas en un panel web ejecutivo.

## Cómo está hecho

* **Lenguaje y Entorno:** Python 3.12 ejecutándose bajo un entorno virtual aislado (`(venv)`). * **Estructura Jerárquica del Repositorio:**

![dcd9d706-7bf0-4e03-a4fd-ceeba6312af9](file:///C:/Users/Pedro/Pictures/Typedown/dcd9d706-7bf0-4e03-a4fd-ceeba6312af9.png)

* **Base de Datos**: persistencia estructurada en mensajes_clasificados_ia.csv` utilizando delimitación por comas (`,`).

* **Capa de Orquestación y Backend (`agente_webhook.py` /`app.py`):** Microservicio basado en el framework Flask corriendo localmente enel puerto 5000, expuesto a internet mediante un túnel seguro de Ngrok yacoplado al webhook POST de la pasarela Twilio Sandbox.

* **Capa Core de Inteligencia Artificial:** Consumo de laAPI oficial de Google GenAI mediante el SDK moderno `google-genai==1.3.0`. El modelo base configurado de forma estricta es `gemini-3.8-flash` para garantizar baja latencia y estabilidad de cuota.

* **Capa de Control Estructurado:** Uso de la libreríaPydantic (`BaseModel`) mediante la clase `ClasificacionLead` para obligar aGemini a devolver una estructura JSON tipada rígida con los campos:`interes_ia`, `motivo_semantico` y `respuesta_automatica`.

* **Capa Analítica y Persistencia:** Librería Pandas para lamanipulación atómica de datos. El archivo de persistencia histórica es`mensajes_clasificados_ia.csv` y utiliza estrictamente una delimitación basadaen COMAS (`,`) para garantizar la homogeneidad analítica.

* **Capa de Visualización y BI (`app_dashboard.py`):**Dashboard público e interactivo desplegado en Streamlit Community Cloud(`rv-motor-crm.streamlit.app`) que consume el repositorio de GitHub pararenderizar métricas financieras y gráficos dinámicos de Plotly.

* **Entorno de Simulación:** Grupo de WhatsApp real"Cliente R&V Motors" (participantes controlados con estímulosvisuales de las Promociones #1 y #2 enlazadas a wa.me/14155238886) utilizadocomo arnés de pruebas de campo.

* **Especificación Completa:** Toda la lógica de negocio,prompts y flujos se encuentran detallados en el archivo `especificacion.md`.

## Reglas de Desarrollo

* **Ciberseguridad de Credenciales:** Las llaves de acceso(`GEMINI_API_KEY`, `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `GITHUB_TOKEN`)pertenecen a variables de entorno críticas. Deben inyectarse en caliente en laconsola de CMD mediante comandos `set`. Queda TERMINANTEMENTE PROHIBIDOhardcodear llaves dentro del código fuente, subirlas a GitHub o exponerlas encomentarios.

* **Tolerancia a Fallos del Webhook:** Cada invocación a la API de Gemini y Twilio debe estar contenida de manera obligatoria dentro debloques estructurados `try/except`. El parseo del JSON de Gemini debe sertolerante a fallos de mayúsculas/minúsculas usando operadores lógicos `or` paramitigar respuestas inesperadas de la IA.

* **Blindaje de Envío en Twilio:** Para prevenir el errorcrítico de Twilio `21654 (ContentSid Required)` dentro del Sandbox, elparámetro `body` de la función `twilio_client.messages.create` debe recibir la variable de texto explícitamente casteada como un string mediante`str(respuesta_automatica)`.

* **Bypass de Advertencia de Ngrok:** Toda respuesta HTT Pgenerada por el webhook de Flask debe inyectar explícitamente en la cabecera elparámetro `resp.headers["ngrok-skip-browser-warning"] ="true"` para evitar que la advertencia visual de Ngrok rompa elparseo de datos de Twilio.

* **Integridad del Repositorio:** Realiza modificacionesincrementales y atómicas (un solo cambio pequeño por petición). Si añades unadependencia, actualiza inmediatamente el archivo `requirements.txt`. No usesdatos personales reales en las pruebas.

## Cómo comprobar que funciona

1. **Levantar el Backend:** Activa el entorno virtual (`.\venv\Scripts\activate`),inyecta las variables de entorno vía CMD y ejecuta `python agente_webhook.py`.El servidor debe quedar escuchando en `http://127.0.0.1:5000`.

2. **Exponer la Red:** En otra consola CMD, inicia el túnelreservado ejecutando `C:\Ngrok\ngrok.exe http 5000` y valida el estado `online`apuntando a `enlisted-ethanol-elitism.ngrok-free.dev`.

3. **Ejecutar Casos de Prueba (Entrada → ResultadoEsperado):**

   * *Mensajecomercial directo:* "Hola, me interesa la moto R&V 200, tengo lainicial en mano..." → El sistema registra la fila en el CSV local como`Lead Caliente`, computa un Ingreso de \$2500.00, calcula un ROI del 1566%,ejecuta el push a GitHub y Twilio responde de vuelta en menos de 3 segundos.

   * *Mensajeoperativo/curioso:* "¿Cuál es su dirección y horarios?" → Registroguardado en el CSV como `Cliente que Solo Pregunta`, Ingreso de \$0.00, ROI de-100% y respuesta con datos de atención.

   * *Mensaje fuera detema o erróneo:* "Hola tía, avísame a qué hora sales..." →Clasificación semántica de `Lead Frío`, almacenamiento preventivo en la base dedatos sin alterar el flujo analítico estratégico y respuesta genérica neutral.

   * *Error deCuota/Caída de Servidor (429/503):* El microservicio intercepta el error en elbloque `except`, muestra el log de protección en el CMD de Flask y genera unbypass seguro sin corromper ni duplicar datos en el CSV histórico.

Version:1.0StartHTML:0000000105EndHTML:0000043688StartFragment:0000038498EndFragment:0000043648<style></style>

## Cómo montar el servicio y arrancar el script

Para levantar el entorno de producción local y el puenteanalítico, se debe seguir este procedimiento estricto en la consola de comandosde Windows (CMD):

1. **Montaje del Entorno Aislado e Instalación de Dependencias:**

   Navegar aldirectorio raíz del proyecto y activar el entorno virtual de Python:

   ```cmd

   cd C:\rv_motor_crm

   .\venv\Scripts\activate

   ```

   Garantizar quetodas las librerías base y SDKs estén congelados ejecutando:

   ```cmd

   pip install -r requirements.txt

   ```

2. **Inyección en Caliente de Variables de Ciberseguridad:**

   Cargar lascredenciales de los proveedores directamente en la memoria temporal de laconsola (reemplazando los valores por las llaves reales y sin dejar espaciosalrededor del signo `=`):

   ```cmd

   set GEMINI_API_KEY=tu_api_key_de_gemini_aqui

   set TWILIO_ACCOUNT_SID=tu_sid_de_twilio_aqui

   set TWILIO_AUTH_TOKEN=tu_auth_token_de_twilio_aqui

   setGITHUB_TOKEN=tu_token_de_github_aqui

   ```

3. **Arranque del Microservicio backend (Flask):**

   Iniciar elorquestador principal en modo escucha activa en el puerto 5000:

   ```cmd

   python agente_webhook.py

   ```

4. **Activación de la Pasarela de Red (Túnel Ngrok):**

   En una segundaventana de CMD independiente, levantar el puente seguro para exponer el puertolocal a internet:

   ```cmd

   cd C:\Ngrok

   ngrok.exe http 5000

   ```

   *Nota: Validar queel subdominio asignado coincida con la URL configurada en la sección"Sandbox Settings" de la consola de Twilio.*

Version:1.0StartHTML:0000000105EndHTML:0000041112StartFragment:0000038501EndFragment:0000041072<style></style>

## Cómo comprobar que funciona (Casos de Prueba)

Una vez que el backend está corriendo y el túnel de Ngrok seencuentra en estado `online`, se ejecutan las validaciones enviando mensajes delenguaje natural al Sandbox corporativo (+1 415 523 8886):

1. **Caso Comercial de Éxito (Lead Caliente):**

   - Entrada:*"Hola, me interesa la moto R&V 200, tengo la inicial en mano de\$1000..."*

   - Resultado:Registro indexado en el CSV local como `Lead Caliente`, cálculo analítico deIngreso de \$2500.00, ROI del 1566% y disparo de la respuesta comercialautomática al celular por Twilio en menos de 3 segundos.

2. **Caso Operativo (Cliente que Solo Pregunta):**

   - Entrada:*"¿En qué dirección física están y cuáles son sus horarios?"*

   - Resultado:Almacenamiento en el CSV como `Cliente que Solo Pregunta`, Ingreso de \$0.00,ROI de -100% y envío de respuesta informativa sobre la sucursal.

3. **Caso Fuera de Contexto (Lead Frío):**

   - Entrada: Mensajeserróneos, cadenas de spam o textos ajenos a motocicletas.

   - Resultado:Clasificación semántica de `Lead Frío`, persistencia en la base de datos paraauditoría de tráfico y respuesta neutral sin alterar las métricas comercialesdel Dashboard.

4. **Caso de Contingencia (Error de Red 429/503):**

   - Entrada: Solicitudentrante cuando la API de Google está saturada o sin cuota diaria.

   - Resultado: Elbloque `try-except` captura la excepción HTTP, imprime el log de error críticoen el CMD de Flask y ejecuta un bypass seguro que previene la caída delservidor y la corrupción de los datos analíticos.

## Qué no hacer

* **NO** borres, reescribas ni alteres la estructura delarchivo analítico `mensajes_clasificados_ia.csv` sin validar que use ladelimitación por comas.

* **NO** cambies la versión del modelo (`gemini-3.8-flash`)ni del SDK (`google-genai`) a variantes obsoletas descontinuadas por Google(como 1.5, 2.0 o 2.5) que gatillan errores 404.

* **NO** alteres la alineación de espacios de los bloquesinternos del `try` de Flask para evitar romper el script con un`IndentationError` o `TabError`.

* **NO** realices despliegues directos a la rama principalde GitHub sin antes verificar la ejecución local limpia en el puerto 5000.
