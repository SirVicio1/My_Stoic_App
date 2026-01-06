import streamlit as st
from openai import OpenAI

# Configuración visual
st.set_page_config(page_title="STOA", page_icon="🏛️")

# Estética limpia
st.markdown("""<style> .stApp { background-color: #Fdfcfb; } h1 { color: #4A4A4A; } </style>""", unsafe_allow_html=True)

st.title("🏛️ STOA: Mentor Estoico")
st.write("Bienvenido. Describe lo que perturba tu paz para someterlo al juicio de la razón.")

# El usuario ingresa su API Key de forma segura
api_key = st.sidebar.text_input("Ingresa tu OpenAI API Key", type="password")

if not api_key:
    st.warning("Por favor, introduce tu API Key en la barra lateral para comenzar.")
else:
    client = OpenAI(api_key=api_key)
    
    # Caja de texto del problema
    problema = st.text_area("¿Cuál es el problema?", placeholder="Ej: Mi madre defiende a otros en lugar de a mí...")

    if problema:
        st.subheader("Auditoría de Conciencia")
        q1 = st.radio("¿Depende esto 100% de ti?", ["No", "Solo mi reacción", "Sí"])
        q2 = st.text_input("¿Qué etiqueta le pones a este evento? (ej: traición, injusticia)")
        
        if st.button("Analizar con Sabiduría"):
            with st.spinner("Los maestros están reflexionando..."):
                prompt = f"Actúa como mentor estoico. Problema: {problema}. Juicio del usuario: {q2}. Control: {q1}. Estructura: 1. Consejo (Dicotomía), 2. Lección (Cita de Marco Aurelio/Séneca/Epicteto), 3. Solución (Virtud), 4. Ejercicio Práctico."
                
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "system", "content": "Eres el Guía de STOA, minimalista y firme."},
                              {"role": "user", "content": prompt}]
                )
                st.markdown(response.choices[0].message.content)

st.sidebar.caption("Tus datos no se guardan. Tu paz es tu responsabilidad.")
