import streamlit as st
import datetime

# Mantener la configuración que elegiste
st.set_page_config(page_title="Formulario de Planta", layout="centered")

st.title("📋 Registro de Actividades Delegados")
st.write("Complete todos los campos obligatorios a continuación.")

st.markdown("---")

# 1. Fecha
fecha = st.date_input("Fecha *", datetime.date.today())

# 2. Planta
planta = st.selectbox("Planta *", ["FAMMA", "FUMISCOR"])

# 3. Líder - Legajo
legajo = st.text_input("Líder ( Legajo - 6 dígitos) *", max_chars=6, placeholder="Ej: 123456")

# 4. Área (Listas según tu definición)
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

# 6. LÓGICA REACTIVA: Máquina asignada y Pieza realizada
no_maquina = st.checkbox("No trabajó en máquina, hizo otras tareas!")

if not no_maquina:
    # Si NO está marcado el botón, se muestran ambas opciones en dos columnas independientes
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        maquina_asignada = st.text_input("Máquina asignada *", placeholder="Ej: Prensa 05")
    with col_m2:
        pieza_realizada = st.text_input("Pieza realizada *", placeholder="Ej: Longeron")
else:
    # Si se marca el botón, ambas opciones desaparecen de la vista y toman valor "N/A" automáticamente
    maquina_asignada = "N/A"
    pieza_realizada = "N/A"
    st.info("ℹ️ Se registrará 'N/A' en máquina y pieza realizada al no trabajar en máquina.")

# 7. Otras tareas asignadas
no_otras_tareas = st.checkbox("No se le asignaron otras tareas!")
if not no_otras_tareas:
    otras_tareas = st.text_input("Otras tareas asignadas *")
else:
    otras_tareas = "N/A"

# 8. Tareas según lo solicitado
tareas_solicitadas = st.selectbox("¿Realizo las actividades según lo solicitado? *", ["Sí", "No", "Parcialmente"])

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

# Botón de guardado con validaciones actualizadas
if st.button("Guardar Registro", type="primary", use_container_width=True):
    
    # Lista para ir acumulando los errores de validación
    errores = []
    
    if len(legajo) != 6 or not legajo.isdigit():
        errores.append("El LEGAJO debe contener exactamente 6 números.")
    if not delegado:
        errores.append("Falta ingresar el delegado a cargo.")
    if not observacion_general:
        errores.append("La observación general es obligatoria.")
        
    # Validación condicional para la máquina y pieza (solo si NO marcó el checkbox)
    if not no_maquina:
        if not maquina_asignada:
            errores.append("Debe ingresar la Máquina asignada o marcar que no trabajó en ella.")
        if not pieza_realizada:
            errores.append("Debe ingresar la Pieza realizada o marcar que no trabajó en máquina.")
            
    if not no_otras_tareas and not otras_tareas:
        errores.append("Debe especificar las Otras tareas asignadas o marcar que no se le asignaron.")

    # Desplegar resultado de la validación
    if errores:
        for error in errores:
            st.error(f"⚠️ {error}")
    else:
        st.success("✅ Formulario validado correctamente. (Listo para enviar a Google Sheets)")
        
        # Muestra temporal de estructura de datos final para verificar que todo se guarde bien
        st.json({
            "Fecha": str(fecha),
            "Planta": planta,
            "Legajo": legajo,
            "Area": area,
            "Delegado": delegado,
            "Maquina Asignada": maquina_asignada,
            "Pieza Realizada": pieza_realizada,
            "Otras Tareas": otras_tareas,
            "Tareas Solicitadas": tareas_solicitadas,
            "Hora Inicio": str(hr_inicio),
            "Hora Fin": str(hr_fin),
            "Minutos Baño": t_bano,
            "Minutos Refrigerio": t_refrigerio,
            "Minutos Gremiales": t_gremiales,
            "Observacion General": observacion_general
        })
