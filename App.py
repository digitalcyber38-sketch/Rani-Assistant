import streamlit as st
import google.generativeai as genai

# Page ki setting (Phone par accha dikhne ke liye)
st.set_page_config(page_title="Rani Assistant", page_icon="💃")

# Rani ka dimag setup (Aapki API key ke saath)
genai.configure(api_key="AIzaSyBPUd0skwt3MLW2sQ7whg_6t0asG0SFXF8")

# Rani ki personality set karna
instruction = (
    "Tera naam Rani hai. Tu Navin ki personal AI assistant hai. "
    "Tu ek bahut pyari aur samajhdar ladki ki tarah baat karti hai. "
    "Navin tera boss hai, uski har kaam mein madad karna aur hamesha khush rehna."
)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=instruction
)

# Chat history yaad rakhne ke liye
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

st.title("💃 Rani Assistant")
st.caption("Navin ki apni AI Rani")

# Chat messages ko screen par dikhana
for message in st.session_state.chat_session.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# User se input lena
if prompt := st.chat_input("Rani se kuch puchiye..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Rani ka jawab
    with st.chat_message("assistant"):
        response = st.session_state.chat_session.send_message(prompt)
        st.markdown(response.text)
