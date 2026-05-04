import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Registro de Deporte", page_icon="🏋️‍♂️")

st.title("🏋️‍♂️ REGISTRO DE ENTRENAMIENTO")

# 1. Conexión con Google Sheets
# Ahora usamos la configuración definida en [connections.gsheets]
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. Leer los datos
try:
    # Intentamos leer la hoja usando la URL de los secrets
    df = conn.read(ttl="0s")
except Exception as e:
    st.error(f"Error de conexión: {e}")
    # Si falla, creamos un DF vacío para que la app no explote
    df = pd.DataFrame(columns=['Fecha', 'Deporte', 'Minutos', 'Comentarios'])

# 3. Formulario de entrada
with st.form(key='deporte_form'):
    fecha = st.date_input("Fecha", value=datetime.now())
    deporte = st.selectbox("Deporte", ["Padel", "Bici", "Flexiones", "Abdominales", "Running", "Gym"])
    minutos = st.number_input("Minutos", min_value=1, step=5)
    comentarios = st.text_area("Comentarios (opcional)")
    
    submit_button = st.form_submit_button(label='GUARDAR SESIÓN')

# 4. Lógica de guardado
if submit_button:
    # Crear el nuevo registro
    nueva_fila = pd.DataFrame([{
        "Fecha": fecha.strftime('%Y-%m-%d'),
        "Deporte": deporte,
        "Minutos": minutos,
        "Comentarios": comentarios
    }])
    
    # Combinar con los datos actuales
    updated_df = pd.concat([df, nueva_fila], ignore_index=True)
    
    # Actualizar la hoja de Google Sheets
    conn.update(data=updated_df)
    
    st.success("✅ ¡Entrenamiento guardado en Google Sheets!")
    st.balloons()
    # Forzar recarga para mostrar los datos nuevos
    st.rerun()

# 5. Visualización de los últimos registros
st.markdown("---")
st.subheader("📊 ÚLTIMOS REGISTROS")
if not df.empty:
    # Mostramos los últimos 10 registros ordenados por fecha descendente
    st.table(df.sort_index(ascending=False).head(10))
else:
    st.info("Aún no hay registros en la hoja de Google.")