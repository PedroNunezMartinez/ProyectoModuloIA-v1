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

# 2. CARGA DE DATOS ADAPTADA A TU EMBUDO REAL
@st.cache_data
def cargar_datos():
    ruta_csv = os.path.join(os.path.dirname(__file__), 'mensajes_clasificados_ia.csv')

    if os.path.exists(ruta_csv):
        df_real = pd.read_csv(ruta_csv, sep=None, engine='python')
        df_real.columns = df_real.columns.str.strip().str.lower()

        columna_encontrada = None
        posibles_nombres = ['interes_ia', 'interes', 'intencion', 'clasificacion', 'categoria', 'label']

        if len(df_real.columns) > 4:
            for nombre in posibles_nombres:
                for col in df_real.columns:
                    if nombre in col:
                        columna_encontrada = col
                        break

        if columna_encontrada:
            df_real = df_real.rename(columns={columna_encontrada: 'interes_ia'})
        else:
            if len(df_real.columns) >= 5:
                df_real.rename(columns={df_real.columns[4]: 'interes_ia'}, inplace=True)

        if 'interes_ia' in df_real.columns:
            estados_validos = ['Lead Caliente', 'Lead Frío', 'Cliente Potencial', 'Cliente que Solo Pregunta']
            df_real['interes_ia'] = df_real['interes_ia'].apply(lambda x: x if str(x).strip() in estados_validos else 'Cliente que Solo Pregunta')

        return df_real

    return pd.DataFrame({
        'cliente': [f'Contacto {i}' for i in range(1, 13)],
        'interes_ia': ['Lead Caliente', 'Lead Frío', 'Cliente Potencial', 'Cliente que Solo Pregunta'] * 3,
        'motivo_semantico': ['Quiere financiar una 150cc', 'Mensaje equivocado', 'Quiere ver motos el sábado', 'Pregunta por horarios'] * 3,
        'respuesta_automatica': ['Claro, aquí tienes los planes...' for _ in range(12)]
    })

df = cargar_datos()

# 3. BARRA LATERAL (Carga de Logo Local y Filtros)
# Aquí hemos configurado tu logo local de forma nativa
if os.path.exists("rv_motor_crm_v1/logo_rv.png"):
    st.sidebar.image("rv_motor_crm_v1/logo_rv.png", width=120)
else:
    st.sidebar.image("https://icons8.com", width=80)  # Respaldo temporal si no encuentra la carpeta local

st.sidebar.title("R&V Motor CRM")
st.sidebar.caption("Módulo de Inteligencia Artificial")

st.sidebar.markdown("---")
st.sidebar.subheader("🧮 Calculadora de ROI")
costo_campana = st.sidebar.number_input("Inversión Campaña ($)", min_value=1.0, value=200.0, step=50.0)
valor_moto_promedio = st.sidebar.number_input("Precio Promedio Moto ($)", min_value=1000.0, value=3000.0, step=100.0)
tasa_conversion = st.sidebar.slider("Tasa de Conversión de Leads %", min_value=1, max_value=100, value=15)

st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Filtros del Embudo")
categorias_reales = ['Lead Caliente', 'Lead Frío', 'Cliente Potencial', 'Cliente que Solo Pregunta']
categorias_seleccionadas = st.sidebar.multiselect("Clasificación IA:", categorias_reales, default=categorias_reales)

df_filtrado = df[df['interes_ia'].isin(categorias_seleccionadas)]

# 4. CUERPO PRINCIPAL
st.title("🏍️ R&V Motor — AI Management & Lead Analytics")
st.markdown("Análisis automatizado de intenciones mediante **Gemini 3.8 Flash** en tiempo real.")
st.markdown("---")

# 5. BLOQUE DE MÉTRICAS (Matemática Financiera)
total_leads = len(df)
leads_valorables = len(df[df['interes_ia'].isin(['Lead Caliente', 'Cliente Potencial'])])
ventas_estimadas = int((leads_valorables * tasa_conversion) / 100)
ingreso_estimado = ventas_estimadas * valor_moto_promedio
roi_calculado = ((ingreso_estimado - costo_campana) / costo_campana) * 100 if costo_campana > 0 else 0

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="📥 Total Mensajes", value=total_leads)
with col2:
    st.metric(label="🎯 Leads de Alto Valor", value=leads_valorables, help="Suma de Leads Calientes y Clientes Potenciales")
with col3:
    st.metric(label="💰 Ingreso Estimado", value=f"${ingreso_estimado:,.2f}", delta=f"{ventas_estimadas} Ventas")
with col4:
    st.metric(label="📈 ROI Proyectado", value=f"{roi_calculado:.1f}%")

st.markdown("---")

# 6. BLOQUE DE GRÁFICOS
st.subheader("📊 Análisis Avanzado de Tráfico y Tendencia")
tab1, tab2 = st.tabs(["📊 Distribución de Leads", "📈 Tendencia Temporal"])

with tab1:
    col_graf1, col_graf2 = st.columns(2)
    
    with col_graf1:
        st.subheader("Tráfico con Conteo en Barra")
        df_conteo = df_filtrado['interes_ia'].value_counts().reset_index()
        df_conteo.columns = ['interes_ia', 'count']
        
        fig_bar = px.bar(
            df_conteo,
            x='interes_ia',
            y='count',
            labels={'interes_ia': 'Clasificación IA', 'count': 'Mensajes'},
            color='interes_ia',
            text='count',
            color_discrete_map={
                'lead caliente': '#EF553B',
                'cliente potencial': '#00CC96',
                'cliente que solo pregunta': '#636EFA',
                'lead frío': '#AB63FA'
            },
            template="plotly_dark"
        )
        fig_bar.update_traces(textposition='outside')
        fig_bar.update_layout(yaxis=dict(title='Total Mensajes (Eje Y)'))
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with col_graf2:
        st.subheader("Distribución del Embudo")
        fig_pie = px.pie(
            df_filtrado,
            names='interes_ia',
            hole=0.4,
            template="plotly_dark",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_pie, use_container_width=True)

with tab2:
    st.subheader("📈 Línea de Tendencia Acumulada de Leads")
    df_linea = df_filtrado.copy()
    if 'fecha' not in df_linea.columns:
        import datetime
        base_fecha = datetime.date.today() - datetime.timedelta(days=10)
        df_linea['fecha_simulada'] = [base_fecha + datetime.timedelta(days=i % 10) for i in range(len(df_linea))]
        df_linea = df_linea.sort_values(by='fecha_simulada')
        df_tendencia = df_linea.groupby(['fecha_simulada', 'interes_ia']).size().reset_index(name='nuevos_leads')
        
        fig_line = px.line(
            df_tendencia,
            x='fecha_simulada',
            y='nuevos_leads',
            color='interes_ia',
            markers=True,
            labels={'fecha_simulada': 'Fecha de Recepción', 'nuevos_leads': 'Cantidad de Leads'},
            template="plotly_dark",
            title="Evolución de contactos por día en R&V Motor"
        )
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        df_tendencia = df_linea.groupby(['fecha', 'interes_ia']).size().reset_index(name='nuevos_leads')
        fig_line = px.line(df_tendencia, x='fecha', y='nuevos_leads', color='interes_ia', markers=True, template="plotly_dark")
        st.plotly_chart(fig_line, use_container_width=True)

st.markdown("---")

# 7. TABLA DE DATOS INTERACTIVA
st.subheader("📋 Registro Histórico e Interacciones del Chatbot")

columnas_visibles = {}
mapeo_columnas = {
    'cliente': ['cliente', 'nombre', 'contacto', 'user', 'id'],
    'interes_ia': ['interes_ia', 'interes', 'intencion', 'clasificacion', 'categoria'],
    'motivo_semantico': ['motivo_semantico', 'motivo', 'razon', 'semantic', 'contexto'],
    'respuesta_automatica': ['respuesta_automatica', 'respuesta', 'bot_response', 'reply']
}

for variable_sistema, sinonimos in mapeo_columnas.items():
    for col in df_filtrado.columns:
        if col in sinonimos:
            columnas_visibles[variable_sistema] = col
            break

if len(columnas_visibles) > 0:
    st.dataframe(
        df_filtrado[list(columnas_visibles.values())],
        use_container_width=True,
        hide_index=True
    )
else:
    st.dataframe(
        df_filtrado,
        use_container_width=True,
        hide_index=True
    )
