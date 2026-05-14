import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Rani Assistant", page_icon="💃")

# Secrets se API Key lena
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("Rani: Navin, Secrets mein API key missing hai!")
    st.stop()

# Sabse stable model name use karna
# 'models/gemini-1.5-flash' ya sirf 'gemini-1.5-flash'
model = genai.GenerativeModel('gemini-1.5-flash')

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("💃 Rani AI Assistant")
st.write("Ji Navin, boliye main aapki kya madad karu?")

# Chat History dikhana
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Rani se kuch puchiye..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        # Instruction ko context mein dena
        context = "Tera naam Rani hai. Tu Navin ki pyari AI assistant hai. Hindi mein baat kar."
        response = model.generate_content(f"{context}\n\nUser: {prompt}")
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        # Agar phir bhi 404 aaye toh alternate model try karna
        st.warning("Rani thoda busy hai, dobara koshish kar rahi hai...")
        try:
            alt_model = genai.GenerativeModel('gemini-pro')
            response = alt_model.generate_content(prompt)
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except:
            st.error(f"Rani: Maaf kijiyega boss, technical issue hai: {e}")
            
