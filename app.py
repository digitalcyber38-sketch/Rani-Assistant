import streamlit as st
from google import genai

st.set_page_config(page_title="Rani Assistant", page_icon="💃")

# API Key check from Streamlit Secrets
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    st.error("Navin, Secrets mein GEMINI_API_KEY daalo!")
    st.stop()

# New SDK Client Setup
client = genai.Client(api_key=api_key)

st.title("💃 Rani AI Assistant")
st.caption("Updated to Gemini 3 Flash")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Rani se puchiye..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Rani ki identity setup (Latest gemini-3-flash-preview)
        instruction = "Tera naam Rani hai. Tu Navin ki pyari AI assistant hai. Hindi mein baat kar."
        
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=f"{instruction}\n\nNavin: {prompt}"
        )
        
        answer = response.text
        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        
    except Exception as e:
        st.error(f"Rani: Arre boss, lagta hai kuch naya update aaya hai: {e}")
        
