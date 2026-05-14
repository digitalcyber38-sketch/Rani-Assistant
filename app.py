import streamlit as st
import requests
import json

st.set_page_config(page_title="Rani Assistant", page_icon="💃")

# Secrets se API Key lena
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    st.error("Rani: Navin, Secrets mein API key nahi mil rahi!")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("💃 Rani AI Assistant")

# Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Rani se kuch puchiye..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 404 Fix: Humne model ka path change kiya hai 'gemini-pro' par
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    
    payload = {
        "contents": [{
            "parts": [{"text": f"Tera naam Rani hai. Tu Navin ki assistant hai. Hindi mein jawab de: {prompt}"}]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()
        
        # Debugging ke liye agar error aaye
        if 'error' in result:
            # Agar gemini-pro bhi na mile, toh gemini-1.0-pro try karein
            st.warning("Model update ho raha hai, ek aur koshish...")
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.0-pro:generateContent?key={api_key}"
            response = requests.post(url, headers=headers, json=payload)
            result = response.json()

        answer = result['candidates'][0]['content']['parts'][0]['text']
        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
            
    except Exception as e:
        st.error(f"Rani: Maaf kijiyega boss, Google server response nahi de raha. Error details: {result}")
        
