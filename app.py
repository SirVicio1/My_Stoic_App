import streamlit as st
from openai import OpenAI

# 1. Configuración de página y Estilo Minimalista Corregido
st.set_page_config(page_title="STOA", page_icon="🏛️", layout="centered")

st.markdown("""
    <style>
    /* Forzamos colores legibles */
    .stApp {
        background-color: #F8F5F2;
    }
    h1, h2, h3, p, span, label {
        color: #2D2D2D !important;
    }
    /* Estilo para las tarjetas de respuesta */
    .stoa-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #E0E0E0;
        margin-bottom: 15px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    .stoa-header {
        color: #8E735B !important;
        font-weight: bold;
        text-transform: uppercase;
        font-size: 0.9em;
        margin-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Título e Instrucciones
st.title("🏛️ STOA")
st.subheader("Tu Refugio de Razón y Virtud")
st.write("Dime qué perturba tu paz. Lo someteremos al juicio de los maestros estoicos.")

# 3. Configuración de API Key en la barra lateral
with st.sidebar:
    st.header("Configuración")
    api_key = st.text_input("Ingresa tu OpenAI API Key", type="password")
    st.info("Tu llave se usa solo para procesar tu consulta y no se guarda.")

# 4. Lógica de la Aplicación
if not api_key:
    st.warning("⚠️ Por favor, ingresa tu API Key en la barra lateral izquierda para continuar.")
else:
    client = OpenAI(api_key=api_key)
    
    # Entrada del Problema
    problema = st.text_area("¿Cuál es la situación?", placeholder="Describe aquí tu problema...")

    if problema:
        st.markdown("---")
        st.markdown("### 🔍 Auditoría de Conciencia")
        st.write("Responde con honestidad antes de recibir el análisis:")
        
        col1, col2 = st.columns(2)
        with col1:
            control = st.radio("¿Depende de ti?", ["No, es externo", "Solo mi juicio", "Sí, totalmente"])
        with col2:
            importancia = st.select_slider("Importancia en 1 año:", options=["Nada", "Poca", "Media", "Mucha"])
            
        juicio = st.text_input("¿Qué etiqueta le pones? (ej. Traición, Injusticia, Desastre)")

        if st.button("PROCESAR CON SABIDURÍA"):
            with st.spinner("Reflexionando bajo los pórticos de la Stoa..."):
                try:
                    prompt_sistema = """
                    Eres el Guía de STOA. Responde de forma minimalista, profunda y firme. 
                    Divide tu respuesta en 4 secciones claras:
                    1. PERSPECTIVA: Usa la dicotomía del control.
                    2. SABIDURÍA: Una cita de Marco Aurelio, Séneca o Epicteto y su explicación.
                    3. ACCIÓN VIRTUOSA: Qué debe hacer el usuario basado en la virtud.
                    4. PRÁCTICA DIARIA: Un ejercicio concreto.
                    Usa un lenguaje elegante pero legible.
                    """
                    
                    user_query = f"Problema: {problema}. Juicio: {juicio}. Control percibido: {control}. Importancia: {importancia}."
                    
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": prompt_sistema},
                            {"role": "user", "content": user_query}
                        ]
                    )
                    
                    # Mostrar resultados en formato de tarjetas limpias
                    res = response.choices[0].message.content
                    st.markdown("---")
                    st.markdown("### 🏛️ El Dictamen de la Razón")
                    st.markdown(res) # La IA generará el formato Markdown
                    
                except Exception as e:
                    st.error(f"Hubo un error con la API: {e}")

st.sidebar.markdown("---")
st.sidebar.caption("“No nos afecta lo que sucede, sino lo que nos decimos sobre lo que sucede.” — Epicteto")
