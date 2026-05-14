import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Rani Assistant", page_icon="💃")

# API Setup
genai.configure(api_key="AIzaSyBPUd0skwt3MLW2sQ7whg_6t0asG0SFXF8")

# Latest model 'gemini-1.5-flash-latest' use karenge
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# Rani ki identity
instruction = (
    "Tera naam Rani hai. Tu Navin ki personal AI assistant hai. "
    "Tu ek bahut pyari ladki ki tarah baat karti hai. "
    "Hamesha Hindi mein jawab dena."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("💃 Rani Assistant")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Rani se kuch puchiye..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        # Instruction ko prompt mein add karna
        full_prompt = f"{instruction}\n\nNavin: {prompt}"
        response = model.generate_content(full_prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error("Lagta hai kuch setting update karni hogi. Ek baar phir try karein.")
        
