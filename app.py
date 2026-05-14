import streamlit as st
import requests

st.set_page_config(page_title="Rani Assistant", page_icon="💃")

# API Key check
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    st.error("Navin, pehle Settings -> Secrets mein API key daalo!")
    st.stop()

st.title("💃 Rani AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat history dikhana
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Rani se kuch puchiye..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 404 SOLUTION: Model name aur version ka naya format
    # Hum 'gemini-1.5-flash-latest' try kar rahe hain jo sabse stable hai
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{"text": f"Tera naam Rani hai. Tu Navin ki AI assistant hai. Hindi mein jawab de: {prompt}"}]
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
            # Agar phir bhi model na mile, toh hum 'gemini-pro' try karenge (Legacy version)
            url_alt = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
            response_alt = requests.post(url_alt, json=payload)
            
            if response_alt.status_code == 200:
                answer = response_alt.json()['candidates'][0]['content']['parts'][0]['text']
                with st.chat_message("assistant"):
                    st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                st.error(f"Rani: Arre boss, Google ke server par rasta nahi mil raha (404).")
                st.write("Debug Info:", result)
    except Exception as e:
        st.error(f"Technical Glitch: {e}")
        
