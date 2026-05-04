import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Registro de Deporte", page_icon="🏋️‍♂️")

st.title("🏋️‍♂️ REGISTRO DE ENTRENAMIENTO")

# 1. Conexión con Google Sheets
# Nota: La URL se toma automáticamente de los "Secrets" que configuramos
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. Leer los datos existentes para mostrarlos
try:
    df = conn.read(ttl="0s") # ttl="0s" obliga a leer datos frescos sin usar caché
except Exception as e:
    st.error("No se pudo conectar con la hoja. Revisa los Secrets.")
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