import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(
    page_title="R&V Motor - IA CRM Dashboard",
    page_icon="🏍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

st.markdown('<div class="main-title">🏍️ R&V Motor — CRM Analytics</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Sistema Inteligente de Orquestación Comercial y Analítica en Tiempo Real</div>', unsafe_allow_html=True)
st.markdown("--- ")

@st.cache_data
def cargar_datos():
    ruta_csv = 'mensajes_clasificados_ia.csv'
    if os.path.exists(ruta_csv):
        df_real = pd.read_csv(ruta_csv, sep=None, engine='python')
        df_real.columns = df_real.columns.str.strip()

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

    return pd.DataFrame({
        'Fecha_Hora': [pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')] * 4,
        'Telefono_Anonimizado': ['WhatsApp: +502XXXX1234'] * 4,
        'Mensaje': ['Hola, me interesa la moto'] * 4,
        'interes_ia': ['Lead Caliente', 'Cliente Potencial', 'Cliente que Solo Pregunta', 'Lead Frío'],
        'motivo_semantico': ['Interés inmediato', 'Pregunta plazos', 'Horarios de atención', 'No responde'],
        'respuesta_automatica': ['¡Hola! Con gusto te ayudamos...'] * 4
    })

df = cargar_datos()

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

st.sidebar.title("R&V Motor CRM")
st.sidebar.caption("Módulo de Inteligencia Artificial")
st.sidebar.markdown("--- ")

st.sidebar.subheader("🔍 Filtros del Embudo")
categorias_disponibles = ['Lead Caliente', 'Cliente Potencial', 'Cliente que Solo Pregunta', 'Lead Frío']
categorias_seleccionadas = st.sidebar.multiselect(
    "Filtrar por Clasificación IA:",
    categorias_disponibles,
    default=categorias_disponibles
)

df_filtrado = df[df['interes_ia'].isin(categorias_seleccionadas)]

total_leads = len(df_filtrado)
leads_calientes = len(df_filtrado[df_filtrado['interes_ia'] == 'Lead Caliente'])
leads_potenciales = len(df_filtrado[df_filtrado['interes_ia'] == 'Cliente Potencial'])
ingreso_total = df_filtrado['Ingreso_Estimado'].sum()
roi_promedio = df_filtrado[df_filtrado['interes_ia'].isin(['Lead Caliente', 'Cliente Potencial'])]['ROI_Numerico'].mean() if len(df_filtrado[df_filtrado['interes_ia'].isin(['Lead Caliente', 'Cliente Potencial'])]) > 0 else -100.0

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="🔥 Leads Calientes", value=f"{leads_calientes} leads")
with col2:
    st.metric(label="⚡ Clientes Potenciales", value=f"{leads_potenciales} leads")
with col3:
    st.metric(label="💰 Ingreso Estimado Acumulado", value=f"US$ {ingreso_total:,.2f}")
with col4:
    st.metric(label="📈 ROI Promedio (Leads Activos)", value=f"{roi_promedio:.1f}%")

st.markdown("--- ")

col_chart1, col_colchart2 = st.columns(2)

with col_chart1:
    st.subheader("📊 Volumen de Interacciones por Intención")
    df_conteo = df_filtrado['interes_ia'].value_counts().reset_index()
    df_conteo.columns = ['interes_ia', 'Cantidad']
    fig_bar = px.bar(
        df_conteo,
        x='interes_ia',
        y='Cantidad',
        color='interes_ia',
        text='Cantidad',
        color_discrete_map={
            'Lead Caliente': '#D32F2F',
            'Cliente Potencial': '#FBC02D',
            'Cliente que Solo Pregunta': '#1976D2',
            'Lead Frío': '#9E9E9E'
        },
        labels={'interes_ia': 'Clasificación Comercial'}
    )
    fig_bar.update_traces(textposition='outside')
    st.plotly_chart(fig_bar, use_container_width=True)

with col_colchart2:
    st.subheader("🎯 Proporción de Conversión de Clientes")
    fig_pie = px.pie(
        df_filtrado,
        names='interes_ia',
        hole=0.4,
        color='interes_ia',
        color_discrete_map={
            'Lead Caliente': '#D32F2F',
            'Cliente Potencial': '#FBC02D',
            'Cliente que Solo Pregunta': '#1976D2',
            'Lead Frío': '#9E9E9E'
        }
    )
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("--- ")

st.subheader("📋 Historial de Interacciones del Chatbot")
columnas_tabla = ['Telefono_Anonimizado', 'Mensaje', 'interes_ia', 'motivo_semantico', 'Ingreso_Estimado', 'respuesta_automatica']
columnas_existentes = [col for col in columnas_tabla if col in df_filtrado.columns]

st.dataframe(
    df_filtrado[columnas_existentes],
    use_container_width=True,
    hide_index=True
)
