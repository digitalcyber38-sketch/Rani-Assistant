import streamlit as st
import requests
import json

st.set_page_config(page_title="Rani Assistant", page_icon="💃")

# Secrets se API Key lena
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    st.error("Rani: Navin, Secrets mein API key missing hai!")
    st.stop()

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
    
    # Updated API URL
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    
    # Rani ki personality
    payload = {
        "contents": [{
            "parts": [{"text": f"Tera naam Rani hai. Tu Navin ki AI assistant hai. Hindi mein baat kar. User ka sawal: {prompt}"}]
        }],
        "safetySettings": [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()
        
        # Check if response has content
        if 'candidates' in result and len(result['candidates']) > 0:
            answer = result['candidates'][0]['content']['parts'][0]['text']
            with st.chat_message("assistant"):
                st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
            st.error(f"Rani: Arre boss, Google ne response block kar diya ya galat key hai. Error: {result}")
            
    except Exception as e:
        st.error(f"Rani: Maaf kijiyega boss, kuch technical dikkat hai: {e}")
        
