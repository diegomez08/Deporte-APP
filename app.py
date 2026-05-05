import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Configuración inicial
st.set_page_config(page_title="GESPORTS - Registro", page_icon="💪")

# --- ESTILO PARA FONDO CLARO (CORREGIDO) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #FFFFFF;
    }
    p, span, label, th, td { color: #1f1f1f !important; }
    h1, h2, h3 { color: #1d6335 !important; }
    .stButton>button { background-color: #1d6335; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA CON TU LOGO ---
col_logo, col_titulo = st.columns([2, 3])
with col_logo:
    try:
        st.image("logo.png", width=280)
    except:
        st.subheader("GESPORTS")

# --- CONEXIÓN Y LÓGICA ---
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
    
    if st.button("🗑️ Borrar último registro"):
        if len(df) > 0:
            updated_df = df.drop(df.index[-1])
            conn.update(data=updated_df)
            st.warning("Registro eliminado")
            st.rerun()
            
    st.markdown("---")
    st.subheader("📈 ESTADÍSTICAS TOTALES")
    stats_deporte = df.groupby('Deporte')['Minutos'].sum().reset_index()
    st.bar_chart(data=stats_deporte, x='Deporte', y='Minutos', color='#1d6335')
else:
    st.info("No hay datos todavía.")