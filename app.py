import streamlit as st
from google import genai
import streamlit.components.v1 as components
import urllib.parse

# Page Setup
st.set_page_config(page_title="Rani Assistant", page_icon="💃")

# API Key check
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    st.error("Navin, Secrets mein GEMINI_API_KEY daalo!")
    st.stop()

# New SDK Client
client = genai.Client(api_key=api_key)

st.title("💃 Rani AI Assistant")

# --- 1. VOICE INPUT (Listening) ---
def voice_input():
    st.markdown("""
        <script>
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'hi-IN'; 
        
        window.startRecognition = () => {
            recognition.start();
        };

        recognition.onresult = (event) => {
            const text = event.results[0][0].transcript;
            const streamlitInput = window.parent.document.querySelector('textarea[aria-label="Rani se puchiye..."]');
            if (streamlitInput) {
                streamlitInput.value = text;
                streamlitInput.focus();
                streamlitInput.dispatchEvent(new Event('input', { bubbles: true }));
            }
        };
        </script>
    """, unsafe_allow_html=True)
    
    if st.button("🎙️ Rani ko bol kar sunao"):
        components.html("<script>window.parent.startRecognition();</script>", height=0)

# --- 2. VOICE OUTPUT (Speaking) ---
def speak_text(text):
    # Text ko URL safe banana
    safe_text = urllib.parse.quote(text[:250]) # Max 250 characters for TTS
    audio_url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={safe_text}&tl=hi&client=tw-ob"
    st.audio(audio_url, format="audio/mp3", autoplay=True)

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# UI Layout
voice_input()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- CHAT LOGIC ---
if prompt := st.chat_input("Rani se puchiye..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        instruction = "Tera naam Rani hai. Tu Navin ki pyari assistant hai. Hindi/Bhojpuri mix mein bahut pyari ladki ban kar jawab de."
        
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=f"{instruction}\n\nNavin: {prompt}"
        )
        
        answer = response.text
        with st.chat_message("assistant"):
            st.markdown(answer)
            # Rani ab bol kar bhi sunayegi
            speak_text(answer)
            
        st.session_state.messages.append({"role": "assistant", "content": answer})
        
    except Exception as e:
        st.error(f"Rani: Arre boss, network issue hai shayad: {e}")
        
