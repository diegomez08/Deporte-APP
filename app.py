import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Registro de Deporte", page_icon="🏋️‍♂️")
st.title("🏋️‍♂️ REGISTRO DE ENTRENAMIENTO")

conn = st.connection("gsheets", type=GSheetsConnection)

# Leer datos forzando que no use caché para ver cambios al instante
try:
    df = conn.read(ttl="0s")
    if not df.empty:
        # CORRECCIÓN DE DECIMALES: Convertimos a entero para que no salga .0
        df['Minutos'] = pd.to_numeric(df['Minutos'], errors='coerce').fillna(0).astype(int)
except Exception as e:
    st.error(f"Error al leer datos: {e}")
    df = pd.DataFrame(columns=['Fecha', 'Deporte', 'Minutos', 'Comentarios'])

# Formulario de entrada
with st.form(key='deporte_form'):
    col1, col2 = st.columns(2)
    with col1:
        fecha = st.date_input("Fecha", value=datetime.now())
        deporte = st.selectbox("Deporte", ["Padel", "Bici", "Flexiones", "Abdominales", "Running", "Gym"])
    with col2:
        minutos = st.number_input("Minutos", min_value=1, step=1, value=30)
    
    comentarios = st.text_area("Comentarios (opcional)")
    submit_button = st.form_submit_button(label='🚀 GUARDAR SESIÓN')

if submit_button:
    nueva_fila = pd.DataFrame([{
        "Fecha": fecha.strftime('%Y-%m-%d'),
        "Deporte": deporte,
        "Minutos": int(minutos), # Aseguramos entero aquí también
        "Comentarios": comentarios
    }])
    
    updated_df = pd.concat([df, nueva_fila], ignore_index=True)
    conn.update(data=updated_df)
    st.success("✅ Guardado en Google Sheets")
    st.rerun()

# Visualización y Botón de Borrar
st.markdown("---")
st.subheader("📊 ÚLTIMOS REGISTROS")

if not df.empty:
    # Mostramos la tabla limpia
    st.table(df.sort_index(ascending=False).head(10))
    
    # BOTÓN DE BORRAR ÚLTIMO REGISTRO
    st.write("")
    if st.button("🗑️ Borrar último registro"):
        if len(df) > 0:
            updated_df = df.drop(df.index[-1]) # Elimina la última fila
            conn.update(data=updated_df)
            st.warning("Registro eliminado")
            st.rerun()
else:
    st.info("No hay datos todavía.")