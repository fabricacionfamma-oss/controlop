import streamlit as st
import datetime

st.set_page_config(page_title="Formulario de Planta", layout="centered")

st.title("📋 Registro de Actividades de Planta")
st.write("Complete todos los campos obligatorios a continuación.")

st.markdown("---")

# 1. Fecha
fecha = st.date_input("Fecha *", datetime.date.today())

# 2. Planta
planta = st.selectbox("Planta *", ["FAMMA", "FUMISCOR"])

# 3. Líder - Legajo (Validaremos que sean 6 dígitos al guardar)
legajo = st.text_input("Líder - LEGAJO (6 dígitos) *", max_chars=6, placeholder="Ej: 123456")

# 4. Área (Dependiendo de la planta elegida, mostramos unas áreas u otras)
# Definimos las opciones según la imagen
areas_famma = [
    "FAMMA - ESTAMPADO - L1", 
    "FAMMA - ESTAMPADO - L2", 
    "FAMMA - ESTAMPADO - CELDAS", 
    "FAMMA - ESTAMPADO - PRP"
]
areas_fumiscor = [
    "FUMISCOR - ESTAMPADO - MECANICAS",
    "FUMISCOR - ESTAMPADO - HIDRAULICAS",
    "FUMISCOR - ESTAMPADO - PROGRESIVAS",
    "FUMISCOR - ESTAMPADO - BALANCINES",
    "FUMISCOR - SOLDADURA - CELDAS ROBOT",
    "FUMISCOR - SOLDADURA - PRP",
    "FUMISCOR - SOLDADURA - CELDAS NUEVAS - NAVE 6"
]

# Lógica dinámica para el Área
opciones_area = areas_famma if planta == "FAMMA" else areas_fumiscor
area = st.selectbox("Área *", opciones_area)

# 5. Delegado a cargo
delegado = st.text_input("Delegado a cargo *")

st.markdown("---")
st.subheader("⚙️ Tareas y Maquinaria")

# 6. Máquina asignada
no_maquina = st.checkbox("No trabajó en máquina, hizo otras tareas!")
if not no_maquina:
    maquina = st.text_input("Máquina asignada / Pieza realizada *")
else:
    maquina = "N/A"

# 7. Otras tareas asignadas
no_otras_tareas = st.checkbox("No se le asignaron otras tareas!")
if not no_otras_tareas:
    otras_tareas = st.text_input("Otras tareas asignadas *")
else:
    otras_tareas = "N/A"

# 8. Tareas según lo solicitado
tareas_solicitadas = st.selectbox("¿Se realizaron las tareas según lo solicitado? *", ["Sí", "No", "Parcialmente"])

st.markdown("---")
st.subheader("⏱️ Tiempos y Horarios")

# Función para crear filas de tiempos + observaciones fácilmente
def fila_tiempo_obs(label_tiempo, es_hora=False):
    col1, col2 = st.columns([1, 2])
    with col1:
        if es_hora:
            tiempo = st.time_input(f"{label_tiempo} *")
        else:
            tiempo = st.number_input(f"{label_tiempo} (Minutos) *", min_value=0, step=5)
    with col2:
        obs = st.text_input(f"Observaciones ({label_tiempo.lower()})", placeholder="Escribe aquí si hay observaciones...")
    return tiempo, obs

# 9 y 10. Horarios de inicio y fin
hr_inicio, obs_inicio = fila_tiempo_obs("Horario inicio de actividades", es_hora=True)
hr_fin, obs_fin = fila_tiempo_obs("Horario fin de actividades", es_hora=True)

# 11, 12 y 13. Tiempos en minutos
t_bano, obs_bano = fila_tiempo_obs("Tiempos de baño")
t_refrigerio, obs_refrigerio = fila_tiempo_obs("Tiempos de refrigerio")
t_gremiales, obs_gremiales = fila_tiempo_obs("Actividades gremiales realizadas")

st.markdown("---")

# 14. Observación final
observacion_general = st.text_area("¿Alguna observación general? *")

# Botón de guardado (Aquí iría la lógica de conexión después)
if st.button("Guardar Registro", type="primary", use_container_width=True):
    # Pequeña validación de legajo (Ejemplo)
    if len(legajo) != 6 or not legajo.isdigit():
        st.error("⚠️ El LEGAJO debe contener exactamente 6 números.")
    elif not delegado:
        st.error("⚠️ Falta ingresar el delegado a cargo.")
    else:
        st.success("✅ Formulario validado correctamente. (Listo para enviar a Google Sheets)")
