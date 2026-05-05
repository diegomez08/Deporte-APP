import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Configuración inicial
st.set_page_config(page_title="GESPORTS - Registro", page_icon="💪")

# --- ESTILO PERSONALIZADO: MODO OSCURO CON CAJA DE LOGO BLANCA ---
st.markdown("""
    <style>
    /* Caja blanca para el logo */
    .logo-container {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 15px;
        display: flex;
        justify-content: center;
        margin-bottom: 25px;
    }
    /* Aseguramos que el resto de la app use los colores oscuros por defecto */
    .stApp {
        background-color: #0e1117;
    }
    h1, h2, h3, p, span, label {
        color: white !important;
    }
    /* Color de los títulos de las gráficas y secciones */
    .stSubheader {
        color: #1d6335 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA CON CONTENEDOR BLANCO PARA EL LOGO ---
st.markdown('<div class="logo-container">', unsafe_allow_html=True)
try:
    st.image("logo.png", width=300)
except:
    st.subheader("GESPORTS")
st.markdown('</div>', unsafe_allow_html=True)

st.title("REGISTRO DE ENTRENAMIENTO")

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
    # Usamos dataframe en lugar de table para que se adapte mejor al modo oscuro
    st.dataframe(df_display.sort_index(ascending=False).head(10), use_container_width=True)
    
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