import streamlit as st
import os
import requests
import json

st.set_page_config(page_title="MentorCore B2B", page_icon="🧠")
st.title("MentorCore 🧠")
st.subheader("Asistent Operațional B2B")

api_key = os.environ.get("GEMINI_API_KEY")
user_input = st.text_area("Ce rezolvăm astăzi?")

if st.button("Procesează"):
    if api_key and user_input:
        # Folosim endpoint-ul STABIL v1
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        
        # Payload corectat pentru instructiuni de sistem
        data = {
            "contents": [{"parts": [{"text": user_input}]}],
            "system_instruction": {"parts": [{"text": "Ești MentorCore, asistent B2B strict operațional."}]}
        }
        
        with st.spinner("Procesez prin API v1..."):
            try:
                response = requests.post(url, headers=headers, json=data)
                result = response.json()
                
                if "candidates" in result:
                    text = result["candidates"][0]["content"]["parts"][0]["text"]
                    st.markdown(text)
                else:
                    st.error(f"Eroare API: {result}")
            except Exception as e:
                st.error(f"Eroare: {e}")
    else:
        st.error("Cheia API lipsește sau input gol.")
