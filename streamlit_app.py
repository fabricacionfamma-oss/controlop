import streamlit as st
import datetime
import requests

# 1. Configuración de la página
st.set_page_config(page_title="Formulario de Planta", layout="centered")

# =========================================================
# === INICIALIZACIÓN DEL ESTADO DE LA SESIÓN (MEMORIA) ===
# =========================================================
if "formulario_enviado" not in st.session_state:
    st.session_state.formulario_enviado = False

# =========================================================
# === CONFIGURACIÓN DE URL ===
# =========================================================
URL_WEBHOOK_GOOGLE = "https://script.google.com/macros/s/AKfycbxVLrj0W21ezNqh0PXEyfAnMX1VXVttORRexo_P81BbXHobZIvKVxWHa_omeP0mrPsF/exec"

st.title("📋 Registro de Actividades Delegados")
st.write("Complete todos los campos obligatorios a continuación.")
st.markdown("---")

# 1. Fecha
fecha = st.date_input("Fecha *", datetime.date.today())

# 2. Planta
planta = st.selectbox("Planta *", ["FAMMA", "FUMISCOR"])

# 3. Líder - Legajo
legajo = st.text_input("Líder ( Legajo - 6 dígitos) *", max_chars=6, placeholder="Ej: 123456")

# 4. Área 
areas_famma = ["FAMMA - ESTAMPADO - L1", "FAMMA - ESTAMPADO - L2", "FAMMA - ESTAMPADO - CELDAS", "FAMMA - ESTAMPADO - PRP"]
areas_fumiscor = ["FUMISCOR - ESTAMPADO - MECANICAS", "FUMISCOR - ESTAMPADO - HIDRAULICAS", "FUMISCOR - ESTAMPADO - PROGRESIVAS", "FUMISCOR - ESTAMPADO - BALANCINES", "FUMISCOR - SOLDADURA - CELDAS ROBOT", "FUMISCOR - SOLDADURA - PRP", "FUMISCOR - SOLDADURA - CELDAS NUEVAS - NAVE 6"]

opciones_area = areas_famma if planta == "FAMMA" else areas_fumiscor
area = st.selectbox("Área *", opciones_area)

# 5. Delegado a cargo
delegado = st.text_input("Delegado a cargo *")

st.markdown("---")
st.subheader("⚙️ Tareas y Maquinaria")

#
