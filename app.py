import streamlit as st
import requests

st.set_page_config(page_title="Rani Assistant", page_icon="💃")

# Secrets check (Make sure GEMINI_API_KEY is in your Streamlit secrets)
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    st.error("Navin, pehle Settings -> Secrets mein API key daalo!")
    st.stop()

st.title("💃 Rani AI Assistant")
st.caption("Navin ki apni pyaari Rani")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat History display
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Rani se kuch puchiye..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 404 FIX: Sahi model name 'gemini-1.5-flash' hai
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    
    # Rani ki personality setup
    payload = {
        "contents": [{
            "parts": [{"text": f"Tera naam Rani hai. Tu Navin ki pyari assistant hai. Hindi/Bhojpuri mix mein baat kar. Sawal: {prompt}"}]
        }]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()

        if response.status_code == 200:
            answer = result['candidates'][0]['content']['parts'][0]['text']
            with st.chat_message("assistant"):
                st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
            st.error(f"Rani: Maaf kijiyega boss, Google error de raha hai. Status: {response.status_code}")
            st.json(result) # Error detail dekhne ke liye
            
    except Exception as e:
        st.error(f"Technical error: {e}")
            
