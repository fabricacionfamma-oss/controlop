import streamlit as st
import datetime
import requests
import streamlit.components.v1 as components # Para el efecto de confeti personalizado

# 1. Configuración de la página
st.set_page_config(page_title="Formulario de Planta", layout="centered")

# =========================================================
# === FUNCIÓN DEL EFECTO DE CONFETI PERSONALIZADO ===
# =========================================================
def lanzar_confeti():
    components.html(
        """
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
        <script>
            // Configuración del confeti: duración de 2.5 segundos, explosión de colores
            var end = Date.now() + (2.5 * 1000); 
            var colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff'];

            (function frame() {
                // Explosión desde la izquierda
                confetti({
                    particleCount: 4,
                    angle: 60,
                    spread: 60,
                    origin: { x: 0 },
                    colors: colors
                });
                // Explosión desde la derecha
                confetti({
                    particleCount: 4,
                    angle: 120,
                    spread: 60,
                    origin: { x: 1 },
                    colors: colors
                });

                if (Date.now() < end) {
                    requestAnimationFrame(frame);
                }
            }());
        </script>
        """,
        height=0, # Ocultar el contenedor del componente
    )

# === YA NO SE LLAMA A LANZAR_CONFETI() AQUÍ AL INICIO ===

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

# === FUNCIÓN RESPONSIVA ===
def fila_tiempo_obs(label_tiempo, es_hora=False, prefijo="", unidad="Minutos"):
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
# === BOTÓN DE ENVÍO ===
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
        # Preparamos paquete de datos Clásico
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
            "HorasGremiales": h_gremiales,
            "ObsGremiales": obs_gremiales,
            "ObservacionGeneral": observacion_general
        }
        
        with st.spinner("Procesando en Google Sheets..."):
            try:
                # Envío Clásico POST
                respuesta = requests.post(URL_WEBHOOK_GOOGLE, json=payload, timeout=15)
                
                if respuesta.status_code == 200:
                    resultado_json = respuesta.json()
                    if resultado_json.get("status") == "exito":
                        st.success(f"### ✅ ¡Registro guardado exitosamente!")
                        st.info(f"Comprobante Fila: {resultado_json.get('fila')}")
                        
                        # =========================================================
                        # === AQUÍ SE LANZA EL CONFETI SOLO EN ÉXITO ===
                        # =========================================================
                        lanzar_confeti() 
                        # st.balloons() # <--- Ya no usamos globos
                        
                    else:
                        st.error(f"❌ Error devuelto: {resultado_json.get('mensaje')}")
                else:
                    st.error(f"⚠️ Error de servidor HTTP {respuesta.status_code}")
            except Exception as e:
                st.error(f"🚨 Error crítico de red: {e}")
