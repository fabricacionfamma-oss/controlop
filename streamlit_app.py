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

# =========================================================
# === FUNCIONES DE VALIDACIÓN DE HORA (CARGA RÁPIDA) ===
# =========================================================
def validar_formato_hora(texto_hora):
    if not texto_hora:
        return False, ""
        
    # Quitamos espacios y los ':' por si el usuario sí los puso
    texto = str(texto_hora).strip().replace(":", "")
    
    # Verificamos que sean 3 o 4 números de corrido (Ej: '630' o '1430')
    if texto.isdigit() and (len(texto) == 3 or len(texto) == 4):
        # Si puso 3 números (ej. 630), le agregamos un 0 adelante -> 0630
        if len(texto) == 3:
            texto = "0" + texto
            
        # Armamos la hora insertando los ':' en el medio
        hora_str = f"{texto[:2]}:{texto[2:]}"
        
        try:
            # Validamos que no pongan horas irreales (ej. 25:99)
            hora_valida = datetime.datetime.strptime(hora_str, "%H:%M")
            return True, hora_valida.strftime("%H:%M")
        except ValueError:
            return False, ""
            
    return False, ""

# =========================================================
# === INTERFAZ DEL FORMULARIO ===
# =========================================================

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

# === FUNCIÓN RESPONSIVA (CARGA RÁPIDA) ===
def fila_tiempo_obs(label_tiempo, es_hora=False, prefijo="", unidad="Minutos"):
    st.markdown(f"**{label_tiempo} ***") 
    
    if es_hora:
        col_t, col_obs = st.columns(2)
        with col_t:
            tiempo_final = st.text_input("Hora (Ej: 1430) *", placeholder="Ej: 0630", max_chars=5, key=f"{prefijo}_t")
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

# 9 y 10. Horarios de inicio y fin
hr_inicio, obs_inicio = fila_tiempo_obs("Horario inicio de actividades", es_hora=True, prefijo="inicio")
hr_fin, obs_fin = fila_tiempo_obs("Horario fin de actividades", es_hora=True, prefijo="fin")

# 11, 12 y 13. Tiempos en minutos y horas
t_bano, obs_bano = fila_tiempo_obs("Tiempos de baño", es_hora=False, prefijo="bano", unidad="Minutos")
t_refrigerio, obs_refrigerio = fila_tiempo_obs("Tiempos de refrigerio", es_hora=False, prefijo="refrig", unidad="Minutos")
h_gremiales, obs_gremiales = fila_tiempo_obs("Actividades gremiales realizadas", es_hora=False, prefijo="gremial", unidad="Horas")

st.markdown("---")

# 14. Observación final
observacion_general = st.text_area("¿Alguna observación general? *")

# =========================================================
# === GESTIÓN DE BOTONES CON BLOQUEO DE SEGURIDAD ===
# =========================================================

boton_guardar = st.button(
    "Guardar Registro", 
    type="primary", 
    use_container_width=True, 
    disabled=st.session_state.formulario_enviado
)

if boton_guardar:
    errores = []
    
    # Validaciones generales
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

    # Validación estricta de las Horas (Carga rápida)
    es_inicio_valido, inicio_formateado = validar_formato_hora(hr_inicio)
    if not es_inicio_valido:
        errores.append("Horario de inicio inválido. Escriba los números de corrido, ej: 0630 o 1445.")
        
    es_fin_valido, fin_formateado = validar_formato_hora(hr_fin)
    if not es_fin_valido:
        errores.append("Horario de fin inválido. Escriba los números de corrido, ej: 0630 o 1445.")

    if errores:
        for error in errores:
            st.error(f"⚠️ {error}")
    else:
        # Preparamos el payload usando las horas ya formateadas y validadas
        payload = {
            "Fecha": str(fecha),
            "Planta": planta,
            "Legajo": legajo,
            "Area": area,
            "Delegado": delegado,
            "MaquinaAsignada": maquina_asignada,
            "PiezaRealizada": pieza_realizada,
            "OtrasTareas": otras_tareas,
            "TareasSolicitadas": tareas_solicitadas,
            "HoraInicio": inicio_formateado,
            "ObsInicio": obs_inicio,
            "HoraFin": fin_formateado,
            "ObsFin": obs_fin,
            "MinutosBano": t_bano,
            "ObsBano": obs_bano,
            "MinutosRefrigerio": t_refrigerio,
            "ObsRefrigerio": obs_refrigerio,
            "HorasGremiales": h_gremiales,
            "ObsGremiales": obs_gremiales,
            "ObservacionGeneral": observacion_general
        }
        
        with st.spinner("Procesando en Google Sheets..."):
            try:
                respuesta = requests.post(URL_WEBHOOK_GOOGLE, json=payload, timeout=15)
                
                if respuesta.status_code == 200:
                    resultado_json = respuesta.json()
                    if resultado_json.get("status") == "exito":
                        
                        # Cambiamos el estado a ENVIADO
                        st.session_state.formulario_enviado = True
                        st.rerun()
                        
                    else:
                        st.error(f"❌ Error devuelto: {resultado_json.get('mensaje')}")
                else:
                    st.error(f"⚠️ Error de servidor HTTP {respuesta.status_code}")
            except Exception as e:
                st.error(f"🚨 Error crítico de red: {e}")

# =========================================================
# === VISTA POST-ENVÍO (Muestra recibo y botón de reinicio) ===
# =========================================================
if st.session_state.formulario_enviado:
    st.success("### ✅ ¡La información se registró correctamente!")
    
    # Botón para cargar otro registro
    if st.button("🔄 Cargar un nuevo formulario", use_container_width=True):
        st.session_state.formulario_enviado = False
        st.rerun()
