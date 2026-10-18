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

# Estilos corporativos
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

# 2. CARGA DE DATOS TOLERANTE A FALLOS
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

    # Datos simulados si el CSV no existe localmente
    ahora = pd.Timestamp.now()
    fechas = [(ahora - pd.Timedelta(minutes=15 * i)).strftime('%Y-%m-%d %H:%M:%S') for i in range(25)]
    import random
    categorias = ['Lead Caliente', 'Cliente Potencial', 'Cliente que Solo Pregunta', 'Lead Frío']
    return pd.DataFrame({
        'Fecha_Hora': fechas,
        'Telefono_Anonimizado': [f'WhatsApp: +502XXXX{random.randint(1000, 9999)}' for _ in range(25)],
        'Mensaje': ['Me interesa comprar una moto' if i % 4 == 0 else '¿Qué precio tiene?' for i in range(25)],
        'interes_ia': [random.choice(categorias) for _ in range(25)],
        'motivo_semantico': ['Interés general' for _ in range(25)],
        'respuesta_automatica': ['¡Hola! En un momento te atendemos...'] * 25
    })

df = cargar_datos()

if 'Fecha_Hora' in df.columns:
    df['Fecha_Hora_dt'] = pd.to_datetime(df['Fecha_Hora'], errors='coerce')
else:
    df['Fecha_Hora_dt'] = pd.Timestamp.now()

# 3. MATEMÁTICA FINANCIERA
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

# 4. BARRA LATERAL
st.sidebar.title("R&V Motor CRM")
st.sidebar.caption("Módulo de Inteligencia Artificial")
st.sidebar.markdown("--- ")

st.sidebar.subheader("🔍 Filtros")
categorias_disponibles = ['Lead Caliente', 'Cliente Potencial', 'Cliente que Solo Pregunta', 'Lead Frío']
categorias_seleccionadas = st.sidebar.multiselect(
    "Filtrar por Clasificación IA:",
    categorias_disponibles,
    default=categorias_disponibles
)

df_filtrado = df[df['interes_ia'].isin(categorias_seleccionadas)]

# 5. METRICAS / KPIs
total_leads = len(df_filtrado)
leads_calientes = len(df_filtrado[df_filtrado['interes_ia'] == 'Lead Caliente'])
leads_potenciales = len(df_filtrado[df_filtrado['interes_ia'] == 'Cliente Potencial'])
ingreso_total = df_filtrado['Ingreso_Estimado'].sum()
roi_promedio = df_filtrado[df_filtrado['interes_ia'].isin(['Lead Caliente', 'Cliente Potencial'])]['ROI_Numerico'].mean() if len(df_filtrado[df_filtrado['interes_ia'].isin(['Lead Caliente', 'Cliente Potencial'])]) > 0 else -100.0

tasa_conversion = 0.0
if total_leads > 0:
    tasa_conversion = ((leads_calientes + leads_potenciales) / total_leads) * 100.0

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric(label="🔥 Leads Calientes", value=f"{leads_calientes} leads")
with col2:
    st.metric(label="⚡ Clientes Potenciales", value=f"{leads_potenciales} leads")
with col3:
    st.metric(label="📊 Tasa de Conversión", value=f"{tasa_conversion:.1f}%")
with col4:
    st.metric(label="💰 Ingreso Estimado", value=f"US$ {ingreso_total:,.2f}")
with col5:
    st.metric(label="📈 ROI Promedio", value=f"{roi_promedio:.1f}%")

st.markdown("--- ")

# 6. PESTAÑAS (TABS) - DISEÑO GRÁFICO CORREGIDO
tab_general, tab_temporal = st.tabs(["📊 Métricas y Proporciones", "📈 Evolución Temporal de Leads"])

colores_map = {
    'Lead Caliente': '#D32F2F',
    'Cliente Potencial': '#FBC02D',
    'Cliente que Solo Pregunta': '#1976D2',
    'Lead Frío': '#9E9E9E'
}

with tab_general:
    # Usamos una división perfecta 1:1 para que las dos columnas tengan exactamente el mismo tamaño
    col_chart_container, col_filters_side = st.columns([1, 1])

    with col_chart_container:
        st.subheader("Volumen de Interacciones por Intención")
        if not df_filtrado.empty:
            df_conteo = df_filtrado['interes_ia'].value_counts().reset_index()
            df_conteo.columns = ['interes_ia', 'Cantidad']

            fig_bar = px.bar(
                df_conteo,
                x='interes_ia',
                y='Cantidad',
                color='interes_ia',
                text='Cantidad',
                color_discrete_map=colores_map,
                labels={'interes_ia': 'Clasificación Comercial', 'Cantidad': 'Total Clientes'}
            )

            fig_bar.update_traces(
                textposition='outside',
                textfont_size=14,
                cliponaxis=False
            )
            # Mantiene la escala de barras dinámica y natural, y reactiva la leyenda interactiva (showlegend=True)
            fig_bar.update_layout(
                showlegend=True,
                margin=dict(t=30, b=10, l=10, r=10)
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Selecciona categorías para generar la gráfica.")

    with col_filters_side:
        st.subheader("Proporción de Conversión de Clientes")
        if not df_filtrado.empty:
            fig_pie = px.pie(
                df_filtrado,
                names='interes_ia',
                hole=0.4,
                color='interes_ia',
                color_discrete_map=colores_map
            )
            # Muestra leyenda en el gráfico de pastel
            fig_pie.update_layout(
                margin=dict(t=30, b=10, l=10, r=10),
                showlegend=True
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No hay datos para mostrar la proporción.")

with tab_temporal:
    st.subheader("Evolución Comercial de Leads en el Tiempo")
    if not df_filtrado.empty and 'Fecha_Hora_dt' in df_filtrado.columns:
        df_linea = df_filtrado.copy()
        df_linea['Fecha_Agrupada'] = df_linea['Fecha_Hora_dt'].dt.strftime('%Y-%m-%d %H:00')
        df_tendencia = df_linea.groupby(['Fecha_Agrupada', 'interes_ia']).size().reset_index(name='Cantidad_Leads')
        df_tendencia = df_tendencia.sort_values(by='Fecha_Agrupada')

        fig_line = px.line(
            df_tendencia,
            x='Fecha_Agrupada',
            y='Cantidad_Leads',
            color='interes_ia',
            markers=True,
            color_discrete_map=colores_map,
            labels={'Fecha_Agrupada': 'Fecha y Hora', 'Cantidad_Leads': 'Cantidad de Mensajes'}
        )
        fig_line.update_layout(
            xaxis_tickangle=-45,
            margin=dict(t=30, b=10, l=10, r=10)
        )
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("No hay datos suficientes para graficar la evolución temporal.")

st.markdown("--- ")

# 7. TABLA DE REGISTROS
st.subheader("📋 Historial de Interacciones del Chatbot")
columnas_tabla = ['Telefono_Anonimizado', 'Mensaje', 'interes_ia', 'motivo_semantico', 'Ingreso_Estimado', 'respuesta_automatica']
columnas_existentes = [col for col in columnas_tabla if col in df_filtrado.columns]

st.dataframe(
    df_filtrado[columnas_existentes],
    use_container_width=True,
    hide_index=True
)
