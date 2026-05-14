import streamlit as st
import requests

st.set_page_config(page_title="Rani Assistant", page_icon="💃")

# Secrets check
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    st.error("Navin, Secrets mein API key missing hai!")
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

    # SAHI URL: gemini-1.5-flash use karein
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{"parts": [{"text": f"Tera naam Rani hai. Tu Navin ki AI assistant hai. Hindi mein jawab de: {prompt}"}]}]
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
            st.error(f"Rani: Arre boss, lagta hai rasta abhi bhi band hai (Status {response.status_code})")
            st.write(result)
    except Exception as e:
        st.error(f"Technical Error: {e}")
        
