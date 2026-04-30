<<<<<<< HEAD
import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. Configuración de la página (Optimizada para móvil)
st.set_page_config(page_title="Mi Deporte Diario", layout="centered")

# 2. Estilo Midnight Blue adaptable
st.markdown("""
    <style>
    .main { background-color: #1b2631; color: #d5dbdb; }
    div.stButton > button { width: 100%; border-radius: 8px; height: 3.5em; font-weight: bold; background-color: #2e86c1; color: white; }
    .stDataFrame { background-color: #212f3d; }
    label { font-weight: bold; color: #85c1e9 !important; }
    </style>
    """, unsafe_allow_html=True)

FILE_NAME = 'registro_deporte.csv'

# 3. Función de carga de datos
def cargar_datos():
    columnas = ['Fecha', 'Deporte', 'Minutos', 'Comentarios']
    if os.path.exists(FILE_NAME):
        try:
            df = pd.read_csv(FILE_NAME)
            for col in columnas:
                if col not in df.columns:
                    df[col] = ""
            return df
        except:
            return pd.DataFrame(columns=columnas)
    return pd.DataFrame(columns=columnas)

df = cargar_datos()

# --- CABECERA ---
st.title("🏃‍♂️ DEPORTE")

# --- FORMULARIO DE REGISTRO ---
with st.expander("➕ REGISTRAR ENTRENAMIENTO", expanded=True):
    with st.form("nuevo_entrenamiento", clear_on_submit=True):
        f_fecha = st.date_input("FECHA", datetime.now())
        f_deporte = st.selectbox("DEPORTE", ["Padel", "Bici", "Flexiones", "Abdominales"])
        f_min = st.number_input("DURACIÓN (MINUTOS)", min_value=0, step=5)
        f_coment = st.text_input("COMENTARIOS (OPCIONAL)")
        
        if st.form_submit_button("GUARDAR SESIÓN"):
            if f_min > 0:
                nueva_fila = pd.DataFrame([[f_fecha.strftime('%Y-%m-%d'), f_deporte, f_min, f_coment]], 
                                          columns=['Fecha', 'Deporte', 'Minutos', 'Comentarios'])
                df = pd.concat([df, nueva_fila], ignore_index=True)
                df.to_csv(FILE_NAME, index=False)
                st.success(f"¡{f_deporte} guardado!")
                st.rerun()
            else:
                st.warning("Indica los minutos realizados")

# --- VISUALIZACIÓN ---
st.write("### 📊 ÚLTIMOS REGISTROS")

if not df.empty:
    # Mostramos los últimos registros arriba para verlos rápido en el iPhone
    df_display = df.copy()
    st.dataframe(
        df_display.iloc[::-1], 
        use_container_width=True,
        hide_index=True
    )

    # --- RESUMEN RÁPIDO ---
    total_min = df['Minutos'].sum()
    st.metric("TOTAL MINUTOS", f"{total_min} min", delta=f"{len(df)} sesiones")

    # --- GESTIÓN ---
    with st.expander("🗑️ BORRAR REGISTROS"):
        opciones = {f"{i} | {row['Fecha']} | {row['Deporte']}": i for i, row in df.iterrows()}
        seleccion = st.selectbox("Selecciona para eliminar:", options=list(opciones.keys()), index=len(opciones)-1)
        
        if st.button("BORRAR SELECCIONADO"):
            idx_sel = opciones[seleccion]
            df = df.drop(idx_sel).reset_index(drop=True)
            df.to_csv(FILE_NAME, index=False)
            st.rerun()
else:
=======
import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. Configuración de la página (Optimizada para móvil)
st.set_page_config(page_title="Mi Deporte Diario", layout="centered")

# 2. Estilo Midnight Blue adaptable
st.markdown("""
    <style>
    .main { background-color: #1b2631; color: #d5dbdb; }
    div.stButton > button { width: 100%; border-radius: 8px; height: 3.5em; font-weight: bold; background-color: #2e86c1; color: white; }
    .stDataFrame { background-color: #212f3d; }
    label { font-weight: bold; color: #85c1e9 !important; }
    </style>
    """, unsafe_allow_html=True)

FILE_NAME = 'registro_deporte.csv'

# 3. Función de carga de datos
def cargar_datos():
    columnas = ['Fecha', 'Deporte', 'Minutos', 'Comentarios']
    if os.path.exists(FILE_NAME):
        try:
            df = pd.read_csv(FILE_NAME)
            for col in columnas:
                if col not in df.columns:
                    df[col] = ""
            return df
        except:
            return pd.DataFrame(columns=columnas)
    return pd.DataFrame(columns=columnas)

df = cargar_datos()

# --- CABECERA ---
st.title("🏃‍♂️ MI RUTINA")

# --- FORMULARIO DE REGISTRO ---
with st.expander("➕ REGISTRAR ENTRENAMIENTO", expanded=True):
    with st.form("nuevo_entrenamiento", clear_on_submit=True):
        f_fecha = st.date_input("FECHA", datetime.now())
        f_deporte = st.selectbox("DEPORTE", ["Padel", "Bici", "Flexiones", "Abdominales"])
        f_min = st.number_input("DURACIÓN (MINUTOS)", min_value=0, step=5)
        f_coment = st.text_input("COMENTARIOS (OPCIONAL)")
        
        if st.form_submit_button("GUARDAR SESIÓN"):
            if f_min > 0:
                nueva_fila = pd.DataFrame([[f_fecha.strftime('%Y-%m-%d'), f_deporte, f_min, f_coment]], 
                                          columns=['Fecha', 'Deporte', 'Minutos', 'Comentarios'])
                df = pd.concat([df, nueva_fila], ignore_index=True)
                df.to_csv(FILE_NAME, index=False)
                st.success(f"¡{f_deporte} guardado!")
                st.rerun()
            else:
                st.warning("Indica los minutos realizados")

# --- VISUALIZACIÓN ---
st.write("### 📊 ÚLTIMOS REGISTROS")

if not df.empty:
    # Mostramos los últimos registros arriba para verlos rápido en el iPhone
    df_display = df.copy()
    st.dataframe(
        df_display.iloc[::-1], 
        use_container_width=True,
        hide_index=True
    )

    # --- RESUMEN RÁPIDO ---
    total_min = df['Minutos'].sum()
    st.metric("TOTAL MINUTOS", f"{total_min} min", delta=f"{len(df)} sesiones")

    # --- GESTIÓN ---
    with st.expander("🗑️ BORRAR REGISTROS"):
        opciones = {f"{i} | {row['Fecha']} | {row['Deporte']}": i for i, row in df.iterrows()}
        seleccion = st.selectbox("Selecciona para eliminar:", options=list(opciones.keys()), index=len(opciones)-1)
        
        if st.button("BORRAR SELECCIONADO"):
            idx_sel = opciones[seleccion]
            df = df.drop(idx_sel).reset_index(drop=True)
            df.to_csv(FILE_NAME, index=False)
            st.rerun()
else:
>>>>>>> 47d6645792aefee69224e342b1dc0331a356efde
    st.info("¡Empieza hoy mismo! Registra tu primer ejercicio arriba.")