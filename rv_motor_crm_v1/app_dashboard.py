import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="R&V Motor - IA CRM Dashboard",
    page_icon="🏍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS personalizado para alinearse a la identidad corporativa de R&V Motor
st.markdown("""
    <style>
    .main-title {
        font-size: 38px;
        font-weight: bold;
        color: #D32F2F;
        text-align: center;
        margin-bottom: 5px;
    }
    .subtitle {
        font-size: 18px;
        color: #555555;
        text-align: center;
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado Principal
st.markdown('<div class="main-title">🏍️ R&V Motor — CRM Analytics</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Sistema Inteligente de Orquestación Comercial y Analítica en Tiempo Real</div>', unsafe_allow_html=True)
st.markdown("--- ")

# 2. CARGA DE DATOS CON CONFIGURACIÓN HÍBRIDA TOLERANTE A FALLOS
@st.cache_data
def cargar_datos():
    ruta_csv = 'mensajes_clasificados_ia.csv'
    if os.path.exists(ruta_csv):
        # Leer CSV
        df_real = pd.read_csv(ruta_csv, sep=None, engine='python')
        df_real.columns = df_real.columns.str.strip()

        # Mapeo inteligente de variantes de columnas
        mapeo_columnas = {
            'interes_ia': ['Interes_IA', 'clasificacion_ia', 'interes_ia', 'intencion', 'clasificacion'],
            'motivo_semantico': ['Motivo_Semantico', 'motivo_analisis', 'motivo_semantico', 'motivo'],
            'respuesta_automatica': ['Respuesta_Automatica', 'respuesta_sugerida', 'respuesta_automatica', 'respuesta']
        }

        for col_estandar, variantes in mapeo_columnas.items():
            for col_existente in df_real.columns:
                if col_existente in variantes:
                    df_real.rename(columns={col_existente: col_estandar}, inplace=True)
                    break

        if 'interes_ia' in df_real.columns:
            categorias_validas = ['Lead Caliente', 'Cliente Potencial', 'Cliente que Solo Pregunta', 'Lead Frío']
            df_real['interes_ia'] = df_real['interes_ia'].apply(
                lambda x: str(x).strip() if str(x).strip() in categorias_validas else 'Cliente que Solo Pregunta'
            )
        return df_real

    # Dataset de respaldo sintético si no se encuentra el archivo físico
    ahora = pd.Timestamp.now()
    fechas = [(ahora - pd.Timedelta(hours=i)).strftime('%Y-%m-%d %H:%M:%S') for i in range(12)]
    return pd.DataFrame({
        'Fecha_Hora': fechas,
        'Telefono_Anonimizado': ['WhatsApp: +502XXXX1234'] * 12,
        'Mensaje': ['Hola, me interesa la moto'] * 12,
        'interes_ia': ['Lead Caliente', 'Cliente Potencial', 'Cliente que Solo Pregunta', 'Lead Frío'] * 3,
        'motivo_semantico': ['Interés inmediato', 'Pregunta plazos', 'Horarios de atención', 'No responde'] * 3,
        'respuesta_automatica': ['¡Hola! Con gusto te ayudamos...'] * 12
    })

df = cargar_datos()

# Asegurar que Fecha_Hora sea tipo datetime para la gráfica de líneas
if 'Fecha_Hora' in df.columns:
    df['Fecha_Hora_dt'] = pd.to_datetime(df['Fecha_Hora'], errors='coerce')
else:
    df['Fecha_Hora_dt'] = pd.Timestamp.now()

# 3. LÓGICA DE MATEMÁTICA FINANCIERA (Criterios de Aceptación de la Especificación de Maestría)
def calcular_ingreso(row):
    cat = str(row['interes_ia']).strip()
    if cat == 'Lead Caliente': return 2500.0
    elif cat == 'Cliente Potencial': return 1200.0
    return 0.0

def calcular_roi(row):
    cat = str(row['interes_ia']).strip()
    if cat == 'Lead Caliente': return 1566.0
    elif cat == 'Cliente Potencial': return 750.0
    return -100.0

if 'interes_ia' in df.columns:
    df['Ingreso_Estimado'] = df.apply(calcular_ingreso, axis=1)
    df['ROI_Numerico'] = df.apply(calcular_roi, axis=1)
else:
    df['Ingreso_Estimado'] = 0.0
    df['ROI_Numerico'] = -100.0

if 'telefono' in df.columns:
    df['Telefono_Anonimizado'] = df['telefono'].apply(lambda x: f"WhatsApp: +502XXXX{str(x)[-4:]}" if len(str(x)) >= 4 else "WhatsApp: Oculto")
elif 'Telefono_Anonimizado' not in df.columns:
    df['Telefono_Anonimizado'] = "WhatsApp: Oculto"

if 'mensaje_texto' in df.columns:
    df.rename(columns={'mensaje_texto': 'Mensaje'}, inplace=True)
if 'id_cliente' in df.columns:
    df.rename(columns={'id_cliente': 'ID'}, inplace=True)

# 4. RENDERS DE LA BARRA LATERAL (Filtros del Líder Comercial)
st.sidebar.title("R&V Motor CRM")
st.sidebar.caption("Módulo de Inteligencia Artificial")
st.sidebar.markdown("--- ")

st.sidebar.subheader("🔍 Filtros del Embudo")
categorias_disponibles = ['Lead Caliente', 'Cliente Potencial', 'Cliente que Solo Pregunta', 'Lead Frío']
categorias_seleccionadas = st.sidebar.multiselect(
    
