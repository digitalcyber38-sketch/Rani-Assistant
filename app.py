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
    
    # Direct API Call (No library dependency)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    
    instruction = "Tera naam Rani hai. Tu Navin ki personal AI assistant hai. Tu ek pyari ladki ki tarah Hindi mein baat karti hai."
    
    data = {
        "contents": [{
            "parts": [{"text": f"{instruction}\n\nNavin: {prompt}"}]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        result = response.json()
        
        # Jawab nikalna
        answer = result['candidates'][0]['content']['parts'][0]['text']
        
        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        
    except Exception as e:
        st.error(f"Rani: Maaf kijiyega boss, system overload hai. Ek baar refresh kijiye. Error: {e}")
        
