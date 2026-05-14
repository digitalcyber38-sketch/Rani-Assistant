import streamlit as st
import google.generativeai as genai

# Page Setup
st.set_page_config(page_title="Rani Assistant", page_icon="💃")

# Secrets se API Key lena (Ye safe tareeka hai)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("Rani: Navin, aapne abhi tak Secrets mein API key nahi daali hai!")
    st.stop()

# Model aur Identity
model = genai.GenerativeModel('gemini-1.5-flash')
instruction = "Tera naam Rani hai. Tu Navin ki pyari aur hoshiyar AI assistant hai. Tu hamesha Hindi/Bhojpuri mein baat karti hai. Navin tera boss hai."

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("💃 Rani AI Assistant")
st.write("Ji Navin, boliye main aapki kya madad karu?")

# Chat History dikhana
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Rani se kuch puchiye..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        # Rani ka response
        full_prompt = f"{instruction}\n\nNavin: {prompt}"
        response = model.generate_content(full_prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Rani: Arre boss, kuch gadbad ho gayi! Error: {e}")
        
