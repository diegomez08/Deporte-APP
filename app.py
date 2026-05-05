import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import base64

# 1. Configuración de página
st.set_page_config(page_title="GESPORTS - Registro", page_icon="💪")

# 2. Función para convertir la imagen a formato web (Base64)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# 3. Estilo CSS para fondo oscuro y contenedor de logo blanco
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
    }
    .logo-box {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 25px;
    }
    h1, h2, h3, p, span, label {
        color: white !important;
    }
    .stSubheader {
        color: #1d6335 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. Cabecera con Logo GESPORTS integrado en caja blanca
try:
    logo_data = get_base64_of_bin_file('logo.png')
    st.markdown(f"""
        <div class="logo-box">
            <img src="data:image/png;base64,{logo_data}" width="280">
        </div>
    """, unsafe_allow_html=True)
except:
    st.markdown("""
        <div class="logo-box">
            <h1 style="color: #1d6335; margin: 0; font-family: sans-serif;">GESPORTS</h1>
        </div>
    """, unsafe_allow_html=True)

st.title("REGISTRO DE ENTRENAMIENTO")

# 5. Conexión con Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    df = conn.read(ttl="0s")
    if not df.empty:
        df['Minutos'] = pd.to_numeric(df['Minutos'], errors='coerce').fillna(0).astype(int)
        df['Fecha'] = pd.to_datetime(df['Fecha'])
except Exception as e:
    df = pd.DataFrame(columns=['Fecha', 'Deporte', 'Minutos', 'Comentarios'])

# 6. Formulario de entrada de datos
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

# 7. Tabla de registros recientes
st.markdown("---")
st.subheader("📊 ÚLTIMOS REGISTROS")

if not df.empty:
    df_display = df.copy()
    df_display['Fecha'] = df_display['Fecha'].dt.strftime('%Y-%m-%d')
    st.dataframe(df_display.sort_index(ascending=False).head(10), use_container_width=True)
    
    if st.button("🗑️ Borrar último registro"):
        if len(df) > 0:
            updated_df = df.drop(df.index[-1])
            conn.update(data=updated_df)
            st.warning("Registro eliminado")
            st.rerun()
            
    # 8. Gráfico de estadísticas (Al final)
    st.markdown("---")
    st.subheader("📈 ESTADÍSTICAS TOTALES (MINUTOS)")
    stats_deporte = df.groupby('Deporte')['Minutos'].sum().reset_index()
    st.bar_chart(data=stats_deporte, x='Deporte', y='Minutos', color='#1d6335')
else:
    st.info("No hay datos todavía.")