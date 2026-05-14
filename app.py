import streamlit as st
import google.generativeai as genai

# Page setup
st.set_page_config(page_title="Rani Assistant", page_icon="💃")

# API Setup
genai.configure(api_key="AIzaSyBPUd0skwt3MLW2sQ7whg_6t0asG0SFXF8")

# Rani ki identity
instruction = (
    "Tera naam Rani hai. Tu Navin ki personal AI assistant hai. "
    "Tu ek bahut pyari ladki ki tarah baat karti hai. "
    "Navin tera boss hai, uski har kaam mein madad karna."
)

# Yahan humne model name badal kar 'gemini-pro' kar diya hai stability ke liye
model = genai.GenerativeModel(
    model_name="gemini-pro"
)

# Chat history handle karne ke liye simple tareeka
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("💃 Rani Assistant")

# Messages dikhana
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input aur response
if prompt := st.chat_input("Rani se kuch puchiye..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        # Instruction ko prompt ke saath jodna taaki wo hamesha Rani bani rahe
        full_prompt = f"{instruction}\n\nUser: {prompt}"
        response = model.generate_content(full_prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Opps! Kuch dikkat hai: {e}")
