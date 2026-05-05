import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Configuración con Logo de Pádel y Título
st.set_page_config(page_title="Registro de Deporte", page_icon="🎾")

# --- CABECERA CON LOGO DE PÁDEL ---
col_logo, col_titulo = st.columns([1, 4])
with col_logo:
    # Icono moderno de pala de pádel
    st.image("https://cdn-icons-png.flaticon.com/512/3257/3257127.png", width=80)
with col_titulo:
    st.title("REGISTRO DE ENTRENAMIENTO")

conn = st.connection("gsheets", type=GSheetsConnection)

# 1. Leer datos de Google Sheets
try:
    df = conn.read(ttl="0s")
    if not df.empty:
        # Limpieza: Minutos a entero y Fecha a datetime
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
        minutos = st.number_input("Minutos", min_value=1, step=1, value=90) # Puesto a 90 por defecto (partido padel)
    
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

# 3. Visualización de Tabla y Botón de Borrar
st.markdown("---")
st.subheader("📊 ÚLTIMOS REGISTROS")

if not df.empty:
    df_display = df.copy()
    # Formateamos la fecha para que se vea limpia en la tabla
    df_display['Fecha'] = df_display['Fecha'].dt.strftime('%Y-%m-%d')
    st.table(df_display.sort_index(ascending=False).head(10))
    
    if st.button("🗑️ Borrar último registro"):
        if len(df) > 0:
            updated_df = df.drop(df.index[-1])
            conn.update(data=updated_df)
            st.warning("Registro eliminado")
            st.rerun()

    # 4. Sección de Gráficos (Al final de la página)
    st.markdown("---")
    st.subheader("📈 ESTADÍSTICAS TOTALES")
    
    # Agrupamos los minutos por cada deporte
    stats_deporte = df.groupby('Deporte')['Minutos'].sum().reset_index()
    
    # Gráfico de barras con color temático
    st.bar_chart(data=stats_deporte, x='Deporte', y='Minutos', color='#00A8E8') # Azul deportivo
else:
    st.info("No hay datos todavía.")