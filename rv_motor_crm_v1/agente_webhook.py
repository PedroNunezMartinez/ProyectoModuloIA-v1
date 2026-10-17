
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Configuración de página de Streamlit
st.set_page_config(
    page_title="R&V Motor - Panel Analítico de IA",
    page_icon="🏍️",
    layout="wide"
)

CSV_FILE = 'mensajes_clasificados_ia.csv'

# Encabezado principal
st.title("🏍️ Sistema Inteligente de Orquestación Comercial y Analítica - R&V Motor")
st.markdown("---")

# Verificar si existe el archivo de persistencia de datos
if not os.path.exists(CSV_FILE):
    st.info("Esperando primeras interacciones... No se ha detectado el archivo 'mensajes_clasificados_ia.csv' todavía.")
    # Crear un dataset simulado de demostración para que el jurado pueda visualizar la UI
    datos_demo = pd.DataFrame({
        'id_interaccion': ['C051', 'C052', 'C053', 'C054', 'C055'],
        'remitente_anonimo': ['+XXX-XXXX-5551', '+XXX-XXXX-5552', '+XXX-XXXX-5553', '+XXX-XXXX-5554', '+XXX-XXXX-5555'],
        'mensaje_original': [
            'Quiero comprar la Yamaha FZ-S hoy mismo a US$2,999',
            'Me interesa la XR 190L, ¿tienen catálogo?',
            '¿Cuál es su dirección y horarios?',
            'No gracias, busco repuestos de otra marca.',
            '¿Cuáles son los requisitos de financiamiento?'
        ],
        'clasificacion': ['Lead Caliente', 'Cliente Potencial', 'Cliente que Solo Pregunta', 'Lead Frío', 'Lead Caliente'],
        'ingreso_estimado': [2500.0, 1200.0, 0.0, 0.0, 2500.0],
        'roi_estimado': [1566.0, 750.0, 0.0, 0.0, 1566.0],
        'respuesta_enviada': [
            '¡Excelente elección! La Yamaha FZ-S...', 
            '¡Hola! Claro que sí, adjunto...', 
            'Hola, nuestra sucursal...', 
            'Entendido, si cambias de parecer...', 
            '¡Hola! Los requisitos de financiamiento...'
        ],
        'modelo_utilizado': ['gemini-3.8-flash'] * 5,
        'estado_entrega': ['Entregado'] * 5
    })
    if st.button("Cargar datos de prueba R&V"): 
        datos_demo.to_csv(CSV_FILE, index=False)
        st.rerun()
else:
    # Cargar datos reales unificados por comas
    df = pd.read_csv(CSV_FILE)
    
    # KPIs Principales
    total_leads = len(df)
    leads_calientes = len(df[df['clasificacion'] == 'Lead Caliente'])
    ingreso_total = df['ingreso_estimado'].sum()
    roi_promedio = df[df['roi_estimado'] > 0]['roi_estimado'].mean() if len(df[df['roi_estimado'] > 0]) > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Interacciones Totales", f"{total_leads}")
    col2.metric("Leads Calientes (Conversión)", f"{leads_calientes}")
    col3.metric("Ingreso Estimado Acumulado", f"US$ {ingreso_total:,.2f}")
    col4.metric("ROI Promedio de Campaña", f"{roi_promedio:.1f}%")
    
    st.markdown("---")
    
    # Dos columnas para visualizaciones interactivas de Plotly
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Distribución Semántica de Intenciones")
        fig_pie = px.pie(
            df, 
            names='clasificacion', 
            color='clasificacion',
            color_discrete_map={
                'Lead Caliente': '#2ecc71',
                'Cliente Potencial': '#3498db',
                'Cliente que Solo Pregunta': '#f1c40f',
                'Lead Frío': '#e74c3c'
            }
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with col_chart2:
        st.subheader("Ingreso Estimado Acumulado por Clasificación")
        fig_bar = px.bar(
            df.groupby('clasificacion')['ingreso_estimado'].sum().reset_index(),
            x='clasificacion',
            y='ingreso_estimado',
            color='clasificacion',
            labels={'ingreso_estimado': 'Ingreso Estimado (USD)', 'clasificacion': 'Categoría'},
            color_discrete_map={
                'Lead Caliente': '#2ecc71',
                'Cliente Potencial': '#3498db',
                'Cliente que Solo Pregunta': '#f1c40f',
                'Lead Frío': '#e74c3c'
            }
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
    # Tabla con datos crudos y protección de privacidad
    st.subheader("Histórico de Interacciones Sincronizadas")
    st.dataframe(df[[
        'id_interaccion', 'remitente_anonimo', 'mensaje_original', 
        'clasificacion', 'ingreso_estimado', 'roi_estimado', 'estado_entrega'
    ]], use_container_width=True)

