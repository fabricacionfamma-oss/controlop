import streamlit as st
import datetime
import requests  # Librería fundamental para enviar datos por internet

st.set_page_config(page_title="Formulario de Planta", layout="centered")

# =========================================================
# === URL DEL WEBHOOK DE GOOGLE APPS SCRIPT ===
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

# === FUNCIÓN RESPONSIVA NATIVA ===
def fila_tiempo_obs(label_tiempo, es_hora=False, prefijo=""):
    st.markdown(f"**{label_tiempo} ***") 
    
    if es_hora:
        col_h, col_m = st.columns(2)
        with col_h:
            hora = st.number_input("Hora (0-23)", min_value=0, max_value=23, step=1, key=f"{prefijo}_h")
        with col_m:
            minuto = st.number_input("Minutos (0-59)", min_value=0, max_value=59, step=1, key=f"{prefijo}_m")
            
        obs = st.text_input("Observaciones", placeholder="Escribe aquí si hay observaciones...", key=f"{prefijo}_obs")
        
        tiempo_final = f"{hora:02d}:{minuto:02d}"
        st.markdown("<br>", unsafe_allow_html=True) 
        return tiempo_final, obs
        
    else:
        col_t, col_obs = st.columns(2)
        with col_t:
            tiempo_final = st.number_input("Cantidad (Minutos) *", min_value=0, step=5, key=f"{prefijo}_t")
        with col_obs:
            obs = st.text_input("Observaciones", placeholder="Opcional...", key=f"{prefijo}_obs")
            
        st.markdown("<br>", unsafe_allow_html=True)
        return tiempo_final, obs

# 9 y 10. Horarios de inicio y fin
hr_inicio, obs_inicio = fila_tiempo_obs("Horario inicio de actividades", es_hora=True, prefijo="inicio")
hr_fin, obs_fin = fila_tiempo_obs("Horario fin de actividades", es_hora=True, prefijo="fin")

# 11, 12 y 13. Tiempos en minutos
t_bano, obs_bano = fila_tiempo_obs("Tiempos de baño", es_hora=False, prefijo="bano")
t_refrigerio, obs_refrigerio = fila_tiempo_obs("Tiempos de refrigerio", es_hora=False, prefijo="refrig")
t_gremiales, obs_gremiales = fila_tiempo_obs("Actividades gremiales realizadas", es_hora=False, prefijo="gremial")

st.markdown("---")

# 14. Observación final
observacion_general = st.text_area("¿Alguna observación general? *")

# =========================================================
# === BOTÓN DE ENVÍO CON SISTEMA ANTI-PÉRDIDA DE DATOS ===
# =========================================================
if st.button("Guardar Registro", type="primary", use_container_width=True):
    
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

    if errores:
        for error in errores:
            st.error(f"⚠️ {error}")
    else:
        # Preparamos el paquete de datos estructurado en formato JSON clásico
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
            "HoraInicio": hr_inicio,
            "ObsInicio": obs_inicio,
            "HoraFin": hr_fin,
            "ObsFin": obs_fin,
            "MinutosBano": t_bano,
            "ObsBano": obs_bano,
            "MinutosRefrigerio": t_refrigerio,
            "ObsRefrigerio": obs_refrigerio,
            "MinutosGremiales": t_gremiales,
            "ObsGremiales": obs_gremiales,
            "ObservacionGeneral": observacion_general
        }
        
        with st.spinner("Procesando en Google Sheets... No cierre esta pestaña."):
            try:
                # Se envían los datos mediante POST y se esperan un máximo de 15 segundos
                respuesta = requests.post(URL_WEBHOOK_GOOGLE, json=payload, timeout=15)
                
                # Comprobar que la comunicación web fue exitosa (Código HTTP 200)
                if respuesta.status_code == 200:
                    resultado_json = respuesta.json()
                    
                    if resultado_json.get("status") == "exito":
                        # === RECIBO OFICIAL PARA EL USUARIO ===
                        num_fila = resultado_json.get("fila")
                        
                        st.success(f"""
                        ### ✅ ¡Se registró correctamente la información!
                        * **Estado:** Guardado exitoso en la nube.
                        * **Comprobante N°:** REC-{fecha.strftime('%Y%m%d')}-{legajo}-{num_fila}
                        * **Fila de registro:** {num_fila}
                        
                        Ya puede cerrar esta pestaña de forma segura.
                        """)
                        st.balloons()
                    else:
                        # Error lógico devuelto desde Google Apps Script
                        st.error(f"❌ Google Sheets rechazó el guardado: {resultado_json.get('mensaje')}")
                else:
                    st.error(f"⚠️ El servidor de Google respondió con código de error {respuesta.status_code}. Intente de nuevo.")
                    
            except requests.exceptions.Timeout:
                st.error("⏳ Tiempo de espera agotado. La conexión de red es muy lenta, verifique si los datos impactaron antes de reintentar.")
            except Exception as e:
                # Error crítico de conexión de red o URL mal pegada
                st.error(f"🚨 Error crítico de red: No se pudo enviar la información. Verifique su señal de internet. Detalles: {e}")
