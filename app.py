import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Configuración con tu logo personalizado
st.set_page_config(page_title="GESPORTS - Registro", page_icon="💪")

# --- CABECERA CON TU LOGO PERSONALIZADO ---
# Usamos el archivo local 'logo.png' que debes subir a tu GitHub
col_logo, col_titulo = st.columns([2, 3])
with col_logo:
    try:
        st.image("logo.png", width=250)
    except:
        st.write("Logo GESPORTS") # Texto de respaldo si no encuentra el archivo

conn = st.connection("gsheets", type=GSheetsConnection)

# 1. Leer datos
try:
    df = conn.read(ttl="0s")
    if not df.empty:
        df['Minutos'] = pd.to_numeric(df['Minutos'], errors='coerce').fillna(0).astype(int)
        df['Fecha'] = pd.to_datetime(df['Fecha'])
except Exception as e:
    st.error(f"Error al leer datos: {e}")
    df = pd.DataFrame(columns=['Fecha', 'Deporte', 'Minutos', 'Comentarios'])

# 2. Formulario de entrada
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
    st.success("✅ Guardado en Google Sheets")
    st.rerun()

# 3. Visualización de Tabla
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

    # 4. Sección de Gráficos (Abajo)
    st.markdown("---")
    st.subheader("📈 ESTADÍSTICAS TOTALES")
    stats_deporte = df.groupby('Deporte')['Minutos'].sum().reset_index()
    # Usamos el color verde del logo para el gráfico
    st.bar_chart(data=stats_deporte, x='Deporte', y='Minutos', color='#1d6335')
else:
    st.info("No hay datos todavía.")