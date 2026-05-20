import streamlit as st
import datetime
import requests

# 1. Configuración de la página
st.set_page_config(page_title="Formulario de Planta", layout="centered")

# =========================================================
# === INICIALIZACIÓN DEL ESTADO DE LA SESIÓN (MEMORIA) ===
# =========================================================
# Controla si el formulario ya se envió con éxito a Google
if "formulario_enviado" not in st.session_state:
    st.session_state.formulario_enviado = False

# Controla si el usuario está viendo la pantalla de vista previa
if "mostrar_previsualizacion" not in st.session_state:
    st.session_state.mostrar_previsualizacion = False

# =========================================================
# === CONFIGURACIÓN DE URL ===
# =========================================================
URL_WEBHOOK_GOOGLE = "https://script.google.com/macros/s/AKfycbxVLrj0W21ezNqh0PXEyfAnMX1VXVttORRexo_P81BbXHobZIvKVxWHa_omeP0mrPsF/exec"

# =========================================================
# === FUNCIONES DE VALIDACIÓN DE HORA (CARGA RÁPIDA) ===
# =========================================================
def validar_formato_hora(texto_hora):
    if not texto_hora:
        return False, ""
        
    texto = str(texto_hora).strip().replace(":", "")
    
    if texto.isdigit() and (len(texto) == 3 or len(texto) == 4):
        if len(texto) == 3:
            texto = "0" + texto
            
        hora_str = f"{texto[:2]}:{texto[2:]}"
        
        try:
            hora_valida = datetime.datetime.strptime(hora_str, "%H:%M")
            return True, hora_valida.strftime("%H:%M")
        except ValueError:
            return False, ""
            
    return False, ""

# =========================================================
# === FUNCIÓN RESPONSIVA PARA FILAS DE TIEMPO ===
# =========================================================
def fila_tiempo_obs(label_tiempo, es_hora=False, prefijo="", unidad="Minutos", ejemplo_hora="0600"):
    st.markdown(f"**{label_tiempo} ***") 
    
    if es_hora:
        col_t, col_obs = st.columns(2)
        with col_t:
            tiempo_final = st.text_input(f"Hora (Ej: {ejemplo_hora}) *", placeholder=f"Ej: {ejemplo_hora}", max_chars=5, key=f"{prefijo}_t")
        with col_obs:
            obs = st.text_input("Observaciones", placeholder="Escribe aquí...", key=f"{prefijo}_obs")
            
        st.markdown("<br>", unsafe_allow_html=True) 
        return tiempo_final, obs
        
    else:
        col_t, col_obs = st.columns(2)
        with col_t:
            if unidad == "Horas":
                tiempo_final = st.number_input("Cantidad (Horas) *", min_value=0.0, step=0.5, format="%.1f", key=f"{prefijo}_t")
            else:
                tiempo_final = st.number_input("Cantidad (Minutos) *", min_value=0, step=5, key=f"{prefijo}_t")
        with col_obs:
            obs = st.text_input("Observaciones", placeholder="Opcional...", key=f"{prefijo}_obs")
            
        st.markdown("<br>", unsafe_allow_html=True)
        return tiempo_final, obs


# =========================================================
# === FLUJO PRINCIPAL DE PANTALLAS ===
# =========================================================

# CASO A: El formulario ya fue enviado con éxito
if st.session_state.formulario_enviado:
    st.title("📋 Registro de Actividades Delegados")
    st.markdown("---")
    st.success("### ✅ ¡La información se registró correctamente!")
    
    if st.button("🔄 Cargar un nuevo formulario", use_container_width=True):
        st.session_state.formulario_enviado = False
        st.session_state.mostrar_previsualizacion = False
        st.rerun()

# CASO B: Mostramos la pantalla de Vista Previa antes de enviar
elif st.session_state.mostrar_previsualizacion:
    st.title("🔍 Vista Previa del Registro")
    st.warning("Revise atentamente los datos cargados antes de confirmar el envío definitivo.")
    st.markdown("---")
    
    # Recuperamos los datos crudos y formateamos las horas para mostrarlas limpias
    _, inicio_formateado = validar_formato_hora(st.session_state.raw_hr_inicio)
    _, fin_formateado = validar_formato_hora(st.session_state.raw_hr_fin)
    
    # Estructuramos la visualización en formato tarjeta/tabla limpia
    st.markdown(f"""
    ### 📂 Datos Generales
    * **Fecha:** {st.session_state.raw_fecha}
    * **Planta:** {st.session_state.raw_planta}
    * **Líder (Legajo):** {st.session_state.raw_legajo}
    * **Área:** {st.session_state.raw_area}
    * **Delegado a cargo:** {st.session_state.raw_delegado}
    
    ### ⚙️ Tareas y Maquinaria
    * **Máquina Asignada:** {st.session_state.raw_maquina_asignada}
    * **Pieza Realizada:** {st.session_state.raw_pieza_realizada}
    * **Otras Tareas:** {st.session_state.raw_otras_tareas}
    * **¿Cumplió lo solicitado?:** {st.session_state.raw_tareas_solicitadas}
    
    ### ⏱️ Horarios, Tiempos y Observaciones
    * **Hora Inicio:** {inicio_formateado}  *(Obs: {st.session_state.raw_obs_inicio if st.session_state.raw_obs_inicio else 'Ninguna'})*
    * **Hora Fin:** {fin_formateado}  *(Obs: {st.session_state.raw_obs_fin if st.session_state.raw_obs_fin else 'Ninguna'})*
    * **Tiempos de Baño:** {st.session_state.raw_t_bano} min  *(Obs: {st.session_state.raw_obs_bano if st.session_state.raw_obs_bano else 'Ninguna'})*
    * **Tiempos de Refrigerio:** {st.session_state.raw_t_refrigerio} min  *(Obs: {st.session_state.raw_obs_refrigerio if st.session_state.raw_obs_refrigerio else 'Ninguna'})*
    * **Horas Gremiales:** {st.session_state.raw_h_gremiales} hs  *(Obs: {st.session_state.raw_obs_gremiales if st.session_state.raw_obs_gremiales else 'Ninguna'})*
    
    ### 💬 Comentarios Finales
    * **Observación General:** {st.session_state.raw_observacion_general}
    """)
    st.markdown("---")
    
    # Botones de Acción para la Vista Previa
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        if st.button("✏️ Modificar / Corregir", use_container_width=True):
            # Regresa al formulario sin alterar los inputs
            st.session_state.mostrar_previsualizacion = False
            st.rerun()
            
    with col_btn2:
        if st.button("🚀 Confirmar y Enviar", type="primary", use_container_width=True):
            # Procede al envío real de los datos guardados en memoria
            payload = {
                "Fecha": str(st.session_state.raw_fecha),
                "Planta": st.session_state.raw_planta,
                "Legajo": st.session_state.raw_legajo,
                "Area": st.session_state.raw_area,
                "Delegado": st.session_state.raw_delegado,
                "MaquinaAsignada": st.session_state.raw_maquina_asignada,
                "PiezaRealizada": st.session_state.raw_pieza_realizada,
                "OtrasTareas": st.session_state.raw_otras_tareas,
                "TareasSolicitadas": st.session_state.raw_tareas_solicitadas,
                "HoraInicio": inicio_formateado,
                "ObsInicio": st.session_state.raw_obs_inicio,
                "HoraFin": fin_formateado,
                "ObsFin": st.session_state.raw_obs_fin,
                "MinutosBano": st.session_state.raw_t_bano,
                "ObsBano": st.session_state.raw_obs_bano,
                "MinutosRefrigerio": st.session_state.raw_t_refrigerio,
                "ObsRefrigerio": st.session_state.raw_obs_refrigerio,
                "HorasGremiales": st.session_state.raw_h_gremiales,
                "ObsGremiales": st.session_state.raw_obs_gremiales,
                "ObservacionGeneral": st.session_state.raw_observacion_general
            }
            
            with st.spinner("Enviando datos de forma segura a Google Sheets..."):
                try:
                    respuesta = requests.post(URL_WEBHOOK_GOOGLE, json=payload, timeout=15)
                    if respuesta.status_code == 200:
                        resultado_json = respuesta.json()
                        if resultado_json.get("status") == "exito":
                            st.session_state.formulario_enviado = True
                            st.rerun()
                        else:
                            st.error(f"❌ Error devuelto por Google: {resultado_json.get('mensaje')}")
                    else:
                        st.error(f"⚠️ Error de servidor HTTP {respuesta.status_code}")
                except Exception as e:
                    st.error(f"🚨 Error de red: {e}")

# CASO C: Pantalla normal del Formulario de carga
else:
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

    # 6. Máquina asignada y Pieza realizada
    no_maquina = st.checkbox("No trabajó en máquina, hizo otras tareas!")

    if not no_maquina:
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            maquina_asignada = st.text_input("Máquina asignada *", placeholder="Ej: Prensa 05")
        with col_m2:
            pieza_realizada = st.text_input("Pieza realizada *", placeholder="Ej: Longeron")
    else:
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

    # 9 y 10. Horarios de inicio y fin
    hr_inicio, obs_inicio = fila_tiempo_obs("Horario inicio de actividades", es_hora=True, prefijo="inicio", ejemplo_hora="0600")
    hr_fin, obs_fin = fila_tiempo_obs("Horario fin de actividades", es_hora=True, prefijo="fin", ejemplo_hora="1418")

    # 11, 12 y 13. Tiempos en minutos y horas
    t_bano, obs_bano = fila_tiempo_obs("Tiempos de baño", es_hora=False, prefijo="bano", unidad="Minutos")
    t_refrigerio, obs_refrigerio = fila_tiempo_obs("Tiempos de refrigerio", es_hora=False, prefijo="refrig", unidad="Minutos")
    h_gremiales, obs_gremiales = fila_tiempo_obs("Actividades gremiales realizadas", es_hora=False, prefijo="gremial", unidad="Horas")

    st.markdown("---")

    # 14. Observación final
    observacion_general = st.text_area("¿Alguna observación general? *")

    # Botón inicial para gatillar la revisión
    if st.button("Revisar Datos", type="primary", use_container_width=True):
        errores = []
        
        if len(legajo) != 6 or not legajo.isdigit():
            errores.append("El LEGAJO debe contener exactamente 6 números.")
        if not delegado:
            errores.append("Falta ingresar el delegado a cargo.")
        if not observacion_general:
            errores.append("La observación general es obligatoria.")
        if not no_maquina:
            if not maquina_asignada: errores.append("Debe ingresar la Máquina asignada.")
            if not pieza_realizada: errores.append("Debe ingresar la Pieza realizada.")
        if not no_otras_tareas and not otras_tareas:
            errores.append("Debe especificar las Otras tareas asignadas.")

        es_inicio_valido, _ = validar_formato_hora(hr_inicio)
        if not es_inicio_valido:
            errores.append("Horario de inicio inválido. Escriba los números de corrido, ej: 0600.")
            
        es_fin_valido, _ = validar_formato_hora(hr_fin)
        if not es_fin_valido:
            errores.append("Horario de fin inválido. Escriba los números de corrido, ej: 1418.")

        if errores:
            for error in errores:
                st.error(f"⚠️ {error}")
        else:
            # GUARDADO EN MEMORIA TEMPORAL
            st.session_state.raw_fecha = fecha
            st.session_state.raw_planta = planta
            st.session_state.raw_legajo = legajo
            st.session_state.raw_area = area
            st.session_state.raw_delegado = delegado
            st.session_state.raw_maquina_asignada = maquina_asignada
            st.session_state.raw_pieza_realizada = pieza_realizada
            st.session_state.raw_otras_tareas = otras_tareas
            st.session_state.raw_tareas_solicitadas = tareas_solicitadas
            st.session_state.raw_hr_inicio = hr_inicio
            st.session_state.raw_obs_inicio = obs_inicio
            st.session_state.raw_hr_fin = hr_fin
            st.session_state.raw_obs_fin = obs_fin
            st.session_state.raw_t_bano = t_bano
            st.session_state.raw_obs_bano = obs_bano
            st.session_state.raw_t_refrigerio = t_refrigerio
            st.session_state.raw_obs_refrigerio = obs_refrigerio
            st.session_state.raw_h_gremiales = h_gremiales
            st.session_state.raw_obs_gremiales = obs_gremiales
            st.session_state.raw_observacion_general = observacion_general
            
            # Activamos el pase de pantalla
            st.session_state.mostrar_previsualizacion = True
            st.rerun()
