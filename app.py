import streamlit as st
import os
import requests

st.title("MentorCore 🧠")
api_key = os.environ.get("GEMINI_API_KEY")

user_input = st.text_area("Ce rezolvăm astăzi?")

if st.button("Procesează"):
    if api_key and user_input:
        # Folosim endpoint-ul REST direct (nu depinde de nicio librărie)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        data = {"contents": [{"parts": [{"text": user_input}]}]}
        
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
