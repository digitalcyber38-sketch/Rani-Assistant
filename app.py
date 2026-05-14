import streamlit as st
import requests

st.set_page_config(page_title="Rani Assistant", page_icon="💃")

# API Key check
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    st.error("Rani: Navin, Secrets mein API key nahi mil rahi!")
    st.stop()

st.title("💃 Rani AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Rani se puchiye..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Naya Endpoint URL (v1beta/models/gemini-1.5-flash)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{"text": f"Tera naam Rani hai. Tu Navin ki AI assistant hai. Hindi mein baat kar: {prompt}"}]
        }]
    }

    try:
        response = requests.post(url, json=payload)
        result = response.json()

        if response.status_code == 200:
            answer = result['candidates'][0]['content']['parts'][0]['text']
            with st.chat_message("assistant"):
                st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
            st.error(f"Rani: Arre boss, Google ne mana kar diya (Error {response.status_code}). Jawab: {result}")
    except Exception as e:
        st.error(f"Rani: Technical glitch! {e}")
        
