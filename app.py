import streamlit as st
import os
import requests

st.title("MentorCore 🧠 - Debug Mode")
api_key = os.environ.get("GEMINI_API_KEY")

if st.button("Verifică modele disponibile"):
    if api_key:
        # Încercăm să listăm modelele pe v1
        url = f"https://generativelanguage.googleapis.com/v1/models?key={api_key}"
        response = requests.get(url)
        st.write(response.json())
    else:
        st.error("Cheia API nu e setată în Secrets!")
