import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Configuración inicial
st.set_page_config(page_title="GESPORTS - Registro", page_icon="💪")

# --- TRUCO PARA FONDO CLARO Y MEJORAR VISIBILIDAD ---
st.markdown("""
    <style>
    .main {
        background-color: #FFFFFF;
    }
    stp { color: black; }
    h1, h2, h3 { color: #1d6335; }
    </style>
    """, unsafe_allow_index=True)

# --- CABECERA CON TU LOGO ---
col_logo, col_titulo = st.columns([2, 3])
with col_logo:
    try:
        # Cargamos el logo con un ancho adecuado
        st.image("logo.png", width=280)
    except:
        st.subheader("GESPORTS")

# (Resto del código de conexión y formulario igual que antes...)
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    df = conn.read(ttl="0s")
    if not df.empty:
        df['Minutos'] = pd.to_numeric(df['Minutos'], errors='coerce').fillna(0).astype(int)
        df['Fecha'] = pd.to_datetime(df['Fecha'])
except Exception as e:
    df = pd.DataFrame(columns=['Fecha', 'Deporte', 'Minutos', 'Comentarios'])

# Formulario
with st.form(key='deporte_form'):
    col1, col2 = st.columns(2)
    with col1:
        fecha = st.date_input("Fecha", value=datetime.now())
        deporte = st.selectbox("Deporte", ["Padel", "Bici", "Flexiones", "Abdominales", "Running", "Gym"])
    with col2:
        minutos = st.number_input("Minutos", min_value=1, step=1, value=90)
    
    comentarios = st.text_area("Comentarios (opcional)")
    submit_button = st.form_submit_button(label='🚀 GUARDAR SESIÓN')

if submit_button:
    nueva_fila = pd.DataFrame([{
        "Fecha": fecha.strftime('%Y-%m-%d'),
        "Deporte": deporte,
        "Minutos": int(minutos),
        "Comentarios": comentarios
    }])
    updated_df = pd.concat([df, nueva_fila], ignore_index=True)
    conn.update(data=updated_df)
    st.success("✅ Guardado correctamente")
    st.rerun()

# Tabla y Gráficos
st.markdown("---")
st.subheader("📊 ÚLTIMOS REGISTROS")

if not df.empty:
    df_display = df.copy()
    df_display['Fecha'] = df_display['Fecha'].dt.strftime('%Y-%m-%d')
    st.table(df_display.sort_index(ascending=False).head(10))
    
    st.markdown("---")
    st.subheader("📈 ESTADÍSTICAS TOTALES")
    stats_deporte = df.groupby('Deporte')['Minutos'].sum().reset_index()
    # Color verde corporativo de tu logo
    st.bar_chart(data=stats_deporte, x='Deporte', y='Minutos', color='#1d6335')